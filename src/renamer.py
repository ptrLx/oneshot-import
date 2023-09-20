import os
import logging


def rename_images(images, args):
    """
    Rename images to the OneShot naming convention.
    """
    # todo docstring
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
        folder_path = args.get_path()
        updated_images = {}

        for date_number, (date, file_name) in images.items():
            file_extension = os.path.splitext(file_name)[-1].lower()
            new_file_name = f"OneShot_{date.strftime('%Y%m%d%H%M%S')}{file_extension}"

            try:
                os.rename(
                    f"{folder_path}/{file_name}", f"{folder_path}/{new_file_name}"
                )
                updated_images[date_number] = (date, new_file_name)
                logging.info(f"Renamed '{file_name}' to '{new_file_name}'")
            except OSError as e:
                print(f"Failed to rename {file_name}: {e}")
                exit(1)

        images.clear()
        images.update(updated_images)
    else:
        print("Aborting.")
        exit(0)
