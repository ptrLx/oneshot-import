import os
import logging
from controller import Controller
from image_entry import ImageEntry


def rename_images(c: Controller) -> None:
    folder_path = c.args.get_image_folder_path()
    updated_images = {}

    for date_number, image_entry in c.images.items():
        file_extension = os.path.splitext(image_entry.file_name)[-1].lower()
        if file_extension == ".jpeg":
            file_extension = ".jpg"
        new_file_name = (
            f"OneShot_{image_entry.date_time.strftime('%Y%m%d%H%M%S')}{file_extension}"
        )

        if image_entry.file_name != new_file_name:
            try:
                os.rename(
                    f"{folder_path}/{image_entry.file_name}",
                    f"{folder_path}/{new_file_name}",
                )
                updated_images[date_number] = ImageEntry(
                    new_file_name,
                    image_entry.date_time,
                    image_entry.date_time_read_from,
                )
                logging.info(f"Renamed '{image_entry.file_name}' to '{new_file_name}'")
            except OSError as e:
                print(f"Failed to rename {image_entry.file_name}: {e}")
                exit(1)

    c.images.update(updated_images)
