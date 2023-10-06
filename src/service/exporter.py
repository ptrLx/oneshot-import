import json
import logging


def exporter_service(controller):
    json_export = []
    for date_number, image_entry in controller.selected_images.items():
        json_entry = {
            "date": date_number,
            "created": image_entry.timestamp(),
            "dayOfYear": image_entry.day_of_year(),
            "relativePath": image_entry.file_name,
            "happiness": controller.args.get_default_happiness(),
            "motivation": "",
            "textContent": controller.args.get_default_text(),
        }
        json_export.append(json_entry)

    file_path = controller.args.get_export_file_location()
    with open(file_path, "w") as json_file:
        json.dump(json_export, json_file, indent=4)

    controller.set_event("export_finished")
