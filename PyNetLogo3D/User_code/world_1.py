#patch number 60x60, patch size 4x4

from Agents.Patch import *
from Agents.Turtle import *
from Interface import *

row_patches_width   = 4
col_patches_width   = 4
max_px              = 60
max_py              = 60

# Set with slides in NetLogo
turtle_behaviour = "Hand On The Wall" # Hand On The Wall, Random Forward 2
maze_being_searched = "Hampton Court Maze" # Empty Maze, Hampton Court Maze, Chevening House Maze
left_cols = 40
right_cols = 40
below_rows = 40
above_rows = 40
entrance_cols = 3
pen_down = True

def declaration():
    breed("Maze")
    own("Turtle", "direction")
    own("Maze", ["start_x", "start_y", "start_width", 
                 "entrance_x", "entrance_y", "entrance_width", 
                 "goal_type", "goal_x", "goal_y", "goal_width"]
        )

def setup_empty_maze(self):

    if self.x >= - left_cols - entrance_cols and self.x <= - entrance_cols and self.y == -below_rows :
        self.set("texture", "grass") # draws bottom left horizontal wall in grass

    if self.x >= entrance_cols and self.x <= right_cols + entrance_cols and self.y == -below_rows :
        self.set("texture", "grass") # draws top right horizontal wall in grass

    if self.x >= - left_cols - entrance_cols and self.x <= - entrance_cols and self.y == above_rows :
        self.set("texture", "grass") # draws top left horizontal wall in grass

    if self.x >= entrance_cols and self.x <= right_cols + entrance_cols and self.y == above_rows :
        self.set("texture", "grass") # draws top right horizontal wall in grass

    if self.x == - left_cols - entrance_cols and self.y >= -below_rows and self.y <= above_rows :
        self.set("texture", "grass") # draws left vertical wall in grass
 
    if self.x == right_cols + entrance_cols and self.y >= -below_rows and self.y <= above_rows :
        self.set("texture", "grass") # draws right vertical wall in grass      

def setup_row(self, row, texture, segments):

    for segment in segments :
        if (self.y == row * row_patches_width) and (self.x >= col_patches_width * segment[0]) and (self.x <= col_patches_width * segment[1]):
            self.set("texture", texture)

def setup_col(self, col, texture, segments):
    
    for segment in segments :
        if (self.x == col * col_patches_width) and (self.y >= row_patches_width * segment[0]) and (self.y <= row_patches_width * segment[1]):
            self.set("texture", texture)


def setup_hampton_court_maze(self):
    
    self.setup_row(5, "grass", [[-9, 10]])
    self.setup_row(4, "grass", [[-8, -5], [-3, -1], [0, 3], [5, 9]])
    self.setup_row(3, "grass", [[-7, -4], [-2, 2], [4, 8]])
    self.setup_row(2, "grass", [[-6, -1], [1, 4], [5, 7]])
    self.setup_row(1, "grass", [[-3, 3], [8, 9]])
    self.setup_row(0, "grass", [[-8, -7], [9, 10]])
    self.setup_row(-1, "grass", [[-9, -8]])
    self.setup_row(-2, "grass", [[-8, -7], [-3, 0], [1, 3]])
    self.setup_row(-3, "grass", [[-4, -1], [2, 4], [6, 8]]) 
    self.setup_row(-4, "grass", [[-7, -1], [1, 9]]) 
    self.setup_row(-5, "grass", [[-8, 10]]) 
    self.setup_row(-6, "grass", [[-9, 0], [1, 10]])  

    self.setup_col(10, "grass", [[-6, 5]])
    self.setup_col(9, "grass", [[-4, -1], [1, 4]])
    self.setup_col(8, "grass", [[-3, 1], [2, 3]])
    self.setup_col(7, "grass", [[-2, 2]])
    self.setup_col(6, "grass", [[-4, 1]])
    self.setup_col(5, "grass", [[-3, 2]])
    self.setup_col(4, "grass", [[-3, 2], [3, 5]]) 
    self.setup_col(3, "grass", [[-2, 1], [2, 4]])  
    self.setup_col(1, "grass", [[-4, -2]]) 
    self.setup_col(0, "grass", [[-5, -2], [1, 3]]) 
    self.setup_col(-1, "grass", [[-4, -3], [4, 5]])  
    self.setup_col(-3, "grass", [[-2, 1], [2, 4]])                
    self.setup_col(-4, "grass", [[-3, 2], [3, 5]]) 
    self.setup_col(-5, "grass", [[-4, 1]])
    self.setup_col(-6, "grass", [[-3, 2]]) 
    self.setup_col(-7, "grass", [[-4, -3], [-2, 0], [1, 3]])  
    self.setup_col(-8, "grass", [[-5, -2], [0, 4]]) 
    self.setup_col(-9, "grass", [[-6, 5]])  

