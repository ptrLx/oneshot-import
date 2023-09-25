#!/usr/bin/env python3

import os
from collections import Counter
import logging
from exporter import generate_import_me, GenerationAbortedException
from inserter import insert_image
from renamer import rename_images, RenameAbortedException
from config import disclaimer, image_extensions
from args import ArgParser
from summarizer import summarize

logging.basicConfig(level=logging.INFO)

args = ArgParser()

# Dictionary of all found images with key as date_number and value as (filename, date_time, datetime_read_from)
# Example: 19601: ("IMG_20230901_203000.jpg", 2023-09-01-20-30-00, "metadata")
images = {}

# Counters for where the date was read from. This will be used after all images where read from folder.
# Possible types: metadata, android, ios, oneshot, whatsapp, skipped, error
counts = Counter()


def generate_json(folder):
    # 1. Fill the images dictionary
    for _root, _dirs, files in os.walk(folder):
        for file_name in files:
            if file_name.lower().endswith(image_extensions):
                insert_image(file_name, images, args, counts)

    # 2. Count the found images
    for date_number, (_, __, datetime_read_from) in images.items():
        counts[datetime_read_from] += 1

    # 3. Generate the JSON export
    if images:
        try:
            rename_images(images, args)
            generate_import_me(images, args)
        except RenameAbortedException:
            print(
                "Images will not be renamed. Skipping generation of the 'import-me.json'."
            )
        except GenerationAbortedException:
            print("Skipping generation of the 'import-me.json'.")


if __name__ == "__main__":
    args.parse()

    folder_path = args.get_path()
    if not (os.path.exists(folder_path) and os.path.isdir(folder_path)):
        logging.error(f"The folder '{folder_path}' does not exist.")
        exit(1)

    export_file_location = args.get_export_file_location()
    if os.path.exists(export_file_location) and not os.path.isfile(
        export_file_location
    ):
        logging.error(f"'{export_file_location}' is not a file.")
        exit(1)

    export_path = os.path.dirname(export_file_location) or "."
    if not os.path.exists(export_path):
        logging.error(f"The folder '{export_path}' does not exist.")
        exit(1)

    print(disclaimer)

    if not args.get_confirmation():
        answer = input("Start the generation now? [y/N] > ").strip().lower()

    if args.get_confirmation() or answer == "yes" or answer == "y":
        print()
        generate_json(folder_path)

        if args.get_summarize():
            summarize(counts)
    else:
        print("Aborting.")
