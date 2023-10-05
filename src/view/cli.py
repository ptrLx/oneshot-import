from view.ui import UI
import logging
import os
from datetime import datetime
from util.config import disclaimer
from controller.controller import Controller
import time


class CLI(UI):
    def __init__(self, controller: Controller, auto_decide: bool) -> None:
        super().__init__(controller, auto_decide)

    def start(self, confirm_actions: bool) -> None:
        # * 1. Ask to start
        if not confirm_actions:
            confirmation = self.confirm(f"{disclaimer}\nStart the generation now?")

        if not (confirm_actions or confirmation):
            print("Aborting.")
            exit(1)

        # * 2. Read images
        self.c.set_event("insert")

        if self.c.wait_for_event("insert_finished"):
            self.c.events["insert_finished"].clear()

        # * 3. Choose images
        folder = self.c.args.get_image_folder_path()
        for date_number, image_list in self.c.images.items():
            if len(image_list) == 1:
                self.c.selected_images[date_number] = image_list[0]
            else:
                # Find all OneShots in the image_list
                oneshots = []
                for image in image_list:
                    if image.date_time_read_from == "oneshot":
                        oneshots.append(image)

                # Oneshots will be preferred over normal images
                if len(oneshots) == 1:
                    self.c.selected_images[date_number] = oneshots[0]
                elif len(oneshots) > 1:
                    choice = self.choose_image(oneshots, folder, oneshots[0].date_time)
                    self.c.selected_images[date_number] = oneshots[choice]

                else:
                    choice = self.choose_image(
                        image_list, folder, image_list[0].date_time
                    )
                    self.c.selected_images[date_number] = image_list[choice]

        # * 4. Count selected images
        self.c.count_selected()

        # * 5. Rename all images
        if self.c.selected_images:
            # Ask for permission to rename all images to the OneShot naming schema
            if not self.c.args.get_confirmation():
                confirmation = self.confirm(
                    "\nAll files that can be imported will be renamed to the OneShot naming schema. Continue?"
                )
                if not confirmation:
                    logging.error(
                        "Images will not be renamed. Skipping generation of the 'import-me.json'."
                    )
                    exit(1)

        self.c.set_event("rename")

        if self.c.wait_for_event("rename_finished"):
            self.c.events["rename_finished"].clear()

        # * 6. Write export file
        file_path = self.c.args.get_export_file_location()

        # If the file already exists, the user should be asked if it can be overwritten
        confirmation = True

        if (
            os.path.exists(file_path)
            and os.path.isfile(file_path)
            and not self.c.args.get_confirmation()
        ):
            confirmation = self.confirm(
                f"\nThe file '{file_path}' already exists. Do you want to overwrite it?"
            )

        if not confirmation:
            logging.error("Skipping generation of the 'import-me.json'.")
            exit(1)

        self.c.set_event("export")

        if self.c.wait_for_event("export_finished"):
            self.c.events["export_finished"].clear()

    def inform(self, msg):
        print(msg)

    def confirm(self, msg: str, default_is_no=True) -> bool:
        if default_is_no:
            answer = input(f"{msg} [y/N] > ").strip().lower()
            print()
            if answer == "yes" or answer == "y":
                return True
            return False
        else:
            answer = input(f"{msg} [Y/n] > ").strip().lower()
            print()
            if answer == "no" or answer == "n":
                return False
            return True

    def choose_image(
        self,
        images: list,  # of ImageEntries
        _image_folder_path: str,
        date_time: datetime,
    ) -> int:
        date_only = datetime.strftime(date_time, "%Y-%m-%d")
        if self.auto_decide:
            logging.info(
                f"Choose {images[0].file_name} automatically for date {date_only}. Skipped images: {images[1:]}"
            )
            return 1
        else:
            while True:
                try:
                    answer = int(
                        input(
                            f"Collision at {date_only}: {[i.file_name for i in images]}. Select index [1..{len(images)}] > "
                        )
                    )
                except ValueError:
                    continue
                if answer in range(1, len(images) + 1):
                    return answer - 1
