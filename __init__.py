import sys
import importlib

bl_info = {
    "name": "Geometry Cleanup",
    "author": "Kharichev Kirill",
    "description": "",
    "blender": (2, 80, 0),
    "version": (0, 0, 1),
    "location": "",
    "warning": "",
    "category": "Generic",
}

modules_names = ['menus', 'ops', 'utils']


modules_full_names = {}
for current_module_name in modules_names:
	modules_full_names[current_module_name] = ('{}.{}'.format(__name__, current_module_name))
	
for current_module_full_name in modules_full_names.values():
	if current_module_full_name in sys.modules:
		importlib.reload(sys.modules[current_module_full_name])
	else:
		globals()[current_module_full_name] = importlib.import_module(current_module_full_name)
		setattr(globals()[current_module_full_name], 'modulesNames', modules_full_names)
     
def register():
	
    for current_module_name in modules_full_names.values():
        if current_module_name in sys.modules:
            if hasattr(sys.modules[current_module_name], 'register'):
                sys.modules[current_module_name].register()

def unregister():
      
    for current_module_name in modules_full_names.values():
	    if current_module_name in sys.modules:
		    if hasattr(sys.modules[current_module_name], 'unregister'):
			    sys.modules[current_module_name].unregister()