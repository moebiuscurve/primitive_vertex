import bpy
import bmesh

bl_info = {
  "name": "Primitive Vertex",
  'author': 'Naveen Kumar',
  'version': (1, 0),
  "blender": (2, 80, 0),
  "location": "View3D > Add > Mesh",
  "category": "Add Mesh"
}

class MESH_OT_primitive_vert_add(bpy.types.Operator):
    """Create object with single primitve vertex or add vertex to existing edit mesh"""
    bl_idname = "mesh.primitive_vert_add"
    bl_label = "Add primitive vertex"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        obj = context.object
        layer = context.view_layer
        collection = bpy.context.collection
        if (obj is not None and obj.type == 'MESH' and obj.data.is_editmode):
            mesh = obj.data
            bm = bmesh.from_edit_mesh(mesh)
            coords = scene.cursor.location - obj.matrix_world.translation
            v = bm.verts.new(coords)
            bmesh.update_edit_mesh(mesh, False, True)
        
        else:            
            mesh = bpy.data.meshes.new("Vert")
            mesh.vertices.add(1)
            
            for obj in scene.objects:
                obj.select_set(False)
                
            obj = bpy.data.objects.new("Vert", mesh)
            obj.location = scene.cursor.location

            #if bpy.data.collections['Collection'] is not None:
                #bpy.data.collections['Collection'].objects.link(obj)
            
            if collection is not None:
                collection.objects.link(obj)
            else:
                scene.collection.objects.link(obj)
            obj.select_set(True)
            layer.objects.active = obj
            layer.update()
        
        return {'FINISHED'}

def draw_func(self, context):
    layout = self.layout
    layout.operator(MESH_OT_primitive_vert_add.bl_idname, 
        text="Vertex", icon='DECORATE')

def register():
    bpy.utils.register_class(MESH_OT_primitive_vert_add)
    bpy.types.VIEW3D_MT_mesh_add.append(draw_func)


def unregister():
    bpy.utils.unregister_class(MESH_OT_primitive_vert_add)
    bpy.types.VIEW3D_MT_mesh_add.remove(draw_func)

if __name__ == "__main__":
    register()
