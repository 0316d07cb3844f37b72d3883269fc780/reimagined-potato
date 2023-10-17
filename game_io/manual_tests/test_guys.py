import unittest
from game_data.test.test_person_fighting import make_person
from game_data.src.persondata import PersonData
from game_data.src.person_fighting import Person_Fighting
from game_io.src.personio import PersonIO
from base_test import test_sprite

class MyTestPerson(unittest.TestCase):
    def test_drawing_a_guy(self):
        my_guy_builder = lambda: PersonIO(make_person(), (100, 100))
        test_sprite(my_guy_builder)

    def test_draw_guy_from_file(self):
        base_guy = PersonData.create_from_string("<file>resources\\People\\Bases\\knight.person_base<\\file>")
        fighter = Person_Fighting(base_guy)
        file_guy_maker = lambda: PersonIO(fighter, (100, 100))
        test_sprite(file_guy_maker)



if __name__ == '__main__':
    unittest.main()
