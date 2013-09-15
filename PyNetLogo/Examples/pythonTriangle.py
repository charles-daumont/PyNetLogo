from Agents.Patch import *
from Agents.Turtle import *
from Interface import *

def add_worlds():
    create_world(12 ,12 , 16, 16)

def declaration():
    own("Turtle", "modulus")

# create a turtle and set its initial location and modulus
def setup():
    clear_all()
    create("Turtle", 1, 
         [
         ("set",("heading", 0)),
         ("set", ("xcor", 0)),
         ("set", ("ycor", 0)),
         ("set", ("modulus", 8)),
         ("set", ("pen_mode", True))
         ]
     )
    reset_ticks()

# ask the turtles to go forward by modulus, create a new turtle to
# draw the next iteration of sierpinski's tree, and return to its place
def grow(self):

    self.hatch (1, 
        [
        ("forward", (self.modulus)),
        ("set", ("modulus", 0.5 * self.modulus))
        ]
    )

# draw the sierpinski tree
def go():
  
    ask(all("Turtle"),
        [
         ("repeat", (3, [("grow",()), ("right",(120))] )),
         ("die", ())
        ] 
    )

turtles_methods_dictionary = {"grow":grow}
patches_methods_dictionary = {}

# nbPatches = 34 patchSize = 12