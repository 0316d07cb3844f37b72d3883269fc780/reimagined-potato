"""
Contains a function taking a gamestate and a group allsprites and adding a representation of the game state to the group
allsprites.
"""

def do_update_io(allsprites, game_state):
    allsprites.empty()
    render_allies(allsprites,game_state)
    render_foes(allsprites,game_state)

def render_allies(allsprites, game_state):
    pass

def render_foes(allsprites, game_state):
    pass