#patch number 60x60, patch size 4x4

from Agents.Patch import *
from Agents.Turtle import *
from Interface import *


#Globals
scale = 0.25
population = 1

#Declare own & breed
def declaration():
    own("Turtle", "flockmates")
    own("Turtle", "nearest_neighbor")       
                                 
def setup():
    clear_all()
    create("Turtle", population,
           [                  
            ("set", ("xcor", 41, "random")),
            ("set", ("ycor", 41, "random")),
            ("set", ("zcor", 25, "random")),
            ("set", ("heading", 360, "random")),
            ("set", ("pitch", 360, "random")),
            ("set", ("roll", 360, "random")),
           ]
    )   

def report_average_pitch_towards_flockmates(self):
    return 
to-report average-pitch-towards-flockmates  ;; turtle procedure
  report mean [0 - (towards-pitch myself)] of flockmates
end

def turn_towards(self, new_heading, max_turn):
    self.turn_at_most(new_heading, max_turn * scale)

def turn_away(self, new_heading, max_turn):
    self.turn_at_most(new_heading, max_turn * scale)
        
def pitch_towards(self, new_pitch, max_turn):
    self.pitch_at_most(new_pitch, max_turn * scale)

def pitch_away(self, new_pitch, max_turn):
    self.pitch_at_most(new_pitch, max_turn * scale)

def turn_at_most(self, turn, max_turn):
    if math.fabs(turn) > max_turn :
        if turn > 0 : self.right(max_turn)   
        else        : self.left(max_turn)    
    else :
        self.right(turn)

def pitch_at_most(self, turn, max_turn):
    
    if math.fabs(turn) > max_turn :
        if turn > 0 : self.tilt_up(max_turn)   
        else        : self.tilt_down(max_turn)    
    else :
        self.tilt_up(turn)
    
def go():
    ask(all("Turtle"), [("flock",())])
    ask(all("Turtles"), [("repeat", (5, [("forward",(scale/2))] ))])

turtles_methods_dictionary = {}
patches_methods_dictionary = {}