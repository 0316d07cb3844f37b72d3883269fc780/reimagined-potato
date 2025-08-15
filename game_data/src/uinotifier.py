class UINotifier:
    def __init__(self):
        self._ui = None

    def notify(self):
        if self._ui:
            self._ui.get_notification()

    def register_ui(self, ui):
        self._ui = ui
