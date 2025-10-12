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

class AnimationLayersPanel(bpy.types.Panel):
    bl_label = "Animation Layers"
    bl_idname = "PT_AnimationLayersPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'SceneCraft'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        layers = scene.animation_layer_collection

        # Display layers
        for i, layer in enumerate(layers):
            box = layout.box()
            box.prop(layer, "layer_name", text="Name")
            box.prop(layer, "layer_opacity", text="Opacity")
            box.prop(layer, "layer_animation_type", text="Animation Type")
            box.prop(layer, "start_frame", text="Start")
            box.prop(layer, "end_frame", text="End")

            # Delete button
            row = box.row()
            row.operator("object.delete_layer", text="Delete").layer_index = i

        # Add layer button
        layout.operator("object.add_layer", text="Add Layer")
        layout.operator("object.bake_layers", text="Bake All Layers")

