import unittest
from game_logic.src.atomic_event import AtomicEvent, EventType


class MyTestCase(unittest.TestCase):
    def test_creation_from_string(self):
        my_event = AtomicEvent(EventType.damage, berries="hello", dark="no")
        my_string = str(my_event)
        recreation = AtomicEvent.create_from_string(my_string)
        self.assertEqual(recreation.event_type, my_event.event_type)
        self.assertEqual(recreation.attributes, my_event.attributes)


if __name__ == '__main__':
    unittest.main()
