###
# Imports
###
# Standard Python library
import math
import copy
import random
# PyNetLogo files
from Datas.Colors   import colors
from Agents.Agent   import Agent
from Datas.Globals  import worlds
# Pygame
import pygame

###
#     Turtles are the moving agents of NetLogo.
#     Attributes :
#     - xcor         : coordinate on the x-axis in the patches grid
#     - ycor         : coordinate on the y-axis in the patches grid
#     - _x           : x coordinate of the center of the turtle in the pixels grid
#     - _y           : y coordinate of the center of the turtle in the pixels grid
#     - heading      : the rotation of the turtle around the z-axis
#     - color        : color of the turtle
#     - shape        : shape of the turtle
#     - hidden       : boolean to know if we have to display the turtle
#     - size         : size of the turtle
#     - pen_mode     : boolean to know if the turtle is drawing a line
#     - pen_size     : size of the drawing line
#     - patch        : patch where the turtle is
###
class Turtle(Agent) :

    ###
    #    Turtle class variables 
    #    - turtles_number      : number of turtles already created
    #    - turtle_daughters    : dictionary to keep dynamic generated classes 
    ###
    turtles_number = 0
    turtle_daughters = {}
    
    ###
    #    Turtle constructor 
    #    - world_name        : name of the world where the turtle is
    #    - actions           : list to put method to apply. 
    #           syntax       : [("methodName",(parameter1,parameter2)), ("methodName2",(parameter1,parameter2))} 
    #           example      : [("set", ("coordinates", Rect(x, y, width, height))]
    ###
    def __init__(self, world_name, actions=[]):
                
        Agent.__init__(self, Turtle.turtles_number + 1, world_name)
        Turtle.turtles_number   += 1
        self.xcor               = 0
        self.ycor               = 0
        self._x                 = 0
        self._y                 = 0
        self.heading            = 0
        self.color              = colors["RED"]
        self.shape              = "circle"
        self.hidden             = False
        self.size               = 0
        self.pen_size           = 1
        self.pen_mode           = False  
        self.patch              = None
        
        self.execute_actions(actions)

        self.patch              = worlds[self.world_name].get_patch(self._x, self._y)
        self.patch.turtles_here.append(self)
        
    ###
    #    Draw the turtle on the Pygame surface in parameter
    #    - window_surface   : surface where the turtle appears
    ###   
    def draw(self, window_surface):
        if self.shape == "circle" :
            pygame.draw.circle(window_surface, self.color, (int(self._x),int(self._y)), int(self.size))
    
    ###
    #    Return the coordinate in a torus world
    ###
    def _torus_coordinates(cls, x, y, patches_size, patches_number):
        
        max_pxcor           = patches_number[0] * patches_size[0]
        max_pycor           = patches_number[1] * patches_size[1]
        _x, _y              = x, y
        
        if x < 0 or x > max_pxcor -1 : _x = x % max_pxcor - 1
        if y < 0 or y > max_pycor -1 : _y = y % max_pycor - 1
            
        return (_x, _y)
    
    #Declaration as a class method 
    _torus_coordinates = classmethod(_torus_coordinates)
    
    ###
    #    Return new coordinates after a movement
    #    - x               : x coordinate of the movement origin
    #    - y               : y coordinate of the movement origin
    #    - angle           : angle of the movement
    #    - distance        : distance of the movement
    #    - patches_size    : size in pixels of every patches
    #    - patches_number  : number of patches on each axis. (patches_number[0] : x-axis, patches_number[1] : y-axis)
    ###
    def _calc_coordinates(cls, x, y, angle, distance, patches_size, patches_number):
              
        # Forward 1 = movement of 1 patch = 1 * patchSize
        distance_x_patches = distance * patches_size[0]
        distance_y_patches = distance * patches_size[1]

        x1 = x + distance_x_patches * math.cos(math.radians(angle))
        y1 = y - distance_y_patches * math.sin(math.radians(angle))
        
        x1, y1 = Turtle._torus_coordinates(x1, y1, patches_size, patches_number)
        
        return (x1, y1)
    
    #Declaration as a class method 
    _calc_coordinates = classmethod(_calc_coordinates)    
        
    ###
    #    Change the turtle's coordinates
    #    - distance        : distance to move
    ###
    def _move(self, distance):

        x0, y0 = self._x, self._y      
        self._x, self._y = Turtle._calc_coordinates(x0, y0, self.heading, distance, worlds[self.world_name].patches_size, worlds[self.world_name].patches_number)
        
        if self.patch != None :
            self.patch.turtles_here.remove(self)
        self.patch = worlds[self.world_name].get_patch(self._x, self._y)
        self.patch.turtles_here.append(self)
        
        #Add a new line in world.linesList
        if self.pen_mode == True :
            worlds[self.world_name].lines_list.append((self, (x0, y0), (self._x, self._y)))
            worlds[self.world_name].updated_lines.append((self, (x0, y0), (self._x, self._y)))
        
        
    ###
    #    Go forward distance steps.
    ### 
    def forward(self, distance):
        self._move(distance)
        
    ###
    #    Go backward distance steps.
    ###     
    def backward(self, distance):
        self._move(-distance)

    ###
    #    Rotate the turtle
    #    - angle             : degree
    ### 
    def _rotate(cls, heading, angle):
        return ((heading + angle) % 360)
        
    #Declaration as a class method
    _rotate = classmethod(_rotate)
    
    ###
    #    Turn left angle unit 
    #    - angle             : degree
    ###      
    def left(self, angle):
        self.heading = Turtle._rotate(self.heading, angle)

    ###
    #    Turn right angle unit 
    #    - angle             : degree
    ###          
    def right(self, angle):
        self.heading = Turtle._rotate(self.heading, -angle)
 
    ###
    #    A turtle create one or more sons with its attributes per default
    #    - nb_sons            : number of sons created
    #    - actions            : list to put actions to perform.
    #           syntax        : [("methodName",(parameter1,parameter2)), ("methodName2",(parameter1,parameter2))}  
    #           example       : [("set",("heading",10)), ("forward",(10))]
    ###          
    def hatch(self, nb_sons=1, actions=[]):
   
        # Add the sons in the list
        for _ in range(0, nb_sons) :
            # The new turtle have its parent attributes
            new_turtle = copy.copy(self)
            new_turtle.patch.turtles_here.append(new_turtle)
            
            # Execution of actions in 'actions'
            new_turtle.execute_actions(actions)
            # Its a copy the constructor is not called, we have to set the id
            Turtle.turtles_number += 1
            new_turtle.set("id", Turtle.turtles_number)
            # We might have problems if a turtle is able to add turtle directly in the real list
            worlds[self.world_name].temp_new_turtles_list.append(new_turtle)  # @UndefinedVariable
 
    ###
    #    Kill the turtle by deleting it from the lists
    ###             
    def die(self):
        # We might have problems if a turtle is able to delete turtle directly in the real list
        self.patch.turtles_here.remove(self)
        worlds[self.world_name].temp_del_turtles_list.append(self)  

        
    ###
    #    Create a daughter class of turtle
    #    - name         : name of the new class
    ###
    def breed(cls, name) :
        class_name = type(name, (cls,), {"__init__": Turtle.__init__})
        Turtle.turtle_daughters[name] = class_name
        
    #Declaration as a class method 
    breed = classmethod(breed)

    ###
    #    Return every turtles of the type in parameter on the current patch
    #    - turtle_type    : type of the turtles we want
    ###
    def here(self, turtle_type="Turtle") :
        
        turtle_list = list()
        
        # If we are looking for a specific type of turtle
        if turtle_type.lower() != "turtle" :        
            for turtle in self.patch.turtles_here :
                if turtle_type == turtle.__class__.__name__ and turtle != self:      
                    turtle_list.append(turtle)
        else :
            turtle_list = self.patch.turtles_here
            turtle_list.remove(self)
                    
        return turtle_list
  
    ###
    #    Convert patches grid coordinate into pixels coordinate
    #    - attribute_name     : "x" or "y"
    #    - attribute_value    : coordinate in the patches grid
    ###  
    def pixels_coordinates(cls, attribute_name, attribute_value, patches_size, patches_number) :
        
        if attribute_name == "x" :
            center = (patches_number[0] - 1) // 2
            value = (attribute_value  + center) * patches_size[0]
        elif attribute_name == "y" :
            center = (patches_number[1] - 1) // 2
            value = (patches_number[1] - 1 - attribute_value - center)* patches_size[1]  
        
        return value
    
    #Declaration as a class method 
    pixels_coordinates = classmethod(pixels_coordinates)
 
    ###
    #    Convert pixels coordinate into patches grid coordinate
    #    - attribute_name     : "x" or "y"
    #    - attribute_value    : coordinate in the pixels grid
    ###    
    def patches_coordinates(cls, attribute_name, attribute_value, patches_size, patches_number) :
        
        if attribute_name == "x" :
            center = (patches_number[0] - 1) // 2
            value = (attribute_value/patches_size[0]) - center
            
        elif attribute_name == "y" :
            center = (patches_number[1] - 1) // 2
            value  = -(attribute_value/patches_size[1]) - center - 1 + patches_number[1]
        
        return value
    
    #Declaration as a class method 
    patches_coordinates = classmethod(patches_coordinates)


    ###
    #    Change the value of the class attribute in parameter
    #    - attribute_name    : attribute to change
    #    - attribute_value   : new value of the attribute
    #    - random            : "random" if the value is a random number
    ###    
    def set(self, attribute_name, attribute_value, rand=""):
        
        max_px = (worlds[self.world_name].patches_number[0] - 1)/2
        max_py = (worlds[self.world_name].patches_number[1] - 1)/2
        
        # When the user give a new patches grid coordinate we change the pixels grid coordinate
        value = attribute_value
        if attribute_name == "xcor" :
            if rand != "" :
                value = random.randrange(-max_px, max_px, 1)
            setattr(self, "xcor", value)   
            setattr(self, "_x", Turtle.pixels_coordinates("x", value, worlds[self.world_name].patches_size, worlds[self.world_name].patches_number))
        elif attribute_name == "ycor" :
            if rand != "" :
                value = random.randrange(-max_py, max_py, 1)
            setattr(self, "ycor", value)   
            setattr(self, "_y", Turtle.pixels_coordinates("y", value, worlds[self.world_name].patches_size, worlds[self.world_name].patches_number))
        else :
            Agent.set(self, attribute_name, attribute_value, rand)

    ###
    #    Return the value of the class attribute in parameter
    #    - attributeName     : attribute to change
    ###           
    def __getattribute__(self, attribute_name):
        
        # If the user asks for patches grid coordinate we update it with our pixels coordinate 
        if attribute_name == "xcor" :
            self.xcor = Turtle.patches_coordinates("x", self._x, worlds[self.world_name].patches_size, worlds[self.world_name].patches_number)
        elif attribute_name == "ycor" :
            self.ycor = Turtle.patches_coordinates("y", self._y, worlds[self.world_name].patches_size, worlds[self.world_name].patches_number)
        return object.__getattribute__(self, attribute_name)
        
    ###
    #    Return the patch the patch right and ahead of the turtle
    #    - angle           : angle of the research
    #    - distance        : distance of the research    
    ###    
    def patch_right_and_ahead(self, angle, distance):

        new_angle = Turtle._rotate(self.heading, -angle)
        x0, y0 = self._x, self._y      
        x0, y0 = Turtle._calc_coordinates(x0, y0, new_angle, distance, worlds[self.world_name].patches_size, worlds[self.world_name].patches_number)

        patch = worlds[self.world_name].get_patch(x0, y0)
        
        return patch   

    ###
    #    Return the patch the patch left and ahead of the turtle
    #    - angle           : angle of the research
    #    - distance        : distance of the research    
    ###
    def patch_left_and_ahead(self, angle, distance):
        
        return self.patch_right_and_ahead(-angle, distance)
 
    ###
    #    Return the patch the patch ahead of the turtle
    #    - distance        : distance of the research    
    ###   
    def patch_ahead(self, distance):
        
        return self.patch_right_and_ahead(0, distance)