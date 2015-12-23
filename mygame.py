import game_framework
import platform
import title_state
import os
if platform.architecture()[0] == '32bit':
 os.environ["PYSDL2_DLL_PATH"] = "./SDL2/x86"
else:
 os.environ["PYSDL2_DLL_PATH"] = "./SDL2/x64"



game_framework.run(title_state)

