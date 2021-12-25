"""
An action that a person will perform at the end of the turn.
"""



class Action():
    def __init__(self, performer, name, method, id):
        self.name = name
        self.performer=performer
        self.perform=method
        self.id=id
        performer.append_action(self)

def create_tackle(tackler, tackled):
    tackle_method=lambda:tackled.damage(6)
    tackle=Action(tackler,"Tackle",tackle_method,1)
    return tackle

def create_brace(bracer):
    def brace(bracer):
        bracer.resist+=4
    return Action(bracer, "Brace", lambda:brace(bracer),2)