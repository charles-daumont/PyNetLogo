# patchSize = 9 patchNumber = 50

from Agents.Patch import *
from Agents.Turtle import *
from Interface import *

# Set with slides in NetLogo
grass_regrow_time       = 30
initial_number_sheep    = 100
sheep_gain_from_food    = 4
sheep_reproduce         = 4
initial_number_wolves   = 50
wolf_gain_from_food     = 20
wolf_reproduce          = 5

def add_worlds():
    create_world(9 ,9 , 25, 25)

def declaration():
    breed("Wolf")
    breed("Sheep")
    own("Turtle", "energy")
    own("Patch", "countdown")

# create a turtle and set its initial location and modulus
def setup():
    clear_all()
    ask(all("Patch"), [("set", ("pcolor", colors["GREEN"])), ("set", ("countdown", grass_regrow_time, "random"))] )
    
    create("Sheep", initial_number_sheep,
           [
            ("set", ("color", colors["WHITE"])),
            ("set", ("size", 5)),
            ("set", ("energy", 2*sheep_gain_from_food, "random")),
            ("set", ("xcor", 60, "random")),
            ("set", ("ycor", 60, "random"))
           ]
    )

    create("Wolf", initial_number_wolves,
           [
            ("set", ("color", colors["BLACK"])),
            ("set", ("size", 7)),
            ("set", ("energy", 2*wolf_gain_from_food, "random")),
            ("set", ("xcor", 60, "random")),
            ("set", ("ycor", 60, "random"))
           ]
    )
    
    reset_ticks()

def move(self):
    self.right(rand()*50)
    self.left(rand()*50)
    self.forward(1)

def eat_grass(self):
    
    self.set("energy", self.energy -1)
    if self.patch.pcolor == colors["GREEN"] :
        self.patch.set("pcolor", colors["BROWN"])
        self.set("energy", self.energy + sheep_gain_from_food)

def reproduce_sheep(self):
    if rand()*100 < sheep_reproduce :
        self.set("energy", self.energy/2)
        self.hatch(1, [("right",(rand()*360)), ("forward",(1))])

def reproduce_wolf(self):
    if rand()*100 < wolf_reproduce :
        self.set("energy", self.energy/2)
        self.hatch(1, [("right",(rand()*360)), ("forward",(1))])

def catch_sheep(self):
    
    self.set("energy", self.energy -1)
    sheep_here = self.here("Sheep")
    prey = one_of("Sheep", sheep_here)
    if prey != None :
        prey.die()
        self.set("energy", self.energy + wolf_gain_from_food)       

def death(self):
    if self.energy < 0 :
        self.die()

def grow_grass(self):
    if self.pcolor == colors["BROWN"] :
        if self.countdown <= 0 :
            self.set("pcolor",colors["GREEN"])
            self.set("countdown", grass_regrow_time)
        else :
            self.set("countdown", self.countdown - 1)


def go():
    
    ask(all("Sheep"), [("move",()), ("eat_grass",()),("death",()), ("reproduce_sheep",())])
    ask(all("Wolf"), [("move",()), ("catch_sheep",()), ("death",()), ("reproduce_wolf",())])
    ask(all("Patch"), [("grow_grass",())])


turtles_methods_dictionary = {"move":move, "eat_grass":eat_grass, "reproduce_sheep":reproduce_sheep, "reproduce_wolf":reproduce_wolf, "death":death, "catch_sheep":catch_sheep}
patches_methods_dictionary = {"grow_grass": grow_grass}

