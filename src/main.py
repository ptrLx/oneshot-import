#!/usr/bin/env python3

import os
from collections import Counter
import logging
from exporter import generate_import_me
from inserter import insert_image
from config import disclaimer, folder_path, image_extensions

logging.basicConfig(level=logging.INFO)

# Dictionary of all found images with key as date_number and value as (datetime, filename)
# Example: 19601: (2023-09-01-20-30-00, "IMG_20230901_203000.jpg")
images = {}

# Counters for where the date was read from.
# Possible types: metadata, android, ios, oneshot, whatsapp, skipped, error
counts = Counter()


def generate_json():
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        # 1. Fill the images dictionary
        for _root, _dirs, files in os.walk(folder_path):
            for file_name in files:
                if file_name.lower().endswith(image_extensions):
                    insert_image(file_name, images, counts)

        # 2. Generate the JSON export
        generate_import_me(images)
    else:
        print(f"The folder '{folder_path}' does not exist.")


def summarize():
    print("\n---------------- RESULT ----------------")
    import_count = counts.total() - counts["skipped"] - counts["error"]
    print(f"Found {counts.total()} images. {import_count} can be imported.")

    if counts.total() == counts["metadata"] + counts["error"] + counts["skipped"]:
        print("All dates where read from EXIF metadata.")
    elif counts.total() == counts["android"] + counts["error"] + counts["skipped"]:
        print("All dates where read from Android file naming schema.")
    elif counts.total() == counts["ios"] + counts["error"] + counts["skipped"]:
        print("All dates where read from IOS file naming schema.")
    elif counts.total() == counts["oneshot"] + counts["error"] + counts["skipped"]:
        print("All dates where read from OneShot file naming schema.")
    elif counts.total() == counts["whatsapp"] + counts["error"] + counts["skipped"]:
        print("All dates where read from WhatsApp file naming schema.")
    else:
        print("Dates where read from:")
        if counts["metadata"]:
            print(f"  - Metadata: {counts['metadata']}")
        if counts["android"]:
            print(f"  - Android file naming schema: {counts['android']}")
        if counts["ios"]:
            print(f"  - IOS file naming schema: {counts['ios']}")
        if counts["oneshot"]:
            print(f"  - OneShot file naming schema: {counts['oneshot']}")
        if counts["whatsapp"]:
            print(f"  - WhatsApp file naming schema: {counts['whatsapp']}")

    if counts["skipped"]:
        print(
            f"{counts['skipped']} images where skipped because the date was already occupied."
        )
    if counts["error"]:
        print(
            f"{counts['error']} images where skipped because the date information was not readable."
        )


if __name__ == "__main__":
    print(disclaimer)

    answer = input("Start the generation now? [y/N] > ")

    print()

    if answer.lower() == "yes" or answer.lower() == "y":
        generate_json()
        summarize()
    else:
        print("Aborting.")
