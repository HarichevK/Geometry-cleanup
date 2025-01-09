import bpy
import utils


class CleanUVMapsOperator(bpy.types.Operator):

    bl_idname = "object.clean_uv_maps"
    bl_label = "Clean UV Maps"

    def execute(self, context):
        
        messages = []

        if (len(bpy.context.selected_objects) == 0):
            messages.append("No objects selected")
        else:
            messages.append("Success!")

        for object in bpy.context.selected_objects:

            if (object.type != 'MESH'):
                messages.append(f"object {object.name} is not a mesh")
                continue    #if not mesh skip

            bpy.context.view_layer.objects.active = object

            if len(object.data.uv_layers) == 0: #mesh is not having any UV
                messages.append(f"! Mesh {object.name} dont have any UV! Should be added manually")    

            elif (len(object.data.uv_layers) > 1): #mesh have more then 1 UV set
                
                object.data.uv_layers[0].name = "map1"

                messages.append(f"Mesh {object.name} have more than 1 uv channel!")
                while (len(object.data.uv_layers) > 1):
                    object.data.uv_layers.active_index = len(object.data.uv_layers) - 1
                    bpy.ops.mesh.uv_texture_remove()


            else: #mesh have only 1 UV set
                object.data.uv_layers[0].name = "map1"


        utils.ShowMessageBox(messages, "UV maps report")
        return {"FINISHED"}
    
class CleanVertexColorsOperator(bpy.types.Operator):
    bl_idname = "object.clean_vertex_colors"
    bl_label = "Clean vertex colors"

    def execute(self, context):

        messages = []

        if (len(bpy.context.selected_objects) == 0):
            messages.append("No objects selected")
        else:
            messages.append("Success!")


        for object in bpy.context.selected_objects:

            if (object.type != 'MESH'): #if not mesh skip
                messages.append(f"object {object.name} is not a mesh")
                continue    
            
            color_attributes_to_remove = []

            bpy.context.view_layer.objects.active = object

            while (len(object.data.color_attributes) != 0):
                bpy.ops.geometry.color_attribute_remove()
                messages.append(f"{object.name}: removed vertex color")

        utils.ShowMessageBox(messages, "Vertex color removal report")

        return {"FINISHED"}

class TriangulateNgons(bpy.types.Operator):
    bl_idname = 'geometry_clenup.triangulate_ngons'
    bl_label = 'Triangulate N-gons'

    def execute(self, context):

        for object in bpy.context.selected_objects:

            if (object.type != 'MESH'): #if not mesh skip
                continue    

            bpy.context.view_layer.objects.active = object
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_face_by_sides(number=4, type='GREATER')
            bpy.ops.mesh.quads_convert_to_tris()

        bpy.ops.object.mode_set(mode='OBJECT')

        return {'FINISHED'}
    
classes = (
    CleanUVMapsOperator,
    CleanVertexColorsOperator,
    TriangulateNgons
)

def register():
	for cls in classes:
		bpy.utils.register_class(cls)


def unregister():
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)