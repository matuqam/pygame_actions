from imports import *
from tools import load_images

class Action:
    def __init__(self, name, controler, required_action_names=None, disallowed_action_names=None, duration=None, stackable=False):
        self.name = name
        self.controler = controler  # object holding this action
        self.images = load_images(IMG_PATH_ACTIONS+name)
        self.required_action_names = [] if required_action_names is None else required_action_names  #
        self.disallowed_action_names = [] if disallowed_action_names is None else disallowed_action_names  #
        self.duration = duration
        self.timer = duration
        self.last = None
        self.key = None
        self.stackable = stackable
        self.ended = False

    def __repr__(self):
        return f'<Action: {self.name}>'
    
    def _is_triggered(self):
        if self.key is None:
            return False
        if self.key in pygame.key.get_pressed():
            return True
        return False

    def _is_active(self):
        return self.ended == False

    def _is_possible(self):
        '''
        check all conditions to run this action
        '''
        # the player or "controler" does not have an active status that prevents this action
        if not set(self.disallowed_action_names).isdisjoint(set([a.name for a in self.controler.actions_active])):
            common = list(set(self.disallowed_action_names).intersection(set([a.name for a in self.controler.actions_active])))
            print(f'## action: {self.name} was not possible due to incompatible action currently active: {", ".join(common)}')
            return False
        # the player has all the actives status required to run this action# 
        if not set(self.required_action_names).issubset(set([a.name for a in self.controler.actions_active])):
            missing = list(set(self.required_action_names).difference(set([a.name for a in self.controler.actions_active])))
            print(f'## action: {self.name} was not possible due to missing required active action(s): {", ".join(missing)}')
            return False
        return True

    def set_key(self, key:pygame.key):
        '''
        set the keyboard key that will trigger the action
        this if for player activated actions
        '''
        self.key = key

    def start(self):
        '''
        starts action
        run when initially calling the action. It will sart the action
        '''
        print(f'## Executed action: {self.name}')
        self.controler.actions_active.append(self)
        # self.last = pygame.time.get_ticks()
        # self.timer += self.duration

    def extend(self):
        '''extends action'''
        print(f'action: {self.name} was extended')

    def end(self):
        '''ends actions'''
        print(f'# action: {self.name} ended')
        self.ended = True

    def tick(self):
        '''
        all instantiated actions will run this at every tick
        will check if action is beeing called by player for player initiated
        actions or if conditions are met for auto activated (aka non player)
        actions
        '''
        # activation
        #     check if the action was requested by user or other
        #     check if the action meets the conditions to be activated
        #         no preventing action is active
        #         all required actions are active
        #         if already active
        #             did it expire -- if not
        #                 is it stackable
        #                     if not it can't be run
        #                     if yes, add to timer or increase effect
        #     activate action
        #         add to list of actions_active of the `controler`
        #         does it have a duration
        #             if so, activate timer
        #             set the `last` value (time it was last activated)
        #     may need to interupt some currently active actions (?) 
        #         ex.: receiving a hit might interupt an attack
        # Deactivation
        if self.ended == False and self.duration is not None:
            if self.timer > 0:
                self.timer -= 1
            if self.timer < 1:
                self.end()
        if self.ended == True:
            return            
                
        #     check if the action is in progress
        #         check if the action has ended
        #             timer expires
        #             required actions for continuation of this action are no longer present
        #             preventing actions are now active making this action interupted
        #                 ex.: player attacking but jump and thus interupted it
        
        # Action relationships
        #     required_activation_actions
        #     required_continuation_actions (subset of required_activation_actions)
        #     preventing_activation_actions
        #     interupting_actions (ex.: Jump does not prevent Attack but will interupt it on activation)
        # if self._is_triggered and self._is_possible:
        #     self.run()

    def run(self):
        '''initiate action'''
        print(f'# Requested action: {self.name}')
        if self._is_possible():
            self.start()



