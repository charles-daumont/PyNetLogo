###
# Imports
###
# Standard Python library
import threading
import importlib
import random
import time
# PyNetLogo files
import Interface
from Agents.Patch   import Patch
from Agents.Turtle  import Turtle


###
#    World Class.
#    Attributes :
#    - id                       : permits the identification of every worlds
#    - world_name               : name of the world
#    - turtles_dictionary       : contains every living turtles, classified by type 
#    - temp_new_turtles_list    : new turtles are not directly added to the dictionary above
#    - temp_del_turtles_list    : turtles are not directly deleted from the dictionary above
#    - patches_list             : contains every patches 
#    - lines_list               : contains every drawing lines
#    - updated_patches          : contains every patches which have been updated during the previous execution loop
#    - updated_lines            : contains every drawing lines which have been updated during the previous execution loop
#    - patches_size             : size of every patches in panda3D unit
#    - patches_number           : number of patches on every axis (patches_number[0] : x-axis, patches_number[1] : y-axis)
#    - run_bool                 : boolean to know the running state of the world
#    - sleep_time               : sleep time between 2 execution loops
#    - transfer_lock            : lock to protect data
### 
class World(threading.Thread):
    
    ###
    #    World class variables 
    #    - worlds_number          : number of worlds already created
    ###
    worlds_number = 0
    
    ###
    #    World constructor 
    #    - patches_size         : size of every patches in panda3D unit
    #    - patches_number       : number of patches on every axis (patches_number[0] : x-axis, patches_number[1] : y-axis)
    #    - world_name           : name of the world
    ###
    def __init__(self, patches_size, patches_number, world_name=""):
        threading.Thread.__init__(self)

        self.id                     = World.worlds_number + 1
        World.worlds_number         += 1
        if world_name == ""         : self.name = "world_" + str(self.id)    
        else                        : self.name = world_name        
        self.turtles_dictionary     = {}
        self.temp_new_turtles_list  = list()
        self.temp_del_turtles_list  = list()
        self.patches_list           = list()
        self.lines_list             = list()
        self.updated_patches        = list()
        self.updated_lines          = list()
        self.patches_size           = patches_size
        self.patches_number         = patches_number
        self.run_bool               = True
        self.sleep_time             = 0
        self.transfer_lock          = threading.Lock()    
        
        self.generate_patches_grid()              
    
    ###
    #    Generate the initial patches grid with standard values
    ###
    def generate_patches_grid(self):
        center_x = (self.patches_number[0] - 1) // 2
        center_y = (self.patches_number[1] - 1) // 2
        
        for x_cor in range(self.patches_number[0]) :
            # Convert coordinates 0,0 top left corner to 0,0 center
            x = x_cor - center_x
            
            for y_cor in range(self.patches_number[1]) :
                # Convert coordinates 0,0 top left corner to 0,0 center
                y = (self.patches_number[1] - 1) - y_cor - center_y
                new_patch = Patch(x, y, x_cor * self.patches_size[0], y_cor * self.patches_size[1], self.patches_size[0], self.patches_size[1], self.name)
                self.patches_list.append(new_patch)
                self.updated_patches.append(new_patch)
            
                   
    ###
    #    Reset the world with the default values
    ###       
    def reset(self):
        self.turtles_dictionary     = {}
        self.temp_new_turtles_list  = list()
        self.temp_del_turtles_list  = list()
        self.patches_list           = list()
        self.lines_list             = list()
        self.updated_patches        = list()
        self.updated_lines          = list()         
                      
        self.generate_patches_grid()       
    
    ###
    #    The world can create several turtles at once
    #    - category           : type of the turtle (turtle, wolf, sheep ...)
    #    - nb_turtles         : number of turtles created
    #    - params             : list to put method to apply
    ###    
    def create(self, category, nb_turtles=1, params=[]):
        
        if not category in self.turtles_dictionary :
            self.turtles_dictionary[category] = []
            
        for _ in range(0, nb_turtles) :
            if category == "Turtle" :
                self.turtles_dictionary["Turtle"].append(Turtle(self.name, params))
            else :
                self.turtles_dictionary[category].append(Turtle.turtle_daughters[category](self.name, params))

    ###
    #    The world can set every patch attribute at once
    #    - patches_list      : patches which perform the actions 
    #    - actions           : list to put method to apply
    #           syntax       : [("methodName",(parameter1,parameter2)), ("methodName2",(parameter1,parameter2))} 
    #           example      : [("set", ("coordinates", Rect(x, y, width, height))]
    ### 
    def _ask_patches(self, patches_list, actions=[]):  

        for patch in patches_list :
            patch.execute_actions(actions)
 
    ###
    #    The world can perform actions on every turtles at once
    #    - turtles_list       : patches which perform the actions
    #    - actions            : list to put actions to perform.
    #           syntax        : [("methodName",(parameter1,parameter2)), ("methodName2",(parameter1,parameter2))}  
    #           example       : [("set",("heading",10)), ("forward",(10))]}
    ###                 
    def _ask_turtles(self, turtles_list, actions=[]):
        from Datas.Globals import worlds
        # Check if the actions are on every turtles or only a specific class        
        for turtle in turtles_list :
            turtle.execute_actions(actions)
        
        if len(worlds) > 1 :
            self.transfer_lock.acquire()
            
        # Add the new turtles to the real list
        for turtle in self.temp_new_turtles_list :
            if not turtle.__class__.__name__ in self.turtles_dictionary :
                self.turtles_dictionary[turtle.__class__.__name__] = []
                
            self.turtles_dictionary[turtle.__class__.__name__].append(turtle)
        
        # Delete turtle in the real list
        for turtle in self.temp_del_turtles_list :
            if turtle in self.turtles_dictionary[turtle.__class__.__name__] :
                self.turtles_dictionary[turtle.__class__.__name__].remove(turtle)
        
        # Reset the temporary turtles list   
        self.temp_new_turtles_list = list()
        self.temp_del_turtles_list = list()
        
        if len(worlds) > 1 :
            self.transfer_lock.release()

    ###
    #    Select a random agent of the category in parameter in the list in parameter
    #    - category          : "turtle", "patch", "wolf" ...
    #    - agent_list        : list where we have to select one agent
    ###
    def one_of(self, category="Turtle", agent_list=None):
        agent = None
        temp_agent_list = list()
        
        if len(agent_list) != 0 :
            # Select every agent in the list which are of the right category
            for agent in agent_list :
                if agent.__class__.__name__ == category :
                    temp_agent_list.append(agent)
            # Select a random agent
            agent = random.choice(temp_agent_list)
            
        return agent
    
    ###
    #    Return the patch at the given coordinates in pixels
    #    - x               : coordinate on the x-axis
    #    - y               : coordinate on the y-axis    
    ###    
    def get_patch(self, x, y):
        
        pos_x = x // self.patches_size[0]
        pos_y = y // self.patches_size[1]
        
        patch_pos = pos_x * self.patches_number[1] + pos_y
        
        return self.patches_list[int(patch_pos)]

    ###
    #    Return the value of the turtle's attribute 
    #    - agent_type       : type of the turtle we are looking for
    #    - id_number        : id of the specific turtle we want
    #    - attribute_name   : name of the attribute we need
    ###   
    def get_from(self, agent_type, id_number, attribute_name):
        return getattr(self.turtles_dictionary[agent_type][id_number], attribute_name)

    ###
    #    Execution loop of the world
    ###     
    def world_processing(self, go_method):
        from Datas.Globals import worlds
        
        if len(worlds) > 1 :
            self.transfer_lock.acquire()
            
        # Add the new turtles (potentially added by an other world) to the real list
        for turtle in self.temp_new_turtles_list :
            if not turtle.__class__.__name__ in self.turtles_dictionary :
                self.turtles_dictionary[turtle.__class__.__name__] = []
                
            self.turtles_dictionary[turtle.__class__.__name__].append(turtle)
        
        # Delete turtle (potentially deleted by an other world) in the real list
        for turtle in self.temp_del_turtles_list :
            if turtle in self.turtles_dictionary[turtle.__class__.__name__] :
                self.turtles_dictionary[turtle.__class__.__name__].remove(turtle)
        
        # Reset the temporary turtles list   
        self.temp_new_turtles_list = list()
        self.temp_del_turtles_list = list()
        
        if len(worlds) > 1 :
            self.transfer_lock.release()
        
        go_method()
 
    ###
    #    A thread must redefine this method, which is called when the thread starts
    ###        
    def run(self):
        from Datas.Globals import worlds_locks
        file_name = "User_code." + self.name
        import_file = importlib.import_module(file_name, package="User_code")
        
        worlds_locks[self.name].acquire()
        import_file.declaration()
        Interface.add_methods("turtle", import_file.turtles_methods_dictionary)
        Interface.add_methods("patch", import_file.patches_methods_dictionary)
        import_file.setup()
        worlds_locks[self.name].release()
               
        while self.run_bool == True:
            worlds_locks[self.name].acquire()
            self.world_processing(import_file.go)
            worlds_locks[self.name].release()
            #time.sleep(self.sleep_time)



