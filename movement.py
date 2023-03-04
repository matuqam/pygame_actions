from enum import Enum, auto

from imports import *


class MovementType(Enum):
    ADDITIVE = auto()
    INTERUPT = auto()
    SEQUENCIAL = auto()


class Movement:
    def __init__(self, other, type:MovementType, direction, duration, speed):
        self.other = other
        self.type = type
        self.direction:pygame.Vector2 = direction
        self.duration = duration
        self.speed = speed


class Movements:
    def __init__(self):
        self.movements:Movement = []

    def _fuse(self, movement:'Movement'):
        '''
        Fuse two Movements together
        The resulting action will have the following attributes
            direction:
                direction1 + direction2
            duration:
                duration1 + duration2
            speed:
                speed1 + speed2
        The fusion is made on the currently active Movement (aka self.sequence[0])
        '''
        if is_empty(self.movements):
            self.movements.append(movement)
            return
        self.movements[0].direction += movement.direction
        self.movements[0].duration += movement.duration
        self.movements[0].speed += movement.speed

    def add(self, movement:'Movement'):
        '''
        A directive describes how to move. Ex.: forward, 
        '''
        if movement.type == MovementType.ADDITIVE:
            self._fuse(movement)
        if movement.type == MovementType.INTERUPT:
            self.movements = [movement]
        if movement.type == MovementType.SEQUENCIAL:
            self.movements.append(movement)

    def _purge_expired_movements(self):
        self.movements = [m for m in self.movements if m.duration > 0]

    def update(self):
        if is_empty(self.movements):
            return
        movement = self.movements[0]
        movement.duration -= 1
        movement.other.manhandle(direction=movement.direction, speed=movement.speed)
        self._purge_expired_movements()


def is_empty(element):
    return len(element) == 0
