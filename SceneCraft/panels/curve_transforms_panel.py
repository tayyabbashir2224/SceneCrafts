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

class CurveTransformsPanel(bpy.types.Panel):
    bl_label = "Curve Transforms"
    bl_idname = "PT_CurveTransformsPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'SceneCraft'

    def draw(self, context):
            layout = self.layout
        
            curve_props = context.scene.curve_operator_props


            row = layout.row()
            row.label(text="Select Frame Range:")
            row = layout.row()
            row.scale_y = 1.2
            row.prop(curve_props, "start_frame")
            row = layout.row()
            row.scale_y = 1.2
            row.prop(curve_props, "end_frame")
            row = layout.row()
            row.label(text="Direction:")
            row = layout.row()
            row.scale_y = 1.2
            row.prop_enum(context.scene.curve_operator_props, "direction", 'X')
            row.prop_enum(context.scene.curve_operator_props, "direction", 'Y')
            row.prop_enum(context.scene.curve_operator_props, "direction", 'Z')
            row = layout.row()
            row.scale_y = 1.2
            row.prop_enum(context.scene.curve_operator_props, "direction", '-X')
            row.prop_enum(context.scene.curve_operator_props, "direction", '-Y')
            row.prop_enum(context.scene.curve_operator_props, "direction", '-Z')
            row = layout.row()
            row.scale_y = 1.2
            row.prop(curve_props, "curve_scale")
            row = layout.row()
            row.label(text="Apply Animation:")        
            row = layout.row()
            row.scale_y = 1.4
#            row.operator("object.generate_curve", text="Animate Along Curve 01")        
            row = layout.row()
            row.scale_y = 1.4
            row.operator("object.generate_curve_02", text="Animate Along Curve 02")        
            row = layout.row()
            row.scale_y = 1.4
            row.operator("object.generate_curve_03", text="Animate Along Curve 03")        
            row = layout.row()
            row.scale_y = 1.4
            row.operator("object.generate_curve_04", text="Animate Along Curve 04")        
            row = layout.row()
            row.scale_y = 1.4
            row.operator("object.generate_curve_05", text="Animate Along Curve 05")        
            row = layout.row()
            row.scale_y = 1.4
            row.operator("object.generate_curve_06", text="Animate Along Curve 06")        
            row = layout.row()
            row.scale_y = 1.4
            row.operator("object.generate_curve_07", text="Animate Along Curve 07")        
            row = layout.row()
            row.scale_y = 1.4
            row.operator("object.generate_curve_08", text="Animate Along Curve 08")        
            row = layout.row()
            row.scale_y = 1.4
            row.operator("object.generate_curve_09", text="Animate Along Curve 09")        
            row = layout.row()
            row.scale_y = 1.4
            row.operator("object.generate_curve_10", text="Animate Along Curve 10")
            row = layout.row()
            row.scale_y = 1.4
            row.operator("object.generate_curve_11", text="Animate Along Curve 11")
  