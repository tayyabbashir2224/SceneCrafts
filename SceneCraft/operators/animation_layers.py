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
import bpy


class OBJECT_OT_AddAnimationLayer(bpy.types.Operator):
    bl_idname = "object.add_animation_layer"
    bl_label = "Add Animation Layer"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene

        # Add a new layer to the animation_layer_collection
        new_layer = scene.animation_layer_collection.add()
        new_layer.layer_name = f"Layer {len(scene.animation_layer_collection)}"

        self.report({'INFO'}, f"Added {new_layer.layer_name}")
        return {'FINISHED'}


class OBJECT_OT_BakeAnimationLayers(bpy.types.Operator):
    bl_idname = "object.bake_animation_layers"
    bl_label = "Bake Animation Layers"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.object
        action = obj.animation_data.action

        # Combine all layers into a single baked action
        for fcurve in action.fcurves:
            for keyframe in fcurve.keyframe_points:
                keyframe.co.y *= context.scene.animation_layer_props.layer_opacity

        self.report({'INFO'}, "Baked all animation layers.")
        return {'FINISHED'}

class OBJECT_OT_DeleteAnimationLayer(bpy.types.Operator):
    bl_idname = "object.delete_animation_layer"
    bl_label = "Delete Animation Layer"
    bl_options = {'REGISTER', 'UNDO'}

    layer_index: bpy.props.IntProperty()  # Layer index to delete

    def execute(self, context):
        scene = context.scene
        layers = scene.animation_layer_collection

        if 0 <= self.layer_index < len(layers):
            layers.remove(self.layer_index)
            self.report({'INFO'}, f"Deleted Layer {self.layer_index + 1}")
        else:
            self.report({'WARNING'}, "Invalid layer index!")

        return {'FINISHED'}


class OBJECT_OT_BakeAnimationLayers(bpy.types.Operator):
    bl_idname = "object.bake_layers"
    bl_label = "Bake Animation Layers"

    def execute(self, context):
        layers = context.scene.animation_layer_collection

        for layer in layers:
            if layer.layer_animation_type == 'FADE':
                self.apply_fade(context, layer)
            elif layer.layer_animation_type == 'SCALE':
                self.apply_scale(context, layer)

        self.report({'INFO'}, "Baked all layers.")
        return {'FINISHED'}

    def apply_fade(self, context, layer):
        # Apply fade-in/out logic using alpha keyframes
        pass

    def apply_scale(self, context, layer):
        # Apply scale-in/out logic using scale keyframes
        pass
