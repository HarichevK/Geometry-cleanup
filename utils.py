import bpy
import bmesh

def ShowMessageBox(messages = [], title = "Message Box", icon = 'INFO'):

    def draw(self, context):
        
        for text in messages:
            self.layout.label(text = text)

    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

def GetUVMapsProblems(obj: bpy.types.Object) -> list[str]:
    
    uv_maps_problems = []

    bm = bmesh.new()
    bm.from_mesh(obj.data)

    if (obj.data.uv_layers.__len__() > 0):
            if (obj.data.uv_layers[0].name != "map1"):
                    uv_maps_problems.append(f"{obj.name}: incorrect UV name")
            if (len(obj.data.uv_layers) > 1):
                uv_maps_problems.append(f"{obj.name}: More then 1 UV map")

            for edge in bm.edges:
                if not edge.smooth and not edge.seam:
                    uv_maps_problems.append(f"{obj.name}: has sharp edge wihout seam")
    else:
        uv_maps_problems.append(f"{obj.name}: no UV maps. Should be added manually")

    return uv_maps_problems