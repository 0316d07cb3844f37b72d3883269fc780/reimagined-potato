"""
Runs all the computations.
"""

class Game_Host():
    def __init__(self, fight_scene):
        self.fight_scene=fight_scene
        self.events=[]

    def add_event(self, event):
        self.check_event(event)
        self.events.append(event)

    def check_event(self,event):
        pass

    def process_event(self,event):
        pass

    def update(self):
        for event in self.events:
            self.process_event(event)
        self.events.clear()

class Event():
    pass