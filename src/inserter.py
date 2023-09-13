import logging
from datetime import datetime
from datereader import DateReader


def date_to_number(input_date):
    reference_date = datetime(1970, 1, 1)
    delta = input_date - reference_date
    days_since_reference = delta.days
    return days_since_reference


def insert_image(file_name, images, args, counts):
    logging.debug(f"Found image: {file_name}")

    date = DateReader.read_metadata(f"{args.get_path()}/{file_name}")
    if date:
        date_number = date_to_number(date)
        if date_number not in images:
            logging.info(f"Date {date} found for image {file_name} in metadata.")
            images[date_number] = (date, file_name)
            counts["metadata"] += 1
        else:
            date_only = datetime.strftime(date, "%Y-%m-%d")
            logging.info(
                f"Skipping image {file_name}. There is already a entry at {date_only}."
            )
            counts["skipped"] += 1
        return

    date = DateReader.read_android_filename(file_name)
    if date:
        date_number = date_to_number(date)
        if date_number not in images:
            logging.info(
                f"Date {date} found for image {file_name} in filename (Android naming schema)."
            )
            images[date_number] = (date, file_name)
            counts["android"] += 1
        else:
            date_only = datetime.strftime(date, "%Y-%m-%d")
            logging.info(
                f"Skipping image {file_name}. There is already a entry at {date_only}."
            )
            counts["skipped"] += 1
        return

    date = DateReader.read_ios_filename(file_name)
    if date:
        date_number = date_to_number(date)
        if date_number not in images:
            logging.info(
                f"Date {date} found for image {file_name} in filename (IOS naming schema)."
            )
            images[date_number] = (date, file_name)
            counts["ios"] += 1
        else:
            date_only = datetime.strftime(date, "%Y-%m-%d")
            logging.info(
                f"Skipping image {file_name}. There is already a entry at {date_only}."
            )
            counts["skipped"] += 1
        return

    date = DateReader.read_oneshot_filename(file_name)
    if date:
        logging.info(
            f"Date {date} found for image {file_name} in filename (OneShot naming schema)."
        )
        date_number = date_to_number(date)
        if date_number not in images:
            images[date_number] = (date, file_name)
            counts["oneshot"] += 1
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
            f"Date {date} found for image {file_name} in filename (WhatsApp naming schema)."
        )
        date_number = date_to_number(date)
        if date_number not in images:
            images[date_number] = (date, file_name)
            counts["whatsapp"] += 1
        else:
            date_only = datetime.strftime(date, "%Y-%m-%d")
            logging.info(
                f"Skipping image {file_name}. There is already a entry at {date_only}."
            )
            counts["skipped"] += 1
        return

    logging.warning(f"Date of image {file_name} not readable.")
    counts["error"] += 1
