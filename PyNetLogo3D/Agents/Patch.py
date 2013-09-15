###
# Imports
###
# PyNetLogo files
from Agents.Agent   import Agent
from Datas.Globals  import worlds

###
#     Patches are the individual static squares in the grid.
#     Attributes :
#     - x                 : coordinate on the x-axis in the patches grid
#     - y                 : coordinate on the y-axis in the patches grid
#     - z                 : coordinate on the z-axis in the patches grid
#     - turtles_here      : list of turtles which are on the patch
###
class Patch(Agent) :
    
    ###
    # Patch class variables 
    # - patches_number : number of patches already created
    ###
    patches_number = 0
    
    ###
    #    Patch constructor 
    #    - x                 : coordinate on the x-axis in the patches grid
    #    - y                 : coordinate on the y-axis in the patches grid
    #    - z                 : coordinate on the z-axis in the patches grid
    #    - _x                : x coordinate of the patch's bottom left corner in the panda3D grid
    #    - _y                : y coordinate of the patch's bottom left corner in the panda3D grid
    #    - _z                : z coordinate of the patch's bottom left corner in the panda3D grid
    #    - size              : size of the 3D cube (panda3D unit) 
    #    - texture           : texture of the patch (replace the NetLogo pcolor) 
    #    - world_name        : name of the world where the patch is
    #    - actions           : list to put method to apply. 
    #           syntax       : [("methodName",(parameter1,parameter2)), ("methodName2",(parameter1,parameter2))} 
    #           example      : [("set", ("coordinates", Rect(x, y, width, height))]
    ###
    def __init__(self, x, y, z, _x, _y, _z, size, texture, world_name, actions=[]):
        
        #We do not load the 3D model if there is no display
        if texture != None :
            Agent.__init__(self, Patch.patches_number + 1, world_name, _x, _y, _z, size, "cube", texture)
        else :
            Agent.__init__(self, Patch.patches_number + 1, world_name, _x, _y, _z, size, None, texture)
            
        Patch.patches_number += 1
        self.x              = x
        self.y              = y
        self.z              = z
        self.turtles_here   = list()
        
        self.execute_actions(actions)
        
    ###
    #    Change the value of the class attribute in parameter
    #    - attribute_name    : attribute to change
    #    - attribute_value   : new value of the attribute
    #    - random            : "random" if the value is a random number
    ###  
    def set(self, attribute_name, attribute_value, rand=""):

        # If the user change the texture, we have to add the patch in the updated list in order to change the display
        if attribute_name == "texture":
            worlds[self.world_name].updated_patches.append(self)
        Agent.set(self, attribute_name, attribute_value, rand)

    ###
    #    Return the panda3D coordinates of the patch's neighbors
    ###        
    def get_neighbors(self):
        x       = self._x
        y       = self._y
        z       = self._z
        size    = self.size
        return ((x,y,z+size),(x+size,y,z),(x,y+size,z),(x-size,y,z),(x,y-size,z),(x,y,z-size))

    ###
    #    Check the visibility of the patches, if it is surrounded by other patches we do not have to display it.
    ### 
    def check_visibility(self):
        
        show = False
        # If there is no texture, we do not have to render the patch
        if self.texture != None : 
            neighbor_number     = 0
            neighbors_positions = self.get_neighbors()
            nb_blocks_x         = worlds[self.world_name].patches_number[0]
            nb_blocks_y         = worlds[self.world_name].patches_number[1]
            nb_blocks_z         = worlds[self.world_name].patches_number[2]
            # Checking every neighbors
            while neighbor_number < len(neighbors_positions) and show == False:
                neigbor_x   = neighbors_positions[neighbor_number][0]
                neigbor_y   = neighbors_positions[neighbor_number][1]
                neigbor_z   = neighbors_positions[neighbor_number][2]
                pos_x       = neigbor_x/self.size
                pos_y       = neigbor_y/self.size
                pos_z       = neigbor_z/self.size

                # If the patch is on the border of the world
                if (pos_x > nb_blocks_x - 1 or pos_x < 0) or (pos_y > nb_blocks_y - 1 or pos_y < 0) or (pos_z > nb_blocks_z - 1 or pos_z < 0) :
                    show = True
                else :
                    neighbor_patch = worlds[self.world_name].get_patch(neigbor_x, neigbor_y, neigbor_z)
                    if neighbor_patch.texture == None :
                        show = True                
                neighbor_number += 1
                
        return show
    