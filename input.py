from enum import Enum, auto
from collections import defaultdict

from imports import *


class InputType(Enum):
    '''
    Expose three key_check types as pygame does not have a KEYPRESSED event type
    but rather has a K_{key} in pygame.key.get_pressed
    '''
    _KEYPRESSED = auto()
    _KEYDOWN = auto()
    _KEYUP = auto()


class Input:
    '''
    Instanciate
    Update on every tick
    call
    return:boolean
        True is key passed key_check_type test 
        (aka key was either pressed, downed or upped)
    '''
    def __init__(self):
        self.keys_downed = defaultdict(lambda: False)
        self.keys_upped = defaultdict(lambda: False)
        self.simon_says_move = False

    def __call__(self, key, key_check_type):
        if key_check_type == InputType._KEYPRESSED:
            return self.key_is_pressed(key)
        elif key_check_type == InputType._KEYDOWN:
            return self.key_downed(key)
        elif key_check_type == InputType._KEYUP:
            return self.key_upped(key)

    def key_is_pressed(self, key):
        '''
        simon_says_move is used to only check for movement at a limited frequency
        see self.update for mechanic setting its value
        Note this should eventyally be done in a different way in order to only
        apply to movement keys
        '''
        return self.simon_says_move and pygame.key.get_pressed()[key]

    def key_downed(self, key):
        return key in self.keys_downed
    
    def key_upped(self, key):
        return key in self.keys_upped
    
    def update(self, game_events):
        self.keys_downed = defaultdict(lambda: False)
        self.keys_upped = defaultdict(lambda: False)
        self.simon_says_move = False
        for event in game_events:
            if event.type == KEYDOWN:
                self.keys_downed[event.key] = True
            elif event.type == KEYUP:
                self.keys_upped[event.key] = True
            elif event.type == MOVEMENT_EVENT:
                self.simon_says_move = True

