from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from datetime import datetime
import re


def __read_metadata(file_path: str) -> datetime:
    try:
        image = Image.open(file_path)
        exif_data = image._getexif()
        date = None
        for tag, value in exif_data.items():
            tag_name = TAGS.get(tag, tag)
            if tag_name == "DateTimeOriginal":
                date = datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
                break

        # * Use this code to look for additional tags like "DateTime" and "CreateDate". This is currently untested.
        # // if not date_tag:
        # //     for tag, value in exif_data.items():
        # //         tag_name = TAGS.get(tag, tag)
        # //         if tag_name == "DateTime" or tag_name == "CreateDate":
        # //             date_tag = value # todo check format
        # //             break

        return date

    except AttributeError:
        return None


def __read_re_date_time(regexp: str, file_name: str) -> datetime:
    pattern = re.compile(
        regexp,
        re.IGNORECASE,
    )
    match = re.search(pattern, file_name)

    if match:
        year = int(match.group(1))
        month = int(match.group(2))
        day = int(match.group(3))
        hour = int(match.group(4))
        minute = int(match.group(5))
        second = int(match.group(6))
        return datetime(year, month, day, hour, minute, second)


def __read_re_date_only(regexp: str, file_name: str) -> datetime:
    pattern = re.compile(
        regexp,
        re.IGNORECASE,
    )
    match = re.search(pattern, file_name)

    if match:
        year = int(match.group(2))
        month = int(match.group(3))
        day = int(match.group(4))
        return datetime(year, month, day)

    return None


def __read_android_filename(file_name: str) -> datetime:
    # Examples: IMG_20230901_203000.jpg, 20230901_203000.PNG
    regexp = r"^(IMG_)?(\d{4})(\d{2})(\d{2})_(\d{2})(\d{2})(\d{2})\.(jpe?g|png)$"
    date_time = __read_re_date_time(regexp, file_name)
    if date_time:
        return date_time

    # Examples: 2023-09-01-20-30-00-000.jpg, 2023-09-01-20-30-00.PNG
    regexp = (
        r"^(\d{4})-(\d{2})-(\d{2})-(\d{2})-(\d{2})-(\d{2})(-(\d{3}))?\.(jpe?g|png)$"
    )
    date_time = __read_re_date_time(regexp, file_name)
    if date_time:
        return date_time

    # Examples: IMG_20230901.jpg, 20230901.PNG
    regexp = r"^(IMG_)?(\d{4})(\d{2})(\d{2})\.(jpe?g|png)$"
    date_time = __read_re_date_only(regexp, file_name)
    if date_time:
        return date_time

    return None


def __read_ios_filename(file_name: str) -> datetime:
    # 20230901_203000000_iOS.jpg
    regexp = r"^(\d{4})(\d{2})(\d{2})_(\d{2})(\d{2})(\d{2})(\d{3})?_iOS\.(jpe?g|png)$"
    return __read_re_date_time(regexp, file_name)


def __read_oneshot_filename(file_name: str) -> datetime:
    # OneShot_20230901203000.jpg
    regexp = r"^OneShot_(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})\.(jpe?g|png)$"
    return __read_re_date_time(regexp, file_name)


def __read_whatsapp_filename(file_name: str) -> datetime:
    # IMG-20230901-WA0007.jpg
    regexp = (r"^(IMG-)?(\d{4})(\d{2})(\d{2})-WA(\d{4})\.(jpe?g|png)$",)
    return __read_re_date_only(regexp, file_name)


def read_date_and_type(self, folder_path: str, file_name: str) -> (datetime, str):
    date = __read_oneshot_filename(file_name)
    if date:
        return date, "oneshot"

    date = __read_metadata(f"{folder_path}/{file_name}")
    if date:
        return date, "metadata"

    date = __read_android_filename(file_name)
    if date:
        return date, "android"

    date = __read_ios_filename(file_name)
    if date:
        return date, "ios"

    date = __read_whatsapp_filename(file_name)
    if date:
        return date, "whatsapp"

    return None, None
