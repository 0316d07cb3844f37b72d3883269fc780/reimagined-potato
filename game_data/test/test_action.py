import unittest
from test_person_data import make_person
from game_data.src.action import create_tackle



class Test_tackle(unittest.TestCase):
    def test_tackle(self):
        tackler, tackled = make_person(), make_person()
        health_before_tackle = tackled.health
        create_tackle(tackler,tackled).perform()
        health_after_tackle=tackled.health
        self.assertEqual(health_before_tackle-4, health_after_tackle)


if __name__ == '__main__':
    unittest.main()
