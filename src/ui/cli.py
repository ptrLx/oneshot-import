from ui.ui import UI
import logging
from datetime import datetime


class CLI(UI):
    def __init__(self, auto_decide: bool) -> None:
        super().__init__(auto_decide)

    def inform(self, msg):
        print(msg)

    def confirm(self, msg: str, default_is_no=True) -> bool:
        if default_is_no:
            answer = input(f"{msg} [y/N] > ").strip().lower()
            print()
            if answer == "yes" or answer == "y":
                return True
            return False
        else:
            answer = input(f"{msg} [Y/n] > ").strip().lower()
            print()
            if answer == "no" or answer == "n":
                return False
            return True

    def choose_image(
        self,
        image_name1: str,
        image_name2: str,
        image_folder_path: str,
        date_time: datetime,
    ) -> int:
        date_only = datetime.strftime(date_time, "%Y-%m-%d")
        if self.auto_decide:
            logging.info(
                f"Skipping image {image_name2}. There is already a entry at {date_only}."
            )
            return 1
        else:
            while True:
                answer = int(
                    input(
                        f"Collision at {date_only}: ({image_name1} [1], {image_name2} [2]) [1/2] > "
                    )
                )
                if answer in (1, 2):
                    return answer
