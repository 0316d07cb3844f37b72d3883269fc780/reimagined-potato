"""
An action that a person will perform at the end of the turn.
"""

from utility.src.string_utils import create_tag,detag,get_id_list


class Action():
    def __init__(self,name, performer, target_list,  method, id):
        self.name = name
        self.performer=performer
        self.target_list=target_list
        self.perform=method
        self.action_id=id
        performer.append_action(self)

    def __str__(self):
        my_string=create_tag("name",self.name)
        my_string+=create_tag("performer_id", self.performer.action_id)
        my_string+=create_tag("target_id_list",self.target_list)
        my_string+=create_tag("id", self.action_id)
        return my_string




def create_tackle(tackler, tackled_list):
    tackle_method=lambda:tackled_list[0].damage(6)
    tackle=Action("Tackle", tackler, tackled_list, tackle_method,1)
    return tackle

def create_brace(bracer, braced=None):
    def brace(bracer):
        bracer.resist+=4
    return Action("Brace", bracer, [],  lambda:brace(bracer),2)


creator_by_id={
    1:create_tackle,
    2:create_brace
}

def create_from_string(string):
    name, performer_id, target_id_list, id = detag(string)
