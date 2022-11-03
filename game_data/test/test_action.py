import unittest
from test_person_fighting import make_person
from game_data.src.action import create_tackle, create_brace, Action



class Test_tackle(unittest.TestCase):


    def assign_tackle(self):
        tackler, tackled = make_person(), make_person()
        self.assertEqual(len(tackler.actions), 0)
        my_tackle=create_tackle(tackler, [tackled])
        self.assertEqual(len(tackler.actions),1)


class Test_String_Utils(unittest.TestCase):
    def test_to_and_from_str(self):
        tackler, tackled = make_person(), make_person()
        my_tackle=create_tackle(tackler, [tackled])
        my_string=str(my_tackle)
        my_other_tackle=Action.create_from_string(my_string)
        self.assertEqual(my_tackle.name,my_other_tackle.name)
        self.assertEqual(my_tackle.target_list,my_other_tackle.target_list)
        self.assertEqual(my_tackle.action_id, my_other_tackle.action_id)




if __name__ == '__main__':
    unittest.main()
