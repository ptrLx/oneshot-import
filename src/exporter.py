import json
import os
import logging
from controller import Controller


class GenerationAbortedException(Exception):
    pass


class Exporter:
    def __init__(self, c: Controller) -> None:
        self.c = c
        self.json_export = []

    def __generate_export(self):
        for date_number, image_entry in self.c.images.items():
            json_entry = {
                "date": date_number,
                "created": int(image_entry.date_time.timestamp()),
                "dayOfYear": image_entry.date_time.timetuple().tm_yday,
                "relativePath": image_entry.file_name,
                "happiness": self.c.args.get_default_happiness(),
                "motivation": "",
                "textContent": self.c.args.get_default_text(),
            }
            self.json_export.append(json_entry)

    def __write_export(self) -> None:
        file_path = self.c.args.get_export_file_location()

        if (
            os.path.exists(file_path)
            and os.path.isfile(file_path)
            and not self.c.args.get_confirmation()
        ):
            confirmation = self.c.ui.confirm(
                f"\nThe file '{file_path}' already exists. Do you want to overwrite it?"
            )
        else:
            confirmation = True

        if confirmation:
            print()
            with open(file_path, "w") as json_file:
                json.dump(self.json_export, json_file, indent=4)
                logging.info(f"Import file written to '{file_path}'")
        else:
            raise GenerationAbortedException

    def export(self):
        self.__generate_export()
        self.__write_export()
