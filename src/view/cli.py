from view.ui import UI
import logging
import os
from datetime import datetime
from util.config import disclaimer
from controller.controller import Controller
from InquirerPy import inquirer

import time
import itertools, sys

_spinner = itertools.cycle(["-", "/", "|", "\\"])


def _next_spin():
    sys.stdout.write(next(_spinner))  # write the next character
    sys.stdout.flush()  # flush stdout buffer (actual character display)
    sys.stdout.write("\b")  # erase the last written char


class CLI(UI):
    def __init__(
        self, controller: Controller, auto_decide: bool, confirm_actions: bool
    ) -> None:
        super().__init__(controller, auto_decide, confirm_actions)

    def start(self) -> None:
        # * 1. Ask to start
        if not self.confirm_actions:
            print(disclaimer)
            confirmation = self.__confirm("Start the generation now?")

        if not (self.confirm_actions or confirmation):
            print("❌ Aborted.")
            self.c.set_event("stop")
            exit(1)

        # * 2. Read images
        self.c.set_event("insert")

        # // if self.c.wait_for_event("insert_finished"):
        # //     self.c.events["insert_finished"].clear()

        # * Loading animation
        while not self.c.event_is_set("insert_finished"):
            _next_spin()
            time.sleep(0.1)

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
                    choice = self.__choose_image(
                        oneshots, folder, oneshots[0].date_time
                    )
                    self.c.selected_images[date_number] = oneshots[choice]

                else:
                    choice = self.__choose_image(
                        image_list, folder, image_list[0].date_time
                    )
                    self.c.select_image(date_number, image_list[choice])

        # * 4. Count selected images
        self.c.count_selected()

        # * 5. Rename all images
        if self.c.selected_images:
            # Ask for permission to rename all images to the OneShot naming schema
            if not self.c.args.get_confirmation():
                confirmation = self.__confirm(
                    "All files that can be imported will be renamed to the OneShot naming schema. Continue?"
                )
                if not confirmation:
                    print(
                        "❌ Images will not be renamed. Skipping generation of the 'import-me.json'."
                    )
                    self.c.set_event("stop")
                    exit(1)

        self.c.set_event("rename")

        # // if self.c.wait_for_event("rename_finished"):
        # //     self.c.events["rename_finished"].clear()

        # * Waiting for rename
        while not self.c.event_is_set("rename_finished"):
            # _next_spin() no loading animation needed. User will see logging about reamed images.
            time.sleep(0.1)

        # * 6. Write export file
        file_path = self.c.args.get_export_file_location()

        # If the file already exists, the user should be asked if it can be overwritten
        confirmation = True

        if (
            os.path.exists(file_path)
            and os.path.isfile(file_path)
            and not self.c.args.get_confirmation()
        ):
            confirmation = self.__confirm(
                f"The file '{file_path}' already exists. Do you want to overwrite it?"
            )

        if not confirmation:
            print("❌ Skipping generation of the 'import-me.json'.")
            self.c.set_event("stop")
            exit(1)

        self.c.set_event("export")

        # // if self.c.wait_for_event("export_finished"):
        # //     self.c.events["export_finished"].clear()

        # * Loading animation
        while not self.c.event_is_set("export_finished"):
            _next_spin()
            time.sleep(0.1)

        print(f"✔️ Import file written to '{file_path}'")

    def __confirm(self, msg: str, default_is_no=True) -> bool:
        return inquirer.confirm(message=msg, default=not default_is_no).execute()

        # // if default_is_no:
        # //     answer = input(f"{msg} [y/N] > ").strip().lower()
        # //     print()
        # //     if answer == "yes" or answer == "y":
        # //         return True
        # //     return False
        # // else:
        # //     answer = input(f"{msg} [Y/n] > ").strip().lower()
        # //     print()
        # //     if answer == "no" or answer == "n":
        # //         return False
        # //     return True

    def __choose_image(
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
            result = inquirer.select(
                message=f"Collision at date {date_only}. Select which image should be taken:",
                choices=[f"{i}: {image.file_name}" for i, image in enumerate(images)],
            ).execute()

            return int(result[0].split(":")[0])

            # // while True:
            # //     try:
            # //         answer = int(
            # //             input(
            # //                 f"Collision at {date_only}: {[i.file_name for i in images]}. Select index [1..{len(images)}] > "
            # //             )
            # //         )
            # //     except ValueError:
            # //         continue
            # //     if answer in range(1, len(images) + 1):
            # //         return answer - 1
