
This Git repository contains 3 versions of PyNetLogo.
	- one world : fastest version but does not allow the multiple world creation. (to use if only one world is needed)
	- multiple worlds : slower than the version above, but allows the multiple world creation.
	- 3D world : 3D PyNetLogo version.

PREREQUISITE OF USE	:
	- install the latest version of Python 3.3.2 	: http://www.python.org/getit/
	- install the latest version of Pygame 1.9.2 	: http://www.pygame.org/
	- install the latest version of Panda3D 1.7.2 	: https://www.panda3d.org/download.php?sdk&version=1.7.2

###                ##
# ONE WORLD VERSION #
###                ##
	
HOW TO USE IT :
	- edit the UserCode.py file, need to contains at least the code in Empty_UserCode.py. You can find several examples in the Examples directory.
		- when you add a new agent method, do not forget to add it in the correct dictionnary at the end of the file. 
	- edit the Datas/Globals.py file with the correct maximum coordinates values and patches size.
	- launch the Main.py file.
	
###                      ##
# MULTIPLE WORLDS VERSION #
###                      ##
	
HOW TO USE IT :
	- edit the User_code/world_1-2.py files, need to contains at least the code in Empty_World.py. You can find several examples in the Examples directory.
		- when you add a new agent method, do not forget to add it in the correct dictionnary at the end of the file. 
	- edit the User_code/Add_worlds.py file with the correct maximum coordinates values and patches size.
	- launch the Main.py file.
	
###         ##
# 3D VERSION #
###         ##
	
HOW TO USE IT :
	- edit the User_code/world_1-2.py files, need to contains at least the code in Empty_World.py. You can find several examples in the Examples directory.
		- when you add a new agent method, do not forget to add it in the correct dictionnary at the end of the file. 
	- edit the User_code/Add_worlds.py file with the correct maximum coordinates values and patches size.
	- launch the Main.py file.

RESSOURCES :
	- free 3D models : http://alice.org/pandagallery/
	- Panda3D tutorials : http://www.panda3d.org/manual/index.php/Main_Page