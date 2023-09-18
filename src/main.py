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


def generate_json():
    folder_path = args.get_path()
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        # 1. Fill the images dictionary
        for _root, _dirs, files in os.walk(folder_path):
            for file_name in files:
                if file_name.lower().endswith(image_extensions):
                    insert_image(file_name, images, args, counts)

        # 2. Generate the JSON export
        generate_import_me(images, args)
    else:
        print(f"The folder '{folder_path}' does not exist.")


if __name__ == "__main__":
    args.parse()

    print(disclaimer)

    if not args.get_confirmation():
        answer = input("Start the generation now? [y/N] > ").strip().lower()
        print()

    if args.get_confirmation() or answer == "yes" or answer == "y":
        generate_json()

        if args.get_summarize():
            summarize(counts)
    else:
        print("Aborting.")
