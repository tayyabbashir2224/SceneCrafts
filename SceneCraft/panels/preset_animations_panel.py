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

class PresetAnimationsPanel(bpy.types.Panel):
    bl_label = "Preset Animations"
    bl_idname = "PT_PresetAnimationsPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'SceneCraft'

    def draw(self, context):
        layout = self.layout
        props = context.scene.preset_animation_props

        # Dropdown for animation preset
        layout.prop(props, "selected_preset", text="Animation Preset")

        # Dropdown for target type
        layout.prop(props, "target_type", text="Target Type")

        # Show collection selector if target type is COLLECTION
        if props.target_type == 'COLLECTION':
            layout.prop_search(props, "target_collection", bpy.data, "collections", text="Target Collection")

        # Dropdown for pattern type
        layout.prop(props, "pattern_type", text="Pattern Type")

        # Custom keyframe range
        layout.label(text="Custom Keyframes:")
        layout.prop(props, "start_frame", text="Start Frame")
        layout.prop(props, "end_frame", text="End Frame")

        # Apply animation button
        layout.operator("object.apply_preset_animation", text="Apply Preset")
