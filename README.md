# Actions System

# About
The purpose of this app is to test an action management system for a pygame.
The objectives are:
* Flexibility
    * The system should facilitate managing interactions between actions:
        If a player is jumping, can it duck, can it roll, etc.
* Management of flow
    * The actions should manage their own behaviour
        The conditions for start and stop, the rules for the activation and deactivation of the action should be self contained.
        The conditions can be checked on other instances.
## Ex.:
The action Jump checks for activation conditions:
* if it was requested: is the jump button pressed
* if is is possible is the player on the ground and ready
* etc.

The action Jump manages the end of the Jump:
* has the player landed on a surface

The action Jump may interupt other actions:
* Attack may have been initiated but is interupted by the Jump

# TODO
* [x] activation of action
* [x] limitation by blocker action present
* [x] limitation by requirement action missing
* [ ] manage action end
* [ ] manage action duration
* [ ] add images and visualize the process
