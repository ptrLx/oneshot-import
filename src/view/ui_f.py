from view.ui import UI


# UI factory
# to ensure cli is working when tk is not installed and to prevent circular imports
def create_ui(
    controller, use_gui: bool, auto_decide: bool, confirm_actions: bool
) -> UI:
    if use_gui:
        from view.gui import GUI

        return GUI(controller, auto_decide, confirm_actions)
    else:
        from view.cli import CLI

        return CLI(controller, auto_decide, confirm_actions)
