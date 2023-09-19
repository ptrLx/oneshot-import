#!/usr/bin/env python3

import os
from collections import Counter
import logging
from exporter import generate_import_me
from inserter import insert_image
from config import disclaimer, image_extensions
from args import ArgParser
from summarizer import summarize

logging.basicConfig(level=logging.INFO)

args = ArgParser()

# Dictionary of all found images with key as date_number and value as (datetime, filename)
# Example: 19601: (2023-09-01-20-30-00, "IMG_20230901_203000.jpg")
images = {}

# Counters for where the date was read from.
# Possible types: metadata, android, ios, oneshot, whatsapp, skipped, error
counts = Counter()


def generate_json(folder):
    # 1. Fill the images dictionary
    for _root, _dirs, files in os.walk(folder):
        for file_name in files:
            if file_name.lower().endswith(image_extensions):
                insert_image(file_name, images, args, counts)

    # 2. Generate the JSON export
    generate_import_me(images, args)


if __name__ == "__main__":
    args.parse()

    folder_path = args.get_path()
    if not (os.path.exists(folder_path) and os.path.isdir(folder_path)):
        logging.error(f"The folder '{folder_path}' does not exist.")
        exit(1)

    export_path = os.path.dirname(args.get_export_file_location())
    if not (os.path.exists(export_path) and os.path.isdir(export_path)):
        logging.error(f"The folder '{folder_path}' does not exist.")
        exit(1)

    print(disclaimer)

    if not args.get_confirmation():
        answer = input("Start the generation now? [y/N] > ").strip().lower()
        print()

    if args.get_confirmation() or answer == "yes" or answer == "y":
        generate_json(folder_path)

        if args.get_summarize():
            summarize(counts)
    else:
        print("Aborting.")
