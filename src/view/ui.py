from abc import ABC, abstractmethod
from datetime import datetime


class UI(ABC):
    def __init__(self, controller, auto_decide: bool) -> None:
        self.auto_decide = auto_decide
        self.c = controller

    @abstractmethod
    def start(self, confirm_actions: bool) -> None:
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
