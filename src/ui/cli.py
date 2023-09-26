from ui.ui import UI
import logging
from datetime import datetime


class CLI(UI):
    def __init__(self, auto_decide):
        super().__init__(auto_decide)

    def inform(self, msg):
        pass

    def confirm(self, msg):
        pass

    def choose_image(self, image_name1, image_name2, image_folder_path, date):
        date_only = datetime.strftime(date, "%Y-%m-%d")
        if self.auto_decide:
            logging.info(
                f"Skipping image {image_name2}. There is already a entry at {date_only}."
            )
            return 1
        else:
            while True:
                answer = int(
                    input(
                        f"Collision at {date_only}: ({image_name1} [1], {image_name2} [2]) [1/2]: "
                    )
                )
                if answer in (1, 2):
                    return answer
