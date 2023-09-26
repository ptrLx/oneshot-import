#!/usr/bin/env python3

import os
import logging
from exporter import Exporter, GenerationAbortedException
from inserter import Inserter
from renamer import Renamer, RenameAbortedException
from config import image_extensions
from controller import Controller
from summarizer import summarize
from config import disclaimer

logging.basicConfig(level=logging.INFO)

c = Controller()
r = Renamer(c)
e = Exporter(c)
i = Inserter(c)


def verify_paths() -> None:
    folder_path = c.args.get_image_folder_path()
    if not (os.path.exists(folder_path) and os.path.isdir(folder_path)):
        logging.error(f"The folder '{folder_path}' does not exist.")
        exit(1)

    export_file_location = c.args.get_export_file_location()
    if os.path.exists(export_file_location) and not os.path.isfile(
        export_file_location
    ):
        logging.error(f"'{export_file_location}' is not a file.")
        exit(1)

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
    # 1. Fill the images dictionary
    for _root, _dirs, files in os.walk(folder):
        for file_name in files:
            if file_name.lower().endswith(image_extensions):
                i.insert_image(file_name)

    # 2. Count the found images
    for date_number, image_entry in c.images.items():
        c.counts[image_entry.date_time_read_from] += 1

    # 3. Generate the JSON export
    if c.images:
        try:
            r.rename_images(c)
            e.export()
        except RenameAbortedException:
            logging.error(
                "Images will not be renamed. Skipping generation of the 'import-me.json'."
            )
        except GenerationAbortedException:
            logging.error("Skipping generation of the 'import-me.json'.")


if __name__ == "__main__":
    c.parse_args()
    c.init_ui()
    verify_paths()

    if confirm_start():
        generate_json()

        if c.args.should_summarize():
            summarize(c.counts)
    else:
        logging.error("Aborting.")
