import bpy
import bmesh
import menus
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

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

def register():
    bpy.utils.register_class(CleanUVMapsOperator)
    bpy.utils.register_class(CleanVertexColorsOperator)
    bpy.utils.register_class(TriangulateNgons)

    bpy.utils.register_class(GeometryCleanupMenu)
    bpy.utils.register_class(UVProblemsMenu)
    bpy.utils.register_class(VertexColorsProblemsMenu)
    bpy.utils.register_class(GeometryProblemsMenu)
    bpy.utils.register_class(MaterialProblemsMenu)

def unregister():
    bpy.utils.unregister_class(CleanUVMapsOperator)
    bpy.utils.unregister_class(CleanVertexColorsOperator)
    bpy.utils.unregister_class(TriangulateNgons)

    bpy.utils.unregister_class(GeometryCleanupMenu)
    bpy.utils.unregister_class(UVProblemsMenu)
    bpy.utils.unregister_class(VertexColorsProblemsMenu)
    bpy.utils.unregister_class(GeometryProblemsMenu)
    bpy.utils.unregister_class(MaterialProblemsMenu)

def ShowMessageBox(messages = [], title = "Message Box", icon = 'INFO'):

    def draw(self, context):
        
        for text in messages:
            self.layout.label(text = text)

    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

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


        ShowMessageBox(messages, "UV maps report")
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

        ShowMessageBox(messages, "Vertex color removal report")

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

if __name__ == "__main__":

    register()