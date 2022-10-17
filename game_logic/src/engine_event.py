class EngineEvent:
    _Events = []

    @classmethod
    def trigger_event(cls, string: str, **kwargs):
        cls._Events.append(str)

    @classmethod
    def get_and_flush_events(cls):
        result = cls._Events
        cls._Events = []
        return result
