from dataclasses import dataclass
from datetime import datetime


@dataclass
class ImageEntry:
    file_name: str
    date_time: datetime
    date_time_read_from: str

    def __init__(self, file_name, date_time, date_time_read_from):
        self.file_name = file_name
        self.date_time = date_time
        self.date_time_read_from = date_time_read_from

    def get_date_number(self):
        reference_date = datetime(1970, 1, 1)
        delta = self.date_time - reference_date
        days_since_reference = delta.days
        return days_since_reference
