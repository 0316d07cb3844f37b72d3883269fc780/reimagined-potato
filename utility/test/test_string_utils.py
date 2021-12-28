import unittest
from utility.src.string_utils import *


class Test_Utils(unittest.TestCase):
    def test_create_tag(self):
        result=create_tag("my_tag","value")
        self.assertEqual(result, "<my_tag>value<\\my_tag>")

    def test_find_next_tag_and_tag_end(self):
        result = create_tag("tag1", "value1")
        result += create_tag("tag2", "value2")
        self.assertTrue(len(result)!=0)
        self.assertEqual(find_next_tag_and_tag_end(result),("tag1",5))

    def test_find_content_and_tag_end(self):
        result = create_tag("tag1", "value1")
        result += create_tag("tag2", "value2")
        tag, opening_end=find_next_tag_and_tag_end(result)
        content_end, closing_end=find_content_and_tag_end(result,tag)
        self.assertEqual((result[opening_end+1:content_end],),("value1",))

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
