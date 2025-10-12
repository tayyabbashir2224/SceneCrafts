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

class ReverseAnimationPanel(bpy.types.Panel):
    bl_label = "Reverse Animation"
    bl_idname = "PT_ReverseAnimationPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'SceneCraft'

    def draw(self, context):
            layout = self.layout
        
            props = context.scene.simple_operator_props
        

             
            scene = context.scene
            row = layout.row()
            row.label(text="Animate Selected Objects Out:")
            row = layout.row()
            row.label(text="Select Pivot Frame:")
            row = layout.row()
            row.scale_y = 1.4
            row.prop(scene, "pivot_frame", text="Pivot Frame")

            row = layout.row()
            row.scale_y = 1.7
            row.operator("object.Reverse_Animation", text="Reverse Animation")
            
            
            
            
        