def setup_chevening_house_maze(self):
    
    self.setup_row(12, "grass", [[-11, 12]])  
    self.setup_row(11, "grass", [[-10, 11]])
    self.setup_row(10, "grass", [[-9, 10]])
    self.setup_row(9, "grass", [[-8, 0], [1, 9]])
    self.setup_row(8, "grass", [[-7, -1], [2, 8]])
    self.setup_row(7, "grass", [[-6, 0], [1, 7]]) 
    self.setup_row(6, "grass", [[-5, 0], [1, 6]]) 
    self.setup_row(5, "grass", [[-4, -1], [2, 5]])
    self.setup_row(4, "grass", [[-3, 0,], [1, 4]])
    self.setup_row(3, "grass", [[-2, 3]]) 
    self.setup_row(2, "grass", [[-1, 2]]) 
    self.setup_row(1, "grass", [[-9, -5], [-4, -2], [3, 5], [6, 8], [10, 11]])
    self.setup_row(0, "grass", [[-9, -7], [3, 5], [6, 10]]) 
    self.setup_row(-1, "grass", [[-1, 0], [1, 2], [7, 9]])
    self.setup_row(-2, "grass", [[-2, 0], [1, 3]])
    self.setup_row(-3, "grass", [[-3, -1], [1, 4]])
    self.setup_row(-4, "grass", [[-4, -2], [2, 5]])
    self.setup_row(-5, "grass", [[-5, -3], [2, 6]]) 
    self.setup_row(-6, "grass", [[-6, -3], [1, 7]]) 
    self.setup_row(-7, "grass", [[-7, -2], [0, 8]]) 
    self.setup_row(-8, "grass", [[-8, 1], [3, 9]])
    self.setup_row(-9, "grass", [[-9, 0], [3, 10]]) 
    self.setup_row(-10, "grass", [[-10, -1], [2, 11]])  
    self.setup_row(-11, "grass", [[-11, 0], [1, 12]])
    
    self.setup_col(12, "grass", [[-11, 12]])
    self.setup_col(11, "grass", [[-10, 1], [2, 11]])
    self.setup_col(10, "grass", [[-9, 0], [1, 10]]) 
    self.setup_col(9, "grass", [[-8, -1], [0, 9]])  
    self.setup_col(8, "grass", [[-7, -2,], [1, 8]])
    self.setup_col(7, "grass", [[-6, -1], [2, 7]]) 
    self.setup_col(6, "grass", [[-5, 0], [1, 6]]) 
    self.setup_col(5, "grass", [[-4, 0], [1, 5]]) 
    self.setup_col(4, "grass", [[-3, -1], [2, 4]])
    self.setup_col(3, "grass", [[-2, 0], [1, 3]]) 
    self.setup_col(2, "grass", [[-10, -7], [-1, 2]])
    self.setup_col(1, "grass", [[-11, -8], [-6, -1], [4, 6], [7, 9]])
    self.setup_col(0, "grass", [[-11, -9], [-7, -1], [4, 6], [7, 9]])
    self.setup_col(-1, "grass", [[-8, -3], [-1, 2]])
    self.setup_col(-2, "grass", [[-7, -4], [-2, 0], [1, 3]])
    self.setup_col(-3, "grass", [[-3, 1], [2, 4]])
    self.setup_col(-4, "grass", [[-4, 0], [1, 5]])
    self.setup_col(-5, "grass", [[-5, 6]]) 
    self.setup_col(-6, "grass", [[-6, 0], [2, 7]])
    self.setup_col(-7, "grass", [[-7, 0], [1, 8]]) 
    self.setup_col(-8, "grass", [[-8, -1], [2, 9]]) 
    self.setup_col(-9, "grass", [[-9, 0], [1, 10]]) 
    self.setup_col(-10, "grass", [[-10, 11]]) 
    self.setup_col(-11, "grass", [[-11, 12]])  



def close_door(self):
    xpos = get_from("Maze", 0, "entrance_x")
    if (self.x >= xpos) and (self.x <= xpos + get_from("Maze", 0, "entrance_width")) and (self.y == get_from("Maze", 0, "entrance_y")) :
        self.set("texture", "dirt") # draws right vertical wall in grass

def walk(self):
    xpos = get_from("Maze", 0, "goal_x")
    if (self.xcor >= xpos) and (self.xcor <= xpos + get_from("Maze", 0, "goal_width")) and (self.ycor == get_from("Maze", 0, "goal_y")) :
        if get_from("Maze", 0, "goal_type") == "Exit" :
            print("Found the exit !")
        else :
            print("Made it to the center of the maze !")
        stop()

    if (turtle_behaviour == "Hand On The Wall") : self.behaviour_wall_following()
    if (turtle_behaviour == "Random Forward 0") : self.behaviour_random_forward_0()
    if (turtle_behaviour == "Random Forward 1") : self.behaviour_random_forward_1()
    if (turtle_behaviour == "Random Forward 2") : self.behaviour_random_forward_2()
    
               
def report_wall(self, angle, distance):
    patch = self.patch_right_and_ahead(angle, distance)
    return (patch.texture == "grass" or patch.texture == "dirt")

def behaviour_wall_following(self):
    #classic 'hand-on-the-wall' behaviour
    if (not self.report_wall(-90*self.direction, 1)) and (self.report_wall(-135*self.direction, math.sqrt(2))) :
        self.right(-90*self.direction)
    while self.report_wall(0, 1) : self.left(-90*self.direction)

    self.forward(1)

