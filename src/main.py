#!/usr/bin/env python3

import os
import logging
from exporter import export_json
from inserter import Inserter
from renamer import rename_images
from config import image_extensions
from controller import Controller
from summarizer import summarize
from config import disclaimer

logging.basicConfig(level=logging.INFO)

c = Controller()
i = Inserter(c)


def verify_paths() -> None:
    folder_path = c.args.get_image_folder_path()
    if not (os.path.exists(folder_path) and os.path.isdir(folder_path)):
        logging.error(f"The folder '{folder_path}' does not exist.")
        exit(1)

    export_file_location = c.args.get_export_file_location()
    if os.path.exists(export_file_location):
        if not os.path.isfile(export_file_location):
            logging.error(f"'{export_file_location}' is not a file.")
            exit(1)
    else:
        export_path = os.path.dirname(export_file_location) or "."
        if not os.path.exists(export_path):
            logging.error(f"The folder '{export_path}' does not exist.")
            exit(1)


def confirm_start() -> None:
    if not c.args.get_confirmation():
        confirmation = c.ui.confirm(f"{disclaimer}\nStart the generation now?")

    return c.args.get_confirmation() or confirmation


def generate_json() -> None:
    folder = c.args.get_image_folder_path()
    file_path = c.args.get_export_file_location()

    # 1. Scan the images dictionary
    for _root, _dirs, files in os.walk(folder):
        for file_name in files:
            if file_name.lower().endswith(image_extensions):
                i.insert_image(file_name)

    # 2. Count the found images
    for _, image_entry in c.images.items():
        c.counts[image_entry.date_time_read_from] += 1

    if c.images:
        # 3. Rename all images

        # Ask for permission to rename all images to the OneShot naming schema
        if not c.args.get_confirmation():
            confirmation = c.ui.confirm(
                "\nAll files that can be imported will be renamed to the OneShot naming schema. Continue?"
            )
            if not confirmation:
                logging.error(
                    "Images will not be renamed. Skipping generation of the 'import-me.json'."
                )
                exit(1)

        rename_images(c)

        # 4. Generate the JSON export

        # If the file already exists, the user should be asked if it can be overwritten
        confirmation = True

        if (
            os.path.exists(file_path)
            and os.path.isfile(file_path)
            and not c.args.get_confirmation()
        ):
            confirmation = c.ui.confirm(
                f"\nThe file '{file_path}' already exists. Do you want to overwrite it?"
            )

        if not confirmation:
            logging.error("Skipping generation of the 'import-me.json'.")
            exit(1)

        export_json(c)


if __name__ == "__main__":
    c.parse_args()
    c.init_ui()
    verify_paths()

    if not confirm_start():
        logging.error("Aborting.")
        exit(1)

    generate_json()

    if c.args.should_summarize():
        summarize(c.counts)
