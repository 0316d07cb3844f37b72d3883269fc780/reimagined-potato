import unittest
from test_person_fighting import make_person
from game_data.src.action import create_tackle, create_brace



class Test_tackle(unittest.TestCase):
    def test_tackle(self):
        tackler, tackled = make_person(), make_person()
        health_before_tackle = tackled.get_health()
        create_tackle(tackler,[tackled]).perform()
        health_after_tackle=tackled.get_health()
        self.assertEqual(health_before_tackle-6, health_after_tackle)

    def assign_tackle(self):
        tackler, tackled = make_person(), make_person()
        self.assertEqual(len(tackler.actions), 0)
        my_tackle=create_tackle(tackler, [tackled])
        self.assertEqual(len(tackler.actions),1)

class Test_brace(unittest.TestCase):
    def test_brace(self):
        bracer=make_person()
        create_brace(bracer).perform()
        self.assertEqual(bracer.resist,4)



if __name__ == '__main__':
    unittest.main()
