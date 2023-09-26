import json
import os
import logging


class GenerationAbortedException(Exception):
    pass


def generate_import_me(images, args):
    json_export = []
    for date_number, image_entry in images.items():
        json_entry = {
            "date": date_number,
            "created": int(image_entry.date_time.timestamp()),
            "dayOfYear": image_entry.date_time.timetuple().tm_yday,
            "relativePath": image_entry.file_name,
            "happiness": args.get_default_happiness(),
            "motivation": "",
            "textContent": args.get_default_text(),
        }
        json_export.append(json_entry)

    __write_import_me(json_export, args)


def __write_import_me(json_export, args):
    file_path = args.get_export_file_location()

    if (
        os.path.exists(file_path)
        and os.path.isfile(file_path)
        and not args.get_confirmation()
    ):
        answer = (
            input(
                f"\nThe file '{file_path}' already exists. Do you want to overwrite it? (y/N): "
            )
            .strip()
            .lower()
        )
    else:
        answer = "yes"

    if args.get_confirmation() or answer == "yes" or answer == "y":
        print()
        with open(file_path, "w") as json_file:
            json.dump(json_export, json_file, indent=4)
            logging.info(f"Import file written to '{file_path}'")
    else:
        raise GenerationAbortedException
