from imports import *
from player import Player
from action import Action
from level import Level

pygame.init()
display = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
# put a movement in the event queue whenever movement should be considered
# this works with KEYPRESSED movement strategy type so keys are not repeated 
# too fast
# MOVEMENT_EVENT = pygame.event.custom_type()
pygame.time.set_timer(pygame.event.Event(MOVEMENT_EVENT), KEY_REPEAT)
# pygame.key.set_repeat(KEY_REPEAT, KEY_REPEAT)  # removed to test specific movement dynamics



level = Level()

def test():
    '''Test senario for action interactions'''
    player = Player()

    go = Action(name='go', controler=player, duration=5)
    run = Action(name='run', controler=player, required_action_names=['go'], duration=10)
    get_to_the_choppa = Action(name='get to the choppa', controler=player, required_action_names=['go', 'run'], duration=15)
    hide = Action(name='hide', controler=player, disallowed_action_names=['run', 'get to the choppa'])

    player.add_possible_action([go, run, get_to_the_choppa, hide])
    player.take_action('get to the choppa')
    player.take_action('go')
    player.take_action('get to the choppa')
    player.take_action('run')
    player.take_action('get to the choppa')
    player.take_action('hide')
    player.update()
    print(f'{player.actions_active=}')
    run.end()
    for i in range(30):
        print(f'{player.actions_active=}')
        player.update()
    print(f'{player.actions_active=}')

def run():
    while True:
        display.fill('pink')

        game_events = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            else:
                game_events.append(event)

        level.process_input(game_events)
        level.update()
        pygame.display.update()
        clock.tick(60)


if __name__ == '__main__':
    run()
