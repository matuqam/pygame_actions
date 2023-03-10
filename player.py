from imports import *
from action import Action
from movement import Movements, Movement, MovementType, is_empty
from input import Input, InputType, MoveInput, Events


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

        self.events = Events()
        self.input = Input(self.events)
        self.move_input = MoveInput(self.events)

        self.dash_speed = 8
        self.dash_surfaces = load_images('./graphics/player/right')

    # actions
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

    def set_timer(self, ticks):
        def count():
            nonlocal ticks
            ticks -= 1
            return ticks > 0
        return count

    def process_input(self, events):
        '''
        Process input and move player.
        The movement keys are processed as a whole to produce a coherent resulting direction.
        This is subject to the limits of `Key rollover`.
        '''
        self.events.update(events)

        # regular movement
        direction = self.move_input()
        if direction is not None:
            self.movements.add(Movement(self, MovementType.SEQUENCIAL, MOVE_DURATION * 10, direction, 2))
        
        # dash
        direction = pygame.Vector2(1, 0)
        if self.input(K_SPACE, InputType._KEYDOWN):
            self.movements.add(Movement(self, MovementType.INTERUPT, 90, direction, self.dash_speed, interupt=False))


    def process_input_complex(self, events):
        '''
        Process input and move player.
        Does not use special input processing for movement keys (aka up, down, left, right).
        Key presses are evaluated independently and the resulting action is taken. The movements
        instance logic dictates the resulting movement.
        
        '''
        self.events.update(events)
        input_type = InputType._KEYPRESSED

        # up: back step, start slow, normal, finish slow
        if self.input(KEY_UP, input_type):
            # normal movement
            direction = pygame.Vector2(0, -self.speed).normalize()
            self.movements.add(Movement(self, self.movement_type, MOVE_DURATION, direction, 4))
        if self.input(KEY_UP, InputType._KEYDOWN):
            # back step (clears movement queue)
            direction = pygame.Vector2(0, self.speed)
            self.movements.add(Movement(self, MovementType.INTERUPT, MOVE_DURATION//2, direction, self.speed * 4))
            # start slow
            direction = pygame.Vector2(0, -self.speed)
            self.movements.add(Movement(self, MovementType.SEQUENCIAL, MOVE_DURATION * 8, direction, 1))
        if self.input(KEY_UP, InputType._KEYUP):
            # end slow (clears movement queue)
            direction = pygame.Vector2(0, -self.speed)
            self.movements.add(Movement(self, MovementType.INTERUPT, MOVE_DURATION * 4, direction, 1))

        # down
        if self.input(KEY_DOWN, input_type):
            direction = pygame.Vector2(0, self.speed)
            self.movements.add(Movement(self, self.movement_type, MOVE_DURATION, direction, self.speed))
        if self.input(KEY_DOWN, InputType._KEYDOWN):
            # back step (clears movement queue)
            direction = pygame.Vector2(0, -self.speed)
            self.movements.add(Movement(self, MovementType.INTERUPT, MOVE_DURATION//2, direction, self.speed * 4))
            # start slow
            direction = pygame.Vector2(0, self.speed)
            self.movements.add(Movement(self, MovementType.SEQUENCIAL, MOVE_DURATION * 8, direction, 1))
        if self.input(KEY_DOWN, InputType._KEYUP):
            # end slow (clears movement queue)
            direction = pygame.Vector2(0, self.speed)
            self.movements.add(Movement(self, MovementType.INTERUPT, MOVE_DURATION * 4, direction, 1))

        # left
        if self.input(KEY_LEFT, input_type):
            direction = pygame.Vector2(-self.speed, 0)
            self.movements.add(Movement(self, self.movement_type, MOVE_DURATION, direction, self.speed))
        if self.input(KEY_LEFT, InputType._KEYDOWN):
            # back step (clears movement queue)
            direction = pygame.Vector2(self.speed, 0)
            self.movements.add(Movement(self, MovementType.INTERUPT, MOVE_DURATION//2, direction, self.speed * 4))
            # start slow
            direction = pygame.Vector2(-self.speed, 0)
            self.movements.add(Movement(self, MovementType.SEQUENCIAL, MOVE_DURATION * 8, direction, 1))
        if self.input(KEY_LEFT, InputType._KEYUP):
            # end slow (clears movement queue)
            direction = pygame.Vector2(-self.speed, 0)
            self.movements.add(Movement(self, MovementType.INTERUPT, MOVE_DURATION * 4, direction, 1))

        # right
        if self.input(KEY_RIGHT, input_type):
            direction = pygame.Vector2(self.speed, 0)
            self.movements.add(Movement(self, self.movement_type, MOVE_DURATION * 4, direction, self.speed))
        if self.input(KEY_RIGHT, InputType._KEYDOWN):
            # back step (clears movement queue)
            direction = pygame.Vector2(-self.speed, 0)
            self.movements.add(Movement(self, MovementType.INTERUPT, MOVE_DURATION//2, direction, self.speed * 4))
            # pause
            direction = pygame.Vector2(0, 0)
            self.movements.add(Movement(self, MovementType.SEQUENCIAL, MOVE_DURATION * 4, direction, 1))
            # start slow
            direction = pygame.Vector2(self.speed, 0)
            self.movements.add(Movement(self, MovementType.SEQUENCIAL, MOVE_DURATION * 4, direction, 1))
        if self.input(KEY_RIGHT, InputType._KEYUP):
            # end slow (clears movement queue)
            direction = pygame.Vector2(self.speed, 0)
            self.movements.add(Movement(self, MovementType.INTERUPT, MOVE_DURATION * 4, direction, 1))

        if self.input(K_u, InputType._KEYDOWN):
            self.movement_type = MovementType.SEQUENCIAL
        if self.input(K_i, InputType._KEYDOWN):
            self.movement_type = MovementType.INTERUPT
        # The MOVEMENT event "limiter" works well with this MovementType
        # ie: it produces a smooth movement as it allows the moement queue to 
        # clear preventing weird vector math #
        if self.input(K_o, InputType._KEYDOWN):
            self.movement_type = MovementType.ADDITIVE


    # movement
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
        self.loop_position()

    def loop_position(self):
        if self.rect.left > pygame.display.get_surface().get_rect().right:
            self.rect.right = 0
        elif self.rect.right < 0:
            self.rect.left = pygame.display.get_surface().get_rect().right
        elif self.rect.bottom < 0:
            self.rect.top = pygame.display.get_surface().get_rect().bottom
        elif self.rect.top > pygame.display.get_surface().get_rect().bottom:
            self.rect.bottom = 0

    # visual
    def set_surface(self):
        if not is_empty(self.movements.movements):
            movement = self.movements.movements[0]
            if movement.speed == self.dash_speed:
                self.surface = self.dash_surfaces[(pygame.time.get_ticks() // 50) % len(self.dash_surfaces)]
            else:
                self.surface = pygame.Surface(size=(64,64))

    def display(self):
        display = pygame.display.get_surface()
        self.set_surface()
        display.blit(self.surface, self.rect.topleft)

    def update(self):
        # self.actions_active = [a for a in self.actions_active if a.ended == False]
        # use movement.Movement for movements
        self.movements.update()

        # for a in self.actions_active:
        #     a.tick()
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
