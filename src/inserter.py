import logging
from datetime import datetime
from datereader import read_date_and_type
from image_entry import ImageEntry
from controller import Controller


class Inserter:
    def __init__(self, c: Controller) -> None:
        self.c = c

    def insert_image(self, file_name: str) -> None:
        folder_path = self.c.args.get_image_folder_path()
        date, type = read_date_and_type(folder_path, file_name)

        if not type:
            logging.warning(f"Date of image {file_name} not readable.")
            self.c.counts["error"] += 1
            return

        image_entry = ImageEntry(file_name, date, type)
        date_number = image_entry.date_number()

        logging.info(f"Date {date} found for image '{file_name}' ({type}).")
        self.c.images[date_number].append(image_entry)

    # * Old blocking code to ask user directly via ui, which image to keep
    # // def insert_image(self, file_name: str) -> None:
    # //     folder_path = self.c.args.get_image_folder_path()
    # //     date, type = read_date_and_type(folder_path, file_name)

    # //     if not type:
    # //         logging.warning(f"Date of image {file_name} not readable.")
    # //         self.c.counts["error"] += 1
    # //         return

    # //     image_entry = ImageEntry(file_name, date, type)
    # //     date_number = image_entry.date_number()

    # //     if date_number not in self.c.images:
    # //         logging.info(f"Date {date} found for image '{file_name}' ({type}).")
    # //         self.c.images[date_number] = image_entry
    # //     else:
    # //         current_image = self.c.images[date_number]
    # //         if type == "oneshot":
    # //             if current_image.date_time_read_from == "oneshot":
    # //                 choice = self.c.ui.choose_image(
    # //                     current_image.file_name,
    # //                     file_name,
    # //                     folder_path,
    # //                     date,
    # //                 )
    # //                 if choice == 2:
    # //                     self.c.images.update({date_number: image_entry})
    # //             else:
    # //                 self.c.images.update({date_number: image_entry})
    # //         else:
    # //             if current_image.date_time_read_from != "oneshot":
    # //                 choice = self.c.ui.choose_image(
    # //                     current_image.file_name,
    # //                     file_name,
    # //                     folder_path,
    # //                     date,
    # //                 )
    # //                 if choice == 2:
    # //                     self.c.images.update({date_number: image_entry})
    # //         # // date_only = datetime.strftime(date, "%Y-%m-%d")
    # //         # // logging.info(
    # //         # //     f"Skipping image {file_name}. There is already a entry at {date_only}."
    # //         # // )

    # //         self.c.counts["skipped"] += 1
