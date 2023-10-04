from collections import defaultdict
from collections import Counter
from ui.ui_f import get_ui
from args import ArgParser
from image_entry import ImageEntry


class Controller:
    def __init__(self) -> None:
        self.args = ArgParser()

        # Dictionary of all found images with key as date_number and value as list of ImageEntry
        # dict<str>:<list<ImageEntry>>
        # Example: 19601: [("IMG_20230901_203000.jpg", 2023-09-01-20-30-00, "metadata"), (...)]
        self.images = defaultdict(list)

        # Dictionary of all chosen images
        # This one will not have date conflicts anymore
        self.selected_images = defaultdict(ImageEntry)

        # Counters for where the date was read from. This will be used after all images where read from folder.
        # Possible types: metadata, android, ios, oneshot, whatsapp, skipped, error
        self.counts = Counter()

        # Either gui or cli
        # Will get initialized later
        self.ui = None

    def parse_args(self) -> None:
        self.args.parse()

    def init_ui(self) -> None:
        self.ui = get_ui(self.args.get_use_gui(), self.args.get_auto_decide())

    def read_images(self) -> None:
        pass

    def write_export(self) -> None:
        pass
