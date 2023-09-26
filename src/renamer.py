import os
import logging


class RenameAbortedException(Exception):
    pass


def rename_images(images, args):
    if not args.get_confirmation():
        answer = (
            input(
                f"\nAll files that can be imported will be renamed to the OneShot naming convention. Continue? (y/N): "
            )
            .strip()
            .lower()
        )
    else:
        answer = "yes"

    if args.get_confirmation() or answer == "yes" or answer == "y":
        print()
        folder_path = args.get_image_folder_path()
        updated_images = {}

        for date_number, image_entry in images.items():
            file_extension = os.path.splitext(image_entry.file_name)[-1].lower()
            new_file_name = f"OneShot_{image_entry.date_time.strftime('%Y%m%d%H%M%S')}{file_extension}"

            if image_entry.file_name != new_file_name:
                try:
                    os.rename(
                        f"{folder_path}/{image_entry.file_name}",
                        f"{folder_path}/{new_file_name}",
                    )
                    updated_images[date_number] = (
                        new_file_name,
                        image_entry.date_time,
                        image_entry.datetime_read_from,
                    )
                    logging.info(
                        f"Renamed '{image_entry.file_name}' to '{new_file_name}'"
                    )
                except OSError as e:
                    print(f"Failed to rename {image_entry.file_name}: {e}")
                    exit(1)

        images.update(updated_images)
    else:
        raise RenameAbortedException
