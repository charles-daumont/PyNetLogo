###
# Imports
###
# PyNetLogo files
from World import *
from Datas.Globals import world

def clear_all():
    world.reset()
    
def create(category="Turtle", nbTurtles=1, params=[]):
    world.create(category, nbTurtles, params)
    
def reset_ticks():
    return 0    
    
def add_methods(agent_type, methods_dictionnary={}):
    if agent_type == "turtle" : 
        for method in methods_dictionnary :
            if hasattr(Turtle, method) == False :
                setattr(Turtle, method, methods_dictionnary[method])
                
    elif agent_type == "patch" :
        for method in methods_dictionnary :
            if hasattr(Patch, method) == False :
                setattr(Patch, method, methods_dictionnary[method])
                
###
#    The world can perform actions on many agents at once
#    - agents_list        : agents which perform the actions ("Turtle", "Patch", "Wolf" ...)
#    - actions            : list to put actions to perform.
#           syntax        : [("methodName",(parameter1,parameter2)), ("methodName2",(parameter1,parameter2))}  
#           example       : [("set",("heading",10)), ("forward",(10))]}
###             
def ask(agents_list, actions=[]):
    if agents_list :
        if agents_list[0].__class__.__name__ == "Patch" :
            world._ask_patches(agents_list, actions)
        else :
            world._ask_turtles(agents_list, actions)
        
def rand(end=0):
    
    if end == 0 :
        return random.random()
    else :
        return random.randrange(0, end, 1)

###
#    Select a random agent of the type in parameter
#    - category            : "turtle", "patch", "wolf" ...
###
def one_of(category="Turtle", agent_list=None):
    
    if agent_list == None :
        agent_list = world.turtlesDictionnary[category]
    
    return world.one_of(category, agent_list)

###
#    Create a new class
###
def breed(class_name) :
    Turtle.breed(class_name)

###
#    Add new attributes to the given class
###    
def own(class_name, attributes) :
    
    if class_name.lower() == "turtle" :
        if type(attributes) == list :
            for attribute in attributes :
                Turtle.own(attribute)
        else :
            Turtle.own(attributes)
            
    elif class_name.lower() == "patch" :
        if type(attributes) == list :
            for attribute in attributes :
                Patch.own(attribute)
        else :
            Patch.own(attributes)
            
    else :
        if type(attributes) == list :
            for attribute in attributes :
                Turtle.turtle_daughters[class_name].own(attribute)
        else :
            Turtle.turtle_daughters[class_name].own(attributes)
 
def get_from(agent_type, id_number, attribute_name):
    
    return world.get_from(agent_type, id_number, attribute_name)

def stop():
    import Datas
    Datas.Globals.boolean_stop = True 

###
#    Return all agents from a given type
###
def all(agent_type):
    if agent_type.lower() == "patch" :
        return world.patches_list
    elif agent_type.lower() != "turtle" :
        return world.turtles_dictionary[agent_type]
    else :
        all_turtles = list()
        for dictionary_type in world.turtles_dictionary :
            all_turtles = all_turtles + world.turtles_dictionary[dictionary_type]         
        return all_turtles

def get_patch(x, y):
    return [world.get_patch(x*world.patches_size[0], y*world.patches_size[1])]