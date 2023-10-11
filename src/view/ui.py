from abc import ABC, abstractmethod
from datetime import datetime


class UI(ABC):
    def __init__(self, controller, skip_confirm_actions: bool) -> None:
        self.c = controller
        self.skip_confirm_actions = skip_confirm_actions

    @abstractmethod
    def start(self) -> None:
        ...
