import unittest
from game_io.src.client_event_builder import builder
from game_io.src.client_event import ClientEvent


class MyTestCase(unittest.TestCase):
    def test_builder(self):
        builder.pass_priority()
        events = ClientEvent.get_and_flush_events()
        self.assertTrue(len(events) == 1)


if __name__ == '__main__':
    unittest.main()
