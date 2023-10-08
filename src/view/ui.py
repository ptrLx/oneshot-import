from abc import ABC, abstractmethod
from datetime import datetime


class UI(ABC):
    def __init__(self, controller, auto_decide: bool, confirm_actions: bool) -> None:
        self.auto_decide = auto_decide
        self.c = controller
        self.confirm_actions = confirm_actions

    @abstractmethod
    def start(self) -> None:
        ...
