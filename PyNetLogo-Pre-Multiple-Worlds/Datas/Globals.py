from World import World

# Variable creation
global max_px
global max_py
global controller
global max_pxcor
global max_pycor
global maxFPS
global ticks
global class_dictionnary
global world

# Variable initialization
max_px              = 25
max_py              = 25
row_patches_width   = 9
col_patches_width   = 9
world               = World([row_patches_width, col_patches_width], [max_px*2 + 1, max_py*2 + 1])
max_pxcor           = world.patches_number[0] * world.patches_size[0]
max_pycor           = world.patches_number[1] * world.patches_size[1]
maxFPS              = 30
ticks               = 0
boolean_stop = False
