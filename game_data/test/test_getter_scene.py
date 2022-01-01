import unittest

from game_data.src.getter_scene import getter


class MyGetterTest(unittest.TestCase):
    def test_setting_and_getting(self):
        myClass = type("ClassName", (), {})
        my_object = myClass()
        getter.register(my_object)
        my_retrieved = getter[my_object.scene_id]
        self.assertEqual(my_retrieved, my_object)


if __name__ == '__main__':
    unittest.main()
