import argparse
import config


class ArgParser:
    def __init__(self):
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

    def parse(self):
        self.args = self.parser.parse_args()

    def get_confirmation(self):
        return self.args.yes

    def get_summarize(self):
        return self.args.summarize

    def get_path(self):
        return self.args.path

    def get_export_file_location(self):
        return self.args.output

    def get_default_text(self):
        return self.args.default_text

    def get_default_happiness(self):
        return self.args.default_happiness
