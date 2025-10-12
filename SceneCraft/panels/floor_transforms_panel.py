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

class FloorTransformsPanel(bpy.types.Panel):
    bl_label = "Floor Transforms"
    bl_idname = "PT_FloorTransformsPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'SceneCraft'

    def draw(self, context):
            layout = self.layout
        
            props = context.scene.simple_operator_props
            fall_down_tiles_props = context.scene.fall_down_tiles
            pop_in_floors_props = context.scene.pop_in_floors
        
            row = layout.row()
            row.scale_y = 1.2
            row.prop(props, "show_bendfloor", icon='TRIA_DOWN' if props.show_bendfloor else 'TRIA_RIGHT')

            if props.show_bendfloor:                      
                # Section 1: Bend Floor
                box = layout.box()
                box.label(text="Select Frame Range:")
                row = box.row()
                row.scale_y = 1.2
                row.prop(context.scene, "bend_start_frame", text="Start Frame")
                row = box.row()
                row.scale_y = 1.2
                row.prop(context.scene, "bend_end_frame", text="End Frame")
                row = box.row()
                row.scale_y = 0.8
                row.label(text="Direction:")
                row = box.row()
                row.scale_y = 1.2
                row.prop(context.scene, "bend_direction_xyz", expand=True)
                row = box.row()
                row.scale_y = 1.5
                row.prop(context.scene, "bend_direction", expand=True)
                row = box.row()
                row.scale_y = 1.7
                row.operator("object.bend_floors", text="Bend Floor")
            row = layout.row()
            row.scale_y = 1.2
            row.prop(props, "show_rollfloor", icon='TRIA_DOWN' if props.show_rollfloor else 'TRIA_RIGHT')

            if props.show_rollfloor:
                # Section 2: Roll Floors
                box = layout.box()
                box.label(text="Select Frame Range:")
                row = box.row()
                row.scale_y = 1.2
                row.prop(context.scene, "roll_start_frame", text="Start Frame")
                row = box.row()
                row.scale_y = 1.2
                row.prop(context.scene, "roll_end_frame", text="End Frame")
                row = box.row()
                row.scale_y = 0.8
                row.label(text="Direction:")
                row = box.row()
                row.scale_y = 1.2
                row.prop(context.scene, "roll_direction_xyz", expand=True)
                row = box.row()
                row.scale_y = 1.7
                row.operator("object.roll_floors", text="Roll Floor")
            row = layout.row()
            row.scale_y = 1.2
            # Section 3: Wipe Floors
            row.prop(props, "show_wipefloor", icon='TRIA_DOWN' if props.show_wipefloor else 'TRIA_RIGHT')

            if props.show_wipefloor:
                box = layout.box()
                box.label(text="Select Frame Range:")
                row = box.row()
                row.scale_y = 1.2
                row.prop(context.scene, "wipe_start_frame", text="Start Frame")
                row = box.row()
                row.scale_y = 1.2
                row.prop(context.scene, "wipe_end_frame", text="End Frame")
                row = box.row()
                row.scale_y = 0.8
                row.label(text="Direction:")
                row = box.row()
                row.scale_y = 1.2
                row.prop(context.scene, "wipe_direction_xyz", expand=True)
                row = box.row()
                row.scale_y = 1.7
                row.operator("object.wipe_floors", text="Wipe Floor")
            row = layout.row()
            row.scale_y = 1.2
            row.prop(props, "show_tilefallfloor", icon='TRIA_DOWN' if props.show_tilefallfloor else 'TRIA_RIGHT')

            if props.show_tilefallfloor:
                # Section 4: Tiles Fall Down  
                box = layout.box()
                box.label(text="Select Frame Range:")
                row = box.row()
                row.scale_y = 1.2
                row.prop(context.scene, "fade_start_frame", text="Start Frame")
                row = box.row()
                row.scale_y = 1.2
                row.prop(context.scene, "fade_end_frame", text="End Frame")
                box.label(text="Choose Collection:")            
                row = box.row() 
                row.scale_y = 1.1   
                row.prop_search(fall_down_tiles_props, "collection_name", bpy.data, "collections")            
                row = box.row()
                row.scale_y = 1.7
                row.operator("object.fall_down_tiles", text="Tiles Fall Down", icon='PLAY')            
            row = layout.row()
            row.scale_y = 1.2
            row.prop(props, "show_tilepopfloor", icon='TRIA_DOWN' if props.show_tilepopfloor else 'TRIA_RIGHT')

            if props.show_tilepopfloor:
                # Section 4: Tiles Fall Down  
                box = layout.box()
                box.label(text="Select Frame Range:")
                row = box.row()
                row.scale_y = 1.2
                row.prop(context.scene, "pop_start_frame", text="Start Frame")
                row = box.row()
                row.scale_y = 1.2
                row.prop(context.scene, "pop_end_frame", text="End Frame")            
                box.label(text="Choose Collection:")
                row = box.row()    
                row.scale_y = 1.1      
                row.prop_search(pop_in_floors_props, "collection_name", bpy.data, "collections")
                row = box.row()
                row.scale_y = 0.8
                row.label(text="Direction:")
                row = box.row()
                row.scale_y = 1.2
                row.prop(context.scene, "pop_direction_xyz", expand=True)
                row = box.row()
                row.scale_y = 1.7
                row.operator("object.pop_in_floors", text="Tiles Pop In", icon='PLAY')
     