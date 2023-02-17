from imports import *
from player import Player
from action import Action

def test():
    '''Test senario for action interactions'''
    player = Player()

    go = Action(name='go', controler=player)
    run = Action(name='run', controler=player)
    get_to_the_choppa = Action(name='get to the choppa', controler=player)
    hide = Action(name='hide', controler=player, disallowed_action_names=['run', 'get to the choppa'])

    player.add_possible_action([go, run, get_to_the_choppa, hide])
    player.take_action('go')
    player.take_action('run')
    player.take_action('get to the choppa')
    player.take_action('hide')
    print(f'{player.actions_active=}')


if __name__ == '__main__':
    test()
