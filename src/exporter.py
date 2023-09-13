import json


def generate_import_me(images, args):
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

    with open(args.get_export_file_location(), "w") as json_file:
        json.dump(json_export, json_file, indent=4)
