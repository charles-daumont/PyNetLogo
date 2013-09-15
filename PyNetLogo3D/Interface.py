###
# Imports
###
# Standard Python library
import copy
# PyNetLogo files
from World import *
from Datas.Globals import worlds, worlds_locks, worlds_display_position


def clear_all():
    world_name = threading.current_thread().name
    worlds[world_name].reset()
    
def create(category, nbTurtles=1, params=[]):
    world_name = threading.current_thread().name
    worlds[world_name].create(category, nbTurtles, params)
    
def reset_ticks():
    return 0   

###
#    Add every methods created by the user to their class
#    agent_type : "patch" or "turtle"
###    
def add_methods(agent_type, methods_dictionnary={}):
    cls = None
    
    if agent_type.lower() == "turtle" :
        cls = Turtle
    elif agent_type.lower() == "patch" :
        cls = Patch
        
    for method in methods_dictionnary :
        if hasattr(cls, method) == False :
            setattr(cls, method, methods_dictionnary[method])
          
###
#    The world can perform actions on many agents at once
#    - agents_list        : agents which perform the actions ("Turtle", "Patch", "Wolf" ...)
#    - actions            : list to put actions to perform.
#           syntax        : [("methodName",(parameter1,parameter2)), ("methodName2",(parameter1,parameter2))}  
#           example       : [("set",("heading",10)), ("forward",(10))]}
###             
def ask(agents_list, actions=[]):
    world_name = threading.current_thread().name
    if agents_list :
        if agents_list[0].__class__.__name__ == "Patch" :
            worlds[world_name]._ask_patches(agents_list, actions)
        else :
            worlds[world_name]._ask_turtles(agents_list, actions)
        
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
    world_name = threading.current_thread().name
    if agent_list == None :
        agent_list = worlds[world_name].turtlesDictionnary[category]
    
    return worlds[world_name].one_of(category, agent_list)

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
    world_name = threading.current_thread().name
    return worlds[world_name].get_from(agent_type, id_number, attribute_name)

def stop():
    world_name = threading.current_thread().name
    worlds[world_name].run_bool = False

###
#    Return all agents from a given type
###
def all(agent_type):
    world_name = threading.current_thread().name
    if agent_type.lower() == "patch" :
        return worlds[world_name].patches_list
    elif agent_type.lower() != "turtle" :
        return worlds[world_name].turtles_dictionary[agent_type]
    else :
        all_turtles = list()
        for dictionary_type in worlds[world_name].turtles_dictionary :
            all_turtles = all_turtles + worlds[world_name].turtles_dictionary[dictionary_type]         
        return all_turtles

def get_patch(x, y, z):
    world_name = threading.current_thread().name
    patches_size = worlds[world_name].patches_size
    return [worlds[world_name].get_patch(x*patches_size, y*patches_size, z*patches_size)]

###
#    Create a new world
#    - patches_size    : size of every patches in panda3D unit
#    - max_px          : number of patches on the half x-axis
#    - max_py          : number of patches on the half y-axis
#    - max_pz          : number of patches on the half z-axis
#    - world_name      : name of the world
###
def create_world(patch_size, max_px, max_py, max_pz, world_name=""): 
    import Datas      
    world                   = World(patch_size, [max_px*2 + 1, max_py*2 + 1, max_pz*2 +1], world_name)
    worlds[world.name]      = world
    worlds_locks[world.name]= threading.Lock()

    worlds_display_position.append(Datas.Globals.max_x)
    Datas.Globals.max_x += world.patches_size * world.patches_number[0]
    if world.patches_size * world.patches_number[1] > Datas.Globals.max_y :
        Datas.Globals.max_y = world.patches_size * world.patches_number[1]
            
###
#    Transfer a turtle from one world to an other
###            
def transfer(agent_set, destination_name):
    worlds[destination_name].transfer_lock.acquire()
    
    for agent in agent_set :
        new_turtle = copy.copy(agent)
        new_turtle.patch = worlds[destination_name].get_patch(new_turtle._x, new_turtle._y, new_turtle._z)
        worlds[destination_name].temp_new_turtles_list.append(new_turtle)
                   
    worlds[destination_name].transfer_lock.release()        
