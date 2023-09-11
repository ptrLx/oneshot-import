disclaimer = """This script imports images from past dates into your OneShot diary.
To get started, copy the images into the 'image' folder.
Make sure to copy only one image per day. Otherwise the importer will select one of them.

A import-me.json file will be generated, which can be imported in the OneShot-App.
"""

# Possible image extensions in lowercase
image_extensions = (".jpg", ".jpeg", ".png")

# Folder that contains the images
folder_path = "image"

export_file_name = "import-me.json"

default_happiness = "NOT_SPECIFIED"

default_text = "Imported by oneshot-import."
