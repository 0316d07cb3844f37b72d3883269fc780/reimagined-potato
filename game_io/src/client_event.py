class ClientEvent:
    _Events = []

    @classmethod
    def trigger_event(cls, event):
        cls._Events += event

    @classmethod
    def get_and_flush_events(cls):
        result = cls._Events
        cls._Events = []
        return result
