import logging
import os
from os import listdir
from os.path import isfile, join

from model.image_entry import ImageEntry
from util.config import image_extensions
from util.datereader import read_date_and_type


def inserter_service(controller):
    folder = controller.args.get_image_folder_path()

    # * also search in subfolders
    # // for _root, _dirs, files in os.walk(folder):
    # //    for file_name in files:

    files = [f for f in listdir(folder) if isfile(join(folder, f))]
    for file_name in files:
        if file_name.lower().endswith(image_extensions):
            date, type = read_date_and_type(folder, file_name)

            if not type:
                logging.warning(f"Date of image {file_name} not readable.")
                controller.inc_count("error")
                continue

            image_entry = ImageEntry(file_name, date, type)
            date_number = image_entry.date_number()

            logging.debug(f"Date {date} found for image '{file_name}' ({type}).")
            controller.images[date_number].append(image_entry)

    controller.set_event("insert_finished")
