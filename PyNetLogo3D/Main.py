###
# Imports
###
# Panda3D
from direct.directbase              import DirectStart
from direct.showbase.DirectObject   import DirectObject
from direct.task.Task               import Task
from direct.gui.DirectGui           import DirectSlider
from pandac.PandaModules import lookAt
from pandac.PandaModules import CardMaker
from pandac.PandaModules import Light, AmbientLight, PointLight
from pandac.PandaModules import Geom, GeomNode
from pandac.PandaModules import Vec4, BitMask32
from pandac.PandaModules import Texture
from pandac.PandaModules import LineSegs
# Standard Python library
import random
# PyNetLogo files
from Datas.Textures         import textures
from User_code.Add_worlds   import add_worlds
from Datas.Globals          import worlds, worlds_locks



class Main(DirectObject):
    def __init__(self):
        
        # Display nodes creation
        self.patches_node    = render.attachNewNode("patches_node")
        self.agents_node     = render.attachNewNode("agents_node")
        self.lines_node      = render.attachNewNode("lines_node")
        self.light_node      = render.attachNewNode("light_node")
        self.floor_node      = render.attachNewNode("floor_node")
        self.frame_node      = render.attachNewNode("frame_node")
        self.env_node        = render.attachNewNode("env_node")
        
        # Light settings
        self.light = True
        self.dlight = PointLight("dlight")
        self.dlight.setColor(Vec4(.8,.8,.5,1))
        self.dlnp = render.attachNewNode(self.dlight)
        self.dlnp.setPos(0,100,100)
        render.setLight(self.dlnp)
        
        ambientLight = AmbientLight("ambientLight")
        ambientLight.setColor(Vec4(.4, .4, .4, 1))
        render.setLight(render.attachNewNode(ambientLight))
        
        #self.create_floor(121, 121, "grass_floor") 
        self.create_frame(121, 121, 0) 
        self.add_model(self.env_node, "env", (60,60,-0.5), 200)
        self.fill_env()
        
        taskMgr.add(self.game_loop, "game_loop")
        taskMgr.add(self.close_window, "close_window")
        
    def toggle_lights(self):
        self.light = not(self.light)
        
        if self.light:
            render.setLight(self.dlnp)
        else:
            render.setLightOff(self.dlnp)
    
    def add_model(self, rendering_node, model, position, scale, heading=0):
        new_model = loader.loadModel("eggs/"+model)
        new_model.setPos(*position)
        new_model.setScale(scale)
        new_model.setH(heading)
        new_model.reparentTo(rendering_node)
    
    def add_line(self, rendering_node, color, thickness, start, end):
        linesegs = LineSegs()  
        linesegs.setColor(*color) 
        linesegs.setThickness(thickness)
        linesegs.drawTo((start[0], start[1], start[2])) 
        linesegs.drawTo((end[0], end[1], end[2]))    
        new_node = linesegs.create()
        rendering_node.attachNewNode(new_node)
        
    def fill_env(self):

        for _ in range (100) :
            self.add_model(self.env_node, "daisy", (random.random()*121,random.random()*121,0), 2)
            self.add_model(self.env_node, "Fern", (random.random()*121,random.random()*121,0), 0.01, random.random()*360)
            self.add_model(self.env_node, "rock", (random.random()*121,random.random()*121,0), random.random()*0.1+0.1, random.random()*360)      

        self.env_node.flattenStrong()
        
    def game_loop(self, task):    
          
        for lock in worlds_locks :
            worlds_locks[lock].acquire()
   
        for world_name in worlds :
            patch_center = worlds[world_name].patches_size / 2.0

            for patch in worlds[world_name].updated_patches :
                if patch.check_visibility() :
                    patch.draw(self.patches_node)
            if len(worlds[world_name].updated_patches) > 0 :
                worlds[world_name].updated_patches = list()
            
            for lines in worlds[world_name].updated_lines :
                start = (lines[1][0]+patch_center, lines[1][1]+patch_center, lines[1][2]+patch_center)
                end = (lines[2][0]+patch_center, lines[2][1]+patch_center, lines[2][2]+patch_center)
                self.add_line(self.lines_node, (1,0,0,1), lines[0].pen_size, start, end)

            if len(worlds[world_name].updated_lines) > 0 :
                self.lines_node.flattenStrong() 
                worlds[world_name].updated_lines = list()
            
            for turtle_type in worlds[world_name].turtles_dictionary :
                for turtle in worlds[world_name].turtles_dictionary[turtle_type] :
                    if not turtle.hidden :
                        turtle.model.setPos(turtle._x+patch_center, turtle._y+patch_center, turtle._z+patch_center)
                        turtle.draw(self.agents_node)
                   
        for lock in worlds_locks :
            worlds_locks[lock].release()
            
        return Task.cont
    
    def close_window(self, task):
        if base.win.isClosed() :  
            for world_name in worlds :
                worlds[world_name].stop()
    
    def create_floor(self, size_x_axis, size_y_axis, texture):
        
        card_maker = CardMaker('')
        card_maker.setFrame(0,size_x_axis,0,size_y_axis)
        '''
        for y in range(size_y_axis):
            for x in range(size_x_axis):
                new_node = self.floorNode.attachNewNode(card_maker.generate())
                new_node.setP(-90)
                new_node.setPos(x, y, 0)
        '''
        new_node = self.floor_node.attachNewNode(card_maker.generate())
        new_node.setP(-90)
        new_node.setPos(0, 0, 0)
        new_node.setTexture(textures[texture])    
        
        self.floor_node.flattenStrong()

    
    def create_frame(self, size_x_axis, size_y_axis, size_z_axis):
        
        edges = [((0,0,0),(size_x_axis, 0, 0)), 
                 ((0,0,0),(0, size_y_axis, 0)),
                 ((0,0,0),(0, 0, size_z_axis)), 
                 ((0,0,size_z_axis),(size_x_axis, 0, size_z_axis)),
                 ((size_x_axis,0,0),(size_x_axis, 0, size_z_axis)),
                 ((size_x_axis,0,0),(size_x_axis, size_y_axis, 0)),
                 ((size_x_axis,0,size_z_axis),(size_x_axis, size_y_axis, size_z_axis)),
                 ((size_x_axis,size_y_axis,0),(size_x_axis, size_y_axis, size_z_axis)),
                 ((0,0,size_z_axis),(0, size_y_axis, size_z_axis)),
                 ((0,size_y_axis,0),(0, size_y_axis, size_z_axis)),
                 ((0,size_y_axis,0),(size_x_axis, size_y_axis, 0)),
                 ((0,size_y_axis,size_z_axis),(size_x_axis, size_y_axis, size_z_axis)),       
                 ]
        
        for edge in edges :
            self.add_line(self.frame_node, (0,0,0,0), 3, edge[0], edge[1])  

def slider_action():
    for world_name in worlds :
        worlds[world_name].sleep_time = slider['value']
 
slider = DirectSlider(pos = (0,-0.95,0.90), scale=0.5, range=(0,1), value=0, pageSize=0.005, command=slider_action)
                 
base.setBackgroundColor(0, 0, 0, 0)                   
base.cam.setPos(60, 0, 100) 
base.cam.lookAt( 60, 60, 0 )

add_worlds()

for world_name in worlds :
    worlds[world_name].start()

panda3D = Main()

run()



