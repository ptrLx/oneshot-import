from abc import ABC, abstractmethod
from datetime import datetime


class UI(ABC):
    def __init__(self, auto_decide) -> None:
        self.auto_decide = auto_decide

    @abstractmethod
    def inform(self, msg) -> None:
        ...

    @abstractmethod
    def confirm(self, msg, default_is_no=True) -> bool:
        ...

    @abstractmethod
    def choose_image(
        self,
        images: list,  # of ImageEntries
        image_folder_path: str,
        date_time: datetime,
    ):
        ...
