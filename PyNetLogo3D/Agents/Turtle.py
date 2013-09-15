###
# Imports
###
# Standard Python library
import math
import copy
import random
# PyNetLogo files
from Agents.Agent   import Agent
from Object_3D      import Object_3D
from Datas.Globals  import worlds

###
#     Turtles are the moving agents of NetLogo.
#     Attributes :
#     - xcor         : coordinate on the x-axis in the patches grid
#     - ycor         : coordinate on the y-axis in the patches grid
#     - zcor         : coordinate on the z-axis in the patches grid
#     - heading      : the rotation of the turtle around the z-axis
#     - pitch        : the angle between the nose of the turtle and the xy-plane
#     - roll         : the rotation around the turtle's forward vector
#     - hidden       : boolean to know if we have to display the turtle
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
                
        Agent.__init__(self, Turtle.turtles_number + 1, world_name, 0, 0, 0, 0.5, "cube", "metal")
        Turtle.turtles_number   += 1
        self.xcor               = 0
        self.ycor               = 0
        self.zcor               = 0
        self.heading            = 0
        self.pitch              = 0
        self.roll               = 0
        self.hidden             = False
        self.pen_mode           = False  
        self.pen_size           = 1
        self.patch              = None
        
        self.execute_actions(actions)

        self.patch              = worlds[self.world_name].get_patch(self._x, self._y, self._z)
        self.patch.turtles_here.append(self)
    
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
    #    Return the coordinate in a torus world
    ###
    def _torus_coordinates(cls, x, y, z, patches_size, patches_number):
        
        max_pxcor           = patches_number[0] * patches_size
        max_pycor           = patches_number[1] * patches_size
        max_pzcor           = patches_number[2] * patches_size
        
        _x, _y, _z          = x, y, z
        
        if x < 0 or x > max_pxcor -1 : _x = x % max_pxcor - 1
        if y < 0 or y > max_pycor -1 : _y = y % max_pycor - 1
        if z < 0 or z > max_pzcor -1 : _z = z % max_pzcor - 1
            
        return (_x, _y, _z)
    
    #Declaration as a class method 
    _torus_coordinates = classmethod(_torus_coordinates)
    
    ###
    #    Return new coordinates after a movement
    #    - x               : x coordinate of the movement origin
    #    - y               : y coordinate of the movement origin
    #    - z               : z coordinate of the movement origin
    #    - heading         : angle of the movement around the z-axis
    #    - pitch           : angle of the movement between the nose of the turtle and the xy-plane
    #    - distance        : distance of the movement
    #    - patches_size    : size of every patches in the panda3D grid
    #    - patches_number  : number of patches on each axis. (patches_number[0] : x-axis, patches_number[1] : y-axis)
    ###

    def _calc_coordinates(cls, x, y, z, heading, pitch, distance, patches_size, patches_number):
              
        # Forward 1 = movement of 1 patch = 1 * patchSize
        distance_patches = distance * patches_size
        distance_xy      = distance_patches * math.cos(math.radians(pitch))

        x1 = x + distance_xy * math.cos(math.radians(heading))
        y1 = y - distance_xy * math.sin(math.radians(heading))
        z1 = z + distance_patches * math.sin(math.radians(pitch))
        
        x1, y1, z1 = Turtle._torus_coordinates(x1, y1, z1, patches_size, patches_number)

        return (x1, y1, z1)
    
    #Declaration as a class method 
    _calc_coordinates = classmethod(_calc_coordinates)    

    ###
    #    Rotate the turtle
    #    - angle             : degree
    ### 
    def _rotate(cls, current_angle, angle):
        return ((current_angle + angle) % 360)
        
    #Declaration as a class method
    _rotate = classmethod(_rotate)
        
    ###
    #    Change the turtle's coordinates
    #    - distance        : distance to move
    ###
    def _move(self, distance):
        
        # Calculate the new coordinates 
        x0, y0, z0 = self._x, self._y, self._z 
        self._x, self._y, self._z = Turtle._calc_coordinates(x0, y0, z0, self.heading, self.pitch, distance, worlds[self.world_name].patches_size, worlds[self.world_name].patches_number)
        
        # Update the patch where the turtle is
        if self.patch != None :
            self.patch.turtles_here.remove(self)
        self.patch = worlds[self.world_name].get_patch(self._x, self._y, self._z)
        self.patch.turtles_here.append(self)
        
        #Add a new line in world.lines_list
        if self.pen_mode == True :
            if ((x0, y0, z0), (self._x, self._y, self._z)) not in worlds[self.world_name].lines_list :
                worlds[self.world_name].lines_list.append((self, (x0, y0, z0), (self._x, self._y, self._z)))
                worlds[self.world_name].updated_lines.append((self, (x0, y0, z0), (self._x, self._y, self._z)))
        
        
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
    #    The nose of the turtle rotates by number degrees, relative to its current orientation.
    #    - angle             : degree
    ###         
    def tilt_up(self, angle):
        self.pitch = Turtle._rotate(self.pitch, angle)
        
    def tilt_down(self, angle):
        self.pitch = Turtle._rotate(self.pitch, -angle)
    
    ###
    #    The wingtip of the turtle rotates to the left number degrees with respect to the current heading and pitch.
    #    - angle             : degree
    ###
    def roll_left(self, angle):
        self.roll = Turtle._rotate(self.roll, angle)

    ###
    #    The wingtip of the turtle rotates to the right number degrees with respect to the current heading and pitch.
    #    - angle             : degree
    ###    
    def roll_right(self, angle):
        self.roll = Turtle._rotate(self.roll, -angle)
        
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
    #    Return the center on the given axis 
    #    - axis               : "x", "y" or "z"
    #    - patches_number     : number of patches on each axis. (patches_number[0] : x-axis, patches_number[1] : y-axis)
    ###     
    def get_center(cls, axis, patches_number):
        
        if axis == "x"      : center = (patches_number[0] - 1) // 2  
        elif axis == "y"    : center = (patches_number[1] - 1) // 2
        elif axis == "z"    : center = (patches_number[2] - 1) // 2
            
            
        return center  
      
    get_center = classmethod(get_center)
    
    ###
    #    Convert NetLogo patches grid coordinate into panda3D coordinate
    #    - attribute_name     : "x", "y" or "z"
    #    - attribute_value    : coordinate in the NetLogo patches grid
    #    - patches_size       : size of every patches in the panda3D grid
    #    - patches_number     : number of patches on each axis. (patches_number[0] : x-axis, patches_number[1] : y-axis)
    ###  
    def panda3D_coordinates(cls, attribute_name, attribute_value, patches_size, patches_number) :
        
        center = Turtle.get_center(attribute_name, patches_number)  
        return (attribute_value  + center) * patches_size
    
    #Declaration as a class method 
    panda3D_coordinates = classmethod(panda3D_coordinates)
 
    ###
    #    Convert panda3D coordinate into patches grid coordinate
    #    - attribute_name     : "x", "y" or "z"
    #    - attribute_value    : coordinate in the panda3D grid
    #    - patches_size       : size of every patches in the panda3D grid
    #    - patches_number     : number of patches on each axis. (patches_number[0] : x-axis, patches_number[1] : y-axis)
    ###    
    def patches_coordinates(cls, attribute_name, attribute_value, patches_size, patches_number) :
        
        center = Turtle.get_center(attribute_name, patches_number)              
        return (attribute_value/patches_size) - center 
    
    #Declaration as a class method 
    patches_coordinates = classmethod(patches_coordinates)

    ###
    #    Change the value of the class attribute in parameter
    #    - attribute_name    : attribute to change
    #    - attribute_value   : new value of the attribute
    #    - rand              : "random" if the value is a random number
    ###    
    def set(self, attribute_name, attribute_value, rand=""):
        
        max_px          = (worlds[self.world_name].patches_number[0] - 1)/2
        max_py          = (worlds[self.world_name].patches_number[1] - 1)/2
        max_pz          = (worlds[self.world_name].patches_number[2] - 1)/2
        patches_size    = worlds[self.world_name].patches_size
        patches_number  = worlds[self.world_name].patches_number
        
        # When the user give a new patches grid coordinate we change the panda3D grid coordinate
        value = attribute_value
        if attribute_name == "xcor" :
            if rand != "" :
                value = random.randrange(-max_px, max_px, 1)
            setattr(self, "xcor", value)   
            setattr(self, "_x", Turtle.panda3D_coordinates("x", value, patches_size, patches_number))
        elif attribute_name == "ycor" :
            if rand != "" :
                value = random.randrange(-max_py, max_py, 1)
            setattr(self, "ycor", value)   
            setattr(self, "_y", Turtle.panda3D_coordinates("y", value, patches_size, patches_number))
        elif attribute_name == "zcor" :
            if rand != "" :
                value = random.randrange(-max_pz, max_pz, 1)
            setattr(self, "zcor", value)   
            setattr(self, "_z", Turtle.panda3D_coordinates("z", value, patches_size, patches_number))
        else :
            Agent.set(self, attribute_name, attribute_value, rand)


    ###
    #    Return the value of the class attribute in parameter
    #    - attribute_name     : attribute to change
    ###           
    def __getattribute__(self, attribute_name):

        # If the user asks for patches grid coordinate we update it with our panda3D coordinate 
        if attribute_name == "xcor" :
            self.xcor = Turtle.patches_coordinates("x", self._x, worlds[self.world_name].patches_size, worlds[self.world_name].patches_number)
        elif attribute_name == "ycor" :
            self.ycor = Turtle.patches_coordinates("y", self._y, worlds[self.world_name].patches_size, worlds[self.world_name].patches_number)
        elif attribute_name == "zcor" :
            self.ycor = Turtle.patches_coordinates("z", self._z, worlds[self.world_name].patches_size, worlds[self.world_name].patches_number)
            
        return Object_3D.__getattribute__(self, attribute_name)


    ###
    #    Change the value of the class attribute in parameter. When we change these attributes we also have to change
    #    these ones on the panda3D loaded model.
    #    - attribute_name     : attribute to change
    #    - attribute_value    : new attribute value
    ### 
    def __setattr__(self, attribute_name, attribute_value):
        Object_3D.__setattr__(self, attribute_name, attribute_value)
        if attribute_name == "_x" : 
            self.model.setX(attribute_value)
        elif attribute_name == "_y" :
            self.model.setY(attribute_value)
        elif attribute_name == "_z" :
            self.model.setZ(attribute_value)
        
        elif attribute_name == "heading" :
            self.model.setH(attribute_value)
        elif attribute_name == "pitch" :
            self.model.setP(attribute_value)
        elif attribute_name == "roll" :
            self.model.setR(attribute_value)
        elif attribute_name == "size" :
            self.model.setScale(attribute_value, attribute_value, attribute_value)
               
    ###
    #    Return the patch the patch right and ahead of the turtle
    #    - angle           : angle of the research
    #    - distance        : distance of the research    
    ###    
    def patch_right_and_ahead(self, angle, distance):

        new_angle = Turtle._rotate(self.heading, -angle)
        x0, y0, z0 = self._x, self._y, self._z   
        x0, y0, z0 = Turtle._calc_coordinates(x0, y0, z0, new_angle, self.pitch, distance, worlds[self.world_name].patches_size, worlds[self.world_name].patches_number)

        patch = worlds[self.world_name].get_patch(x0, y0, z0)
        
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