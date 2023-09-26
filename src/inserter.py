import logging
from datetime import datetime
from datereader import read_date_and_type
from image_entry import ImageEntry
from controller import Controller


class Inserter:
    def __init__(self, c: Controller) -> None:
        self.c = c

    def insert_image(self, file_name: str) -> None:
        date, type = self.__get_date_and_type(
            self.c.args.get_image_folder_path(), file_name
        )

        if not type:
            logging.warning(f"Date of image {file_name} not readable.")
            self.c.counts["error"] += 1
            return

        image_entry = ImageEntry(file_name, date, type)
        date_number = image_entry.get_date_number()

        if date_number not in self.c.images:
            logging.info(
                f"Date {date} found for image '{file_name}' in filename ({type})."
            )
            self.c.images[date_number] = image_entry
        else:
            if type == "oneshot":
                if self.c.images[date_number].date_time_read_from == "oneshot":
                    choice = self.c.ui.choose_image(
                        self.c.images[date_number].file_name,
                        file_name,
                        self.c.args.get_image_folder_path(),
                        date,
                    )
                    if choice == 2:
                        self.c.images.update({date_number: image_entry})
                else:
                    self.c.images.update({date_number: image_entry})
            else:
                date_only = datetime.strftime(date, "%Y-%m-%d")
                logging.info(
                    f"Skipping image {file_name}. There is already a entry at {date_only}."
                )

            self.c.counts["skipped"] += 1
