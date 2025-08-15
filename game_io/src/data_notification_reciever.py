class DataNotificationReciever:
    def __init__(self):
        self._data_element = None

    def register_at_data_element(self, data_element):
        self._data_element = data_element
        data_element.register_ui(self)

    def get_notification(self):
        self.redraw_self()

