###
# Imports
###
# PyNetLogo files
from Datas.Textures         import textures
# Panda3D
from pandac.PandaModules    import Vec4, BitMask32
from direct.actor.Actor     import Actor

HIGHLIGHTCOLOR = Vec4(.5,.5,.5,0)
DEFAULTCOLOR = Vec4(1,1,1,0)

###
#     Object_3D Class.
#     Attributes :
#    - model      : loaded 3D model (with animation if it is a turtle
#    - _x         : coordinate on the x-axis in the panda3D grid
#    - _y         : coordinate on the y-axis in the panda3D grid
#    - _z         : coordinate on the z-axis in the panda3D grid
#    - size       : size of the 3D model
#    - texture    : texture to apply on the 3D model
###
class Object_3D(object):

    ###
    #    Object_3D constructor 
    #    - x           : coordinate on the x-axis in the panda3D grid
    #    - y           : coordinate on the y-axis in the panda3D grid
    #    - z           : coordinate on the z-axis in the panda3D grid
    #    - size        : size of the 3D model
    #    - model       : name of the 3D model to load
    #    - texture     : texture to apply on the 3D model
    ###
    def __init__(self, x, y, z, size, model, texture=None):

        self.model = None
        # if the 3D_object is a turtle, we create an actor instead of a static model
        if model != None :
            self.model = Actor("eggs/"+model+".egg")
            self.model.setPos((x, y, z))
            self.model.setScale(size, size, size)
        
        self._x = x
        self._y = y
        self._z = z
        self.size = size
        self.texture = texture

    ###
    #    Return the value of the class attribute in parameter
    #    - attribute_name     : attribute to change
    ###   
    def __getattribute__(self, attribute_name):
        return object.__getattribute__(self, attribute_name)
 
    ###
    #    Change the value of the class attribute in parameter. 
    #    - attribute_name     : attribute to change
    #    - attribute_value    : new attribute value
    ###       
    def __setattr__(self, attribute_name, attribute_value):
        object.__setattr__(self, attribute_name, attribute_value)
 
    ###
    #    Add the 3D object in the rendering tree of panda3D
    #    - render_node : parent node of the 3D object
    ###       
    def draw(self, render_node):
        if self.texture != None :
            if self.model == None :
                self.model = loader.loadModel("eggs/cube.egg")
                self.model.setPos((self._x, self._y, self._z))
                self.model.setScale(self.size, self.size, self.size) 
            
            self.rendernode = render_node
            self.model.setTexture(textures[self.texture])
            self.model.reparentTo(render_node)
            self.model.setCollideMask(BitMask32.bit(1))
            self.model.setTag('cube',str(self._x) + ',' + str(self._y) + ',' + str(self._z))

    ###
    #    Change the color of the 3D_object
    #    - render_node : parent node of the 3D object
    ### 
    def highlight(self, boolean):
        if boolean == True :
            self.model.setColor(HIGHLIGHTCOLOR)
        else :
            self.model.setColor(DEFAULTCOLOR)
        
