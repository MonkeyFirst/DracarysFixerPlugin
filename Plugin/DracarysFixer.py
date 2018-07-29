bl_info = {
    "name": "Dracarys Fixer for Urho3D",
    "author": "Monkey1st",
    "category": "Object",
    "blender": (2, 79, 0)   
}

import bpy

class AutoConstraintToET(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.auto_constraint"
    bl_label = "AutoConstraintToEmptyTargets"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        for ob in context.selected_objects:
            AddConstraintsToObject(ob)
        
        return {'FINISHED'}
          
def AddConstraintsToObject(selectedObj):
    if selectedObj.type == 'ARMATURE':
        for i, bone in enumerate(selectedObj.pose.bones):
            et = ReturnObjectByName("ET_"+bone.name)
            if et != None:
                #print ("we find et "+ et.name)
                AddConstraintToBone(et, bone)
     
def ReturnObjectByName (passedName= ""):
    r = None
    obs = bpy.data.objects
    for ob in obs:
        if ob.name == passedName:
            r = ob
    return r

def RemoveAllPrevConstraints(bone):
    for c in bone.constraints:    
        bone.constraints.remove( c )

def AddConstraintToBone(et, bone):
    
    RemoveAllPrevConstraints(bone)
    
    constraint = bone.constraints.new('COPY_TRANSFORMS')
    constraint.influence = 1.0
    constraint.target = et
    constraint.subtarget = et.name
    #constraint.use_scale_x = False
    #constraint.use_scale_y = False
    #constraint.use_scale_z = False
    constraint.target_space = 'WORLD'
    constraint.owner_space = 'WORLD'

class CreateEmptyTargets(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.create_empty_targets"
    bl_label = "CreateEmptyTargetsForBones"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        for ob in context.selected_objects:
            AddEmptyTargets(ob) 
        return {'FINISHED'}

def AddEmptyTargets(selectedObj):
    if selectedObj.type == 'ARMATURE':
        for i, bone in enumerate(selectedObj.data.bones):
            o = bpy.data.objects.new("ET_" + bone.name, None )
            bpy.context.scene.objects.link( o )
            o.empty_draw_size = 1
            o.empty_draw_type = 'PLAIN_AXES'
            #ParentSet(o, selectedObj, bone)
            #o.location.y = o.location.y - bone.length
            constraint = o.constraints.new('CHILD_OF')
            constraint.influence = 1.0
            constraint.target = selectedObj
            constraint.subtarget = bone.name
            constraint.use_scale_x = False
            constraint.use_scale_y = False
            constraint.use_scale_z = False
            constraint.target_space = 'WORLD'
            constraint.owner_space = 'WORLD'

class CustomMenu(bpy.types.Menu):
    bl_label = "Dracaris Fixer"
    bl_idname = "OBJECT_MT_custom_menu"

    def draw(self, context):
        layout = self.layout

        layout.operator("object.create_empty_targets")
        layout.operator("object.auto_constraint")
        layout.label(text="Urho3D tools for fixing all kind of dragons", icon='WORLD_DATA')


def draw_item(self, context):
    layout = self.layout
    layout.menu(CustomMenu.bl_idname)


def register():
    bpy.utils.register_class(AutoConstraintToET)
    bpy.utils.register_class(CreateEmptyTargets)
    bpy.utils.register_class(CustomMenu)

    # lets add ourselves to the main header
    bpy.types.INFO_HT_header.append(draw_item)


def unregister():
    bpy.utils.unregister_class(AutoConstraintToET)
    bpy.utils.unregister_class(CreateEmptyTargets)
    bpy.utils.unregister_class(CustomMenu)

    bpy.types.INFO_HT_header.remove(draw_item)

if __name__ == "__main__":
    register()

    # The menu can also be called from scripts
    bpy.ops.wm.call_menu(name=CustomMenu.bl_idname)
