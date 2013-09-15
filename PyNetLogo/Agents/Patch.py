###
# Imports
###
# Pygame 
import pygame
from pygame.locals  import Rect
# PyNetLogo files
from Datas.Colors   import colors
from Agents.Agent   import Agent
from Datas.Globals  import worlds

###
#     Patches are the individual static squares in the grid.
#     Attributes :
#     - x                 : coordinate on the x-axis in the patches grid
#     - y                 : coordinate on the y-axis in the patches grid
#     - pcolor            : color of the patch
#     - coordinates       : coordinates of the patch in the Pygame system (pixels coordinates)
#     - turtles_here      : list of turtles which are on the patch
###
class Patch(Agent) :
    
    ###
    #    Patch class variables 
    #    - patches_number : number of patches already created
    ###
    patches_number = 0
    
    ###
    #    Patch constructor 
    #    - x                 : x coordinate of the patch in the patches grid
    #    - y                 : y coordinate of the patch in the patches grid
    #    - x_pixel           : x coordinate of the patch's top left corner in the pixels grid
    #    - y_pixel           : y coordinate of the patch's top left corner in the pixels grid
    #    - width             : width of the rectangle, square per default
    #    - height            : height of the rectangle
    #    - world_name        : name of the world where the patch is
    #    - actions           : list to put method to apply. 
    #           syntax       : [("methodName",(parameter1,parameter2)), ("methodName2",(parameter1,parameter2))} 
    #           example      : [("set", ("coordinates", Rect(x, y, width, height))]
    ###
    def __init__(self, x, y, x_pixel, y_pixel, width, height, world_name, actions=[]):
        
        Agent.__init__(self, Patch.patches_number + 1, world_name)
        Patch.patches_number += 1
        self.x              = x
        self.y              = y
        self.pcolor         = colors["WHITE"]
        self.coordinates    = Rect(x_pixel, y_pixel, width, height)
        self.turtles_here   = list()
        
        self.execute_actions(actions)
            
    ###
    #    Draw the patch on the Pygame surface in parameter
    #    - window_surface    : surface where the patch appears
    ###    
    def draw(self, window_surface):
        pygame.draw.rect(window_surface, self.pcolor, self.coordinates)
        
    ###
    #    Change the value of the class attribute in parameter
    #    - attribute_name    : attribute to change
    #    - attribute_value   : new value of the attribute
    #    - random            : "random" if the value is a random number
    ###  
    def set(self, attribute_name, attribute_value, rand=""):
        
        if attribute_name == "pcolor" :
            worlds[self.world_name].updated_patches.append(self)
        Agent.set(self, attribute_name, attribute_value, rand)