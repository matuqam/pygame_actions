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
* [x] manage action end
* [x] manage action duration
* [ ] add specific actions with action keys and animations
    * [x] add rect and fill with color to be able to see player
    * [x] move right
    * [x] modify move so that it moves for a determined amount of time (4 seconds)
        * [x] used a closure and timer var to run 180 ticks ~ 3 seconds (at 60 FPS)
    * [x] allow move up
    * [x] have multiple movement types
        * [x] modify the movement so that they can chain instead of add
        * [x] modify the movement so that it can interupt
    * [ ] add animations to the move actions
* [ ] experiment with speed ramp up and ramp down
    * [ ] use s curve ramp up
    * [ ] usr s curve ramp down
* [ ] add images and visualize the process
