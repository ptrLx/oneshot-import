import logging
import os
import sys
import threading
from collections import Counter, defaultdict
from datetime import datetime

from model.image_entry import ImageEntry
from service.exporter import exporter_service
from service.inserter import inserter_service
from service.renamer import renamer_service
from util.args import ArgParser
from view.ui_f import create_ui

event_names = [
    "stop",
    "insert",
    "rename",
    "export",
    "insert_finished",
    "rename_finished",
    "export_finished",
]


class Controller:
    def __init__(self) -> None:
        self.args = ArgParser()

        # Dictionary of all found images with key as date_number and value as list of ImageEntry
        # dict<str>:<list<ImageEntry>>
        # Example: 19601: [("IMG_20230901_203000.jpg", 2023-09-01-20-30-00, "metadata"), (...)]
        self.images = defaultdict(list)

        # Dictionary of all chosen images
        # This one will not have date conflicts anymore
        self.selected_images = defaultdict(ImageEntry)

        # Counters for where the date was read from. This will be used after all images where read from folder.
        # Possible types: metadata, android, ios, oneshot, whatsapp, skipped, error
        self.counts = Counter()

        # Either gui or cli
        # Will get initialized later
        self.ui = None

        self.events = {x: threading.Event() for x in event_names}

    def verify_paths(self) -> None:
        folder_path = self.args.get_image_folder_path()
        export_file_location = self.args.get_export_file_location()

        if not (os.path.exists(folder_path) and os.path.isdir(folder_path)):
            logging.error(f"The folder '{folder_path}' does not exist.")
            sys.exit(1)

        if os.path.exists(export_file_location):
            if not os.path.isfile(export_file_location):
                logging.error(f"'{export_file_location}' is not a file.")
                sys.exit(1)
        else:
            export_path = os.path.dirname(export_file_location) or "."
            if not os.path.exists(export_path):
                logging.error(f"The folder '{export_path}' does not exist.")
                sys.exit(1)

    def init_args(self) -> None:
        self.args.parse()
        self.verify_paths()
        self.ui = create_ui(
            self,
            self.args.get_use_gui(),
            self.args.get_confirmation(),
        )

    def start_ui(self) -> None:
        try:
            self.ui.start()
        except KeyboardInterrupt:
            print("❌ Aborted.")
        finally:
            self.set_event("stop")

    def start_runner(self) -> None:
        flag = False
        while not (self.event_is_set("stop") or flag):
            if self.events["insert"].wait(0.2):
                self.events["insert"].clear()
                inserter_service(self)
                flag = True

        flag = False
        while not (self.event_is_set("stop") or flag):
            if self.events["rename"].wait(0.2):
                self.events["rename"].clear()
                renamer_service(self)
                flag = True

        flag = False
        while not (self.event_is_set("stop") or flag):
            if self.events["export"].wait(0.2):
                self.events["export"].clear()
                exporter_service(self)
                flag = True

    def set_event(self, event: str) -> None:
        if event in event_names:
            self.events[event].set()
        else:
            raise ValueError("Unknown event!")

    def event_is_set(self, event: str) -> bool:
        if event in event_names:
            return self.events[event].is_set()
        else:
            raise ValueError("Unknown event!")

    def wait_for_event(self, event: str) -> bool:
        if event in event_names:
            return self.events[event].wait()
        else:
            raise ValueError("Unknown event!")

    def clear_event(self, event: str) -> None:
        if event in event_names:
            self.events[event].clear()
        else:
            raise ValueError("Unknown event!")

    def image_list_generator(self):
        # Only image_lists where a choice has to be made will be yielded
        for date_number, image_list in self.images.items():
            if len(image_list) == 1:  # Only one image exists
                self.select_image(date_number, image_list[0])
            else:
                # Find all OneShots in the image_list
                oneshots = []
                for image in image_list:
                    if image.date_time_read_from == "oneshot":
                        oneshots.append(image)

                # Oneshots will be preferred over normal images
                if len(oneshots) == 0:  # No OneShot in the image list
                    if self.args.get_auto_decide():
                        selected_entry = image_list[0]
                        selected_filename = selected_entry.file_name
                        date_only = datetime.strftime(
                            selected_entry.date_time, "%Y-%m-%d"
                        )
                        self.select_image(date_number, image_list[0])
                        logging.info(
                            f"Choose {selected_filename} automatically for date {date_only}. Skipped images: {[i.file_name for i in image_list[1:]]}"
                        )
                    else:
                        yield date_number, image_list
                elif len(oneshots) == 1:  # One OneShot where found
                    selected_entry = oneshots[0]
                    selected_filename = selected_entry.file_name
                    date_only = datetime.strftime(selected_entry.date_time, "%Y-%m-%d")
                    self.select_image(date_number, selected_entry)
                    logging.info(
                        f"Choose {selected_filename} for date {date_only} as it is the only OneShot. Skipped images: {[i.file_name for i in image_list if i.file_name != selected_filename]}"
                    )
                else:  # Multiple OneShots where found
                    if self.args.get_auto_decide():
                        selected_entry = oneshots[0]
                        selected_filename = selected_entry.file_name
                        date_only = datetime.strftime(
                            selected_filename.date_time, "%Y-%m-%d"
                        )
                        self.select_image(date_number, selected_entry)
                        logging.info(
                            f"Choose {selected_filename} automatically for date {date_only}. Skipped images: {[i.file_name for i in image_list if i.file_name != selected_filename]}"
                        )
                    else:
                        yield date_number, oneshots

    def next_image_list(self):
        if not hasattr(self, "image_list_gen"):
            self.image_list_gen = self.image_list_generator()

        return next(self.image_list_gen)

    def select_image(self, date_number, image: ImageEntry):
        self.selected_images[date_number] = image

    def inc_count(self, type: str):
        self.counts[type] += 1

    def count_selected(self) -> None:
        for _, image_entry in self.selected_images.items():
            self.counts[image_entry.date_time_read_from] += 1
