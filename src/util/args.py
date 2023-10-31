import argparse

import util.config as config


class ArgParser:
    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(
            description="Import images from the past into OneShot."
        )

        self.parser.add_argument(
            "-y", "--yes", action="store_true", help="no confirmation request"
        )
        self.parser.add_argument(
            "--summarize",
            action="store_true",
            default=True,
            help="summarize import results",
        )
        self.parser.add_argument(
            "--no-summarize",
            action="store_false",
            dest="summarize",
            help="disable summarization",
        )
        self.parser.add_argument(
            "-p",
            "--path",
            type=str,
            default=config.default_image_path,
            help="specify a path where the images are located",
        )
        self.parser.add_argument(
            "-o",
            "--output",
            type=str,
            default=config.default_export_file_path,
            help="specify a path where the export should be stored",
        )
        self.parser.add_argument(
            "--default-text",
            type=str,
            default=config.default_text,
            help="specify default text",
        )
        self.parser.add_argument(
            "--default-happiness",
            choices=[
                "NOT_SPECIFIED",
                "VERY_HAPPY",
                "HAPPY",
                "NEUTRAL",
                "SAD",
                "VERY_SAD",
            ],
            type=str,
            default=config.default_happiness,
            help="specify default happiness level",
        )
        self.parser.add_argument(
            "--gui", action="store_true", default=True, help="start the gui"
        )
        self.parser.add_argument(
            "--auto",
            action="store_true",
            default=False,
            help="automatically pick an image if a date collision happens",
        )
        self.parser.add_argument(
            "--no-auto",
            action="store_false",
            dest="auto",
            help="disable automatic decision on date collision (OneShots will still win over other images)",
        )
        self.parser.add_argument(
            "--no-gui", "--cli", action="store_false", dest="gui", help="use the cli"
        )

    def parse(self) -> None:
        self.args = self.parser.parse_args()

    def get_confirmation(self) -> bool:
        return self.args.yes

    def should_summarize(self) -> bool:
        return self.args.summarize

    def get_image_folder_path(self) -> str:
        return self.args.path

    def get_export_file_location(self) -> str:
        return self.args.output

    def get_default_text(self) -> str:
        return self.args.default_text

    def get_default_happiness(self) -> str:
        return self.args.default_happiness

    def get_use_gui(self) -> bool:
        return self.args.gui

    def get_auto_decide(self) -> bool:
        return self.args.auto
