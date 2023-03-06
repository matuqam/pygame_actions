# imported by imports

import pygame
from pygame.locals import *

SCREEN_SIZE = (800, 600)

MOVE_DURATION = 5
KEY_REPEAT = 100
MOVEMENT_EVENT = pygame.event.custom_type()

KEY_UP = K_w
KEY_DOWN = K_s
KEY_LEFT = K_a
KEY_RIGHT = K_d
KEY_MELEE = K_j
KEY_MELEE_CHANGE = K_u
KEY_RANGE = K_m
KEY_MAGIC = K_k
KEY_MAGIC_CHANGE = K_i
KEY_SPEED_UP = K_0
KEY_SPEED_RESET = K_9
KEY_SPEED_DOWN = K_8

IMG_PATH_ACTIONS = '../graphics/actions/'