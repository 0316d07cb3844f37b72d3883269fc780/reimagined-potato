import unittest
from utility.src.string_utils import *

class Test_Utils(unittest.TestCase):
    def test_create_tag(self):
        result=create_tag("my_tag","value")
        self.assertEqual(result, "<my_tag>value<\\my_tag>")


    def test_detag(self):
        result=create_tag("tag1","value1")
        result+=create_tag("tag2","value2")
        value1,value2=detag(result)
        rebuild=create_tag("tag1",value1)
        rebuild+=create_tag("tag2",value2)
        self.assertEqual(result,rebuild)

    def test_get_id_list(self):
        my_id_list=[1,10,23,100,4]
        self.assertEqual(my_id_list,get_id_list(str(my_id_list)))




if __name__ == '__main__':
    unittest.main()
