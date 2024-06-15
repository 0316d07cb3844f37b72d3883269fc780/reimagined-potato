import unittest
from utility.src.logging_util import client_networker_logger
from utility.src.string_utils import root_path


class MyTestCase(unittest.TestCase):
    def test_something(self):
        client_networker_logger.info("test")
        client_networker_logger.info("test_next_line")
        with open(root_path("logs\\" + "client_network_logs"), "r") as file:
            line_count = sum(1 for line in file)
        self.assertEqual(line_count, 2)


if __name__ == '__main__':
    unittest.main()
