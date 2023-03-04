from imports import *
from action import Action
from movement import Movements, Movement, MovementType


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
        self.speed = 1
        self.direction = pygame.Vector2()
        self.timer = lambda:False

        self.movements = Movements()

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
        MOVE_DURATION = 180 # (in ticks)
        for event in events:
            if event.type == KEYDOWN:
                if event.key == KEY_UP:
                    # self.timer = self.set_timer(MOVE_DURATION)
                    # self.direction += pygame.Vector2(0, -self.speed)
                    self.movements.add(Movement(self, MovementType.SEQUENCIAL, pygame.Vector2(0, -self.speed), 60, self.speed))
                if event.key == KEY_DOWN:
                    # self.timer = self.set_timer(MOVE_DURATION)
                    # self.direction += pygame.Vector2(0, self.speed)
                    self.movements.add(Movement(self, MovementType.SEQUENCIAL, pygame.Vector2(0, self.speed), 60, self.speed))
                if event.key == KEY_LEFT:
                    # self.timer = self.set_timer(MOVE_DURATION)
                    # self.direction += pygame.Vector2(-self.speed, 0)
                    self.movements.add(Movement(self, MovementType.SEQUENCIAL, pygame.Vector2(-self.speed, 0), 60, self.speed))
                if event.key == KEY_RIGHT:
                    self.movements.add(Movement(self, MovementType.SEQUENCIAL, pygame.Vector2(self.speed, 0), 60, self.speed))
                if event.key == K_i:
                    self.movements.add(Movement(self, MovementType.INTERUPT, pygame.Vector2(self.speed * 2, 0), 60, self.speed))
                if event.key == K_o:
                    self.movements.add(Movement(self, MovementType.ADDITIVE, pygame.Vector2(0, self.speed), 60, self.speed))
                    # self.timer = self.set_timer(MOVE_DURATION)
                    # self.direction += pygame.Vector2(self.speed, 0)
            # if event.type == KEYUP:
            #     if event.key == KEY_UP:
            #         self.direction -= pygame.Vector2(0, -self.speed)
            #     if event.key == KEY_DOWN:
            #         self.direction -= pygame.Vector2(0, self.speed)
            #     if event.key == KEY_LEFT:
            #         self.direction -= pygame.Vector2(-self.speed, 0)
            #     if event.key == KEY_RIGHT:
            #         self.direction -= pygame.Vector2(self.speed, 0)
        self.move()
    
    def set_timer(self, ticks):
        def count():
            nonlocal ticks
            ticks -= 1
            return ticks > 0
        return count

    def move(self):
        if self.timer():
            self.rect.center += self.direction * self.speed
    
    def manhandle(self, direction, speed):
        '''
        moved by other object
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


# if __name__ == '__main__':
#     player = Player()

#     go = Action(name='go', controler=player)
#     run = Action(name='run', controler=player, required_action_names=['go'])
#     get_to_the_choppa = Action(name='get to the choppa', controler=player, required_action_names=['go', 'run'])
#     hide = Action(name='hide', controler=player, disallowed_action_names=['run', 'get to the choppa'])

#     player.add_possible_action([go, run, get_to_the_choppa, hide])
#     player.take_action('get to the choppa')
#     player.take_action('go')
#     player.take_action('get to the choppa')
#     player.take_action('run')
#     player.take_action('get to the choppa')
#     player.take_action('hide')
#     player.tick()
#     print(f'{player.actions_active=}')
#     run.end()
#     player.tick()
#     print(f'{player.actions_active=}')
