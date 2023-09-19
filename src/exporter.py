import json
import os
import logging


def generate_import_me(images, args):
    if images:
        json_export = []
        for date_number, (date, file_name) in images.items():
            json_entry = {
                "date": date_number,
                "created": int(date.timestamp()),
                "dayOfYear": date.timetuple().tm_yday,
                "relativePath": file_name,
                "happiness": args.get_default_happiness(),
                "motivation": "",
                "textContent": args.get_default_text(),
            }
            json_export.append(json_entry)

        write_import_me(json_export, args)


def write_import_me(json_export, args):
    file_path = args.get_export_file_location()

    if (
        os.path.exists(file_path)
        and os.path.isfile(file_path)
        and not args.get_confirmation()
    ):
        answer = (
            input(
                f"The file '{file_path}' already exists. Do you want to overwrite it? (y/N): "
            )
            .strip()
            .lower()
        )
    else:
        answer = "yes"

    if args.get_confirmation() or answer == "yes" or answer == "y":
        with open(file_path, "w") as json_file:
            json.dump(json_export, json_file, indent=4)
            logging.info(f"Import file was written to {file_path}")
