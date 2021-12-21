"""
An action that a person will perform at the end of the turn.
"""



class Action():
    def __init__(self, performer, name, method, id):
        self.name = name
        self.performer=performer
        self.perform=method
        self.id=id

def create_tackle(tackler, tackled):
    tackle_method=lambda:tackled.damage(4)
    tackle=Action(tackler,"Tackle",tackle_method,1)
    return tackle