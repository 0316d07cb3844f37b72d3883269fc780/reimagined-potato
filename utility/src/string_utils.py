"""
Contains utility functions for turning objects into strings and back.
"""

def create_tag(tag, string_to_add):
    return "<"+tag+">"+string_to_add+"<\\"+tag+">"

def find_next_tag_and_tag_end(string):
    end=string.find(">")
    return string[1:end],end

def find_content_and_tag_end(string, tag):
    content_end=string.find("<\\"+tag+">")
    tag_end=string[content_end:].find(">")+content_end
    return content_end,tag_end

def detag(string):
    to_detag=string
    result=()
    while(len(to_detag)!=0):
        tag, opening_end=find_next_tag_and_tag_end(to_detag)
        content_end, closing_end=find_content_and_tag_end(to_detag,tag)
        result+=(str(to_detag[opening_end+1:content_end]),)
        to_detag=str(to_detag[closing_end+1:])
    return result

def get_id_list(string):
    return [int(a) for a in (list(string[1:-1].split(",")))]


