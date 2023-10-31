import itertools
import os
import sys
import time
from datetime import datetime

from InquirerPy import inquirer

from controller.controller import Controller
from util.config import disclaimer
from util.summarizer import Summarizer
from view.ui import UI

_spinner = itertools.cycle(["-", "/", "|", "\\"])


def _next_spin():
    sys.stdout.write(next(_spinner))  # write the next character
    sys.stdout.flush()  # flush stdout buffer (actual character display)
    sys.stdout.write("\b")  # erase the last written char


class CLI(UI):
    def __init__(self, controller: Controller, skip_confirm_actions: bool) -> None:
        super().__init__(controller, skip_confirm_actions)

    def start(self) -> None:
        # * 1. Ask to start
        print(disclaimer)

        if not self.__confirm("Start the generation now?"):
            print("❌ Aborted.")
            self.c.set_event("stop")
            sys.exit(0)

        # * 2. Read images
        self.c.set_event("insert")

        # * Loading animation
        while not self.c.event_is_set("insert_finished"):
            _next_spin()
            time.sleep(0.1)
        self.c.clear_event("insert_finished")

        # * 3. Choose images
        folder = self.c.args.get_image_folder_path()
        for date_number, image_list in self.c.image_list_generator():
            choice = self.__choose_image(image_list, image_list[0].date_time)
            self.c.select_image(date_number, image_list[choice])

        # * 4. Count selected images
        self.c.count_selected()

        # * 5. Rename all images
        if self.c.selected_images:
            # Ask for permission to rename all images to the OneShot naming schema
            if not self.__confirm(
                "All files that can be imported will be renamed to the OneShot naming schema. Continue?"
            ):
                print(
                    "❌ Images will not be renamed. Skipping generation of the 'import-me.json'."
                )
                self.c.set_event("stop")
                sys.exit(0)

        self.c.set_event("rename")

        # * Waiting for rename
        while not self.c.event_is_set("rename_finished"):
            # _next_spin() no loading animation needed. User will see logging about reamed images.
            time.sleep(0.1)
        self.c.clear_event("rename_finished")

        # * 6. Write export file
        file_path = self.c.args.get_export_file_location()

        # If the file already exists, the user should be asked if it can be overwritten
        if os.path.exists(file_path) and os.path.isfile(file_path):
            if not self.__confirm(
                f"The file '{file_path}' already exists. Do you want to overwrite it?"
            ):
                print("❌ Skipping generation of the 'import-me.json'.")
                self.c.set_event("stop")
                sys.exit(1)

        self.c.set_event("export")

        # * Loading animation
        while not self.c.event_is_set("export_finished"):
            _next_spin()
            time.sleep(0.1)
        self.c.clear_event("export_finished")

        print(f"\n✔️ Import file written to '{file_path}.'")

        print(Summarizer().summarize(self.c.counts))

    def __confirm(self, msg: str, default_is_no=True) -> bool:
        if not self.skip_confirm_actions:
            return inquirer.confirm(message=msg, default=not default_is_no).execute()
        else:
            return True

    def __choose_image(
        self,
        images: list,  # of ImageEntries
        date_time: datetime,
    ) -> int:
        date_only = datetime.strftime(date_time, "%Y-%m-%d")
        result = inquirer.select(
            message=f"Collision at date {date_only}. Select which image should be taken:",
            choices=[f"{i}: {image.file_name}" for i, image in enumerate(images)],
        ).execute()

        return int(result[0].split(":")[0])
