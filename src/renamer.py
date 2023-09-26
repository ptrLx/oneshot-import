import os
import logging
from controller import Controller


class RenameAbortedException(Exception):
    pass


class Renamer:
    def __init__(self, c: Controller) -> None:
        self.c = c

    def rename_images(self) -> None:
        if not self.c.args.get_confirmation():
            self.c.ui.confirm(
                confirmation="\nAll files that can be imported will be renamed to the OneShot naming convention. Continue?"
            )
        else:
            confirmation = True

        if confirmation:
            print()
            folder_path = self.c.args.get_image_folder_path()
            updated_images = {}

            for date_number, image_entry in self.c.images.items():
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

            self.c.images.update(updated_images)
        else:
            raise RenameAbortedException
