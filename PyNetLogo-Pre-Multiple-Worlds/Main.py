import pygame
from pygame.locals  import *

import Datas.Globals
from Datas.Globals  import *
from UserCode       import *
from Interface      import *
    

######
#
# START MAIN
#
######

# Set up pygame
pygame.init()

done = False
forever = False

# Set up the window
window_surface = pygame.display.set_mode((max_pxcor, max_pycor), 0, 32)
pygame.display.set_caption('PyNetLogo')

# We have 3 surfaces, patches, lines, turtles
patches_surface = pygame.Surface((max_pxcor,max_pycor))

lines_surface = pygame.Surface((max_pxcor, max_pycor))
lines_surface.fill((1,1,1))
lines_surface.set_colorkey((1,1,1))

clock = pygame.time.Clock()

declaration()
add_methods("turtle", turtles_methods_dictionary)
add_methods("patch", patches_methods_dictionary)
setup()

# Display loop   
while done == False :
    
    for event in pygame.event.get():                # User did something
        if event.type == pygame.QUIT:               # If user clicked close
            done = True                             # Flag that we are done so we exit this loop
        if event.type == pygame.KEYDOWN:
            if event.key == K_UP:
                go()
            if event.key == K_DOWN:
                setup()
            if event.key == K_KP_PLUS:
                Datas.Globals.maxFPS += 5
            if event.key == K_KP_MINUS:
                Datas.Globals.maxFPS -= 5
           
    forever = True
    
    i = 0
    
    while forever == True and Datas.Globals.boolean_stop == False:
        clock.tick()
        go()
        i += 1
        loop_duration = clock.tick()
        if i*loop_duration > Datas.Globals.maxFPS :
            forever = False   
    
    # Displaying patches
    for patch in world.updated_patches :
        patch.draw(patches_surface)  
    window_surface.blit(patches_surface,(0,0))    
    world.updated_patches = list()   
            
    # Displaying lines
    for line in world.updated_lines :
        pygame.draw.line(lines_surface, line[0].color, line[1], line[2], line[0].pen_size)
    window_surface.blit(lines_surface,(0,0))
    world.updated_lines = list()
       
    # Displaying turtles
    for turtle_type in world.turtles_dictionary :
        for turtle in world.turtles_dictionary[turtle_type] :
            if not turtle.hidden :
                turtle.draw(window_surface)

    
    # Limit to 30 frames per second            
    #clock.tick(10000)
    #print(clock.get_fps())
    pygame.display.update()            
                
pygame.quit()

######
#
# END MAIN
#
######
