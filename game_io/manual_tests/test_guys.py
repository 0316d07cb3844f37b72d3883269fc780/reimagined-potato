import unittest
from game_data.test.test_person_fighting import make_person
from game_io.src.person_io import Person_IO
from base_test import test_sprite

class MyTestPerson(unittest.TestCase):
    def test_drawing_a_guy(self):
        my_guy_builder = lambda: Person_IO(make_person(), (100, 100))
        test_sprite(my_guy_builder)



if __name__ == '__main__':
    unittest.main()
