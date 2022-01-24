"""
Contains utility functions for turning objects into strings and back.
"""


def _t(tag): return "<" + tag + ">"


def _et(tag): return "<\\" + tag + ">"


def create_tag(tag: str, string_to_add) -> str:
    return _t(tag) + str(string_to_add).replace("<", "<!") + _et(tag)


def _find_next_tag_and_tag_end(string: str) -> tuple:
    end = string.find(">")
    return string[1:end], end


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


def _detag_given_tag(string: str, tag: str) -> tuple:
    tag_start, content_start = _find_tag_and_tag_end(string, tag)
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
    return [int(a) for a in (list(string[1:-1].split(",")))]
