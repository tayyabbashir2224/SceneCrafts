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

class ObjectTransformsPanel(bpy.types.Panel):
    bl_label = "Object Transforms"
    bl_idname = "PT_ObjectTransformsPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'SceneCraft'

    def draw(self, context):
        layout = self.layout
        props = context.scene.simple_operator_props

        # Frame Range Section
        row = layout.row()
        row.label(text="Select Frame Range:")

        row = layout.row()
        row.scale_y = 1.2
        row.prop(props, "start_frame")

        row = layout.row()
        row.scale_y = 1.2
        row.prop(props, "end_frame")

        # Animate In/Out Section
        row = layout.row()
        row.prop(props, "show_transform", text="Animate In/Out:", icon='TRIA_DOWN' if props.show_transform else 'TRIA_RIGHT')

        if props.show_transform:
            # Animate In
            row = layout.row()
            row.scale_y = 1.2
            row.prop(props, "distance_offset")

            row = layout.row()
            row.scale_y = 1.5
            row.operator("object.animate_in_y", text="Animate In Y")
            row.operator("object.b_animate_in_y", text="Bounce In Y")

            row = layout.row()
            row.scale_y = 1.5
            row.operator("object.animate_in_x", text="Animate In X")
            row.operator("object.b_animate_in_x", text="Bounce In X")

            row = layout.row()
            row.scale_y = 1.5
            row.operator("object.animate_in_z", text="Animate In Z")
            row.operator("object.b_animate_in_z", text="Bounce In Z")
        row = layout.row()
        row.prop(props, "show_scale", text="Scale In/Out:", icon='TRIA_DOWN' if props.show_scale else 'TRIA_RIGHT')

        if props.show_scale:
            # Scale In/Out
            row = layout.row()
            row.label(text="Scale In/Out:")

            row = layout.row()
            row.label(text="Origin Point at:")

            row = layout.row()
            row.scale_y = 1.4
            row.prop_enum(props, "origin_point", 'BOTTOM')
            row.prop_enum(props, "origin_point", 'TOP')

            row = layout.row()
            row.scale_y = 1.3
            row.prop(props, "object_scale_factor")

            row = layout.row()
            row.scale_y = 1.5
            row.operator("object.scale_in", text="Scale In/Out")

            # Fall Down
        row = layout.row()
        row.prop(props, "show_fall", text="Fall Down", icon='TRIA_DOWN' if props.show_fall else 'TRIA_RIGHT')

        if props.show_fall:
            row = layout.row()
            row.label(text="Fall Down:")

            row = layout.row()
            row.scale_y = 1.2
            row.prop(props, "distance_offset")

            row = layout.row()
            row.scale_y = 1.3
            row.prop(props, "object_min_scale_factor")

            row = layout.row()
            row.scale_y = 1.5
            row.operator("object.fall_down_z", text="Fall Down")

            # Spiral In
        row = layout.row()
        row.prop(props, "show_spiral", text="Spiral In/Out:", icon='TRIA_DOWN' if props.show_spiral else 'TRIA_RIGHT')

        if props.show_spiral:
            row = layout.row()
            row.label(text="Spiral In/Out:")

            row = layout.row()
            row.label(text="Spiral Around Axis:")

            row = layout.row()
            row.scale_y = 1.2
            row.prop_enum(props, "spiral_direction", 'X')
            row.prop_enum(props, "spiral_direction", 'Y')
            row.prop_enum(props, "spiral_direction", 'Z')

            row = layout.row()
            row.scale_y = 1.2
            row.prop(props, "distance_offset")

            row = layout.row()
            row.scale_y = 1.2
            row.prop(props, "spiral_angle")

            row = layout.row()
            row.scale_y = 1.4
            row.operator("object.animate_in_y_rotate", text="Spiral in From Y")

            row = layout.row()
            row.scale_y = 1.4
            row.operator("object.animate_in_x_rotate", text="Spiral in From X")

            row = layout.row()
            row.scale_y = 1.4
            row.operator("object.animate_in_z_rotate", text="Spiral in From Z")

            # Rotate In/Out
        row = layout.row()
        row.prop(props, "show_rotate", text="Rotate In/Out:", icon='TRIA_DOWN' if props.show_rotate else 'TRIA_RIGHT')

        if props.show_rotate:
            row = layout.row()
            row.label(text="Rotate In/Out:")

            row = layout.row()
            row.label(text="Origin Point at:")

            row = layout.row()
            row.scale_y = 1.4
            row.prop_enum(props, "origin_point", 'BOTTOM')
            row.prop_enum(props, "origin_point", 'TOP')

            row = layout.row()
            row.scale_y = 1.3
            row.prop(props, "rotate_angle")

            row = layout.row()
            row.scale_y = 1.5
            row.operator("object.rotate_in_x", text="Rotate X Axis")
            row.operator("object.rotate_in_x2", text="Rotate -X Axis")

            row = layout.row()
            row.scale_y = 1.5
            row.operator("object.rotate_in_y", text="Rotate Y Axis")
            row.operator("object.rotate_in_y2", text="Rotate -Y Axis")

            row = layout.row()
            row.scale_y = 1.5
            row.operator("object.rotate_in_z", text="Rotate Z Axis")
            row.operator("object.rotate_in_z2", text="Rotate -Z Axis")

            # Pop Up
        row = layout.row()
        row.prop(props, "show_popup", text="Pop Up:", icon='TRIA_DOWN' if props.show_popup else 'TRIA_RIGHT')

        if props.show_popup:
            row = layout.row()
            row.label(text="Pop Up:")

            row = layout.row()
            row.scale_y = 1.4
            row.operator("object.pop_up", text="Pop up")

            row = layout.row()
            row.scale_y = 1.4
            row.operator("object.pop_up_x", text="& Rotate X")
            row.operator("object.pop_up_x2", text="& Rotate -X")

            row = layout.row()
            row.scale_y = 1.4
            row.operator("object.pop_up_y", text="& Rotate Y")
            row.operator("object.pop_up_y2", text="& Rotate -Y")

            row = layout.row()
            row.scale_y = 1.4
            row.operator("object.pop_up_z", text="& Rotate Z")
            row.operator("object.pop_up_z2", text="& Rotate -Z")

            row = layout.row()
            row.scale_y = 1.4
            row.operator("object.pop_up_twist", text="Pop up & Twist")
