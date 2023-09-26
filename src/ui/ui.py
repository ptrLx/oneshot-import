from abc import ABC, abstractmethod


class UI(ABC):
    def __init__(self, auto_decide):
        self.auto_decide = auto_decide

    @abstractmethod
    def inform(self, msg):
        ...

    @abstractmethod
    def confirm(self, msg):
        ...

    @abstractmethod
    def choose_image(self, image_name1, image_name2, image_folder_path, date):
        ...
