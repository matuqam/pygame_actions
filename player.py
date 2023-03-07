from imports import *
from action import Action
from movement import Movements, Movement, MovementType
from input import Input, InputType


class Player:
    def __init__(self, actions_active=None, rect:Rect=None):
        self.actions_active = [] if actions_active is None else actions_active
        # actions activated by player
        self.actions_player = []
        # actions activated by others ex.: debuff
        self.actions_non_player = []
        # list of unique possible actions (no duplicates)
        self.action_repertoire = []

        self.rect = rect if rect is not None else Rect(64, 64, 0, 0)
        self.surface = pygame.Surface(size=(64,64))
        self.speed = 2
        self.direction = pygame.Vector2()
        self.timer = lambda:False

        self.movements = Movements()
        self.movement_type = MovementType.SEQUENCIAL

        self.input = Input()

    def add_possible_action(self, action):
        '''add action to possible_actions'''
        try:
            for a in action:
                self.action_repertoire.append(a)
        except:
            self.action_repertoire.append(action)
        self.action_repertoire = list(set(self.action_repertoire))

    def take_action(self, action_name):
        for action in self.action_repertoire:
            if action.name == action_name:
                action.run()

    def process_input(self, events):
        self.input.update(events)
        input_type = InputType._KEYPRESSED

        # up: back step, start slow, normal, finish slow
        if self.input(KEY_UP, input_type):
            # normal movement
            direction = pygame.Vector2(0, -self.speed).normalize()
            self.movements.add(Movement(self, self.movement_type, direction, MOVE_DURATION, 4))
        if self.input(KEY_UP, InputType._KEYDOWN):
            # back step (clears movement queue)
            direction = pygame.Vector2(0, self.speed)
            self.movements.add(Movement(self, MovementType.INTERUPT, direction, MOVE_DURATION//2, self.speed * 4))
            # start slow
            direction = pygame.Vector2(0, -self.speed)
            self.movements.add(Movement(self, MovementType.SEQUENCIAL, direction, MOVE_DURATION * 8, 1))
        if self.input(KEY_UP, InputType._KEYUP):
            # end slow (clears movement queue)
            direction = pygame.Vector2(0, -self.speed)
            self.movements.add(Movement(self, MovementType.INTERUPT, direction, MOVE_DURATION * 4, 1))

        # down
        if self.input(KEY_DOWN, input_type):
            direction = pygame.Vector2(0, self.speed)
            self.movements.add(Movement(self, self.movement_type, direction, MOVE_DURATION, self.speed))
        if self.input(KEY_DOWN, InputType._KEYDOWN):
            # back step (clears movement queue)
            direction = pygame.Vector2(0, -self.speed)
            self.movements.add(Movement(self, MovementType.INTERUPT, direction, MOVE_DURATION//2, self.speed * 4))
            # start slow
            direction = pygame.Vector2(0, self.speed)
            self.movements.add(Movement(self, MovementType.SEQUENCIAL, direction, MOVE_DURATION * 8, 1))
        if self.input(KEY_DOWN, InputType._KEYUP):
            # end slow (clears movement queue)
            direction = pygame.Vector2(0, self.speed)
            self.movements.add(Movement(self, MovementType.INTERUPT, direction, MOVE_DURATION * 4, 1))

        # left
        if self.input(KEY_LEFT, input_type):
            direction = pygame.Vector2(-self.speed, 0)
            self.movements.add(Movement(self, self.movement_type, direction, MOVE_DURATION, self.speed))
        if self.input(KEY_LEFT, InputType._KEYDOWN):
            # back step (clears movement queue)
            direction = pygame.Vector2(self.speed, 0)
            self.movements.add(Movement(self, MovementType.INTERUPT, direction, MOVE_DURATION//2, self.speed * 4))
            # start slow
            direction = pygame.Vector2(-self.speed, 0)
            self.movements.add(Movement(self, MovementType.SEQUENCIAL, direction, MOVE_DURATION * 8, 1))
        if self.input(KEY_LEFT, InputType._KEYUP):
            # end slow (clears movement queue)
            direction = pygame.Vector2(-self.speed, 0)
            self.movements.add(Movement(self, MovementType.INTERUPT, direction, MOVE_DURATION * 4, 1))

        # right
        if self.input(KEY_RIGHT, input_type):
            direction = pygame.Vector2(self.speed, 0)
            self.movements.add(Movement(self, self.movement_type, direction, MOVE_DURATION, self.speed))
        if self.input(KEY_RIGHT, InputType._KEYDOWN):
            # back step (clears movement queue)
            direction = pygame.Vector2(-self.speed, 0)
            self.movements.add(Movement(self, MovementType.INTERUPT, direction, MOVE_DURATION//2, self.speed * 4))
            # start slow
            direction = pygame.Vector2(self.speed, 0)
            self.movements.add(Movement(self, MovementType.SEQUENCIAL, direction, MOVE_DURATION * 8, 1))
        if self.input(KEY_RIGHT, InputType._KEYUP):
            # end slow (clears movement queue)
            direction = pygame.Vector2(self.speed, 0)
            self.movements.add(Movement(self, MovementType.INTERUPT, direction, MOVE_DURATION * 4, 1))


        if self.input(K_u, InputType._KEYDOWN):
            self.movement_type = MovementType.SEQUENCIAL
        if self.input(K_i, InputType._KEYDOWN):
            self.movement_type = MovementType.INTERUPT
        # The MOVEMENT event "limiter" works well with this MovementType
        # ie: it produces a smooth movement as it allows the moement queue to 
        # clear preventing weird vector math #
        if self.input(K_o, InputType._KEYDOWN):
            self.movement_type = MovementType.ADDITIVE

    def set_timer(self, ticks):
        def count():
            nonlocal ticks
            ticks -= 1
            return ticks > 0
        return count

    def move(self):
        '''
        The use of timer works in combination with the KEYDOWN way of checking
        for movement keys. It allows an otherwise puctual event (the KEYDOWN event)
        to have a lasting effect but yet still limited unlike the key.get_pressed()

        It can work with movement that needs to be increments. Or attacks that
        need to be intermittent such as sword attacks.

        moving in this manner was called like this:
            ```
            ...
            if event.type == KEYDOWN:
                ...
                self.timer = self.set_timer(MOVE_DURATION)
                self.direction += pygame.Vector2(0, -self.speed)
            ...
            self.move()
            ```
        '''
        if self.timer():
            self.rect.center += self.direction * self.speed
    
    def manhandle(self, direction, speed):
        '''
        moved by other object
        This adds another movement strategy beside self.move()
        Notably, it does not use the self.timer()
        '''
        self.rect.center += (direction * speed)
        
    def display(self):
        display = pygame.display.get_surface()
        display.blit(self.surface, self.rect.topleft)

    def update(self):
        self.actions_active = [a for a in self.actions_active if a.ended == False]
        # use movement.Movement for movements
        self.movements.update()

        for a in self.actions_active:
            a.tick()
        self.display()


if __name__ == '__main__':
    player = Player()

    go = Action(name='go', controler=player)
    run = Action(name='run', controler=player, required_action_names=['go'])
    get_to_the_choppa = Action(name='get to the choppa', controler=player, required_action_names=['go', 'run'])
    hide = Action(name='hide', controler=player, disallowed_action_names=['run', 'get to the choppa'])

    player.add_possible_action([go, run, get_to_the_choppa, hide])
    player.take_action('get to the choppa')
    player.take_action('go')
    player.take_action('get to the choppa')
    player.take_action('run')
    player.take_action('get to the choppa')
    player.take_action('hide')
    # player.tick()  # This method was removed in a previous update.
    print(f'{player.actions_active=}')
    run.end()
    # player.tick()  # This method was removed in a previous update.
    print(f'{player.actions_active=}')
