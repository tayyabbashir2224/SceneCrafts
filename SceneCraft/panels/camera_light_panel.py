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


class CameraLightAnimationsPanel(bpy.types.Panel):
    bl_label = "Camera and Light Animations"
    bl_idname = "PT_CameraLightAnimationsPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'SceneCraft'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        props = context.scene.simple_operator_props

        # Camera Animation Section
        row = layout.row()
        row.prop(props, "show_cam", icon='TRIA_DOWN' if props.show_cam else 'TRIA_RIGHT')

        if props.show_cam:
            camera_props = scene.camera_animation_props
            layout.prop(camera_props, "camera_preset")
            layout.prop(camera_props, "start_frame")
            layout.prop(camera_props, "end_frame")
            layout.prop(camera_props, "target_object")
            layout.operator("scenecraft.apply_camera_animation", text="Apply Camera Animation")

        # Separator
        layout.separator()
        row = layout.row()
        row.prop(props, "show_light", icon='TRIA_DOWN' if props.show_light else 'TRIA_RIGHT')

        if props.show_light:
            # Light Animation Section
            light_props = scene.light_animation_props
            layout.prop(light_props, "light_preset")

            # Show additional options based on the preset
            if light_props.light_preset == 'MOVEMENT':
                layout.prop(light_props, "movement_path_type", text="Path Type")
                layout.prop(light_props, "z_oscillation", text="Z Oscillation")
                layout.prop(light_props, "target_object", text="Target Object (For Custom Path)")
            elif light_props.light_preset == 'FLICKER':
                layout.prop(light_props, "flicker_speed", text="Flicker Speed")
            elif light_props.light_preset == 'PULSE':
                layout.prop(light_props, "pulse_speed", text="Pulse Speed")
            elif light_props.light_preset == 'COLOR':
                layout.label(text="Gradient Colors:")
                row = layout.row(align=True)
                row.operator("scene.add_gradient_color", text="Add Color")
                row.operator("scene.remove_gradient_color", text="Remove Color")

                for i, color in enumerate(light_props.gradient_colors):
                    row = layout.row()
                    row.prop(color, "color", text=f"Color {i+1}")

            # Common properties for all presets
            layout.prop(light_props, "start_frame")
            layout.prop(light_props, "end_frame")
            layout.operator("scenecraft.apply_light_animation", text="Apply Light Animation")
