from imports import *
from action import Action


class Player:
    def __init__(self, actions_active=None):
        self.actions_active = [] if actions_active is None else actions_active
        # actions activated by player
        self.actions_player = []
        # actions activated by others ex.: debuff
        self.actions_non_player = []
        # list of unique possible actions (no duplicates)
        self.action_repertoire = []

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
    print(f'{player.actions_active=}')
