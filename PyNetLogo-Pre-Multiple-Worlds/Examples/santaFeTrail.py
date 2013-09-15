#patch number 16x16, patch size 13x13

from Agents.Patch import *
from Agents.Turtle import *
from Interface import *
import Datas.Globals

file_path           = "C:\\Users\\Charles\\Desktop\\Santa Fe Trail\\"
which_behaviour     = "Look-ALR-1" #Koza, Look-ALR-1
max_steps            = 650

import sys
sys.path.append(file_path)
file_name = "Santa-Fe-Trail-Program-" + which_behaviour
file_behaviour = __import__(file_name)

# Set with slides and globals in NetLogo
food_colour         = colors["GREEN"]
eaten_food_colour   = colors["DARK_GREEN"]
trail_colour        = colors["BROWN"]
background_colour   = colors["LIGHT_GREEN"]
food_amount         = 89
steps               = 0
sensing_steps       = 0
food_eaten          = 0
ant_actions         = ""
init_actions        = False
actions             = ""   

def declaration():
    return 0

def setup_gobal_settings():
    return 0   

def add_food(self):
    self.pcolor = food_colour

def add_gap(self):
    self.pcolor = trail_colour

def setup_santa_fe_trail():
    ask(all("Patch"), [("set",("pcolor", background_colour))])
    
    x = 0
    y = 0
    file = open(file_path + "Santa-Fe-Trail.dat", "r")
    
    for line in file :
        for symbol in line :
            if symbol == "1" : ask(get_patch(x, y), [("add_food",())])
            if symbol == "0" : ask(get_patch(x, y), [("add_gap",())])
            x += 1       
        x = 0
        y += 1
          
    file.close()
    
def execute_behaviour():
    return 0
    '''
    file = open(file_name, "r")
    
    global ant_actions
    for line in file :
        ant_actions += line
    
    file.close()
    '''
    
    
def food(self):
    return self.pcolor == food_colour
    
def move(self):
    global food_eaten, steps
    
    if steps < max_steps and food_eaten < food_amount :
        self.forward(1)
        if self.patch.pcolor == food_colour :
            self.patch.pcolor = eaten_food_colour
            food_eaten +=1
        steps += 1


def turn_left(self):
    global steps
    if steps < max_steps and food_eaten < food_amount :
        self.left(90)
        steps += 1  

def turn_right(self):
    global steps
    if steps < max_steps and food_eaten < food_amount :
        self.right(90)
        steps += 1        

def food_ahead(self):
    global sensing_steps
    sensing_steps += 1 
    return (self.patch_ahead(1)).food()

def food_on_my_left(self):
    global sensing_steps
    sensing_steps += 1
    return (self.patch_right_and_ahead(90, 1)).food()    

def food_on_my_right(self):
    global sensing_steps
    sensing_steps += 1
    return (self.patch_left_and_ahead(90, 1)).food()

def food_ALR(self):
    global sensing_steps
    sensing_steps += 1
    if (self.patch_ahead(1)).food() :
        return "ahead"
    if (self.patch_left_and_ahead(90, 1)).food() :
        return "turn_left"
    if (self.patch_right_and_ahead(90, 1)).food() :
        return "turn_right"
    return "ahead"

def food_direction(self):
    global sensing_steps, steps
    sensing_steps += 1
    if (self.patch_ahead(1)).food() :
        return 0
    if (self.patch_left_and_ahead(90, 1)).food() :
        steps += 1
        return -90
    if (self.patch_right_and_ahead(90, 1)).food() :
        steps += 1
        return 90
    return 0             
                               
def setup():
    clear_all()
    
    setup_gobal_settings()
    setup_santa_fe_trail()
    execute_behaviour()
    
    create("Turtle", 1, 
         [
         ("set",("size", 5)),
         ("set", ("color", colors["BLACK"])),
         ("set", ("xcor", -15.5)),
         ("set", ("ycor", 15.5)),
         ("set", ("heading", 0)),         
         ("set", ("pen_mode", True))
         ]
     )
        
def go():
    if steps >= max_steps           : stop()
    if food_eaten >= food_amount    : stop()
    
    global init_actions
    if not init_actions :
        init_actions = True
        
    ask(all("Turtle"), [("actions",())])
    if Datas.Globals.boolean_stop == True :
        print ("Motor steps : ", steps)
        print ("sensing steps : ", sensing_steps)
        print ("Total steps : ", steps + sensing_steps)
        print ("Food eaten : ", food_eaten)


turtles_methods_dictionnary = {"actions": file_behaviour.actions, "move":move, "turn_left":turn_left, "turn_right":turn_right, "food_ahead":food_ahead, "food_on_my_left":food_on_my_left, "food_on_my_right":food_on_my_right, "food_ALR":food_ALR, "food_direction":food_direction}
patches_methods_dictionnary = {"add_food": add_food, "add_gap": add_gap, "food":food}