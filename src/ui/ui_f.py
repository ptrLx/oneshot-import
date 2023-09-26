# UI factory
def get_ui(use_gui, auto_decide):
    if use_gui:
        # to ensure cli is working when tk is not installed
        from ui.gui import GUI

        return GUI(auto_decide)
    else:
        from ui.cli import CLI

        return CLI(auto_decide)
