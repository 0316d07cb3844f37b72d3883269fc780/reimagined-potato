import unittest

from utility.src.string_utils import *
import utility.src.string_utils as su


class Test_Utils(unittest.TestCase):
    def test_create_tag(self):
        result = create_tag("my_tag", "value")
        self.assertEqual(result, "<my_tag>value<\\my_tag>")


    def test_get_id_list(self):
        my_id_list = [1, 10, 23, 100, 4]
        self.assertEqual(my_id_list, get_id_list(str(my_id_list)))

    def test_detag_given_tags(self):
        string = create_tag("my_tag1", "value1") + create_tag("my_tag2", "value2") + create_tag("my_tag1", "value3")
        result = detag_given_tags(string, "my_tag2", "my_tag1", "my_tag1")
        expected_result = ("value2", "value1", "value3")
        self.assertEqual(result, expected_result)

    def test_detag_repeated(self):
        string = create_tag("my_tag1", "value1") + create_tag("my_tag2", "value2") + create_tag("my_tag1", "value3")
        result=detag_repeated(string,"my_tag1")
        expected_result=["value1","value3"]
        self.assertEqual(result, expected_result)

    def test_hostile_detag(self):
        string = "<\\garbage end tag>" + create_tag("my_tag1", "value1") + create_tag("my_tag2", "value2")
        result = detag_given_tags(string, "my_tag2", "my_tag1")
        expected_result = ("value2", "value1")
        self.assertEqual(result, expected_result)

    def test_detagging_what_is_not_there(self):
        string="no tags"
        self.assertEqual(detag_given_tags(string,"tag"),("",))

    def test_list_tags_and_values(self):
        string = create_tag("my_tag1", "value1") + create_tag("my_tag2", "value2") + create_tag("my_tag1", "value3")
        result = list_tags_and_values(string)
        expected_result = [("my_tag1","value1"), ("my_tag2","value2"), ("my_tag1","value3")]
        self.assertEqual(result, expected_result)

    def test_finding_the_files(self):
        string = "Noise<noisetag>noise_value<\\noisetag><!!file>file content.cool_file_ending<!!\\file>"
        expected_result=(37,83,2,"file content.cool_file_ending")
        self.assertEqual(expected_result, su._find_next_file(string))

    def test_load_file(self):
        string = "testtext<tag><!file>\\utility\\test\\resources\\string_util.test_format<!\\file><!tag>"
        expected_result = "testtext<tag>cool file content<!!tag>content<!!\\tag>\nline 2 <!tag><!tag>"
        self.assertEqual(expected_result,load_files(string))






if __name__ == '__main__':
    unittest.main()
