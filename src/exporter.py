import json

from config import export_file_name, default_happiness, default_text


def generate_import_me(images):
    json_export = []
    for date_number, (date, file_name) in images.items():
        json_entry = {
            "date": date_number,
            "created": int(date.timestamp()),
            "dayOfYear": date.timetuple().tm_yday,
            "relativePath": file_name,
            "happiness": default_happiness,
            "motivation": "",
            "textContent": default_text,
        }
        json_export.append(json_entry)

    with open(export_file_name, "w") as json_file:
        json.dump(json_export, json_file, indent=4)
