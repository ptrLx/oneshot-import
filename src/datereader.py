from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from datetime import datetime
import re


class DateReader:
    @staticmethod
    def read_metadata(file_path):
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

    @staticmethod
    def read_android_filename(file_name):
        # Examples: IMG_20230901_203000.jpg, 20230901_203000.PNG
        pattern = re.compile(
            r"^(IMG_)?(\d{4})(\d{2})(\d{2})_(\d{2})(\d{2})(\d{2})\.(jpe?g|png)$",
            re.IGNORECASE,
        )
        match = re.search(pattern, file_name)

        if match:
            year = int(match.group(2))
            month = int(match.group(3))
            day = int(match.group(4))
            hour = int(match.group(5))
            minute = int(match.group(6))
            second = int(match.group(7))
            return datetime(year, month, day, hour, minute, second)

        # Examples: 2023-09-01-20-30-00-000.jpg, 2023-09-01-20-30-00.PNG
        pattern = re.compile(
            r"^(\d{4})-(\d{2})-(\d{2})-(\d{2})-(\d{2})-(\d{2})(-(\d{3}))?\.(jpe?g|png)$",
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

        # Examples: IMG_20230901.jpg, 20230901.PNG
        pattern = re.compile(
            r"^(IMG_)?(\d{4})(\d{2})(\d{2})\.(jpe?g|png)$",
            re.IGNORECASE,
        )
        match = re.search(pattern, file_name)

        if match:
            year = int(match.group(2))
            month = int(match.group(3))
            day = int(match.group(4))
            return datetime(year, month, day)

        return None

    @staticmethod
    def read_ios_filename(file_name):
        # 20230901_203000000_iOS.jpg
        pattern = re.compile(
            r"^(\d{4})(\d{2})(\d{2})_(\d{2})(\d{2})(\d{2})(\d{3})?_iOS\.(jpe?g|png)$",
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

        return None

    @staticmethod
    def read_oneshot_filename(file_name):
        # OneShot_20230901203000.jpg
        pattern = re.compile(
            r"^OneShot_(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})\.(jpe?g|png)$",
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

        return None

    @staticmethod
    def read_whatsapp_filename(file_name):
        # IMG-20230901-WA0007.jpg
        pattern = re.compile(
            r"^(IMG-)?(\d{4})(\d{2})(\d{2})-WA(\d{4})\.(jpe?g|png)$",
            re.IGNORECASE,
        )
        match = re.search(pattern, file_name)

        if match:
            year = int(match.group(2))
            month = int(match.group(3))
            day = int(match.group(4))
            return datetime(year, month, day)

        return None
