###
# Imports
###
# Standard Python library
import random
import types
# PyNetLogo files
from Object_3D import Object_3D

###
#     Agent Class.
#     Attributes :
#    - id           : permits the identification of every agents
#    - world_name   : the name of the world which contains the agent
###
class Agent(Object_3D):

    ###
    #    Agent constructor 
    #    - number       : permits the identification of every agents
    #    - world_name   : the name of the world which contains the agent
    #    - _x           : coordinate on the x-axis in the panda3D grid
    #    - _y           : coordinate on the y-axis in the panda3D grid
    #    - _z           : coordinate on the z-axis in the panda3D grid
    #    - size         : size of the 3D model
    #    - model        : name of the 3D model to load
    #    - texture      : texture to apply on the 3D model
    ###
    def __init__(self, number, world_name, _x, _y, _z, size, model, texture):
        Object_3D.__init__(self, _x, _y, _z, size, model, texture)
        self.id         = number
        self.world_name = world_name
    
    ###
    #    Add a new attribute to the class
    #    - attribute_name    : name of the new attribute
    #    - attribute_value   : new value of the attribute
    ###
    def own(cls, attribute_name, attribute_value=0) :
        if hasattr(cls, attribute_name) == False :
            setattr(cls, attribute_name, attribute_value)
        else :
            print ("\"{0}\" is already an attribute of {1}".format(attribute_name, cls.__name__))
            
    #Declaration as a class method 
    own = classmethod(own) 
    
    ###
    #    Change the value of the class attribute in parameter
    #    - attribute_name    : attribute to change
    #    - attribute_value   : new value of the attribute
    #    - random            : "random" if the value is a random number
    ### 
    def set(self, attribute_name, attribute_value, rand=""):
        if hasattr(self, attribute_name) == True :
            if rand == "" :
                setattr(self, attribute_name, attribute_value)
            else :
                setattr(self, attribute_name, int(attribute_value * random.random()))
        else :
            print("\"{0}\" is not an attribute of {1}".format(attribute_name, self.__class__.__name__))
    
    ###
    #    Permits to apply several methods to the agent
    #    - actions            : list to put actions to perform.
    #           syntax        : [("methodName",(parameter1,parameter2)), ("methodName2",(parameter1,parameter2))}  
    #           example       : [("set",("heading",10)), ("forward",(10))]
    ###              
    def execute_actions(self, actions):

        for action in actions :
            if action != None and action != ():
                # If action case ("if", ("self.id == 1", [("forward",(1)), ("set",("heading", 2))]) )
                if action[0].lower() == "if" :
                    if eval(action[1][0]) == True :
                        self.execute_actions(action[1][1])
                else :
                    actionType = type(getattr(self.__class__, action[0]))
                    # If the action match a class method 
                    if (hasattr(self.__class__, action[0]) == True) and (actionType == types.FunctionType or actionType == types.MethodType) :
                        method = getattr(self.__class__, action[0])
                        # If the function has more than one parameter, they are in a tuple. We have to unpack it to execute the method.
                        if type(action[1]) == tuple :                       
                            method(self, *action[1])   # * is the unpacking operator
                        else :
                            method(self, action[1])
                    else :
                        print ("\"{0}\" is not in the class \'{1}\'".format(action[0], self.__class__.__name__))
    
    ###
    #    Permits to apply several methods to the agent many times
    #    - repeat_number      : how many times the method applies the actions on the agent
    #    - actions            : list to put actions to perform.
    #           syntax        : [("methodName",(parameter1,parameter2)), ("methodName2",(parameter1,parameter2))}  
    #           example       : [("set",("heading",10)), ("forward",(10))]
    ###      
    def repeat(self, repeat_number, actions={}):
    
        for _ in range(0, repeat_number) :
            self.execute_actions(actions)