def behaviour_random_forward_0(self):
    if self.report_wall(0, 1) :
        if self.report_wall(-90, 1) :
            self.left(-90)
        elif self.report_wall(-270, 1) :
            self.right(-90)
        elif rand()*2 > 1 :
            self.left(-90)
        else :
            self.right(-90)
    
    self.forward(1)

def behaviour_random_forward_1(self):
    if self.report_wall(0, 1) :
        self.backward(1)
    else :
        r = rand(2)
        if r == 0 :
            if not self.report_wall(-90, 1) :
                self.right(-90)
                self.forward(1)
        elif r == 1 :
            if not self.report_wall(-270, 1) :
                self.left(-90)
                self.forward(1)
        else :
            f = rand(5)
            while (not self.report_wall(0, 1) and f > 0) :
                self.forward(1)
                f = f - 1

def behaviour_random_forward_2(self):
    
    r = rand(3)
    if r == 0 :
        if not self.report_wall(-90, 1) :
            self.right(-90)
            self.forward(1)
    elif r == 1 :
        if not self.report_wall(-270, 1) :
            self.left(-90)
            self.forward(1)
    else :
        if not self.report_wall(0, 1) :
            self.forward(1)        
                                 
def setup():
    clear_all()
    if maze_being_searched == "Empty Maze" :
        ask(all("Patch"), [("setup_empty_maze",())])
        create("Maze", 1,
           [
            ("set", ("hidden", True)),
            ("set", ("start_x", 0)),
            ("set", ("start_y", -below_rows -5)),
            ("set", ("start_width", 6)),
            ("set", ("entrance_x", - entrance_cols + 1)),
            ("set", ("entrance_y", - below_rows)),
            ("set", ("entrance_width", 2 * entrance_cols - 2)),
            ("set", ("goal_type", "Exit")),
            ("set", ("goal_x", - entrance_cols + 1)),
            ("set", ("goal_y", above_rows)),
            ("set", ("goal_width", 2 * entrance_cols - 2))
           ]
        )
        
    if maze_being_searched == "Hampton Court Maze" :
        ask(all("Patch"), [("setup_hampton_court_maze",())])
        create("Maze", 1,
            [
             ("set", ("hidden", True)),
             ("set", ("start_x", col_patches_width /2)),
             ("set", ("start_y", -row_patches_width * 7 -1)),
             ("set", ("start_width", row_patches_width + 2)),
             ("set", ("entrance_x", 0)),
             ("set", ("entrance_y", - row_patches_width * 6)),
             ("set", ("entrance_width", col_patches_width)),
             ("set", ("goal_type", "Centre")),
             ("set", ("goal_x", 0)),
             ("set", ("goal_y", -2 * row_patches_width)),
             ("set", ("goal_width", col_patches_width))
            ]
         )
        
    if maze_being_searched == "Chevening House Maze" :
            ask(all("Patch"), [("setup_chevening_house_maze",())])
            create("Maze", 1,
                [
                 ("set", ("hidden", True)),
                 ("set", ("start_x", col_patches_width /2)),
                 ("set", ("start_y", -row_patches_width * 12)),
                 ("set", ("start_width", row_patches_width + 2)),
                 ("set", ("entrance_x", 1)),
                 ("set", ("entrance_y", - row_patches_width * 11)),
                 ("set", ("entrance_width", col_patches_width -2)),
                 ("set", ("goal_type", "Centre")),
                 ("set", ("goal_x", 1)),
                 ("set", ("goal_y", -row_patches_width)),
                 ("set", ("goal_width", col_patches_width - 2))
                ]
             )
             
    create("Turtle", 1,
           [
            ("set", ("pen_size", 2)),                     
            ("set", ("xcor", get_from("Maze", 0, "start_x"))),
            ("set", ("ycor", get_from("Maze", 0, "start_y"))),
            ("set", ("pen_mode", pen_down)),
            ("set", ("heading", -90)),
            ("repeat", (get_from("Maze", 0, "start_width"), [("forward",(1))] )),
            ("set", ("direction", 1)),
           ]
    )

    if not maze_being_searched == "Chevening House Maze" :
        if rand(2) == 1 :
            heading = 0
            direction = 1
        else :
            heading = 180
            direction = -1
        ask(all("Turtle"), [("set", ("heading", heading)), ("set", ("direction", direction)), ("forward", (2.5))])
    
    ask(all("Patch"), [("close_door",())])    

      
def go():
    ask(all("Turtle"), [("walk",())])


turtles_methods_dictionary = {"report_wall": report_wall, "behaviour_wall_following":behaviour_wall_following, "walk":walk, "behaviour_random_forward_0":behaviour_random_forward_0, "behaviour_random_forward_1":behaviour_random_forward_1, "behaviour_random_forward_2":behaviour_random_forward_2}
patches_methods_dictionary = {"setup_empty_maze": setup_empty_maze, "close_door":close_door, "setup_row":setup_row, "setup_col":setup_col, "setup_hampton_court_maze":setup_hampton_court_maze, "setup_chevening_house_maze":setup_chevening_house_maze}