from enum import Enum, auto
from collections import defaultdict

from imports import *


class Events:
    def __init__(self):
        '''
        Holds the keyboard key pressed, down and up information
        '''
        self.keys_pressed = None
        self.keys_upped = defaultdict(lambda: False)
        self.keys_downed = defaultdict(lambda: False)

    def update(self, game_events):
        '''
        populates keyboard event data from pygame.event and pygame.key.get_pressed()
        run at every tick of the game.
        '''
        self.keys_pressed = pygame.key.get_pressed()
        self.keys_upped = defaultdict(lambda: False)
        self.keys_downed = defaultdict(lambda: False)
        self.simon_says = False
        for event in game_events:
            if event.type == KEYDOWN:
                self.keys_downed[event.key] = True
            elif event.type == KEYUP:
                self.keys_upped[event.key] = True
            elif event.type == MOVEMENT_EVENT:
                self.simon_says = True


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
        True if key passed key_check_type test 
        (aka key was either pressed, downed or upped)
    '''
    def __init__(self, events):
        self.keys_pressed = None
        self.keys_upped = defaultdict(lambda: False)
        self.keys_downed = defaultdict(lambda: False)
        self.simon_says = False
        self.events = events

    def __call__(self, key, key_check_type):
        '''
        Call the instance to do a spedified check on a key
        Ex.:
            check if the "w" key went down (aka just got pressed)
            ```
            input = Input() # This is done in the setup of the game
            input(K_w, InputType._KEYDOWN) # this is done in the game loop
            ```
        return:bool
            returns True if the specified check is true
        '''
        if key_check_type == InputType._KEYPRESSED:
            return self._key_is_pressed(key)
        elif key_check_type == InputType._KEYDOWN:
            return self.key_downed(key)
        elif key_check_type == InputType._KEYUP:
            return self.key_upped(key)

    def _key_is_pressed(self, key):
        '''
        simon_says is used to only check for key_pressed at a limited frequency
        see self.update for mechanic setting its value
        Note this could be modified in order to only
        apply to selected keys (ex. movement keys)
        '''
        return self.events.simon_says and pygame.key.get_pressed()[key]

    def key_downed(self, key):
        return key in self.events.keys_downed
    
    def key_upped(self, key):
        return key in self.events.keys_upped


class MoveInput(Input):
    '''
    Process input of movement keys (for up, down, left and right).
    Produces risidual movement (ie: left + right = no movement)
    Note: on many keyboards there is a limit on keyboard key press detection
          which can erroneously lead one to think this class is buggy
          -see the concept of `Key rollover`
    Use by calling the instance.
    returns direction as a vector of leght 1 (aka normalized vector)
    '''
    direction_vectors = {
        KEY_UP: pygame.Vector2(0, -1),
        KEY_DOWN: pygame.Vector2(0, 1),
        KEY_LEFT: pygame.Vector2(-1, 0),
        KEY_RIGHT: pygame.Vector2(1, 0),
    }

    def __init__(self, events):
        super().__init__(events)
        
    def __call__(self):
        vector = self._direction()
        return vector
    
    def _direction(self):
        vector = pygame.Vector2()
        if self.events.simon_says:
            for key in MoveInput.direction_vectors.keys():
                if self._key_is_pressed(key):
                    vector += MoveInput.direction_vectors[key]
            try:
                vector = vector.normalize()
            except:
                ...
            if vector == pygame.Vector2():
                return None
            return vector
    
    def _key_is_pressed(self, key):
        '''
        check if key is currently pressed
        '''
        return pygame.key.get_pressed()[key]

