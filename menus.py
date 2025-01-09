import bpy
from . import utils

def DrawProblems(layout, problems, text):

    if (len(problems) > 0):
        layout.label(text=f"{text} {len(problems)}", icon='ERROR')
        for problem in problems:
            layout.label(text=problem)
    else:
        layout.label(text="Everything good", icon='CHECKMARK')
    bl_label = "Geometry Cleanup"
    bl_idname = "OBJECT_MT_geometry_cleanup"

    def draw(self, context):
        layout = self.layout


        layout.menu(menu="view3d.uv_problems", text="UV problems",)
        layout.menu(menu="view3d.vertex_colors_problems", text="Vertex colors problems")
        layout.menu(menu="view3d.geometry_problems", text="Geometry problems")
        layout.menu(menu="view3d.materials_problems", text="Materials problems")


        layout.operator("object.clean_uv_maps")
        layout.operator("object.clean_vertex_colors")
        layout.operator("geometry_clenup.triangulate_ngons")

class UVProblemsMenu(bpy.types.Menu):
    bl_idname = "view3d.uv_problems"
    bl_label = "UV maps problems"

    def draw(self, context):
        layout = self.layout
        uv_maps_problems = []

        for obj in bpy.context.selected_objects:
            uv_maps_problems.append(utils.GetUVMapsProblems(obj=obj))

        DrawProblems(layout, uv_maps_problems, "UV MAPS problems")

class VertexColorsProblemsMenu(bpy.types.Menu):
    bl_idname = "view3d.vertex_colors_problems"
    bl_label = "Vertex colors problems"

    def draw(self, context):
        layout = self.layout

        vertex_colors_problems = []

        for obj in bpy.context.selected_objects:
            if (len(obj.data.color_attributes) != 0):
                vertex_colors_problems.append(f"{obj.name}: has vertex colors")

        DrawProblems(layout, vertex_colors_problems, "VERTEX COLORS problems")

class GeometryProblemsMenu(bpy.types.Menu):
    bl_idname = "view3d.geometry_problems"
    bl_label = "Geometry problems"

    def draw(self, context):
        layout = self.layout
        
        ngons_problems = []

        for obj in bpy.context.selected_objects:
            
            #Object type check
            if (obj.type != "MESH"):
                ngons_problems.append(f"{obj.name}: is not a mesh")
                continue
                
            ngons_amount = 0
            obj.data.update()

            #N-Gons calculatuon
            for polygon in obj.data.polygons:
                if (len(polygon.vertices) > 4):
                    ngons_amount += 1
            if (ngons_amount > 0):
                ngons_problems.append(f"{obj.name} has {ngons_amount} N-Gons")
            
        DrawProblems(layout, ngons_problems, "GEOMETRY problems")

class MaterialProblemsMenu(bpy.types.Menu):
    bl_idname = "view3d.materials_problems"
    bl_label = "Materials problems"

    def draw(self, context):
        layout = self.layout

        materials_problems = []

        for obj in bpy.context.selected_objects:

            if (len(obj.data.materials) > 1):
                materials_problems.append(f"{obj.name} has more then 1 material")

            for mat in obj.data.materials:
                if not mat.name.endswith("_mat"):
                    materials_problems.append(f"{obj.name} has incorrect material naming: {mat.name}")

        DrawProblems(layout, materials_problems, "MATERIALS problems")
                
class GeometryCleanupMenu(bpy.types.Menu):
    bl_label = "Geometry Cleanup"
    bl_idname = "OBJECT_MT_geometry_cleanup"

    def draw(self, context):
        layout = self.layout


        layout.menu(menu="view3d.uv_problems", text="UV problems",)
        layout.menu(menu="view3d.vertex_colors_problems", text="Vertex colors problems")
        layout.menu(menu="view3d.geometry_problems", text="Geometry problems")
        layout.menu(menu="view3d.materials_problems", text="Materials problems")


        layout.operator("object.clean_uv_maps")
        layout.operator("object.clean_vertex_colors")
        layout.operator("geometry_clenup.triangulate_ngons")

classes = (
    UVProblemsMenu,
    VertexColorsProblemsMenu,
    GeometryProblemsMenu,
    MaterialProblemsMenu,
    GeometryCleanupMenu
)

def register():
	for cls in classes:
		bpy.utils.register_class(cls)


def unregister():
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)