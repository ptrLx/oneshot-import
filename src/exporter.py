import json
import os
import logging
from controller import Controller


def export_json(c: Controller):
    json_export = []
    for date_number, image_entry in c.selected_images.items():
        json_entry = {
            "date": date_number,
            "created": image_entry.timestamp(),
            "dayOfYear": image_entry.day_of_year(),
            "relativePath": image_entry.file_name,
            "happiness": c.args.get_default_happiness(),
            "motivation": "",
            "textContent": c.args.get_default_text(),
        }
        json_export.append(json_entry)

    file_path = c.args.get_export_file_location()
    with open(file_path, "w") as json_file:
        json.dump(json_export, json_file, indent=4)
        logging.info(f"Import file written to '{file_path}'")
