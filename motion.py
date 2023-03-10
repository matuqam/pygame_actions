'''
Have movement (in the general sense as this can be an action)
and image be managed by one class (or at least one module).
'''
##############
##Requirements
##############
# * define a sequence of movement
#   * position
#       * initial
#       * evolution of position by click
#           * change by:
#               * speed
#               * function
#   * image (aka Surface) during the sequence
# 
#
###########
###Examples
###########
#   * dash
#       * starts at player position at time 0
#           * moves with
#               * given speed
#               * given direction
#               * for given duration
#           * has given visuals (aka Surface) during movement duration
#       * modifies (possibly) the players movement method
#           * example dash prevents regular movements un it ends
#           * this could be done by
#               * making the movement uninteruptible (no change possible until end)
#               * changing the player status when this movement starts
#               * setting allowed states in the motion definition
# 
#########
##Details
#########
# A motion can be a sequence of simle movement such as:
#   1- walk east 10 steps
#   2- walk north 8 steps
#   3- shoot arrow, throw knife
#   4- jump
#   5- dash
#   ...
# 
##########
# Required access for Motion class
##########
# because the Motion will affect the player or other instance,
# it needs to have a ref to the instance (lets call it `other`)
# because the Motion can be a collection of simple movements,
# it needs to have access to the predefined movements and Motions
# 
# A Motion can be a 
#   * composition 
#       * of Motions, 
#       * of movements or
#   * a simple movement (or action)
# #
from imports import *


class Motion:
    '''
    Contains movement and animation for a game element
    Motion may hold other Motions
    `other` is the target for the Motion
    '''
    def __init__(self, other, duration, direction, speed, motions=None, visual=None):
        self.other = other
        self.duration = duration
        self.timer = duration
        self.direction = direction
        self.speed = speed
        self.motions = [] if motions is None else motions
        self.visual = visual
    
    @property
    def motion(self):
        if self.motions:
            return self.motions[0]
        else:
            return self

    def purge_expired(self):
        if not self.motions:
            return
        self.motions = [m for m in self.motions if m.timer > 0]

    def update(self):
        if self.motions:
            motion = self.motions[0].motion
        else:
            motion = self
        if motion.timer < 1:
            return
        motion.timer -= 1
        if hasattr(motion.other, 'move'):
            motion.other.move(direction=motion.direction, speed=motion.speed)
        self.purge_expired()
        
        # visual
        if motion.visual is not None:
            motion.visual.update()
            if hasattr(motion.other, 'image'):
                motion.other.image = motion.visual.image


class Visual:
    '''
    Holds images
    TODO
        Consider having a `duration` attibute to determine the length of the animation
        the duration of each image would then be self.duration / len(self.images).
        Having a duration of -1 could indicate a looping animation.
        Could either/also use an attribute to keep track of the number of loops completed.
        Returns if the animation has completed or if the duration ended.
    '''
    def __init__(self, animation_folder, update_function=None):
        self.images = load_images(animation_folder)
        self.image_index = 0
        self.animation_speed = 0.1
        self.image = self.images[self.image_index] if self.images else None
        self.update_function = update_image if update_function is None else update_function

    def update(self):
        return self.update_function(self)


def update_image(visual):
    '''
    update other.image to next according to other.animation_speed
    returns wether other animation has cycles (aka has ended)
    '''
    animation_cycled = False
    if visual.images:
        nb_images = len(visual.images)
        visual.image_index += visual.animation_speed
        if int(visual.image_index) > (nb_images - 1):
            visual.image_index = 0
            animation_cycled = True
        visual.image = visual.images[int(visual.image_index)]
    return animation_cycled

if __name__ == '__main__':
    def main():
        import sys
        
        pygame.init()
        display = pygame.display.set_mode((800, 600))

        class Thing:
            def __init__(self):
                self.pos = pygame.Vector2(0, 0)
                self.image = pygame.Surface((64, 64))

            def move(self, direction, speed):
                self.pos += direction * speed

        other = Thing()
        visual_up = Visual('./graphics/player/up')
        visual_down = Visual('./graphics/player/down')
        visual_left = Visual('./graphics/player/left')
        visual_right = Visual('./graphics/player/right')
        move_up = Motion(other, 100, pygame.Vector2(0, -1), 1, None, visual_up)
        move_down = Motion(other, 100, pygame.Vector2(0, 1), 1, None, visual_down)
        move_left = Motion(other, 100, pygame.Vector2(-1, 0), 1, None, visual_left)
        move_right = Motion(other, 100, pygame.Vector2(1, 0), 1, None, visual_right)
        motion = Motion(None, 0, pygame.Vector2(), 0, [move_right, move_down, move_left, move_up], visual_right)

        def quit():
            pygame.quit()
            sys.exit()

        def update(steps=1):
            for _ in range(steps):
                display.fill('pink')
                motion.update()
                display.blit(motion.motion.visual.image, other.pos)
                pygame.display.update()

        while motion.motion.timer > 0:
            update()
    main()