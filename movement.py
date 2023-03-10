from enum import Enum, auto
from math import erf

from imports import *


class MovementType(Enum):
    ADDITIVE = auto()
    INTERUPT = auto()
    SEQUENCIAL = auto()


class Movement:
    '''
    Encapsulates the movement (duration, direction, speed and position) of a pygame element (other).
    Duration of a Movement serves as a timer. It is decremented and once reaches 0, the Movement
    has served its purpose.

    TODO
      * [ ] explore using functions to fluxuate the values of direction, speed and position
    '''
    def __init__(self, 
                 other, 
                 type:MovementType, 
                 duration, 
                 direction, 
                 speed, 
                 position=None, 
                 interupt:bool=True):
        self.other = other
        self.type = type
        self.duration = duration
        self.timer = duration
        self.direction:pygame.Vector2 = direction
        self.speed = speed
        self.position = position
        self.interupt = interupt

    def set_direction(self):
        ...

    def set_speed(self):
        ...
        # self.speed = erf( (self.duration - self.timer)/40 ) * 4
        # self.speed = FAST_S( (self.duration - self.timer)/40 ) * 4
        # self.speed = SLOW_S( (self.duration - self.timer)/40 ) * 5

    def set_position(self):
        ...

    def update(self):
        self.timer -= 1
        self.set_direction()
        self.set_speed()
        self.set_position()
        self.other.manhandle(direction=self.direction, speed=self.speed)


class Movements:
    '''
    Uses Movement class to encapsulate movement.
    Gets called at every tick of pygame to move objects.
    Once a Movement has "expired" (aka timer is decremented to 0), it is removed (aka purged).
    '''
    def __init__(self):
        self.movements:Movement = []

    def __bool__(self):
        return bool(self.movements)
    
    def __iter__(self):
        iter(self.movements)

    def __len__(self):
        return len(self.movements)
    
    def __repr__(self):
        return f'<{self.__class__.__name__}({len(self)} Movement>)'

    def _fuse(self, movement:'Movement'):
        '''
        Fuse two Movements together: the current movement and the new one. Other movements are descarded
        The resulting action will have the following attributes
            direction:
                direction1 + direction2
            duration:
                duration1 = duration2
            speed:
                speed1 = speed2
        The fusion is made on the currently active Movement (aka self.sequence[0])
        '''
        if is_empty(self.movements):
            self.movements.append(movement)
            return
        self.movements = [self.movements[0]]
        if (self.movements[0].direction + movement.direction).magnitude() == 0:
            self.movements[0].direction = self.movements[0].direction + movement.direction
        else:
            self.movements[0].direction = (self.movements[0].direction + movement.direction).normalize()
        self.movements[0].timer = movement.duration
        self.movements[0].speed = movement.speed

    def add(self, movement:'Movement'):
        '''
        A directive describes how to move. Ex.: forward, 
        '''
        if movement.type == MovementType.ADDITIVE:
            self._fuse(movement)
        if movement.type == MovementType.INTERUPT:
            if is_empty(self.movements):
                self.movements = [movement]
            elif self.movements[0].interupt:
                self.movements = [movement]
            else:
                self.movements = self.movements + [movement]


        if movement.type == MovementType.SEQUENCIAL:
            self.movements.append(movement)

    def _purge_expired_movements(self):
        self.movements = [m for m in self.movements if m.timer > 0]

    def update(self):
        if not self:
            return
        movement = self.movements[0]
        movement.update()
        self._purge_expired_movements()
        print(self)


def is_empty(element):
    return len(element) == 0
