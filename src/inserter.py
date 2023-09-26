import logging
from datetime import datetime
from datereader import DateReader
from image_entry import ImageEntry


def insert_image(file_name, images, args, counts, ui):
    logging.debug(f"Found image: {file_name}.")

    date = DateReader.read_oneshot_filename(file_name)
    if date:
        logging.info(
            f"Date {date} found for image '{file_name}' in filename (OneShot naming schema)."
        )
        image_entry = ImageEntry(file_name, date, "oneshot")
        date_number = image_entry.get_date_number()
        if date_number not in images:
            images[date_number] = image_entry
        else:
            if images[date_number].date_time_read_from == "oneshot":
                choice = ui.choose_image(
                    images[date_number].file_name,
                    file_name,
                    args.get_image_folder_path(),
                    date,
                )
                if choice == 2:
                    images.update({date_number: image_entry})
            else:
                images.update({date_number: image_entry})
            counts["skipped"] += 1
        return

    date = DateReader.read_metadata(f"{args.get_image_folder_path()}/{file_name}")
    if date:
        image_entry = ImageEntry(file_name, date, "metadata")
        date_number = image_entry.get_date_number()
        if date_number not in images:
            logging.info(f"Date {date} found for image '{file_name}' in metadata.")
            images[date_number] = image_entry
        else:
            date_only = datetime.strftime(date, "%Y-%m-%d")
            logging.info(
                f"Skipping image {file_name}. There is already a entry at {date_only}."
            )
            counts["skipped"] += 1
        return

    date = DateReader.read_android_filename(file_name)
    if date:
        image_entry = ImageEntry(file_name, date, "android")
        date_number = image_entry.get_date_number()
        if date_number not in images:
            logging.info(
                f"Date {date} found for image '{file_name}' in filename (Android naming schema)."
            )
            images[date_number] = image_entry
        else:
            date_only = datetime.strftime(date, "%Y-%m-%d")
            logging.info(
                f"Skipping image {file_name}. There is already a entry at {date_only}."
            )
            counts["skipped"] += 1
        return

    date = DateReader.read_ios_filename(file_name)
    if date:
        image_entry = ImageEntry(file_name, date, "ios")
        date_number = image_entry.get_date_number()
        if date_number not in images:
            logging.info(
                f"Date {date} found for image '{file_name}' in filename (IOS naming schema)."
            )
            images[date_number] = image_entry
        else:
            date_only = datetime.strftime(date, "%Y-%m-%d")
            logging.info(
                f"Skipping image {file_name}. There is already a entry at {date_only}."
            )
            counts["skipped"] += 1
        return

    date = DateReader.read_whatsapp_filename(file_name)
    if date:
        logging.info(
            f"Date {date} found for image '{file_name}' in filename (WhatsApp naming schema)."
        )
        image_entry = ImageEntry(file_name, date, "whatsapp")
        date_number = image_entry.get_date_number()
        if date_number not in images:
            images[date_number] = image_entry
        else:
            date_only = datetime.strftime(date, "%Y-%m-%d")
            logging.info(
                f"Skipping image {file_name}. There is already a entry at {date_only}."
            )
            counts["skipped"] += 1
        return

    logging.warning(f"Date of image {file_name} not readable.")
    counts["error"] += 1
