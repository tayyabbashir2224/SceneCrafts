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

class MultiObjectTransformsPanel(bpy.types.Panel):
    bl_label = "Multi-Object Transforms"
    bl_idname = "PT_MultiObjectTransformsPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'SceneCraft'

    def draw(self, context):
            layout = self.layout
        
            props = context.scene.simple_operator_props
            row = layout.row()
            row.prop(props, "show_uniobj", icon='TRIA_DOWN' if props.show_uniobj else 'TRIA_RIGHT')

            if props.show_uniobj:            

                box = layout.box()
                row = box.row()
                row = box.row()
                row.scale_y = 1.2
                row.prop(context.scene, "uni_animation_start_frame", text="Start Frame")
                row = box.row()
                row.scale_y = 1.2
                row.prop(context.scene, "uni_animation_end_frame", text="End Frame")
                row = box.row()
                row.scale_y = 1.2
                row.prop_search(context.scene.uniform_objects_animation_props, "collection_name", bpy.data, "collections")
                row = box.row()
                row.scale_y = 1.3
                row.prop(context.scene.uniform_objects_animation_props, "animate_from_z")
                row = box.row()
                row.scale_y = 1.3
                row.prop(context.scene.uniform_objects_animation_props, "animate_from_y")
                row = box.row()
                row.scale_y = 1.3
                row.prop(context.scene.uniform_objects_animation_props, "animate_from_x")
                
                row = box.row()
                row.scale_y = 1.3
                row.prop(context.scene.uniform_objects_animation_props, "rotation_x")
                row = box.row()
                row.scale_y = 1.3
                row.prop(context.scene.uniform_objects_animation_props, "rotation_y")
                row = box.row()
                row.scale_y = 1.3
                row.prop(context.scene.uniform_objects_animation_props, "rotation_z")

                row = box.row()

                row.scale_y = 1.9
                row.operator("object.uniform_objects_animation", text="Animate Objects")
            row = layout.row()
            row.scale_y = 1.2
            row.prop(props, "show_ranobj", icon='TRIA_DOWN' if props.show_ranobj else 'TRIA_RIGHT')

            if props.show_ranobj:           
                
                box = layout.box()

                row = box.row()
                row.label(text="Select Frame Range:") 
                row = box.row()
                row.scale_y = 1.2
                row.prop(context.scene, "random_animation_start_frame", text="Start Frame")
                row = box.row()
                row.scale_y = 1.2
                row.prop(context.scene, "random_animation_end_frame", text="End Frame")
                row = box.row()
                row.label(text="Select Collection:") 
                row = box.row()
                row.scale_y = 1.2
                row.prop_search(context.scene.random_objects_animation_props, "collection_name", bpy.data, "collections")
                

                row = box.row()
                row.label(text="Animate From Z:") 
                row = box.row()
                row.scale_y = 1.2
                row.prop(context.scene.random_objects_animation_props, "min_z_distance")
                row = box.row()
                row.scale_y = 1.2
                row.prop(context.scene.random_objects_animation_props, "max_z_distance")
                
                
                row = box.row()
                row.label(text="Animate From Y:")
                row = box.row()
                row.scale_y = 1.2
                row.prop(context.scene.random_objects_animation_props, "min_y_distance")
                row = box.row()
                row.scale_y = 1.2
                row.prop(context.scene.random_objects_animation_props, "max_y_distance")
                
                
                row = box.row()
                row.label(text="Animate From X:")
                row = box.row()
                row.scale_y = 1.2
                row.prop(context.scene.random_objects_animation_props, "min_x_distance")
                row = box.row()
                row.scale_y = 1.2
                row.prop(context.scene.random_objects_animation_props, "max_x_distance")
                
                
                
                row = box.row()
                row.label(text="X Rotation:")
                row = box.row()
                row.scale_y = 1.2
                row.prop(context.scene.random_objects_animation_props, "min_x_rotation")
                row = box.row()
                row.scale_y = 1.2
                row.prop(context.scene.random_objects_animation_props, "max_x_rotation")
                
                row = box.row()
                row.label(text="Y Rotation:")
                row = box.row()
                row.scale_y = 1.2
                row.prop(context.scene.random_objects_animation_props, "min_y_rotation")
                row = box.row()
                row.scale_y = 1.2
                row.prop(context.scene.random_objects_animation_props, "max_y_rotation")
                
                row = box.row()
                row.label(text="Z Rotation:")
                row = box.row()
                row.scale_y = 1.2
                row.prop(context.scene.random_objects_animation_props, "min_z_rotation")
                row = box.row()
                row.scale_y = 1.2
                row.prop(context.scene.random_objects_animation_props, "max_z_rotation")

                row = box.row()
                row.scale_y = 1.9
                row.operator("object.random_objects_animation", text="Random Objects Animation") 
        