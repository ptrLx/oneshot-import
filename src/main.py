#!/usr/bin/env python3

import os
from collections import Counter
import logging
from datereader import DateReader

logging.basicConfig(level=logging.INFO)

disclaimer = """This script imports images from past dates into your OneShot diary.
To get started, copy the images into the 'image' folder.
Make sure to copy only one image per day. Otherwise the importer will select one of them.

A import-me.json file will be generated, which can be imported in the OneShot-App.
"""

# Folder that contains the images
folder_path = "image"

default_happiness = "NOT_SPECIFIED"

default_text_entry = "imported with oneshot-import"

# Possible image extensions in lowercase
image_extensions = (".jpg", ".jpeg", ".png")

images = {}

# Counters for where the date was read from.
# Possible types: metadata, android, ios, oneshot, whatsapp, error
counts = Counter()

def insert_image(file_name):
    logging.debug(f"Found image: {file_name}")

    date = DateReader.read_metadata(f"{folder_path}/{file_name}")
    if date:
        logging.info(f"Date {date} found for image {file_name} in metadata.")
        images[date] = file_name
        counts["metadata"] += 1
        return

    date = DateReader.read_android_filename(file_name)
    if date:
        logging.info(f"Date {date} found for image {file_name} in filename (Android naming schema).")
        images[date] = file_name
        counts["android"] += 1
        return
    
    date = DateReader.read_ios_filename(file_name)
    if date:
        logging.info(f"Date {date} found for image {file_name} in filename (IOS naming schema).")
        images[date] = file_name
        counts["ios"] += 1
        return
    
    date = DateReader.read_oneshot_filename(file_name)
    if date:
        logging.info(f"Date {date} found for image {file_name} in filename (OneShot naming schema).")
        images[date] = file_name
        counts["oneshot"] += 1
        return

    date = DateReader.read_whatsapp_filename(file_name)
    if date:
        logging.info(f"Date {date} found for image {file_name} in filename (WhatsApp naming schema).")
        images[date] = file_name
        counts["whatsapp"] += 1
        return
    
    logging.warning(f"Date of image {file_name} not readable.")
    counts["error"] += 1


def generate_import_me():
    #todo
    pass


def generate_json():
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        for _root, _dirs, files in os.walk(folder_path):
            for file_name in files:
                if file_name.lower().endswith(image_extensions):
                    insert_image(file_name)
        
        generate_import_me()
    else:
        print(f"The folder '{folder_path}' does not exist.")
    

def summarize():
    print("---------------- RESULT ----------------")
    print(f"Imported {counts.total()} images.")

    if counts.total() == counts['metadata'] + counts['error']:
        print("All dates where read from EXIF metadata.")
    elif counts.total() == counts['android'] + counts['error']:
        print("All dates where read from Android file naming schema.")
    elif counts.total() == counts['ios'] + counts['error']:
        print("All dates where read from IOS file naming schema.")
    elif counts.total() == counts['oneshot'] + counts['error']:
        print("All dates where read from OneShot file naming schema.")
    else:
        print("dates where read from:")
        if counts['metadata']:
            print(f"  - Metadata: {counts['metadata']}")
        if counts['android']:
            print(f"  - Android file naming schema: {counts['android']}")
        if counts['ios']:
            print(f"  - IOS file naming schema: {counts['ios']}")
        if counts['oneshot']:
            print(f"  - OneShot file naming schema: {counts['oneshot']}")

    if counts['error']:
        print(f"{counts['error']} images where skipped (no readable date information).")


if __name__ == "__main__":
    print(disclaimer)

    answer = input("Start the generation now? [y/N] > ")

    print()

    if answer.lower() == "yes" or answer.lower() == "y":
        generate_json()
        summarize()
    else:
        print("Aborting.")
