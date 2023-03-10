from imports import *
from player import Player


class Level:
    def __init__(self):
        self.player = Player(rect=Rect(200, 200, 64, 64))
        self.elements = []
        self.elements.append(self.player)

    def process_input(self, game_events):
        for e in self.elements:
            e.process_input(game_events)
            # e.process_input_complex(game_events)  # alternative input processing mode

    def update(self):
        for e in self.elements:
            e.update()

