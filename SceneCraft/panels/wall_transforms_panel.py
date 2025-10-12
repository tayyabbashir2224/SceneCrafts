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

class WallTransformsPanel(bpy.types.Panel):
    bl_label = "Wall Transforms"
    bl_idname = "PT_WallTransformsPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'SceneCraft'

    def draw(self, context):
            layout = self.layout
        
            props = context.scene.simple_operator_props
            pop_in_walls_props = context.scene.pop_in_walls          
            rotate_in_walls_props = context.scene.rotate_in_walls
             
            row = layout.row()
            row.scale_y = 1.2
            row = layout.row()
            row.prop(props, "show_wallbend", icon='TRIA_DOWN' if props.show_wallbend else 'TRIA_RIGHT')

            if props.show_wallbend:            
                        
                # Bend Walls Section
                box = layout.box()
                box.label(text="Select Frame Range:")
                row = box.row()
                row.scale_y = 1.2
                row.prop(context.scene, "bend_walls_start_frame", text="Start Frame")   
                row = box.row()
                row.scale_y = 1.2    
                row.prop(context.scene, "bend_walls_end_frame", text="End Frame")        
                box.label(text="Direction:")        
                row = box.row()
                row.scale_y = 1.2
                row.prop(context.scene, "bend_walls_direction_xyz", expand=True)
                row = box.row()
                row.scale_y = 1.2
                row.prop(context.scene, "bend_walls_direction", expand=True)
                row = box.row()
                row.scale_y = 1.7
                row.operator("object.bend_walls", text="Bend Wall")  
                # Roll Walls Section
            row = layout.row()
            row.scale_y = 1.2
            row.prop(props, "show_wallroll", icon='TRIA_DOWN' if props.show_wallroll else 'TRIA_RIGHT')

            if props.show_wallroll:                 
                
                box = layout.box()
                box.label(text="Select Frame Range:")
                row = box.row()
                row.scale_y = 1.2
                row.prop(context.scene, "roll_walls_start_frame", text="Start Frame")
                row = box.row()
                row.scale_y = 1.2
                row.prop(context.scene, "roll_walls_end_frame", text="End Frame")
                row = box.row()
                row.label(text="Direction:")
                row = box.row()
                row.scale_y = 1.2
                row.prop(context.scene, "roll_walls_direction_xyz", expand=True)
                row = box.row()
                row.scale_y = 1.7
                row.operator("object.roll_walls", text="Roll Wall")
            row = layout.row()
            row.scale_y = 1.1
                # Wipe Walls Section
            row.prop(props, "show_wallwipe", icon='TRIA_DOWN' if props.show_wallwipe else 'TRIA_RIGHT')

            if props.show_wallwipe: 
                        
                box = layout.box()
                box.label(text="Select Frame Range:")
                row = box.row()
                row.scale_y = 1.2
                row.prop(context.scene, "wipe_walls_start_frame", text="Start Frame")
                row = box.row()
                row.scale_y = 1.2
                row.prop(context.scene, "wipe_walls_end_frame", text="End Frame")
                row = box.row()
                row.label(text="Direction:")
                row = box.row()
                row.scale_y = 1.2
                row.prop(context.scene, "wipe_walls_direction_xyz", expand=True)
                row = box.row()
                row.scale_y = 1.7
                row.operator("object.wipe_walls", text="Wipe Animation")
            row = layout.row()
            row.scale_y = 1.1
                # Pop In Walls Section
            row.prop(props, "show_wallpop", icon='TRIA_DOWN' if props.show_wallpop else 'TRIA_RIGHT')

            if props.show_wallpop: 
                
                box = layout.box()
                box.label(text="Select Frame Range:")
                row = box.row()
                row.scale_y = 1.2
                row.prop(context.scene, "pop_w_start_frame", text="Start Frame")
                row = box.row()
                row.scale_y = 1.2
                row.prop(context.scene, "pop_w_end_frame", text="End Frame")
                row = box.row()
                row.label(text="Choose Collection:")
                row = box.row()
                row.scale_y = 1.1
                row.prop_search(pop_in_walls_props, "collection_name", bpy.data, "collections")
                row = box.row()
                row.scale_y = 1.1
                row.label(text="Direction:")
                row = box.row()
                row.scale_y = 1.3
                row.prop(context.scene, "pop_w_direction_xyz", expand=True)
                row = box.row()
                row.scale_y = 1.7
                row.operator("object.pop_in_walls", text="Tiles Pop In", icon='PLAY')
            row = layout.row()
            row.scale_y = 1.1
                # Rotate In Walls Section
            row.prop(props, "show_wallrotate", icon='TRIA_DOWN' if props.show_wallrotate else 'TRIA_RIGHT')

            if props.show_wallrotate: 
                
                box = layout.box()
                box.label(text="Selct Frame Range:")
                row = box.row()
                row.scale_y = 1.2
                row.prop(context.scene, "rotate_w_start_frame", text="Start Frame")
                row = box.row()
                row.scale_y = 1.2
                row.prop(context.scene, "rotate_w_end_frame", text="End Frame")
                row = box.row()
                row.scale_y = 1.2
                row.label(text="Choose Collection:")
                row = box.row()
                row.scale_y = 1.1
                row.prop_search(rotate_in_walls_props, "collection_name", bpy.data, "collections")
                row = box.row()
                row.scale_y = 1.1
                row.label(text="Direction:")
                row = box.row()
                row.scale_y = 1.2
                row.prop(context.scene, "rotate_w_direction_xyz", expand=True)
                row = box.row()
                row.scale_y = 1.7
                row.operator("object.rotate_in_walls", text="Tiles Rotate In", icon='PLAY')
     