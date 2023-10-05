disclaimer = """This script imports images from past dates into your OneShot diary.
To get started, copy the images into the 'image' folder.
Make sure to copy only one image per day. Otherwise you will get asked which picture to choose (OneShots will always be preferred over other images).
Start with '--auto' to let the importer choose an image.

A 'import-me.json' file will be generated, which can be imported in the OneShot-App.

Be aware that all images will be renamed to the OneShot naming schema.
"""

# Possible image extensions in lowercase
image_extensions = (".jpg", ".jpeg", ".png")

default_export_file_path = "import-me.json"
default_image_path = "image"
default_happiness = "NOT_SPECIFIED"
default_text = "Imported by oneshot-import."
