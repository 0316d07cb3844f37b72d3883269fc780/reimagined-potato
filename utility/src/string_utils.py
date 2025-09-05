"""
Contains utility functions for turning objects into strings and back.
"""

from global_variables import ROOT


def _t(tag): return "<" + tag + ">"


def _et(tag): return "<\\" + tag + ">"


def create_tag(tag: str, string_to_add) -> str:
    return _t(tag) + str(string_to_add).replace("<", "<!") + _et(tag)


def _find_next_tag_and_tag_end(string: str) -> tuple:
    tag_start=string.find("<")
    if string[tag_start+1]=="\\" :
        return _find_next_tag_and_tag_end(string[tag_start+1:])
    end = string.find(">")
    return string[tag_start+1:end], end


def _find_content_and_tag_end(string: str, tag: str) -> tuple:
    content_end = string.find(_et(tag))
    tag_end = string[content_end:].find(">") + content_end
    return content_end, tag_end


def _find_tag_and_tag_end(string: str, tag: str) -> tuple:
    tag_start = string.find(_t(tag))
    tag_end = string[tag_start:].find(">") + tag_start
    return tag_start, tag_end


def _detag(string: str) -> tuple:
    to_detag = string
    result = ()
    while (len(to_detag) != 0):
        tag, opening_end = _find_next_tag_and_tag_end(to_detag)
        content_end, closing_end = _find_content_and_tag_end(to_detag, tag)
        result += (str(to_detag[opening_end + 1:content_end]),)
        to_detag = str(to_detag[closing_end + 1:])
    return result


def list_tags_and_values(string: str) -> list:
    to_detag = string
    result = []
    while len(to_detag)!=0:
        tag, opening_end = _find_next_tag_and_tag_end(to_detag)
        if tag == '':
            break
        content_end, closing_end = _find_content_and_tag_end(to_detag, tag)
        content = str(to_detag[opening_end + 1:content_end])
        result += [(tag, content.replace("<!", "<"))]
        to_detag = str(to_detag[closing_end + 1:])
    return result


def _detag_given_tag(string: str, tag: str) -> tuple:
    tag_start, content_start = _find_tag_and_tag_end(string, tag)
    if tag_start == -1:
        result = ""
        remainder = string
        return result, remainder
    content_end, tag_end = _find_content_and_tag_end(string, tag)
    result = string[content_start + 1:content_end]
    result = result.replace("<!", "<")
    remainder = string[:tag_start] + string[tag_end + 1:]
    return result, remainder


def detag_given_tags(string: str, *tags: (str,)) -> tuple:
    result = ()
    for tag in tags:
        value, string = _detag_given_tag(string, tag)
        result += (value,)
    return result


def detag_repeated(string: str, tag: str) -> list:
    results = []
    while (_t(tag) in string):
        result, string = _detag_given_tag(string, tag)
        results += [result]
    return results


def get_id_list(string: str) -> list:
    if string == "[]":
        return []
    if "," not in string:
        return [int(string[1:-1])]
    return [int(a) for a in (list(string[1:-1].split(",")))]


def _find_next_file(string: str):
    ending_of_file_tag = string.find("file>")
    if ending_of_file_tag == -1:
        return -1, -1, 0, ""
    reversed_string= string[ending_of_file_tag::-1]
    order_of_depth = reversed_string.find("<")-1  # AKA amount of ! bangs
    start_of_file_tag = ending_of_file_tag-1-order_of_depth
    end_of_closing_tag = string.find("\\file>")+6
    start_of_content = string[start_of_file_tag:end_of_closing_tag].find(">")+1
    end_of_content = -start_of_content-1
    file_name = string[start_of_file_tag:end_of_closing_tag][start_of_content:end_of_content]
    return start_of_file_tag, end_of_closing_tag, order_of_depth, file_name


def increase_order(string: str, order: int) -> str:
    return string.replace("<", "<"+"!"*order)


def load_files(string: str) -> str:
    start, end, order, file_name=_find_next_file(string)
    if start == -1:
        return string
    with open(root_path(file_name)) as file:
        file_content=file.read()
    return string[:start]+increase_order(file_content, order)+string[end:]


def unroot_path(path: str) -> str:
    if path is None:
        return None
    path = path.replace("/", "\\")
    return path.replace(ROOT, "", 1)


def root_path(path: str) -> str:
    if path is None:
        return None
    return ROOT + path


def read_and_clean_file(path: str) -> str:
    with open(root_path(path)) as file:
        file_contents = file.read()
    int_tags = detag_repeated(file_contents, "int")
    file_contents += "".join(int_tags)
    return file_contents


def write_string_to_file(to_be_written: str, path: str):
    with open(root_path(path), "a") as file:
        file.write(to_be_written)

