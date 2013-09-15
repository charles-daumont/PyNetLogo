###
# Imports
###
# Pygame
import pygame
# PyNetLogo files
import Datas.Globals
from Datas.Globals import worlds, worlds_locks, worlds_display_position
from User_code.Add_worlds import add_worlds    

######
#
# START MAIN
#
######

# Set up pygame
pygame.init()

add_worlds()

done = False
worlds_surfaces = {}
   
window_surface = pygame.display.set_mode((Datas.Globals.max_x, Datas.Globals.max_y), 0, 32)
pygame.display.set_caption("PyNetLogo")

for world_name in worlds :
    worlds_surfaces[world_name] = {}
    max_pxcor = worlds[world_name].patches_size[0] * worlds[world_name].patches_number[0]
    max_pycor = worlds[world_name].patches_size[1] * worlds[world_name].patches_number[1]
    
    # 3 surfaces, turtles, patches, lines 
    worlds_surfaces[world_name]["turtles_surface"] = pygame.Surface((max_pxcor,max_pycor))
    worlds_surfaces[world_name]["turtles_surface"].fill((1,1,1))
    worlds_surfaces[world_name]["turtles_surface"].set_colorkey((1,1,1))
    
    worlds_surfaces[world_name]["patches_surface"] = pygame.Surface((max_pxcor,max_pycor))
    worlds_surfaces[world_name]["patches_surface"].fill((1,1,1))
    worlds_surfaces[world_name]["patches_surface"].set_colorkey((1,1,1))
    
    worlds_surfaces[world_name]["lines_surface"] = pygame.Surface((max_pxcor, max_pycor))
    worlds_surfaces[world_name]["lines_surface"].fill((1,1,1))
    worlds_surfaces[world_name]["lines_surface"].set_colorkey((1,1,1))

clock = pygame.time.Clock()

for world_name in worlds :
    worlds[world_name].start()


# Display loop   
while done == False :
    
    for event in pygame.event.get():                # User did something
        if event.type == pygame.QUIT:               # If user clicked close
            done = True                             # Flag that we are done so we exit this loop
            for world_name in worlds :
                worlds[world_name].run_bool = False
    
    for lock in worlds_locks :
        worlds_locks[lock].acquire()
        
    # Displaying patches
    for world_name in worlds :
        x_display_position = worlds_display_position[worlds[world_name].id - 1]
        for patch in worlds[world_name].updated_patches :
            patch.draw(worlds_surfaces[world_name]["patches_surface"])  
        window_surface.blit(worlds_surfaces[world_name]["patches_surface"],(x_display_position,0))    
        worlds[world_name].updated_patches = list()   
                
        # Displaying lines
        for line in worlds[world_name].updated_lines :
            pygame.draw.line(worlds_surfaces[world_name]["lines_surface"], line[0].color, line[1], line[2], line[0].pen_size)
        window_surface.blit(worlds_surfaces[world_name]["lines_surface"],(x_display_position,0))
        worlds[world_name].updated_lines = list()
 
        # Displaying turtles
        for turtle_type in worlds[world_name].turtles_dictionary :
            for turtle in worlds[world_name].turtles_dictionary[turtle_type] :
                if not turtle.hidden :
                    turtle.draw(worlds_surfaces[world_name]["turtles_surface"])

        window_surface.blit(worlds_surfaces[world_name]["turtles_surface"],(x_display_position,0))
        worlds_surfaces[world_name]["turtles_surface"] = pygame.Surface((max_pxcor,max_pycor))
        worlds_surfaces[world_name]["turtles_surface"].fill((1,1,1))
        worlds_surfaces[world_name]["turtles_surface"].set_colorkey((1,1,1))
        
    for lock in worlds_locks :
        worlds_locks[lock].release()
                
    # Limit to 30 frames per second            
    clock.tick(30) 
    pygame.display.update()            
               
pygame.quit()

######
#
# END MAIN
#
######
