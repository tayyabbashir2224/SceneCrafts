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
import math #import sin, cos, pi
from mathutils import Vector
import os

from ..base_operators import BaseCurveOperator
addon_dirc = os.path.dirname(os.path.realpath(__file__))

class CurveOperator(BaseCurveOperator):
    bl_idname = "object.curve_operator"
    bl_label = "Curve Operator"

    def execute(self, context):
                      
        # Check if there is an active object
        if context.active_object is not None and context.active_object.type == 'MESH':
            selected_object = context.active_object
            
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            
            # Delete existing keyframes on angle and scale properties
            selected_object.animation_data_clear()

            if 'scale' in selected_object and selected_object['scale']:
                selected_object.keyframe_delete(data_path='["scale"]')
                
            # Check if there is a Curve Modifier on the selected object and remove it
            curve_modifier = next((modifier for modifier in selected_object.modifiers if modifier.type == 'CURVE'), None)
            if curve_modifier:
                selected_object.modifiers.remove(curve_modifier)
                
            # Store the original dimensions of the selected object
            original_x_dimension = selected_object.dimensions.x
            original_y_dimension = selected_object.dimensions.y
            original_z_dimension = selected_object.dimensions.z

            # Set the origin point of the selected object to the center of its geometry
            bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')  

            # Append the curve object from the external blend file
            blend_file_path = addon_dirc + "/Assets.blend"
            curve_object_name = "Curve Twist"
            base_name = "Animation Curve"  # Base name for the new curve objects

            # Check if the object already exists in the scene
            existing_objects = [obj for obj in bpy.data.objects if obj.name.startswith(base_name)]
            existing_object = next((obj for obj in existing_objects if obj.name == curve_object_name), None)

            if existing_object:
                # Update the existing object
                curve_object = existing_object
                curve_object.data = bpy.data.objects[curve_object_name].data.copy()
            else:
                # Create a new object
                with bpy.data.libraries.load(blend_file_path) as (data_from, data_to):
                    if curve_object_name in data_from.objects:
                        data_to.objects = [curve_object_name]

                # Check if the object is loaded
                if curve_object_name in bpy.data.objects:
                    curve_object = bpy.data.objects[curve_object_name]

                    # Create a new object and link the data from the appended curve object
                    new_object_name = base_name + str(len(existing_objects)).zfill(3)
                    curve_object = curve_object.copy()
                    curve_object.name = new_object_name
                    bpy.context.collection.objects.link(curve_object)  # Link to the active collection
                    
                    
                    
                    
              

        curve_scale = context.scene.curve_operator_props.curve_scale
        
        if context.scene.curve_operator_props.direction == 'X':
            bpy.context.view_layer.objects.active = curve_object
            bpy.context.object.rotation_euler = (0, 0, math.radians(-90))
                    
                        
            # Set the scale factor based on x dimension
            scale_factor = (selected_object.dimensions.x / 3) * curve_scale
            curve_object.scale = (scale_factor, scale_factor, scale_factor)
                        
            curve_object.location.x = selected_object.location.x 
            curve_object.location.y = selected_object.location.y + (selected_object.dimensions.y / 2 + selected_object.dimensions.z / 2) / 2
            curve_object.location.z = selected_object.location.z - (selected_object.dimensions.y / 2 + selected_object.dimensions.z / 2) / 2

            # Set the curve modifier on the selected object
            curve_modifier = selected_object.modifiers.new(name="Curve Modifier", type='CURVE')
            curve_modifier.deform_axis = 'POS_Y'  # Set the deform axis to 'POS_Y'
            curve_modifier.object = curve_object  # Set the new curve object
                
            # Rotate the selected object 180 degrees on the y axis
            selected_object.rotation_euler.x = math.radians(90)
            selected_object.rotation_euler.y = math.radians(180)
                    
        elif context.scene.curve_operator_props.direction == 'Y':
                        
            # Set the scale factor based on y dimension
            scale_factor = (selected_object.dimensions.y / 3) * curve_scale
            curve_object.scale = (scale_factor, scale_factor, scale_factor)
                        
            curve_object.location.x = selected_object.location.x - (selected_object.dimensions.x / 2 + selected_object.dimensions.z / 2) / 2  # Half the X dimension
            curve_object.location.y = selected_object.location.y
            curve_object.location.z = selected_object.location.z - (selected_object.dimensions.x / 2 + selected_object.dimensions.z / 2) / 2
                        
            # Set the curve modifier on the selected object
            curve_modifier = selected_object.modifiers.new(name="Curve Modifier", type='CURVE')
            curve_modifier.deform_axis = 'POS_Y'  # Set the deform axis to 'POS_Y'
            curve_modifier.object = curve_object  # Set the new curve object
                
            # Rotate the selected object 180 degrees on the x axis
            selected_object.rotation_euler.x = math.radians(180)
            selected_object.rotation_euler.y = math.radians(-90)
                
        
        
        
        
        elif context.scene.curve_operator_props.direction == '-X':
            
            # Rotate the curve object -90 degrees on the Z axis
            bpy.context.view_layer.objects.active = curve_object
            bpy.context.object.rotation_euler = (0, 0, math.radians(90))
                    
                        
            # Set the scale factor based on x dimension
            scale_factor = (selected_object.dimensions.x / 3) * curve_scale
            curve_object.scale = (scale_factor, scale_factor, scale_factor)
                        
            curve_object.location.x = selected_object.location.x 
            curve_object.location.y = selected_object.location.y - (selected_object.dimensions.y / 2 + selected_object.dimensions.z / 2) / 2
            curve_object.location.z = selected_object.location.z - (selected_object.dimensions.y / 2 + selected_object.dimensions.z / 2) / 2

            # Set the curve modifier on the selected object
            curve_modifier = selected_object.modifiers.new(name="Curve Modifier", type='CURVE')
            curve_modifier.deform_axis = 'POS_Y'  # Set the deform axis to 'POS_Y'
            curve_modifier.object = curve_object  # Set the new curve object
                
            # Rotate the selected object 180 degrees on the y axis
            selected_object.rotation_euler.x = math.radians(-90)
            selected_object.rotation_euler.y = math.radians(180)
                    
        elif context.scene.curve_operator_props.direction == '-Y':
            # Rotate the curve object 180 degrees on the Z axis
            bpy.context.view_layer.objects.active = curve_object
            bpy.context.object.rotation_euler = (0, 0, math.radians(180))
                        
            # Set the scale factor based on y dimension
            scale_factor = (selected_object.dimensions.y / 3) * curve_scale
            curve_object.scale = (scale_factor, scale_factor, scale_factor)
                        
            curve_object.location.x = selected_object.location.x + (selected_object.dimensions.x / 2 + selected_object.dimensions.z / 2) / 2  # Half the X dimension
            curve_object.location.y = selected_object.location.y
            curve_object.location.z = selected_object.location.z - (selected_object.dimensions.x / 2 + selected_object.dimensions.z / 2) / 2
                        
            # Set the curve modifier on the selected object
            curve_modifier = selected_object.modifiers.new(name="Curve Modifier", type='CURVE')
            curve_modifier.deform_axis = 'POS_Y'  # Set the deform axis to 'POS_Y'
            curve_modifier.object = curve_object  # Set the new curve object
                
            # Rotate the selected object 180 degrees on the x axis
            selected_object.rotation_euler.x = math.radians(180)
            selected_object.rotation_euler.y = math.radians(90)
                
        elif context.scene.curve_operator_props.direction == 'Z':
            if original_y_dimension <= 2*original_x_dimension:
                bpy.context.view_layer.objects.active = curve_object
                bpy.context.object.rotation_euler = (math.radians(-90), 0, math.radians(180))
            else:
                bpy.context.view_layer.objects.active = curve_object
                bpy.context.object.rotation_euler = (math.radians(-90), 0, math.radians(-90))
                        
            # Set the scale factor based on z dimension
            scale_factor = (selected_object.dimensions.z / 3) * curve_scale
            curve_object.scale = (scale_factor, scale_factor, scale_factor)
                        
            curve_object.location.z = selected_object.location.z
            curve_object.location.y = selected_object.location.y
            curve_object.location.x = selected_object.location.x 
            
            # Set the curve modifier on the selected object
            curve_modifier = selected_object.modifiers.new(name="Curve Modifier", type='CURVE')
            curve_modifier.deform_axis = 'POS_Y'  # Set the deform axis to 'POS_Y'
            curve_modifier.object = curve_object  # Set the new curve object
            
            
            if original_y_dimension <= 2*original_x_dimension:
                # Rotate the selected object 180 degrees on the Y axis
                selected_object.rotation_euler.y = math.radians(180)
                selected_object.rotation_euler.z = math.radians(-90)
            else:
                # Rotate the selected object 180 degrees on the Y axis
                selected_object.rotation_euler.y = math.radians(180)
                selected_object.rotation_euler.z = math.radians(90)
            

            pass
        
        elif context.scene.curve_operator_props.direction == '-Z':
            if original_y_dimension <= 2*original_x_dimension:
                bpy.context.view_layer.objects.active = curve_object
                bpy.context.object.rotation_euler = (math.radians(90), 0, math.radians(360))
            else:
                bpy.context.view_layer.objects.active = curve_object
                bpy.context.object.rotation_euler = (math.radians(90), 0, math.radians(90))


            # Set the scale factor based on z dimension
            scale_factor = (selected_object.dimensions.z / 3) * curve_scale
            curve_object.scale = (scale_factor, scale_factor, scale_factor)

            curve_object.location.z = selected_object.location.z
            curve_object.location.y = selected_object.location.y
            curve_object.location.x = selected_object.location.x 

            # Set the curve modifier on the selected object
            curve_modifier = selected_object.modifiers.new(name="Curve Modifier", type='CURVE')
            curve_modifier.deform_axis = 'POS_Y'  # Set the deform axis to 'POS_Y'
            curve_modifier.object = curve_object  # Set the new curve object

            if original_y_dimension <= 2*original_x_dimension:
                # Rotate the selected object 180 degrees on the Y axis
                selected_object.rotation_euler.y = math.radians(180)
                selected_object.rotation_euler.z = math.radians(90)
            else:
                # Rotate the selected object 180 degrees on the Y axis
                selected_object.rotation_euler.y = math.radians(180)
                selected_object.rotation_euler.z = math.radians(-90)
            
            pass
        
        # Store the original location of the selected object
        original_location = selected_object.location.copy()
        
        

        # Calculate End Frame and Start Frame values
        end_frame = context.scene.curve_operator_props.end_frame
        start_frame = context.scene.curve_operator_props.start_frame
        mid_frame = (context.scene.curve_operator_props.start_frame + context.scene.curve_operator_props.end_frame) / 2
        move_factor = 2.64 * curve_scale if context.scene.curve_operator_props.direction == 'X,Y,Z' else -2.64 * curve_scale
        
        
        # Set keyframes
        selected_object.location = original_location
        selected_object.keyframe_insert(data_path="location", frame=end_frame)

        # Set End Frame keyframes for X/Y Direction
        if context.scene.curve_operator_props.direction == 'X':   
            selected_object.location.x += -move_factor * selected_object.dimensions.x
        elif context.scene.curve_operator_props.direction == 'Y':
                selected_object.location.y += -move_factor * selected_object.dimensions.y

        # Set End Frame keyframes for -X/-Y Direction
        elif context.scene.curve_operator_props.direction == '-X':   
            selected_object.location.x -= -move_factor * selected_object.dimensions.x
        elif context.scene.curve_operator_props.direction == '-Y':
                selected_object.location.y -= -move_factor * selected_object.dimensions.y
                
        # Set End Frame keyframes for Z Direction
        elif context.scene.curve_operator_props.direction == 'Z':
            selected_object.location.z += move_factor * selected_object.dimensions.z
            
        # Set End Frame keyframes for -Z Direction
        elif context.scene.curve_operator_props.direction == '-Z':
            selected_object.location.z -= move_factor * selected_object.dimensions.z
            
           

        # Reset location to original and set Start Frame keyframes
        selected_object.keyframe_insert(data_path="location", frame=start_frame)
        
        
        
        # Set keyframes for Scale at Start Frame
        selected_object.scale = (0, 0, 0)
        selected_object.keyframe_insert(data_path="scale", frame=start_frame)

        # Set keyframes for Scale at Mid Frame with cubic interpolation
        selected_object.scale = (1, 1, 1)
        selected_object.keyframe_insert(data_path="scale", frame=mid_frame)
        
        # Redraw the UI to simulate a click
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
        
        

        return {'FINISHED'}

   
class CurveOperator02(BaseCurveOperator):
    bl_idname = "object.generate_curve_02"
    bl_label = "Generate Curve 02"
    bl_description = "ِAnimate the selected object alonge curve 02"

    def execute(self, context):
        

        # Check if there is an active object
        if context.active_object is not None and context.active_object.type == 'MESH':
            selected_object = context.active_object
            
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            
            # Delete existing keyframes on angle and scale properties
            selected_object.animation_data_clear()

            if 'scale' in selected_object and selected_object['scale']:
                selected_object.keyframe_delete(data_path='["scale"]')
            
            # Check if there is a Curve Modifier on the selected object and remove it
            curve_modifier = next((modifier for modifier in selected_object.modifiers if modifier.type == 'CURVE'), None)
            if curve_modifier:
                selected_object.modifiers.remove(curve_modifier)
                
                   
            # Store the original dimensions of the selected object
            original_x_dimension = selected_object.dimensions.x
            original_y_dimension = selected_object.dimensions.y
            original_z_dimension = selected_object.dimensions.z

            # Set the origin point of the selected object to the center of its geometry
            bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')  

            # Append the curve object from the external blend file
            blend_file_path = addon_dirc + "/Assets.blend"
            curve_object_name = "Curve Twist 02"
            base_name = "Animation Curve2"  # Base name for the new curve objects

            # Check if the object already exists in the scene
            existing_objects = [obj for obj in bpy.data.objects if obj.name.startswith(base_name)]
            existing_object = next((obj for obj in existing_objects if obj.name == curve_object_name), None)

            if existing_object:
                # Update the existing object
                curve_object = existing_object
                curve_object.data = bpy.data.objects[curve_object_name].data.copy()
            else:
                # Create a new object
                with bpy.data.libraries.load(blend_file_path) as (data_from, data_to):
                    if curve_object_name in data_from.objects:
                        data_to.objects = [curve_object_name]

                # Check if the object is loaded
                if curve_object_name in bpy.data.objects:
                    curve_object = bpy.data.objects[curve_object_name]

                    # Create a new object and link the data from the appended curve object
                    new_object_name = base_name + str(len(existing_objects)).zfill(3)
                    curve_object = curve_object.copy()
                    curve_object.name = new_object_name
                    bpy.context.collection.objects.link(curve_object)  # Link to the active collection
                    
                    
                    
                    
              
        curve_scale = context.scene.curve_operator_props.curve_scale
        
        if context.scene.curve_operator_props.direction == 'X':
            # Rotate the curve object -90 degrees on the Z axis
            bpy.context.view_layer.objects.active = curve_object
            bpy.context.object.rotation_euler = (0, 0, math.radians(-90))
                    
                        
            # Set the scale factor based on x dimension
            scale_factor = (selected_object.dimensions.x / 3) * curve_scale
            curve_object.scale = (scale_factor, scale_factor, scale_factor)
                        
            curve_object.location.x = selected_object.location.x 
            curve_object.location.y = selected_object.location.y + (selected_object.dimensions.y / 2 + selected_object.dimensions.z / 2) / 2
            curve_object.location.z = selected_object.location.z - (selected_object.dimensions.y / 2 + selected_object.dimensions.z / 2) / 2

            # Set the curve modifier on the selected object
            curve_modifier = selected_object.modifiers.new(name="Curve Modifier", type='CURVE')
            curve_modifier.deform_axis = 'POS_Y'  # Set the deform axis to 'POS_Y'
            curve_modifier.object = curve_object  # Set the new curve object
                
            # Rotate the selected object 180 degrees on the y axis
            selected_object.rotation_euler.x = math.radians(90)
            selected_object.rotation_euler.y = math.radians(180)
                    
        elif context.scene.curve_operator_props.direction == 'Y':
                        
            # Set the scale factor based on y dimension
            scale_factor = (selected_object.dimensions.y / 3) * curve_scale
            curve_object.scale = (scale_factor, scale_factor, scale_factor)
                        
            curve_object.location.x = selected_object.location.x - (selected_object.dimensions.x / 2 + selected_object.dimensions.z / 2) / 2  # Half the X dimension
            curve_object.location.y = selected_object.location.y
            curve_object.location.z = selected_object.location.z - (selected_object.dimensions.x / 2 + selected_object.dimensions.z / 2) / 2
                    
            # Set the curve modifier on the selected object
            curve_modifier = selected_object.modifiers.new(name="Curve Modifier", type='CURVE')
            curve_modifier.deform_axis = 'POS_Y'  # Set the deform axis to 'POS_Y'
            curve_modifier.object = curve_object  # Set the new curve object
                
            # Rotate the selected object 180 degrees on the x axis
            selected_object.rotation_euler.x = math.radians(180)
            selected_object.rotation_euler.y = math.radians(-90)
                
            
        
        
        
        elif context.scene.curve_operator_props.direction == '-X':
            # Rotate the curve object -90 degrees on the Z axis
            bpy.context.view_layer.objects.active = curve_object
            bpy.context.object.rotation_euler = (0, 0, math.radians(90))
                    
                        
            # Set the scale factor based on x dimension
            scale_factor = (selected_object.dimensions.x / 3) * curve_scale
            curve_object.scale = (scale_factor, scale_factor, scale_factor)
                        
            curve_object.location.x = selected_object.location.x 
            curve_object.location.y = selected_object.location.y - (selected_object.dimensions.y / 2 + selected_object.dimensions.z / 2) / 2
            curve_object.location.z = selected_object.location.z - (selected_object.dimensions.y / 2 + selected_object.dimensions.z / 2) / 2

            # Set the curve modifier on the selected object
            curve_modifier = selected_object.modifiers.new(name="Curve Modifier", type='CURVE')
            curve_modifier.deform_axis = 'POS_Y'  # Set the deform axis to 'POS_Y'
            curve_modifier.object = curve_object  # Set the new curve object
                
            # Rotate the selected object 180 degrees on the y axis
            selected_object.rotation_euler.x = math.radians(-90)
            selected_object.rotation_euler.y = math.radians(180)
                    
        elif context.scene.curve_operator_props.direction == '-Y':
            # Rotate the curve object 180 degrees on the Z axis
            bpy.context.view_layer.objects.active = curve_object
            bpy.context.object.rotation_euler = (0, 0, math.radians(180))
                        
            # Set the scale factor based on y dimension
            scale_factor = (selected_object.dimensions.y / 3) * curve_scale
            curve_object.scale = (scale_factor, scale_factor, scale_factor)
                        
            curve_object.location.x = selected_object.location.x + (selected_object.dimensions.x / 2 + selected_object.dimensions.z / 2) / 2  # Half the X dimension
            curve_object.location.y = selected_object.location.y
            curve_object.location.z = selected_object.location.z - (selected_object.dimensions.x / 2 + selected_object.dimensions.z / 2) / 2
                        
            # Set the curve modifier on the selected object
            curve_modifier = selected_object.modifiers.new(name="Curve Modifier", type='CURVE')
            curve_modifier.deform_axis = 'POS_Y'  # Set the deform axis to 'POS_Y'
            curve_modifier.object = curve_object  # Set the new curve object
                
            # Rotate the selected object 180 degrees on the x axis
            selected_object.rotation_euler.x = math.radians(180)
            selected_object.rotation_euler.y = math.radians(90)
                
                
        elif context.scene.curve_operator_props.direction == 'Z':

            if original_y_dimension <= 2*original_x_dimension:
                bpy.context.view_layer.objects.active = curve_object
                bpy.context.object.rotation_euler = (math.radians(-90), 0, math.radians(180))
            else:
                bpy.context.view_layer.objects.active = curve_object
                bpy.context.object.rotation_euler = (math.radians(-90), 0, math.radians(-90))
                        
            # Set the scale factor based on z dimension
            scale_factor = (selected_object.dimensions.z / 3) * curve_scale
            curve_object.scale = (scale_factor, scale_factor, scale_factor)
                        
            curve_object.location.z = selected_object.location.z
            curve_object.location.y = selected_object.location.y
            curve_object.location.x = selected_object.location.x 
            
            # Set the curve modifier on the selected object
            curve_modifier = selected_object.modifiers.new(name="Curve Modifier", type='CURVE')
            curve_modifier.deform_axis = 'POS_Y'  # Set the deform axis to 'POS_Y'
            curve_modifier.object = curve_object  # Set the new curve object
            
            if original_y_dimension <= 2*original_x_dimension:
                # Rotate the selected object 180 degrees on the Y axis
                selected_object.rotation_euler.y = math.radians(180)
                selected_object.rotation_euler.z = math.radians(-90)
            else:
                # Rotate the selected object 180 degrees on the Y axis
                selected_object.rotation_euler.y = math.radians(180)
                selected_object.rotation_euler.z = math.radians(90)


            pass
        
        elif context.scene.curve_operator_props.direction == '-Z':
            
            if original_y_dimension <= 2*original_x_dimension:
                bpy.context.view_layer.objects.active = curve_object
                bpy.context.object.rotation_euler = (math.radians(90), 0, math.radians(360))
            else:
                bpy.context.view_layer.objects.active = curve_object
                bpy.context.object.rotation_euler = (math.radians(90), 0, math.radians(90))

            # Set the scale factor based on z dimension
            scale_factor = (selected_object.dimensions.z / 3) * curve_scale
            curve_object.scale = (scale_factor, scale_factor, scale_factor)

            curve_object.location.z = selected_object.location.z
            curve_object.location.y = selected_object.location.y
            curve_object.location.x = selected_object.location.x 

            # Set the curve modifier on the selected object
            curve_modifier = selected_object.modifiers.new(name="Curve Modifier", type='CURVE')
            curve_modifier.deform_axis = 'POS_Y'  # Set the deform axis to 'POS_Y'
            curve_modifier.object = curve_object  # Set the new curve object
            
            if original_y_dimension <= 2*original_x_dimension:
                # Rotate the selected object 180 degrees on the Y axis
                selected_object.rotation_euler.y = math.radians(180)
                selected_object.rotation_euler.z = math.radians(90)
            else:
                # Rotate the selected object 180 degrees on the Y axis
                selected_object.rotation_euler.y = math.radians(180)
                selected_object.rotation_euler.z = math.radians(-90)
                
            
            pass
        
        
        
        # Store the original location of the selected object
        original_location = selected_object.location.copy()
        
        

        # Calculate End Frame and Start Frame values
        end_frame = context.scene.curve_operator_props.end_frame
        start_frame = context.scene.curve_operator_props.start_frame
        mid_frame = (context.scene.curve_operator_props.start_frame + context.scene.curve_operator_props.end_frame) / 2
        move_factor = 3.3 * curve_scale if context.scene.curve_operator_props.direction == 'X,Y,Z' else -3.3 * curve_scale
        
        
        # Set keyframes
        selected_object.location = original_location
        selected_object.keyframe_insert(data_path="location", frame=end_frame)

        # Set End Frame keyframes for X/Y Direction
        if context.scene.curve_operator_props.direction == 'X':
            selected_object.location.x += -move_factor * selected_object.dimensions.x
        elif context.scene.curve_operator_props.direction == 'Y':
            selected_object.location.y += -move_factor * selected_object.dimensions.y

        # Set End Frame keyframes for -X/-Y Direction
        elif context.scene.curve_operator_props.direction == '-X':
            selected_object.location.x -= -move_factor * selected_object.dimensions.x
        elif context.scene.curve_operator_props.direction == '-Y':
            selected_object.location.y -= -move_factor * selected_object.dimensions.y
                
        # Set End Frame keyframes for Z Direction
        elif context.scene.curve_operator_props.direction == 'Z':
            selected_object.location.z += move_factor * selected_object.dimensions.z
            
            
        # Set End Frame keyframes for -Z Direction
        elif context.scene.curve_operator_props.direction == '-Z':
            selected_object.location.z -= move_factor * selected_object.dimensions.z
            
           

        # Reset location to original and set Start Frame keyframes
        selected_object.keyframe_insert(data_path="location", frame=start_frame)
        
        
        
        # Set keyframes for Scale at Start Frame
        selected_object.scale = (0, 0, 0)
        selected_object.keyframe_insert(data_path="scale", frame=start_frame)

        # Set keyframes for Scale at Mid Frame with cubic interpolation
        selected_object.scale = (1, 1, 1)
        selected_object.keyframe_insert(data_path="scale", frame=mid_frame)
        
        # Redraw the UI to simulate a click
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
        


        
        return {'FINISHED'}
    
 
class CurveOperator03(BaseCurveOperator):
    bl_idname = "object.generate_curve_03"
    bl_label = "Generate Curve 03"
    bl_description = "ِAnimate the selected object alonge curve 03"

    def execute(self, context):
        
              
        # Check if there is an active object
        if context.active_object is not None and context.active_object.type == 'MESH':
            selected_object = context.active_object
            
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            
            # Delete existing keyframes on angle and scale properties
            selected_object.animation_data_clear()

            if 'scale' in selected_object and selected_object['scale']:
                selected_object.keyframe_delete(data_path='["scale"]')
            
            # Check if there is a Curve Modifier on the selected object and remove it
            curve_modifier = next((modifier for modifier in selected_object.modifiers if modifier.type == 'CURVE'), None)
            if curve_modifier:
                selected_object.modifiers.remove(curve_modifier)
                
                    
            # Store the original dimensions of the selected object
            original_x_dimension = selected_object.dimensions.x
            original_y_dimension = selected_object.dimensions.y
            original_z_dimension = selected_object.dimensions.z

            # Set the origin point of the selected object to the center of its geometry
            bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')  

            # Append the curve object from the external blend file
            blend_file_path = addon_dirc + "/Assets.blend"
            curve_object_name = "Curve Twist 03"
            base_name = "Animation Curve3"  # Base name for the new curve objects

            # Check if the object already exists in the scene
            existing_objects = [obj for obj in bpy.data.objects if obj.name.startswith(base_name)]
            existing_object = next((obj for obj in existing_objects if obj.name == curve_object_name), None)

            if existing_object:
                # Update the existing object
                curve_object = existing_object
                curve_object.data = bpy.data.objects[curve_object_name].data.copy()
            else:
                # Create a new object
                with bpy.data.libraries.load(blend_file_path) as (data_from, data_to):
                    if curve_object_name in data_from.objects:
                        data_to.objects = [curve_object_name]

                # Check if the object is loaded
                if curve_object_name in bpy.data.objects:
                    curve_object = bpy.data.objects[curve_object_name]

                    # Create a new object and link the data from the appended curve object
                    new_object_name = base_name + str(len(existing_objects)).zfill(3)
                    curve_object = curve_object.copy()
                    curve_object.name = new_object_name
                    bpy.context.collection.objects.link(curve_object)  # Link to the active collection
                    
                    
                    
                    
              

        curve_scale = context.scene.curve_operator_props.curve_scale
        
        if context.scene.curve_operator_props.direction == 'X':
            # Rotate the curve object -90 degrees on the Z axis
            bpy.context.view_layer.objects.active = curve_object
            bpy.context.object.rotation_euler = (0, 0, math.radians(-90))
                    
                        
            # Set the scale factor based on x dimension
            scale_factor = (selected_object.dimensions.x / 3) * curve_scale
            curve_object.scale = (scale_factor, scale_factor, scale_factor)
                        
            curve_object.location.x = selected_object.location.x 
            curve_object.location.y = selected_object.location.y + (selected_object.dimensions.y / 2 + selected_object.dimensions.z / 2) / 2
            curve_object.location.z = selected_object.location.z - (selected_object.dimensions.y / 2 + selected_object.dimensions.z / 2) / 2

            # Set the curve modifier on the selected object
            curve_modifier = selected_object.modifiers.new(name="Curve Modifier", type='CURVE')
            curve_modifier.deform_axis = 'POS_Y'  # Set the deform axis to 'POS_Y'
            curve_modifier.object = curve_object  # Set the new curve object
                
            # Rotate the selected object 180 degrees on the y axis
            selected_object.rotation_euler.x = math.radians(90)
            selected_object.rotation_euler.y = math.radians(180)
                    
        elif context.scene.curve_operator_props.direction == 'Y':
                        
            # Set the scale factor based on y dimension
            scale_factor = (selected_object.dimensions.y / 3) * curve_scale
            curve_object.scale = (scale_factor, scale_factor, scale_factor)
                        
            curve_object.location.x = selected_object.location.x - (selected_object.dimensions.x / 2 + selected_object.dimensions.z / 2) / 2  # Half the X dimension
            curve_object.location.y = selected_object.location.y
            curve_object.location.z = selected_object.location.z - (selected_object.dimensions.x / 2 + selected_object.dimensions.z / 2) / 2
                        
            # Set the curve modifier on the selected object
            curve_modifier = selected_object.modifiers.new(name="Curve Modifier", type='CURVE')
            curve_modifier.deform_axis = 'POS_Y'  # Set the deform axis to 'POS_Y'
            curve_modifier.object = curve_object  # Set the new curve object
                
            # Rotate the selected object 180 degrees on the x axis
            selected_object.rotation_euler.x = math.radians(180)
            selected_object.rotation_euler.y = math.radians(-90)
                
        
        
        elif context.scene.curve_operator_props.direction == '-X':
            # Rotate the curve object -90 degrees on the Z axis
            bpy.context.view_layer.objects.active = curve_object
            bpy.context.object.rotation_euler = (0, 0, math.radians(90))
                    
                        
            # Set the scale factor based on x dimension
            scale_factor = (selected_object.dimensions.x / 3) * curve_scale
            curve_object.scale = (scale_factor, scale_factor, scale_factor)
                        
            curve_object.location.x = selected_object.location.x 
            curve_object.location.y = selected_object.location.y - (selected_object.dimensions.y / 2 + selected_object.dimensions.z / 2) / 2
            curve_object.location.z = selected_object.location.z - (selected_object.dimensions.y / 2 + selected_object.dimensions.z / 2) / 2

            # Set the curve modifier on the selected object
            curve_modifier = selected_object.modifiers.new(name="Curve Modifier", type='CURVE')
            curve_modifier.deform_axis = 'POS_Y'  # Set the deform axis to 'POS_Y'
            curve_modifier.object = curve_object  # Set the new curve object
                
            # Rotate the selected object 180 degrees on the y axis
            selected_object.rotation_euler.x = math.radians(-90)
            selected_object.rotation_euler.y = math.radians(180)
                    
        elif context.scene.curve_operator_props.direction == '-Y':
                # Rotate the curve object 180 degrees on the Z axis
                bpy.context.view_layer.objects.active = curve_object
                bpy.context.object.rotation_euler = (0, 0, math.radians(180))
                        
                # Set the scale factor based on y dimension
                scale_factor = (selected_object.dimensions.y / 3) * curve_scale
                curve_object.scale = (scale_factor, scale_factor, scale_factor)
                        
                curve_object.location.x = selected_object.location.x + (selected_object.dimensions.x / 2 + selected_object.dimensions.z / 2) / 2  # Half the X dimension
                curve_object.location.y = selected_object.location.y
                curve_object.location.z = selected_object.location.z - (selected_object.dimensions.x / 2 + selected_object.dimensions.z / 2) / 2
                        
                # Set the curve modifier on the selected object
                curve_modifier = selected_object.modifiers.new(name="Curve Modifier", type='CURVE')
                curve_modifier.deform_axis = 'POS_Y'  # Set the deform axis to 'POS_Y'
                curve_modifier.object = curve_object  # Set the new curve object
                
                # Rotate the selected object 180 degrees on the x axis
                selected_object.rotation_euler.x = math.radians(180)
                selected_object.rotation_euler.y = math.radians(90)
                
        elif context.scene.curve_operator_props.direction == 'Z':
            if original_y_dimension <= 2*original_x_dimension:
                bpy.context.view_layer.objects.active = curve_object
                bpy.context.object.rotation_euler = (math.radians(-90), 0, math.radians(180))
            else:
                bpy.context.view_layer.objects.active = curve_object
                bpy.context.object.rotation_euler = (math.radians(-90), 0, math.radians(-90))
                        
            # Set the scale factor based on z dimension
            scale_factor = (selected_object.dimensions.z / 3) * curve_scale
            curve_object.scale = (scale_factor, scale_factor, scale_factor)
                        
            curve_object.location.z = selected_object.location.z
            curve_object.location.y = selected_object.location.y
            curve_object.location.x = selected_object.location.x 
            
            # Set the curve modifier on the selected object
            curve_modifier = selected_object.modifiers.new(name="Curve Modifier", type='CURVE')
            curve_modifier.deform_axis = 'POS_Y'  # Set the deform axis to 'POS_Y'
            curve_modifier.object = curve_object  # Set the new curve object
            
            if original_y_dimension <= 2*original_x_dimension:
                # Rotate the selected object 180 degrees on the Y axis
                selected_object.rotation_euler.y = math.radians(180)
                selected_object.rotation_euler.z = math.radians(-90)
            else:
                # Rotate the selected object 180 degrees on the Y axis
                selected_object.rotation_euler.y = math.radians(180)
                selected_object.rotation_euler.z = math.radians(90)
            


            pass
        
        elif context.scene.curve_operator_props.direction == '-Z':
            if original_y_dimension <= 2*original_x_dimension:
                bpy.context.view_layer.objects.active = curve_object
                bpy.context.object.rotation_euler = (math.radians(90), 0, math.radians(360))
            else:
                bpy.context.view_layer.objects.active = curve_object
                bpy.context.object.rotation_euler = (math.radians(90), 0, math.radians(90))


            # Set the scale factor based on z dimension
            scale_factor = (selected_object.dimensions.z / 3) * curve_scale
            curve_object.scale = (scale_factor, scale_factor, scale_factor)

            curve_object.location.z = selected_object.location.z
            curve_object.location.y = selected_object.location.y
            curve_object.location.x = selected_object.location.x 

            # Set the curve modifier on the selected object
            curve_modifier = selected_object.modifiers.new(name="Curve Modifier", type='CURVE')
            curve_modifier.deform_axis = 'POS_Y'  # Set the deform axis to 'POS_Y'
            curve_modifier.object = curve_object  # Set the new curve object

            if original_y_dimension <= 2*original_x_dimension:
                # Rotate the selected object 180 degrees on the Y axis
                selected_object.rotation_euler.y = math.radians(180)
                selected_object.rotation_euler.z = math.radians(90)
            else:
                # Rotate the selected object 180 degrees on the Y axis
                selected_object.rotation_euler.y = math.radians(180)
                selected_object.rotation_euler.z = math.radians(-90)
            
            pass
        
        
        
        # Store the original location of the selected object
        original_location = selected_object.location.copy()
        
        

        # Calculate End Frame and Start Frame values
        end_frame = context.scene.curve_operator_props.end_frame
        start_frame = context.scene.curve_operator_props.start_frame
        mid_frame = (context.scene.curve_operator_props.start_frame + context.scene.curve_operator_props.end_frame) / 2
        move_factor = 3.3 * curve_scale if context.scene.curve_operator_props.direction == 'X,Y,Z' else -3.3 * curve_scale
        
        
        # Set keyframes
        selected_object.location = original_location
        selected_object.keyframe_insert(data_path="location", frame=end_frame)

        # Set End Frame keyframes for X/Y Direction
        if context.scene.curve_operator_props.direction == 'X':
            selected_object.location.x += -move_factor * selected_object.dimensions.x
        elif context.scene.curve_operator_props.direction == 'Y':
                selected_object.location.y += -move_factor * selected_object.dimensions.y

        # Set End Frame keyframes for -X/-Y Direction
        elif context.scene.curve_operator_props.direction == '-X':
            selected_object.location.x -= -move_factor * selected_object.dimensions.x
        elif context.scene.curve_operator_props.direction == '-Y':
                selected_object.location.y -= -move_factor * selected_object.dimensions.y
                
        # Set End Frame keyframes for Z Direction
        elif context.scene.curve_operator_props.direction == 'Z':
            selected_object.location.z += move_factor * selected_object.dimensions.z
            
        
        # Set End Frame keyframes for -Z Direction
        elif context.scene.curve_operator_props.direction == '-Z':
            selected_object.location.z -= move_factor * selected_object.dimensions.z
            
            
            
            
           

        # Reset location to original and set Start Frame keyframes
        selected_object.keyframe_insert(data_path="location", frame=start_frame)
        
        
        
        # Set keyframes for Scale at Start Frame
        selected_object.scale = (0, 0, 0)
        selected_object.keyframe_insert(data_path="scale", frame=start_frame)

        # Set keyframes for Scale at Mid Frame with cubic interpolation
        selected_object.scale = (1, 1, 1)
        selected_object.keyframe_insert(data_path="scale", frame=mid_frame)
        
        # Redraw the UI to simulate a click
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
        


        
        
        return {'FINISHED'}

  
class CurveOperator04(BaseCurveOperator):
    bl_idname = "object.generate_curve_04"
    bl_label = "Generate Curve 04"
    bl_description = "ِAnimate the selected object alonge curve 04"
    

    
    def execute(self, context):
                      
        # Check if there is an active object
        if context.active_object is not None and context.active_object.type == 'MESH':
            selected_object = context.active_object
            
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            
            # Delete existing keyframes on angle and scale properties
            selected_object.animation_data_clear()

            if 'scale' in selected_object and selected_object['scale']:
                selected_object.keyframe_delete(data_path='["scale"]')
            
            # Check if there is a Curve Modifier on the selected object and remove it
            curve_modifier = next((modifier for modifier in selected_object.modifiers if modifier.type == 'CURVE'), None)
            if curve_modifier:
                selected_object.modifiers.remove(curve_modifier)
                
                    
            # Store the original dimensions of the selected object
            original_x_dimension = selected_object.dimensions.x
            original_y_dimension = selected_object.dimensions.y
            original_z_dimension = selected_object.dimensions.z

            # Set the origin point of the selected object to the center of its geometry
            bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')  

            # Append the curve object from the external blend file
            blend_file_path = addon_dirc + "/Assets.blend"
            curve_object_name = "Curve Twist 04"
            base_name = "Animation Curve"  # Base name for the new curve objects

            # Check if the object already exists in the scene
            existing_objects = [obj for obj in bpy.data.objects if obj.name.startswith(base_name)]
            existing_object = next((obj for obj in existing_objects if obj.name == curve_object_name), None)

            if existing_object:
                # Update the existing object
                curve_object = existing_object
                curve_object.data = bpy.data.objects[curve_object_name].data.copy()
            else:
                # Create a new object
                with bpy.data.libraries.load(blend_file_path) as (data_from, data_to):
                    if curve_object_name in data_from.objects:
                        data_to.objects = [curve_object_name]

                # Check if the object is loaded
                if curve_object_name in bpy.data.objects:
                    curve_object = bpy.data.objects[curve_object_name]

                    # Create a new object and link the data from the appended curve object
                    new_object_name = base_name + str(len(existing_objects)).zfill(3)
                    curve_object = curve_object.copy()
                    curve_object.name = new_object_name
                    bpy.context.collection.objects.link(curve_object)  # Link to the active collection
                    
                    
                    
                    
              

        curve_scale = context.scene.curve_operator_props.curve_scale
        
        if context.scene.curve_operator_props.direction == 'X':
            bpy.context.view_layer.objects.active = curve_object
            bpy.context.object.rotation_euler = (0, 0, math.radians(-90))
                    
                        
            # Set the scale factor based on x dimension
            scale_factor = (selected_object.dimensions.x / 3) * curve_scale
            curve_object.scale = (scale_factor, scale_factor, scale_factor)
                        
            curve_object.location.x = selected_object.location.x 
            curve_object.location.y = selected_object.location.y + (selected_object.dimensions.y / 2 + selected_object.dimensions.z / 2) / 2
            curve_object.location.z = selected_object.location.z - (selected_object.dimensions.y / 2 + selected_object.dimensions.z / 2) / 2

            # Set the curve modifier on the selected object
            curve_modifier = selected_object.modifiers.new(name="Curve Modifier", type='CURVE')
            curve_modifier.deform_axis = 'POS_Y'  # Set the deform axis to 'POS_Y'
            curve_modifier.object = curve_object  # Set the new curve object
                
            # Rotate the selected object 180 degrees on the y axis
            selected_object.rotation_euler.x = math.radians(90)
            selected_object.rotation_euler.y = math.radians(180)
                    
        elif context.scene.curve_operator_props.direction == 'Y':
                        
            # Set the scale factor based on y dimension
            scale_factor = (selected_object.dimensions.y / 3) * curve_scale
            curve_object.scale = (scale_factor, scale_factor, scale_factor)
                        
            curve_object.location.x = selected_object.location.x - (selected_object.dimensions.x / 2 + selected_object.dimensions.z / 2) / 2  # Half the X dimension
            curve_object.location.y = selected_object.location.y
            curve_object.location.z = selected_object.location.z - (selected_object.dimensions.x / 2 + selected_object.dimensions.z / 2) / 2
                        
            # Set the curve modifier on the selected object
            curve_modifier = selected_object.modifiers.new(name="Curve Modifier", type='CURVE')
            curve_modifier.deform_axis = 'POS_Y'  # Set the deform axis to 'POS_Y'
            curve_modifier.object = curve_object  # Set the new curve object
                
            # Rotate the selected object 180 degrees on the x axis
            selected_object.rotation_euler.x = math.radians(180)
            selected_object.rotation_euler.y = math.radians(-90)
                
        
        
        
        
        elif context.scene.curve_operator_props.direction == '-X':
            
            # Rotate the curve object -90 degrees on the Z axis
            bpy.context.view_layer.objects.active = curve_object
            bpy.context.object.rotation_euler = (0, 0, math.radians(90))
                    
                        
            # Set the scale factor based on x dimension
            scale_factor = (selected_object.dimensions.x / 3) * curve_scale
            curve_object.scale = (scale_factor, scale_factor, scale_factor)
                        
            curve_object.location.x = selected_object.location.x 
            curve_object.location.y = selected_object.location.y - (selected_object.dimensions.y / 2 + selected_object.dimensions.z / 2) / 2
            curve_object.location.z = selected_object.location.z - (selected_object.dimensions.y / 2 + selected_object.dimensions.z / 2) / 2

            # Set the curve modifier on the selected object
            curve_modifier = selected_object.modifiers.new(name="Curve Modifier", type='CURVE')
            curve_modifier.deform_axis = 'POS_Y'  # Set the deform axis to 'POS_Y'
            curve_modifier.object = curve_object  # Set the new curve object
                
            # Rotate the selected object 180 degrees on the y axis
            selected_object.rotation_euler.x = math.radians(-90)
            selected_object.rotation_euler.y = math.radians(180)
                    
        elif context.scene.curve_operator_props.direction == '-Y':
            # Rotate the curve object 180 degrees on the Z axis
            bpy.context.view_layer.objects.active = curve_object
            bpy.context.object.rotation_euler = (0, 0, math.radians(180))
                        
            # Set the scale factor based on y dimension
            scale_factor = (selected_object.dimensions.y / 3) * curve_scale
            curve_object.scale = (scale_factor, scale_factor, scale_factor)
                        
            curve_object.location.x = selected_object.location.x + (selected_object.dimensions.x / 2 + selected_object.dimensions.z / 2) / 2  # Half the X dimension
            curve_object.location.y = selected_object.location.y
            curve_object.location.z = selected_object.location.z - (selected_object.dimensions.x / 2 + selected_object.dimensions.z / 2) / 2
                        
            # Set the curve modifier on the selected object
            curve_modifier = selected_object.modifiers.new(name="Curve Modifier", type='CURVE')
            curve_modifier.deform_axis = 'POS_Y'  # Set the deform axis to 'POS_Y'
            curve_modifier.object = curve_object  # Set the new curve object
                
            # Rotate the selected object 180 degrees on the x axis
            selected_object.rotation_euler.x = math.radians(180)
            selected_object.rotation_euler.y = math.radians(90)
                
        elif context.scene.curve_operator_props.direction == 'Z':
            if original_y_dimension <= 2*original_x_dimension:
                bpy.context.view_layer.objects.active = curve_object
                bpy.context.object.rotation_euler = (math.radians(-90), 0, math.radians(180))
            else:
                bpy.context.view_layer.objects.active = curve_object
                bpy.context.object.rotation_euler = (math.radians(-90), 0, math.radians(-90))
                        
            # Set the scale factor based on z dimension
            scale_factor = (selected_object.dimensions.z / 3) * curve_scale
            curve_object.scale = (scale_factor, scale_factor, scale_factor)
                        
            curve_object.location.z = selected_object.location.z
            curve_object.location.y = selected_object.location.y
            curve_object.location.x = selected_object.location.x 
            
            # Set the curve modifier on the selected object
            curve_modifier = selected_object.modifiers.new(name="Curve Modifier", type='CURVE')
            curve_modifier.deform_axis = 'POS_Y'  # Set the deform axis to 'POS_Y'
            curve_modifier.object = curve_object  # Set the new curve object
            
            
            if original_y_dimension <= 2*original_x_dimension:
                # Rotate the selected object 180 degrees on the Y axis
                selected_object.rotation_euler.y = math.radians(180)
                selected_object.rotation_euler.z = math.radians(-90)
            else:
                # Rotate the selected object 180 degrees on the Y axis
                selected_object.rotation_euler.y = math.radians(180)
                selected_object.rotation_euler.z = math.radians(90)
            

            pass
        
        elif context.scene.curve_operator_props.direction == '-Z':
            if original_y_dimension <= 2*original_x_dimension:
                bpy.context.view_layer.objects.active = curve_object
                bpy.context.object.rotation_euler = (math.radians(90), 0, math.radians(360))
            else:
                bpy.context.view_layer.objects.active = curve_object
                bpy.context.object.rotation_euler = (math.radians(90), 0, math.radians(90))


            # Set the scale factor based on z dimension
            scale_factor = (selected_object.dimensions.z / 3) * curve_scale
            curve_object.scale = (scale_factor, scale_factor, scale_factor)

            curve_object.location.z = selected_object.location.z
            curve_object.location.y = selected_object.location.y
            curve_object.location.x = selected_object.location.x 

            # Set the curve modifier on the selected object
            curve_modifier = selected_object.modifiers.new(name="Curve Modifier", type='CURVE')
            curve_modifier.deform_axis = 'POS_Y'  # Set the deform axis to 'POS_Y'
            curve_modifier.object = curve_object  # Set the new curve object

            if original_y_dimension <= 2*original_x_dimension:
                # Rotate the selected object 180 degrees on the Y axis
                selected_object.rotation_euler.y = math.radians(180)
                selected_object.rotation_euler.z = math.radians(90)
            else:
                # Rotate the selected object 180 degrees on the Y axis
                selected_object.rotation_euler.y = math.radians(180)
                selected_object.rotation_euler.z = math.radians(-90)
            
            pass
        
        # Store the original location of the selected object
        original_location = selected_object.location.copy()
        
        

        # Calculate End Frame and Start Frame values
        end_frame = context.scene.curve_operator_props.end_frame
        start_frame = context.scene.curve_operator_props.start_frame
        mid_frame = (context.scene.curve_operator_props.start_frame + context.scene.curve_operator_props.end_frame) / 2
        move_factor = 4 * curve_scale if context.scene.curve_operator_props.direction == 'X,Y,Z' else -4 * curve_scale
        
        
        # Set keyframes
        selected_object.location = original_location
        selected_object.keyframe_insert(data_path="location", frame=end_frame)

        # Set End Frame keyframes for X/Y Direction
        if context.scene.curve_operator_props.direction == 'X':   
            selected_object.location.x += -move_factor * selected_object.dimensions.x
        elif context.scene.curve_operator_props.direction == 'Y':
                selected_object.location.y += -move_factor * selected_object.dimensions.y

        # Set End Frame keyframes for -X/-Y Direction
        elif context.scene.curve_operator_props.direction == '-X':   
            selected_object.location.x -= -move_factor * selected_object.dimensions.x
        elif context.scene.curve_operator_props.direction == '-Y':
                selected_object.location.y -= -move_factor * selected_object.dimensions.y
                
        # Set End Frame keyframes for Z Direction
        elif context.scene.curve_operator_props.direction == 'Z':
            selected_object.location.z += move_factor * selected_object.dimensions.z
            
        # Set End Frame keyframes for -Z Direction
        elif context.scene.curve_operator_props.direction == '-Z':
            selected_object.location.z -= move_factor * selected_object.dimensions.z
            
           

        # Reset location to original and set Start Frame keyframes
        selected_object.keyframe_insert(data_path="location", frame=start_frame)
        
        
        
        # Set keyframes for Scale at Start Frame
        selected_object.scale = (0, 0, 0)
        selected_object.keyframe_insert(data_path="scale", frame=start_frame)

        # Set keyframes for Scale at Mid Frame with cubic interpolation
        selected_object.scale = (1, 1, 1)
        selected_object.keyframe_insert(data_path="scale", frame=mid_frame)
        
        # Redraw the UI to simulate a click
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
        
            

        return {'FINISHED'}
    
       
class CurveOperator05(BaseCurveOperator):
    bl_idname = "object.generate_curve_05"
    bl_label = "Generate Curve 05"
    bl_description = "ِAnimate the selected object alonge curve 05"
    

    
    def execute(self, context):
                      
        # Check if there is an active object
        if context.active_object is not None and context.active_object.type == 'MESH':
            selected_object = context.active_object
            
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            
            # Delete existing keyframes on angle and scale properties
            selected_object.animation_data_clear()

            if 'scale' in selected_object and selected_object['scale']:
                selected_object.keyframe_delete(data_path='["scale"]')
            
            # Check if there is a Curve Modifier on the selected object and remove it
            curve_modifier = next((modifier for modifier in selected_object.modifiers if modifier.type == 'CURVE'), None)
            if curve_modifier:
                selected_object.modifiers.remove(curve_modifier)
                
                    
            # Store the original dimensions of the selected object
            original_x_dimension = selected_object.dimensions.x
            original_y_dimension = selected_object.dimensions.y
            original_z_dimension = selected_object.dimensions.z

            # Set the origin point of the selected object to the center of its geometry
            bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')  

            # Append the curve object from the external blend file
            blend_file_path = addon_dirc + "/Assets.blend"
            curve_object_name = "Curve Twist 05"
            base_name = "Animation Curve"  # Base name for the new curve objects

            # Check if the object already exists in the scene
            existing_objects = [obj for obj in bpy.data.objects if obj.name.startswith(base_name)]
            existing_object = next((obj for obj in existing_objects if obj.name == curve_object_name), None)

            if existing_object:
                # Update the existing object
                curve_object = existing_object
                curve_object.data = bpy.data.objects[curve_object_name].data.copy()
            else:
                # Create a new object
                with bpy.data.libraries.load(blend_file_path) as (data_from, data_to):
                    if curve_object_name in data_from.objects:
                        data_to.objects = [curve_object_name]

                # Check if the object is loaded
                if curve_object_name in bpy.data.objects:
                    curve_object = bpy.data.objects[curve_object_name]

                    # Create a new object and link the data from the appended curve object
                    new_object_name = base_name + str(len(existing_objects)).zfill(3)
                    curve_object = curve_object.copy()
                    curve_object.name = new_object_name
                    bpy.context.collection.objects.link(curve_object)  # Link to the active collection
                    
                    
                    
                    
              

        curve_scale = context.scene.curve_operator_props.curve_scale
        
        if context.scene.curve_operator_props.direction == 'X':
            bpy.context.view_layer.objects.active = curve_object
            bpy.context.object.rotation_euler = (0, 0, math.radians(-90))
                    
                        
            # Set the scale factor based on x dimension
            scale_factor = (selected_object.dimensions.x / 3) * curve_scale
            curve_object.scale = (scale_factor, scale_factor, scale_factor)
                        
            curve_object.location.x = selected_object.location.x 
            curve_object.location.y = selected_object.location.y + (selected_object.dimensions.y / 2 + selected_object.dimensions.z / 2) / 2
            curve_object.location.z = selected_object.location.z - (selected_object.dimensions.y / 2 + selected_object.dimensions.z / 2) / 2

            # Set the curve modifier on the selected object
            curve_modifier = selected_object.modifiers.new(name="Curve Modifier", type='CURVE')
            curve_modifier.deform_axis = 'POS_Y'  # Set the deform axis to 'POS_Y'
            curve_modifier.object = curve_object  # Set the new curve object
                
            # Rotate the selected object 180 degrees on the y axis
            selected_object.rotation_euler.x = math.radians(90)
            selected_object.rotation_euler.y = math.radians(180)
                    
        elif context.scene.curve_operator_props.direction == 'Y':
                        
            # Set the scale factor based on y dimension
            scale_factor = (selected_object.dimensions.y / 3) * curve_scale
            curve_object.scale = (scale_factor, scale_factor, scale_factor)
                        
            curve_object.location.x = selected_object.location.x - (selected_object.dimensions.x / 2 + selected_object.dimensions.z / 2) / 2  # Half the X dimension
            curve_object.location.y = selected_object.location.y
            curve_object.location.z = selected_object.location.z - (selected_object.dimensions.x / 2 + selected_object.dimensions.z / 2) / 2
                        
            # Set the curve modifier on the selected object
            curve_modifier = selected_object.modifiers.new(name="Curve Modifier", type='CURVE')
            curve_modifier.deform_axis = 'POS_Y'  # Set the deform axis to 'POS_Y'
            curve_modifier.object = curve_object  # Set the new curve object
                
            # Rotate the selected object 180 degrees on the x axis
            selected_object.rotation_euler.x = math.radians(180)
            selected_object.rotation_euler.y = math.radians(-90)
                
        
        
        
        
        elif context.scene.curve_operator_props.direction == '-X':
            
            # Rotate the curve object -90 degrees on the Z axis
            bpy.context.view_layer.objects.active = curve_object
            bpy.context.object.rotation_euler = (0, 0, math.radians(90))
                    
                        
            # Set the scale factor based on x dimension
            scale_factor = (selected_object.dimensions.x / 3) * curve_scale
            curve_object.scale = (scale_factor, scale_factor, scale_factor)
                        
            curve_object.location.x = selected_object.location.x 
            curve_object.location.y = selected_object.location.y - (selected_object.dimensions.y / 2 + selected_object.dimensions.z / 2) / 2
            curve_object.location.z = selected_object.location.z - (selected_object.dimensions.y / 2 + selected_object.dimensions.z / 2) / 2

            # Set the curve modifier on the selected object
            curve_modifier = selected_object.modifiers.new(name="Curve Modifier", type='CURVE')
            curve_modifier.deform_axis = 'POS_Y'  # Set the deform axis to 'POS_Y'
            curve_modifier.object = curve_object  # Set the new curve object
                
            # Rotate the selected object 180 degrees on the y axis
            selected_object.rotation_euler.x = math.radians(-90)
            selected_object.rotation_euler.y = math.radians(180)
                    
        elif context.scene.curve_operator_props.direction == '-Y':
            # Rotate the curve object 180 degrees on the Z axis
            bpy.context.view_layer.objects.active = curve_object
            bpy.context.object.rotation_euler = (0, 0, math.radians(180))
                        
            # Set the scale factor based on y dimension
            scale_factor = (selected_object.dimensions.y / 3) * curve_scale
            curve_object.scale = (scale_factor, scale_factor, scale_factor)
                        
            curve_object.location.x = selected_object.location.x + (selected_object.dimensions.x / 2 + selected_object.dimensions.z / 2) / 2  # Half the X dimension
            curve_object.location.y = selected_object.location.y
            curve_object.location.z = selected_object.location.z - (selected_object.dimensions.x / 2 + selected_object.dimensions.z / 2) / 2
                        
            # Set the curve modifier on the selected object
            curve_modifier = selected_object.modifiers.new(name="Curve Modifier", type='CURVE')
            curve_modifier.deform_axis = 'POS_Y'  # Set the deform axis to 'POS_Y'
            curve_modifier.object = curve_object  # Set the new curve object
                
            # Rotate the selected object 180 degrees on the x axis
            selected_object.rotation_euler.x = math.radians(180)
            selected_object.rotation_euler.y = math.radians(90)
                
        elif context.scene.curve_operator_props.direction == 'Z':
            if original_y_dimension <= 2*original_x_dimension:
                bpy.context.view_layer.objects.active = curve_object
                bpy.context.object.rotation_euler = (math.radians(-90), 0, math.radians(180))
            else:
                bpy.context.view_layer.objects.active = curve_object
                bpy.context.object.rotation_euler = (math.radians(-90), 0, math.radians(-90))
                        
            # Set the scale factor based on z dimension
            scale_factor = (selected_object.dimensions.z / 3) * curve_scale
            curve_object.scale = (scale_factor, scale_factor, scale_factor)
                        
            curve_object.location.z = selected_object.location.z
            curve_object.location.y = selected_object.location.y
            curve_object.location.x = selected_object.location.x 
            
            # Set the curve modifier on the selected object
            curve_modifier = selected_object.modifiers.new(name="Curve Modifier", type='CURVE')
            curve_modifier.deform_axis = 'POS_Y'  # Set the deform axis to 'POS_Y'
            curve_modifier.object = curve_object  # Set the new curve object
            
            
            if original_y_dimension <= 2*original_x_dimension:
                # Rotate the selected object 180 degrees on the Y axis
                selected_object.rotation_euler.y = math.radians(180)
                selected_object.rotation_euler.z = math.radians(-90)
            else:
                # Rotate the selected object 180 degrees on the Y axis
                selected_object.rotation_euler.y = math.radians(180)
                selected_object.rotation_euler.z = math.radians(90)
            

            pass
        
        elif context.scene.curve_operator_props.direction == '-Z':
            if original_y_dimension <= 2*original_x_dimension:
                bpy.context.view_layer.objects.active = curve_object
                bpy.context.object.rotation_euler = (math.radians(90), 0, math.radians(360))
            else:
                bpy.context.view_layer.objects.active = curve_object
                bpy.context.object.rotation_euler = (math.radians(90), 0, math.radians(90))


            # Set the scale factor based on z dimension
            scale_factor = (selected_object.dimensions.z / 3) * curve_scale
            curve_object.scale = (scale_factor, scale_factor, scale_factor)

            curve_object.location.z = selected_object.location.z
            curve_object.location.y = selected_object.location.y
            curve_object.location.x = selected_object.location.x 

            # Set the curve modifier on the selected object
            curve_modifier = selected_object.modifiers.new(name="Curve Modifier", type='CURVE')
            curve_modifier.deform_axis = 'POS_Y'  # Set the deform axis to 'POS_Y'
            curve_modifier.object = curve_object  # Set the new curve object

            if original_y_dimension <= 2*original_x_dimension:
                # Rotate the selected object 180 degrees on the Y axis
                selected_object.rotation_euler.y = math.radians(180)
                selected_object.rotation_euler.z = math.radians(90)
            else:
                # Rotate the selected object 180 degrees on the Y axis
                selected_object.rotation_euler.y = math.radians(180)
                selected_object.rotation_euler.z = math.radians(-90)
            
            pass
        
        # Store the original location of the selected object
        original_location = selected_object.location.copy()
        
        

        # Calculate End Frame and Start Frame values
        end_frame = context.scene.curve_operator_props.end_frame
        start_frame = context.scene.curve_operator_props.start_frame
        mid_frame = (context.scene.curve_operator_props.start_frame + context.scene.curve_operator_props.end_frame) / 2
        move_factor = 4.2 * curve_scale if context.scene.curve_operator_props.direction == 'X,Y,Z' else -4.2 * curve_scale
        
        
        # Set keyframes
        selected_object.location = original_location
        selected_object.keyframe_insert(data_path="location", frame=end_frame)

        # Set End Frame keyframes for X/Y Direction
        if context.scene.curve_operator_props.direction == 'X':   
            selected_object.location.x += -move_factor * selected_object.dimensions.x
        elif context.scene.curve_operator_props.direction == 'Y':
                selected_object.location.y += -move_factor * selected_object.dimensions.y

        # Set End Frame keyframes for -X/-Y Direction
        elif context.scene.curve_operator_props.direction == '-X':   
            selected_object.location.x -= -move_factor * selected_object.dimensions.x
        elif context.scene.curve_operator_props.direction == '-Y':
                selected_object.location.y -= -move_factor * selected_object.dimensions.y
                
        # Set End Frame keyframes for Z Direction
        elif context.scene.curve_operator_props.direction == 'Z':
            selected_object.location.z += move_factor * selected_object.dimensions.z
            
        # Set End Frame keyframes for -Z Direction
        elif context.scene.curve_operator_props.direction == '-Z':
            selected_object.location.z -= move_factor * selected_object.dimensions.z
            
           

        # Reset location to original and set Start Frame keyframes
        selected_object.keyframe_insert(data_path="location", frame=start_frame)
        
        
        
        # Set keyframes for Scale at Start Frame
        selected_object.scale = (0, 0, 0)
        selected_object.keyframe_insert(data_path="scale", frame=start_frame)

        # Set keyframes for Scale at Mid Frame with cubic interpolation
        selected_object.scale = (1, 1, 1)
        selected_object.keyframe_insert(data_path="scale", frame=mid_frame)
        
        # Redraw the UI to simulate a click
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
        
            

        return {'FINISHED'}
    
    
class CurveOperator06(BaseCurveOperator):
    bl_idname = "object.generate_curve_06"
    bl_label = "Generate Curve 06"
    bl_description = "ِAnimate the selected object alonge curve 06"
    

    
    def execute(self, context):
                      
        # Check if there is an active object
        if context.active_object is not None and context.active_object.type == 'MESH':
            selected_object = context.active_object
            
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            
            # Delete existing keyframes on angle and scale properties
            selected_object.animation_data_clear()

            if 'scale' in selected_object and selected_object['scale']:
                selected_object.keyframe_delete(data_path='["scale"]')
            
            
            # Check if there is a Curve Modifier on the selected object and remove it
            curve_modifier = next((modifier for modifier in selected_object.modifiers if modifier.type == 'CURVE'), None)
            if curve_modifier:
                selected_object.modifiers.remove(curve_modifier)
                    
            # Store the original dimensions of the selected object
            original_x_dimension = selected_object.dimensions.x
            original_y_dimension = selected_object.dimensions.y
            original_z_dimension = selected_object.dimensions.z

            # Set the origin point of the selected object to the center of its geometry
            bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')  

            # Append the curve object from the external blend file
            blend_file_path = addon_dirc + "/Assets.blend"
            curve_object_name = "Curve Twist 06"
            base_name = "Animation Curve"  # Base name for the new curve objects

            # Check if the object already exists in the scene
            existing_objects = [obj for obj in bpy.data.objects if obj.name.startswith(base_name)]
            existing_object = next((obj for obj in existing_objects if obj.name == curve_object_name), None)

            if existing_object:
                # Update the existing object
                curve_object = existing_object
                curve_object.data = bpy.data.objects[curve_object_name].data.copy()
            else:
                # Create a new object
                with bpy.data.libraries.load(blend_file_path) as (data_from, data_to):
                    if curve_object_name in data_from.objects:
                        data_to.objects = [curve_object_name]

                # Check if the object is loaded
                if curve_object_name in bpy.data.objects:
                    curve_object = bpy.data.objects[curve_object_name]

                    # Create a new object and link the data from the appended curve object
                    new_object_name = base_name + str(len(existing_objects)).zfill(3)
                    curve_object = curve_object.copy()
                    curve_object.name = new_object_name
                    bpy.context.collection.objects.link(curve_object)  # Link to the active collection
                    
                    
                    
                    
              

        curve_scale = context.scene.curve_operator_props.curve_scale
        
        if context.scene.curve_operator_props.direction == 'X':
            bpy.context.view_layer.objects.active = curve_object
            bpy.context.object.rotation_euler = (0, 0, math.radians(-90))
                    
                        
            # Set the scale factor based on x dimension
            scale_factor = (selected_object.dimensions.x / 3) * curve_scale
            curve_object.scale = (scale_factor, scale_factor, scale_factor)
                        
            curve_object.location.x = selected_object.location.x 
            curve_object.location.y = selected_object.location.y + (selected_object.dimensions.y / 2 + selected_object.dimensions.z / 2) / 2
            curve_object.location.z = selected_object.location.z - (selected_object.dimensions.y / 2 + selected_object.dimensions.z / 2) / 2

            # Set the curve modifier on the selected object
            curve_modifier = selected_object.modifiers.new(name="Curve Modifier", type='CURVE')
            curve_modifier.deform_axis = 'POS_Y'  # Set the deform axis to 'POS_Y'
            curve_modifier.object = curve_object  # Set the new curve object
                
            # Rotate the selected object 180 degrees on the y axis
            selected_object.rotation_euler.x = math.radians(90)
            selected_object.rotation_euler.y = math.radians(180)
                    
        elif context.scene.curve_operator_props.direction == 'Y':
                        
            # Set the scale factor based on y dimension
            scale_factor = (selected_object.dimensions.y / 3) * curve_scale
            curve_object.scale = (scale_factor, scale_factor, scale_factor)
                        
            curve_object.location.x = selected_object.location.x - (selected_object.dimensions.x / 2 + selected_object.dimensions.z / 2) / 2  # Half the X dimension
            curve_object.location.y = selected_object.location.y
            curve_object.location.z = selected_object.location.z - (selected_object.dimensions.x / 2 + selected_object.dimensions.z / 2) / 2
                        
            # Set the curve modifier on the selected object
            curve_modifier = selected_object.modifiers.new(name="Curve Modifier", type='CURVE')
            curve_modifier.deform_axis = 'POS_Y'  # Set the deform axis to 'POS_Y'
            curve_modifier.object = curve_object  # Set the new curve object
                
            # Rotate the selected object 180 degrees on the x axis
            selected_object.rotation_euler.x = math.radians(180)
            selected_object.rotation_euler.y = math.radians(-90)
                
        
        
        
        
        elif context.scene.curve_operator_props.direction == '-X':
            
            # Rotate the curve object -90 degrees on the Z axis
            bpy.context.view_layer.objects.active = curve_object
            bpy.context.object.rotation_euler = (0, 0, math.radians(90))
                    
                        
            # Set the scale factor based on x dimension
            scale_factor = (selected_object.dimensions.x / 3) * curve_scale
            curve_object.scale = (scale_factor, scale_factor, scale_factor)
                        
            curve_object.location.x = selected_object.location.x 
            curve_object.location.y = selected_object.location.y - (selected_object.dimensions.y / 2 + selected_object.dimensions.z / 2) / 2
            curve_object.location.z = selected_object.location.z - (selected_object.dimensions.y / 2 + selected_object.dimensions.z / 2) / 2

            # Set the curve modifier on the selected object
            curve_modifier = selected_object.modifiers.new(name="Curve Modifier", type='CURVE')
            curve_modifier.deform_axis = 'POS_Y'  # Set the deform axis to 'POS_Y'
            curve_modifier.object = curve_object  # Set the new curve object
                
            # Rotate the selected object 180 degrees on the y axis
            selected_object.rotation_euler.x = math.radians(-90)
            selected_object.rotation_euler.y = math.radians(180)
                    
        elif context.scene.curve_operator_props.direction == '-Y':
            # Rotate the curve object 180 degrees on the Z axis
            bpy.context.view_layer.objects.active = curve_object
            bpy.context.object.rotation_euler = (0, 0, math.radians(180))
                        
            # Set the scale factor based on y dimension
            scale_factor = (selected_object.dimensions.y / 3) * curve_scale
            curve_object.scale = (scale_factor, scale_factor, scale_factor)
                        
            curve_object.location.x = selected_object.location.x + (selected_object.dimensions.x / 2 + selected_object.dimensions.z / 2) / 2  # Half the X dimension
            curve_object.location.y = selected_object.location.y
            curve_object.location.z = selected_object.location.z - (selected_object.dimensions.x / 2 + selected_object.dimensions.z / 2) / 2
                        
            # Set the curve modifier on the selected object
            curve_modifier = selected_object.modifiers.new(name="Curve Modifier", type='CURVE')
            curve_modifier.deform_axis = 'POS_Y'  # Set the deform axis to 'POS_Y'
            curve_modifier.object = curve_object  # Set the new curve object
                
            # Rotate the selected object 180 degrees on the x axis
            selected_object.rotation_euler.x = math.radians(180)
            selected_object.rotation_euler.y = math.radians(90)
                
        elif context.scene.curve_operator_props.direction == 'Z':
            if original_y_dimension <= 2*original_x_dimension:
                bpy.context.view_layer.objects.active = curve_object
                bpy.context.object.rotation_euler = (math.radians(-90), 0, math.radians(180))
            else:
                bpy.context.view_layer.objects.active = curve_object
                bpy.context.object.rotation_euler = (math.radians(-90), 0, math.radians(-90))
                        
            # Set the scale factor based on z dimension
            scale_factor = (selected_object.dimensions.z / 3) * curve_scale
            curve_object.scale = (scale_factor, scale_factor, scale_factor)
                        
            curve_object.location.z = selected_object.location.z
            curve_object.location.y = selected_object.location.y
            curve_object.location.x = selected_object.location.x 
            
            # Set the curve modifier on the selected object
            curve_modifier = selected_object.modifiers.new(name="Curve Modifier", type='CURVE')
            curve_modifier.deform_axis = 'POS_Y'  # Set the deform axis to 'POS_Y'
            curve_modifier.object = curve_object  # Set the new curve object
            
            
            if original_y_dimension <= 2*original_x_dimension:
                # Rotate the selected object 180 degrees on the Y axis
                selected_object.rotation_euler.y = math.radians(180)
                selected_object.rotation_euler.z = math.radians(-90)
            else:
                # Rotate the selected object 180 degrees on the Y axis
                selected_object.rotation_euler.y = math.radians(180)
                selected_object.rotation_euler.z = math.radians(90)
            

            pass
        
        elif context.scene.curve_operator_props.direction == '-Z':
            if original_y_dimension <= 2*original_x_dimension:
                bpy.context.view_layer.objects.active = curve_object
                bpy.context.object.rotation_euler = (math.radians(90), 0, math.radians(360))
            else:
                bpy.context.view_layer.objects.active = curve_object
                bpy.context.object.rotation_euler = (math.radians(90), 0, math.radians(90))


            # Set the scale factor based on z dimension
            scale_factor = (selected_object.dimensions.z / 3) * curve_scale
            curve_object.scale = (scale_factor, scale_factor, scale_factor)

            curve_object.location.z = selected_object.location.z
            curve_object.location.y = selected_object.location.y
            curve_object.location.x = selected_object.location.x 

            # Set the curve modifier on the selected object
            curve_modifier = selected_object.modifiers.new(name="Curve Modifier", type='CURVE')
            curve_modifier.deform_axis = 'POS_Y'  # Set the deform axis to 'POS_Y'
            curve_modifier.object = curve_object  # Set the new curve object

            if original_y_dimension <= 2*original_x_dimension:
                # Rotate the selected object 180 degrees on the Y axis
                selected_object.rotation_euler.y = math.radians(180)
                selected_object.rotation_euler.z = math.radians(90)
            else:
                # Rotate the selected object 180 degrees on the Y axis
                selected_object.rotation_euler.y = math.radians(180)
                selected_object.rotation_euler.z = math.radians(-90)
            
            pass
        
        # Store the original location of the selected object
        original_location = selected_object.location.copy()
        
        

        # Calculate End Frame and Start Frame values
        end_frame = context.scene.curve_operator_props.end_frame
        start_frame = context.scene.curve_operator_props.start_frame
        mid_frame = (context.scene.curve_operator_props.start_frame + context.scene.curve_operator_props.end_frame) / 2
        move_factor = 7.2 * curve_scale if context.scene.curve_operator_props.direction == 'X,Y,Z' else -7.2 * curve_scale
        
        
        # Set keyframes
        selected_object.location = original_location
        selected_object.keyframe_insert(data_path="location", frame=end_frame)

        # Set End Frame keyframes for X/Y Direction
        if context.scene.curve_operator_props.direction == 'X':   
            selected_object.location.x += -move_factor * selected_object.dimensions.x
        elif context.scene.curve_operator_props.direction == 'Y':
                selected_object.location.y += -move_factor * selected_object.dimensions.y

        # Set End Frame keyframes for -X/-Y Direction
        elif context.scene.curve_operator_props.direction == '-X':   
            selected_object.location.x -= -move_factor * selected_object.dimensions.x
        elif context.scene.curve_operator_props.direction == '-Y':
                selected_object.location.y -= -move_factor * selected_object.dimensions.y
                
        # Set End Frame keyframes for Z Direction
        elif context.scene.curve_operator_props.direction == 'Z':
            selected_object.location.z += move_factor * selected_object.dimensions.z
            
        # Set End Frame keyframes for -Z Direction
        elif context.scene.curve_operator_props.direction == '-Z':
            selected_object.location.z -= move_factor * selected_object.dimensions.z
            
           

        # Reset location to original and set Start Frame keyframes
        selected_object.keyframe_insert(data_path="location", frame=start_frame)
        
        
        
        # Set keyframes for Scale at Start Frame
        selected_object.scale = (0, 0, 0)
        selected_object.keyframe_insert(data_path="scale", frame=start_frame)

        # Set keyframes for Scale at Mid Frame with cubic interpolation
        selected_object.scale = (1, 1, 1)
        selected_object.keyframe_insert(data_path="scale", frame=mid_frame)
        
        # Redraw the UI to simulate a click
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
        
            

        return {'FINISHED'}
    
 
class CurveOperator07(BaseCurveOperator):
    bl_idname = "object.generate_curve_07"
    bl_label = "Generate Curve 07"
    bl_description = "ِAnimate the selected object alonge curve 07"
    

    
    def execute(self, context):
                      
        # Check if there is an active object
        if context.active_object is not None and context.active_object.type == 'MESH':
            selected_object = context.active_object
            
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            
            # Delete existing keyframes on angle and scale properties
            selected_object.animation_data_clear()

            if 'scale' in selected_object and selected_object['scale']:
                selected_object.keyframe_delete(data_path='["scale"]')
            
            # Check if there is a Curve Modifier on the selected object and remove it
            curve_modifier = next((modifier for modifier in selected_object.modifiers if modifier.type == 'CURVE'), None)
            if curve_modifier:
                selected_object.modifiers.remove(curve_modifier)
                
                    
            # Store the original dimensions of the selected object
            original_x_dimension = selected_object.dimensions.x
            original_y_dimension = selected_object.dimensions.y
            original_z_dimension = selected_object.dimensions.z

            # Set the origin point of the selected object to the center of its geometry
            bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')  

            # Append the curve object from the external blend file
            blend_file_path = addon_dirc + "/Assets.blend"
            curve_object_name = "Curve Twist 07"
            base_name = "Animation Curve"  # Base name for the new curve objects

            # Check if the object already exists in the scene
            existing_objects = [obj for obj in bpy.data.objects if obj.name.startswith(base_name)]
            existing_object = next((obj for obj in existing_objects if obj.name == curve_object_name), None)

            if existing_object:
                # Update the existing object
                curve_object = existing_object
                curve_object.data = bpy.data.objects[curve_object_name].data.copy()
            else:
                # Create a new object
                with bpy.data.libraries.load(blend_file_path) as (data_from, data_to):
                    if curve_object_name in data_from.objects:
                        data_to.objects = [curve_object_name]

                # Check if the object is loaded
                if curve_object_name in bpy.data.objects:
                    curve_object = bpy.data.objects[curve_object_name]

                    # Create a new object and link the data from the appended curve object
                    new_object_name = base_name + str(len(existing_objects)).zfill(3)
                    curve_object = curve_object.copy()
                    curve_object.name = new_object_name
                    bpy.context.collection.objects.link(curve_object)  # Link to the active collection
                    
                    
                    
                    
              

        curve_scale = context.scene.curve_operator_props.curve_scale
        
        if context.scene.curve_operator_props.direction == 'X':
            bpy.context.view_layer.objects.active = curve_object
            bpy.context.object.rotation_euler = (0, 0, math.radians(-90))
                    
                        
            # Set the scale factor based on x dimension
            scale_factor = (selected_object.dimensions.x / 3) * curve_scale
            curve_object.scale = (scale_factor, scale_factor, scale_factor)
                        
            curve_object.location.x = selected_object.location.x 
            curve_object.location.y = selected_object.location.y + (selected_object.dimensions.y / 2 + selected_object.dimensions.z / 2) / 2
            curve_object.location.z = selected_object.location.z - (selected_object.dimensions.y / 2 + selected_object.dimensions.z / 2) / 2

            # Set the curve modifier on the selected object
            curve_modifier = selected_object.modifiers.new(name="Curve Modifier", type='CURVE')
            curve_modifier.deform_axis = 'POS_Y'  # Set the deform axis to 'POS_Y'
            curve_modifier.object = curve_object  # Set the new curve object
                
            # Rotate the selected object 180 degrees on the y axis
            selected_object.rotation_euler.x = math.radians(90)
            selected_object.rotation_euler.y = math.radians(180)
                    
        elif context.scene.curve_operator_props.direction == 'Y':
                        
            # Set the scale factor based on y dimension
            scale_factor = (selected_object.dimensions.y / 3) * curve_scale
            curve_object.scale = (scale_factor, scale_factor, scale_factor)
                        
            curve_object.location.x = selected_object.location.x - (selected_object.dimensions.x / 2 + selected_object.dimensions.z / 2) / 2  # Half the X dimension
            curve_object.location.y = selected_object.location.y
            curve_object.location.z = selected_object.location.z - (selected_object.dimensions.x / 2 + selected_object.dimensions.z / 2) / 2
                        
            # Set the curve modifier on the selected object
            curve_modifier = selected_object.modifiers.new(name="Curve Modifier", type='CURVE')
            curve_modifier.deform_axis = 'POS_Y'  # Set the deform axis to 'POS_Y'
            curve_modifier.object = curve_object  # Set the new curve object
                
            # Rotate the selected object 180 degrees on the x axis
            selected_object.rotation_euler.x = math.radians(180)
            selected_object.rotation_euler.y = math.radians(-90)
                
        
        
        
        
        elif context.scene.curve_operator_props.direction == '-X':
            
            # Rotate the curve object -90 degrees on the Z axis
            bpy.context.view_layer.objects.active = curve_object
            bpy.context.object.rotation_euler = (0, 0, math.radians(90))
                    
                        
            # Set the scale factor based on x dimension
            scale_factor = (selected_object.dimensions.x / 3) * curve_scale
            curve_object.scale = (scale_factor, scale_factor, scale_factor)
                        
            curve_object.location.x = selected_object.location.x 
            curve_object.location.y = selected_object.location.y - (selected_object.dimensions.y / 2 + selected_object.dimensions.z / 2) / 2
            curve_object.location.z = selected_object.location.z - (selected_object.dimensions.y / 2 + selected_object.dimensions.z / 2) / 2

            # Set the curve modifier on the selected object
            curve_modifier = selected_object.modifiers.new(name="Curve Modifier", type='CURVE')
            curve_modifier.deform_axis = 'POS_Y'  # Set the deform axis to 'POS_Y'
            curve_modifier.object = curve_object  # Set the new curve object
                
            # Rotate the selected object 180 degrees on the y axis
            selected_object.rotation_euler.x = math.radians(-90)
            selected_object.rotation_euler.y = math.radians(180)
                    
        elif context.scene.curve_operator_props.direction == '-Y':
            # Rotate the curve object 180 degrees on the Z axis
            bpy.context.view_layer.objects.active = curve_object
            bpy.context.object.rotation_euler = (0, 0, math.radians(180))
                        
            # Set the scale factor based on y dimension
            scale_factor = (selected_object.dimensions.y / 3) * curve_scale
            curve_object.scale = (scale_factor, scale_factor, scale_factor)
                        
            curve_object.location.x = selected_object.location.x + (selected_object.dimensions.x / 2 + selected_object.dimensions.z / 2) / 2  # Half the X dimension
            curve_object.location.y = selected_object.location.y
            curve_object.location.z = selected_object.location.z - (selected_object.dimensions.x / 2 + selected_object.dimensions.z / 2) / 2
                        
            # Set the curve modifier on the selected object
            curve_modifier = selected_object.modifiers.new(name="Curve Modifier", type='CURVE')
            curve_modifier.deform_axis = 'POS_Y'  # Set the deform axis to 'POS_Y'
            curve_modifier.object = curve_object  # Set the new curve object
                
            # Rotate the selected object 180 degrees on the x axis
            selected_object.rotation_euler.x = math.radians(180)
            selected_object.rotation_euler.y = math.radians(90)
                
        elif context.scene.curve_operator_props.direction == 'Z':
            if original_y_dimension <= 2*original_x_dimension:
                bpy.context.view_layer.objects.active = curve_object
                bpy.context.object.rotation_euler = (math.radians(-90), 0, math.radians(180))
            else:
                bpy.context.view_layer.objects.active = curve_object
                bpy.context.object.rotation_euler = (math.radians(-90), 0, math.radians(-90))
                        
            # Set the scale factor based on z dimension
            scale_factor = (selected_object.dimensions.z / 3) * curve_scale
            curve_object.scale = (scale_factor, scale_factor, scale_factor)
                        
            curve_object.location.z = selected_object.location.z
            curve_object.location.y = selected_object.location.y
            curve_object.location.x = selected_object.location.x 
            
            # Set the curve modifier on the selected object
            curve_modifier = selected_object.modifiers.new(name="Curve Modifier", type='CURVE')
            curve_modifier.deform_axis = 'POS_Y'  # Set the deform axis to 'POS_Y'
            curve_modifier.object = curve_object  # Set the new curve object
            
            
            if original_y_dimension <= 2*original_x_dimension:
                # Rotate the selected object 180 degrees on the Y axis
                selected_object.rotation_euler.y = math.radians(180)
                selected_object.rotation_euler.z = math.radians(-90)
            else:
                # Rotate the selected object 180 degrees on the Y axis
                selected_object.rotation_euler.y = math.radians(180)
                selected_object.rotation_euler.z = math.radians(90)
            

            pass
        
        elif context.scene.curve_operator_props.direction == '-Z':
            if original_y_dimension <= 2*original_x_dimension:
                bpy.context.view_layer.objects.active = curve_object
                bpy.context.object.rotation_euler = (math.radians(90), 0, math.radians(360))
            else:
                bpy.context.view_layer.objects.active = curve_object
                bpy.context.object.rotation_euler = (math.radians(90), 0, math.radians(90))


            # Set the scale factor based on z dimension
            scale_factor = (selected_object.dimensions.z / 3) * curve_scale
            curve_object.scale = (scale_factor, scale_factor, scale_factor)

            curve_object.location.z = selected_object.location.z
            curve_object.location.y = selected_object.location.y
            curve_object.location.x = selected_object.location.x 

            # Set the curve modifier on the selected object
            curve_modifier = selected_object.modifiers.new(name="Curve Modifier", type='CURVE')
            curve_modifier.deform_axis = 'POS_Y'  # Set the deform axis to 'POS_Y'
            curve_modifier.object = curve_object  # Set the new curve object

            if original_y_dimension <= 2*original_x_dimension:
                # Rotate the selected object 180 degrees on the Y axis
                selected_object.rotation_euler.y = math.radians(180)
                selected_object.rotation_euler.z = math.radians(90)
            else:
                # Rotate the selected object 180 degrees on the Y axis
                selected_object.rotation_euler.y = math.radians(180)
                selected_object.rotation_euler.z = math.radians(-90)
            
            pass
        
        # Store the original location of the selected object
        original_location = selected_object.location.copy()
        
        

        # Calculate End Frame and Start Frame values
        end_frame = context.scene.curve_operator_props.end_frame
        start_frame = context.scene.curve_operator_props.start_frame
        mid_frame = (context.scene.curve_operator_props.start_frame + context.scene.curve_operator_props.end_frame) / 2
        move_factor = 6 * curve_scale if context.scene.curve_operator_props.direction == 'X,Y,Z' else -6 * curve_scale
        
        
        # Set keyframes
        selected_object.location = original_location
        selected_object.keyframe_insert(data_path="location", frame=end_frame)

        # Set End Frame keyframes for X/Y Direction
        if context.scene.curve_operator_props.direction == 'X':   
            selected_object.location.x += -move_factor * selected_object.dimensions.x
        elif context.scene.curve_operator_props.direction == 'Y':
                selected_object.location.y += -move_factor * selected_object.dimensions.y

        # Set End Frame keyframes for -X/-Y Direction
        elif context.scene.curve_operator_props.direction == '-X':   
            selected_object.location.x -= -move_factor * selected_object.dimensions.x
        elif context.scene.curve_operator_props.direction == '-Y':
                selected_object.location.y -= -move_factor * selected_object.dimensions.y
                
        # Set End Frame keyframes for Z Direction
        elif context.scene.curve_operator_props.direction == 'Z':
            selected_object.location.z += move_factor * selected_object.dimensions.z
            
        # Set End Frame keyframes for -Z Direction
        elif context.scene.curve_operator_props.direction == '-Z':
            selected_object.location.z -= move_factor * selected_object.dimensions.z
            
           

        # Reset location to original and set Start Frame keyframes
        selected_object.keyframe_insert(data_path="location", frame=start_frame)
        
        
        
        # Set keyframes for Scale at Start Frame
        selected_object.scale = (0, 0, 0)
        selected_object.keyframe_insert(data_path="scale", frame=start_frame)

        # Set keyframes for Scale at Mid Frame with cubic interpolation
        selected_object.scale = (1, 1, 1)
        selected_object.keyframe_insert(data_path="scale", frame=mid_frame)
        
        # Redraw the UI to simulate a click
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
            

        return {'FINISHED'}
    
    
class CurveOperator08(BaseCurveOperator):
    bl_idname = "object.generate_curve_08"
    bl_label = "Generate Curve 08"
    bl_description = "ِAnimate the selected object alonge curve 08"
    

    
    def execute(self, context):
                      
        # Check if there is an active object
        if context.active_object is not None and context.active_object.type == 'MESH':
            selected_object = context.active_object
            
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            
            # Delete existing keyframes on angle and scale properties
            selected_object.animation_data_clear()

            if 'scale' in selected_object and selected_object['scale']:
                selected_object.keyframe_delete(data_path='["scale"]')
            
            # Check if there is a Curve Modifier on the selected object and remove it
            curve_modifier = next((modifier for modifier in selected_object.modifiers if modifier.type == 'CURVE'), None)
            if curve_modifier:
                selected_object.modifiers.remove(curve_modifier)
                
                    
            # Store the original dimensions of the selected object
            original_x_dimension = selected_object.dimensions.x
            original_y_dimension = selected_object.dimensions.y
            original_z_dimension = selected_object.dimensions.z

            # Set the origin point of the selected object to the center of its geometry
            bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')  

            # Append the curve object from the external blend file
            blend_file_path = addon_dirc + "/Assets.blend"
            curve_object_name = "Curve Twist 08"
            base_name = "Animation Curve"  # Base name for the new curve objects

            # Check if the object already exists in the scene
            existing_objects = [obj for obj in bpy.data.objects if obj.name.startswith(base_name)]
            existing_object = next((obj for obj in existing_objects if obj.name == curve_object_name), None)

            if existing_object:
                # Update the existing object
                curve_object = existing_object
                curve_object.data = bpy.data.objects[curve_object_name].data.copy()
            else:
                # Create a new object
                with bpy.data.libraries.load(blend_file_path) as (data_from, data_to):
                    if curve_object_name in data_from.objects:
                        data_to.objects = [curve_object_name]

                # Check if the object is loaded
                if curve_object_name in bpy.data.objects:
                    curve_object = bpy.data.objects[curve_object_name]

                    # Create a new object and link the data from the appended curve object
                    new_object_name = base_name + str(len(existing_objects)).zfill(3)
                    curve_object = curve_object.copy()
                    curve_object.name = new_object_name
                    bpy.context.collection.objects.link(curve_object)  # Link to the active collection
                    
                    
                    
                    
              
        curve_scale = context.scene.curve_operator_props.curve_scale
        
        if context.scene.curve_operator_props.direction == 'X':
            bpy.context.view_layer.objects.active = curve_object
            bpy.context.object.rotation_euler = (0, 0, math.radians(-90))
                    
                        
            # Set the scale factor based on x dimension
            scale_factor = (selected_object.dimensions.x / 3) * curve_scale
            curve_object.scale = (scale_factor, scale_factor, scale_factor)
                        
            curve_object.location.x = selected_object.location.x 
            curve_object.location.y = selected_object.location.y + (selected_object.dimensions.y / 2 + selected_object.dimensions.z / 2) / 2
            curve_object.location.z = selected_object.location.z - (selected_object.dimensions.y / 2 + selected_object.dimensions.z / 2) / 2

            # Set the curve modifier on the selected object
            curve_modifier = selected_object.modifiers.new(name="Curve Modifier", type='CURVE')
            curve_modifier.deform_axis = 'POS_Y'  # Set the deform axis to 'POS_Y'
            curve_modifier.object = curve_object  # Set the new curve object
                
            # Rotate the selected object 180 degrees on the y axis
            selected_object.rotation_euler.x = math.radians(90)
            selected_object.rotation_euler.y = math.radians(180)
                    
        elif context.scene.curve_operator_props.direction == 'Y':
                        
            # Set the scale factor based on y dimension
            scale_factor = (selected_object.dimensions.y / 3) * curve_scale
            curve_object.scale = (scale_factor, scale_factor, scale_factor)
                        
            curve_object.location.x = selected_object.location.x - (selected_object.dimensions.x / 2 + selected_object.dimensions.z / 2) / 2  # Half the X dimension
            curve_object.location.y = selected_object.location.y
            curve_object.location.z = selected_object.location.z - (selected_object.dimensions.x / 2 + selected_object.dimensions.z / 2) / 2
                        
            # Set the curve modifier on the selected object
            curve_modifier = selected_object.modifiers.new(name="Curve Modifier", type='CURVE')
            curve_modifier.deform_axis = 'POS_Y'  # Set the deform axis to 'POS_Y'
            curve_modifier.object = curve_object  # Set the new curve object
                
            # Rotate the selected object 180 degrees on the x axis
            selected_object.rotation_euler.x = math.radians(180)
            selected_object.rotation_euler.y = math.radians(-90)
                
        
        
        
        
        elif context.scene.curve_operator_props.direction == '-X':
            
            # Rotate the curve object -90 degrees on the Z axis
            bpy.context.view_layer.objects.active = curve_object
            bpy.context.object.rotation_euler = (0, 0, math.radians(90))
                    
                        
            # Set the scale factor based on x dimension
            scale_factor = (selected_object.dimensions.x / 3) * curve_scale
            curve_object.scale = (scale_factor, scale_factor, scale_factor)
                        
            curve_object.location.x = selected_object.location.x 
            curve_object.location.y = selected_object.location.y - (selected_object.dimensions.y / 2 + selected_object.dimensions.z / 2) / 2
            curve_object.location.z = selected_object.location.z - (selected_object.dimensions.y / 2 + selected_object.dimensions.z / 2) / 2

            # Set the curve modifier on the selected object
            curve_modifier = selected_object.modifiers.new(name="Curve Modifier", type='CURVE')
            curve_modifier.deform_axis = 'POS_Y'  # Set the deform axis to 'POS_Y'
            curve_modifier.object = curve_object  # Set the new curve object
                
            # Rotate the selected object 180 degrees on the y axis
            selected_object.rotation_euler.x = math.radians(-90)
            selected_object.rotation_euler.y = math.radians(180)
                    
        elif context.scene.curve_operator_props.direction == '-Y':
            # Rotate the curve object 180 degrees on the Z axis
            bpy.context.view_layer.objects.active = curve_object
            bpy.context.object.rotation_euler = (0, 0, math.radians(180))
                        
            # Set the scale factor based on y dimension
            scale_factor = (selected_object.dimensions.y / 3) * curve_scale
            curve_object.scale = (scale_factor, scale_factor, scale_factor)
                        
            curve_object.location.x = selected_object.location.x + (selected_object.dimensions.x / 2 + selected_object.dimensions.z / 2) / 2  # Half the X dimension
            curve_object.location.y = selected_object.location.y
            curve_object.location.z = selected_object.location.z - (selected_object.dimensions.x / 2 + selected_object.dimensions.z / 2) / 2
                        
            # Set the curve modifier on the selected object
            curve_modifier = selected_object.modifiers.new(name="Curve Modifier", type='CURVE')
            curve_modifier.deform_axis = 'POS_Y'  # Set the deform axis to 'POS_Y'
            curve_modifier.object = curve_object  # Set the new curve object
                
            # Rotate the selected object 180 degrees on the x axis
            selected_object.rotation_euler.x = math.radians(180)
            selected_object.rotation_euler.y = math.radians(90)
                
        elif context.scene.curve_operator_props.direction == 'Z':
            if original_y_dimension <= 2*original_x_dimension:
                bpy.context.view_layer.objects.active = curve_object
                bpy.context.object.rotation_euler = (math.radians(-90), 0, math.radians(180))
            else:
                bpy.context.view_layer.objects.active = curve_object
                bpy.context.object.rotation_euler = (math.radians(-90), 0, math.radians(-90))
                        
            # Set the scale factor based on z dimension
            scale_factor = (selected_object.dimensions.z / 3) * curve_scale
            curve_object.scale = (scale_factor, scale_factor, scale_factor)
                        
            curve_object.location.z = selected_object.location.z
            curve_object.location.y = selected_object.location.y
            curve_object.location.x = selected_object.location.x 
            
            # Set the curve modifier on the selected object
            curve_modifier = selected_object.modifiers.new(name="Curve Modifier", type='CURVE')
            curve_modifier.deform_axis = 'POS_Y'  # Set the deform axis to 'POS_Y'
            curve_modifier.object = curve_object  # Set the new curve object
            
            
            if original_y_dimension <= 2*original_x_dimension:
                # Rotate the selected object 180 degrees on the Y axis
                selected_object.rotation_euler.y = math.radians(180)
                selected_object.rotation_euler.z = math.radians(-90)
            else:
                # Rotate the selected object 180 degrees on the Y axis
                selected_object.rotation_euler.y = math.radians(180)
                selected_object.rotation_euler.z = math.radians(90)
            

            pass
        
        elif context.scene.curve_operator_props.direction == '-Z':
            if original_y_dimension <= 2*original_x_dimension:
                bpy.context.view_layer.objects.active = curve_object
                bpy.context.object.rotation_euler = (math.radians(90), 0, math.radians(360))
            else:
                bpy.context.view_layer.objects.active = curve_object
                bpy.context.object.rotation_euler = (math.radians(90), 0, math.radians(90))


            # Set the scale factor based on z dimension
            scale_factor = (selected_object.dimensions.z / 3) * curve_scale
            curve_object.scale = (scale_factor, scale_factor, scale_factor)

            curve_object.location.z = selected_object.location.z
            curve_object.location.y = selected_object.location.y
            curve_object.location.x = selected_object.location.x 

            # Set the curve modifier on the selected object
            curve_modifier = selected_object.modifiers.new(name="Curve Modifier", type='CURVE')
            curve_modifier.deform_axis = 'POS_Y'  # Set the deform axis to 'POS_Y'
            curve_modifier.object = curve_object  # Set the new curve object

            if original_y_dimension <= 2*original_x_dimension:
                # Rotate the selected object 180 degrees on the Y axis
                selected_object.rotation_euler.y = math.radians(180)
                selected_object.rotation_euler.z = math.radians(90)
            else:
                # Rotate the selected object 180 degrees on the Y axis
                selected_object.rotation_euler.y = math.radians(180)
                selected_object.rotation_euler.z = math.radians(-90)
            
            pass
        
        # Store the original location of the selected object
        original_location = selected_object.location.copy()
        
        

        # Calculate End Frame and Start Frame values
        end_frame = context.scene.curve_operator_props.end_frame
        start_frame = context.scene.curve_operator_props.start_frame
        mid_frame = (context.scene.curve_operator_props.start_frame + context.scene.curve_operator_props.end_frame) / 2
        move_factor = 4 * curve_scale if context.scene.curve_operator_props.direction == 'X,Y,Z' else -4 * curve_scale
        
        
        # Set keyframes
        selected_object.location = original_location
        selected_object.keyframe_insert(data_path="location", frame=end_frame)

        # Set End Frame keyframes for X/Y Direction
        if context.scene.curve_operator_props.direction == 'X':   
            selected_object.location.x += -move_factor * selected_object.dimensions.x
        elif context.scene.curve_operator_props.direction == 'Y':
                selected_object.location.y += -move_factor * selected_object.dimensions.y

        # Set End Frame keyframes for -X/-Y Direction
        elif context.scene.curve_operator_props.direction == '-X':   
            selected_object.location.x -= -move_factor * selected_object.dimensions.x
        elif context.scene.curve_operator_props.direction == '-Y':
                selected_object.location.y -= -move_factor * selected_object.dimensions.y
                
        # Set End Frame keyframes for Z Direction
        elif context.scene.curve_operator_props.direction == 'Z':
            selected_object.location.z += move_factor * selected_object.dimensions.z
            
        # Set End Frame keyframes for -Z Direction
        elif context.scene.curve_operator_props.direction == '-Z':
            selected_object.location.z -= move_factor * selected_object.dimensions.z
            
           

        # Reset location to original and set Start Frame keyframes
        selected_object.keyframe_insert(data_path="location", frame=start_frame)
        
        
        
        # Set keyframes for Scale at Start Frame
        selected_object.scale = (0, 0, 0)
        selected_object.keyframe_insert(data_path="scale", frame=start_frame)

        # Set keyframes for Scale at Mid Frame with cubic interpolation
        selected_object.scale = (1, 1, 1)
        selected_object.keyframe_insert(data_path="scale", frame=mid_frame)
        
        # Redraw the UI to simulate a click
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
        
            

        return {'FINISHED'}
   
    
class CurveOperator09(BaseCurveOperator):
    bl_idname = "object.generate_curve_09"
    bl_label = "Generate Curve 09"
    bl_description = "ِAnimate the selected object alonge curve 09"
    

    
    def execute(self, context):
                      
        # Check if there is an active object
        if context.active_object is not None and context.active_object.type == 'MESH':
            selected_object = context.active_object
            
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            
            # Delete existing keyframes on angle and scale properties
            selected_object.animation_data_clear()

            if 'scale' in selected_object and selected_object['scale']:
                selected_object.keyframe_delete(data_path='["scale"]')
            
            # Check if there is a Curve Modifier on the selected object and remove it
            curve_modifier = next((modifier for modifier in selected_object.modifiers if modifier.type == 'CURVE'), None)
            if curve_modifier:
                selected_object.modifiers.remove(curve_modifier)
                
                   
            # Store the original dimensions of the selected object
            original_x_dimension = selected_object.dimensions.x
            original_y_dimension = selected_object.dimensions.y
            original_z_dimension = selected_object.dimensions.z

            # Set the origin point of the selected object to the center of its geometry
            bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')  

            # Append the curve object from the external blend file
            blend_file_path = addon_dirc + "/Assets.blend"
            curve_object_name = "Curve Twist 09"
            base_name = "Animation Curve"  # Base name for the new curve objects

            # Check if the object already exists in the scene
            existing_objects = [obj for obj in bpy.data.objects if obj.name.startswith(base_name)]
            existing_object = next((obj for obj in existing_objects if obj.name == curve_object_name), None)

            if existing_object:
                # Update the existing object
                curve_object = existing_object
                curve_object.data = bpy.data.objects[curve_object_name].data.copy()
            else:
                # Create a new object
                with bpy.data.libraries.load(blend_file_path) as (data_from, data_to):
                    if curve_object_name in data_from.objects:
                        data_to.objects = [curve_object_name]

                # Check if the object is loaded
                if curve_object_name in bpy.data.objects:
                    curve_object = bpy.data.objects[curve_object_name]

                    # Create a new object and link the data from the appended curve object
                    new_object_name = base_name + str(len(existing_objects)).zfill(3)
                    curve_object = curve_object.copy()
                    curve_object.name = new_object_name
                    bpy.context.collection.objects.link(curve_object)  # Link to the active collection
                    
                    
                    
                    
              

        curve_scale = context.scene.curve_operator_props.curve_scale
        
        if context.scene.curve_operator_props.direction == 'X':
            bpy.context.view_layer.objects.active = curve_object
            bpy.context.object.rotation_euler = (0, 0, math.radians(-90))
                    
                        
            # Set the scale factor based on x dimension
            scale_factor = (selected_object.dimensions.x / 3) * curve_scale
            curve_object.scale = (scale_factor, scale_factor, scale_factor)
                        
            curve_object.location.x = selected_object.location.x 
            curve_object.location.y = selected_object.location.y + (selected_object.dimensions.y / 2 + selected_object.dimensions.z / 2) / 2
            curve_object.location.z = selected_object.location.z - (selected_object.dimensions.y / 2 + selected_object.dimensions.z / 2) / 2

            # Set the curve modifier on the selected object
            curve_modifier = selected_object.modifiers.new(name="Curve Modifier", type='CURVE')
            curve_modifier.deform_axis = 'POS_Y'  # Set the deform axis to 'POS_Y'
            curve_modifier.object = curve_object  # Set the new curve object
                
            # Rotate the selected object 180 degrees on the y axis
            selected_object.rotation_euler.x = math.radians(90)
            selected_object.rotation_euler.y = math.radians(180)
                    
        elif context.scene.curve_operator_props.direction == 'Y':
                        
            # Set the scale factor based on y dimension
            scale_factor = (selected_object.dimensions.y / 3) * curve_scale
            curve_object.scale = (scale_factor, scale_factor, scale_factor)
                        
            curve_object.location.x = selected_object.location.x - (selected_object.dimensions.x / 2 + selected_object.dimensions.z / 2) / 2  # Half the X dimension
            curve_object.location.y = selected_object.location.y
            curve_object.location.z = selected_object.location.z - (selected_object.dimensions.x / 2 + selected_object.dimensions.z / 2) / 2
                        
            # Set the curve modifier on the selected object
            curve_modifier = selected_object.modifiers.new(name="Curve Modifier", type='CURVE')
            curve_modifier.deform_axis = 'POS_Y'  # Set the deform axis to 'POS_Y'
            curve_modifier.object = curve_object  # Set the new curve object
                
            # Rotate the selected object 180 degrees on the x axis
            selected_object.rotation_euler.x = math.radians(180)
            selected_object.rotation_euler.y = math.radians(-90)
                
        
        
        
        
        elif context.scene.curve_operator_props.direction == '-X':
            
            # Rotate the curve object -90 degrees on the Z axis
            bpy.context.view_layer.objects.active = curve_object
            bpy.context.object.rotation_euler = (0, 0, math.radians(90))
                    
                        
            # Set the scale factor based on x dimension
            scale_factor = (selected_object.dimensions.x / 3) * curve_scale
            curve_object.scale = (scale_factor, scale_factor, scale_factor)
                        
            curve_object.location.x = selected_object.location.x 
            curve_object.location.y = selected_object.location.y - (selected_object.dimensions.y / 2 + selected_object.dimensions.z / 2) / 2
            curve_object.location.z = selected_object.location.z - (selected_object.dimensions.y / 2 + selected_object.dimensions.z / 2) / 2

            # Set the curve modifier on the selected object
            curve_modifier = selected_object.modifiers.new(name="Curve Modifier", type='CURVE')
            curve_modifier.deform_axis = 'POS_Y'  # Set the deform axis to 'POS_Y'
            curve_modifier.object = curve_object  # Set the new curve object
                
            # Rotate the selected object 180 degrees on the y axis
            selected_object.rotation_euler.x = math.radians(-90)
            selected_object.rotation_euler.y = math.radians(180)
                    
        elif context.scene.curve_operator_props.direction == '-Y':
            # Rotate the curve object 180 degrees on the Z axis
            bpy.context.view_layer.objects.active = curve_object
            bpy.context.object.rotation_euler = (0, 0, math.radians(180))
                        
            # Set the scale factor based on y dimension
            scale_factor = (selected_object.dimensions.y / 3) * curve_scale
            curve_object.scale = (scale_factor, scale_factor, scale_factor)
                        
            curve_object.location.x = selected_object.location.x + (selected_object.dimensions.x / 2 + selected_object.dimensions.z / 2) / 2  # Half the X dimension
            curve_object.location.y = selected_object.location.y
            curve_object.location.z = selected_object.location.z - (selected_object.dimensions.x / 2 + selected_object.dimensions.z / 2) / 2
                        
            # Set the curve modifier on the selected object
            curve_modifier = selected_object.modifiers.new(name="Curve Modifier", type='CURVE')
            curve_modifier.deform_axis = 'POS_Y'  # Set the deform axis to 'POS_Y'
            curve_modifier.object = curve_object  # Set the new curve object
                
            # Rotate the selected object 180 degrees on the x axis
            selected_object.rotation_euler.x = math.radians(180)
            selected_object.rotation_euler.y = math.radians(90)
                
        elif context.scene.curve_operator_props.direction == 'Z':
            if original_y_dimension <= 2*original_x_dimension:
                bpy.context.view_layer.objects.active = curve_object
                bpy.context.object.rotation_euler = (math.radians(-90), 0, math.radians(180))
            else:
                bpy.context.view_layer.objects.active = curve_object
                bpy.context.object.rotation_euler = (math.radians(-90), 0, math.radians(-90))
                        
            # Set the scale factor based on z dimension
            scale_factor = (selected_object.dimensions.z / 3) * curve_scale
            curve_object.scale = (scale_factor, scale_factor, scale_factor)
                        
            curve_object.location.z = selected_object.location.z
            curve_object.location.y = selected_object.location.y
            curve_object.location.x = selected_object.location.x 
            
            # Set the curve modifier on the selected object
            curve_modifier = selected_object.modifiers.new(name="Curve Modifier", type='CURVE')
            curve_modifier.deform_axis = 'POS_Y'  # Set the deform axis to 'POS_Y'
            curve_modifier.object = curve_object  # Set the new curve object
            
            
            if original_y_dimension <= 2*original_x_dimension:
                # Rotate the selected object 180 degrees on the Y axis
                selected_object.rotation_euler.y = math.radians(180)
                selected_object.rotation_euler.z = math.radians(-90)
            else:
                # Rotate the selected object 180 degrees on the Y axis
                selected_object.rotation_euler.y = math.radians(180)
                selected_object.rotation_euler.z = math.radians(90)
            

            pass
        
        elif context.scene.curve_operator_props.direction == '-Z':
            if original_y_dimension <= 2*original_x_dimension:
                bpy.context.view_layer.objects.active = curve_object
                bpy.context.object.rotation_euler = (math.radians(90), 0, math.radians(360))
            else:
                bpy.context.view_layer.objects.active = curve_object
                bpy.context.object.rotation_euler = (math.radians(90), 0, math.radians(90))


            # Set the scale factor based on z dimension
            scale_factor = (selected_object.dimensions.z / 3) * curve_scale
            curve_object.scale = (scale_factor, scale_factor, scale_factor)

            curve_object.location.z = selected_object.location.z
            curve_object.location.y = selected_object.location.y
            curve_object.location.x = selected_object.location.x 

            # Set the curve modifier on the selected object
            curve_modifier = selected_object.modifiers.new(name="Curve Modifier", type='CURVE')
            curve_modifier.deform_axis = 'POS_Y'  # Set the deform axis to 'POS_Y'
            curve_modifier.object = curve_object  # Set the new curve object

            if original_y_dimension <= 2*original_x_dimension:
                # Rotate the selected object 180 degrees on the Y axis
                selected_object.rotation_euler.y = math.radians(180)
                selected_object.rotation_euler.z = math.radians(90)
            else:
                # Rotate the selected object 180 degrees on the Y axis
                selected_object.rotation_euler.y = math.radians(180)
                selected_object.rotation_euler.z = math.radians(-90)
            
            pass
        
        # Store the original location of the selected object
        original_location = selected_object.location.copy()
        
        

        # Calculate End Frame and Start Frame values
        end_frame = context.scene.curve_operator_props.end_frame
        start_frame = context.scene.curve_operator_props.start_frame
        mid_frame = (context.scene.curve_operator_props.start_frame + context.scene.curve_operator_props.end_frame) / 2
        move_factor = 5 * curve_scale if context.scene.curve_operator_props.direction == 'X,Y,Z' else -5 * curve_scale
        
        
        # Set keyframes
        selected_object.location = original_location
        selected_object.keyframe_insert(data_path="location", frame=end_frame)

        # Set End Frame keyframes for X/Y Direction
        if context.scene.curve_operator_props.direction == 'X':   
            selected_object.location.x += -move_factor * selected_object.dimensions.x
        elif context.scene.curve_operator_props.direction == 'Y':
                selected_object.location.y += -move_factor * selected_object.dimensions.y

        # Set End Frame keyframes for -X/-Y Direction
        elif context.scene.curve_operator_props.direction == '-X':   
            selected_object.location.x -= -move_factor * selected_object.dimensions.x
        elif context.scene.curve_operator_props.direction == '-Y':
                selected_object.location.y -= -move_factor * selected_object.dimensions.y
                
        # Set End Frame keyframes for Z Direction
        elif context.scene.curve_operator_props.direction == 'Z':
            selected_object.location.z += move_factor * selected_object.dimensions.z
            
        # Set End Frame keyframes for -Z Direction
        elif context.scene.curve_operator_props.direction == '-Z':
            selected_object.location.z -= move_factor * selected_object.dimensions.z
            
           

        # Reset location to original and set Start Frame keyframes
        selected_object.keyframe_insert(data_path="location", frame=start_frame)
        
        
        
        # Set keyframes for Scale at Start Frame
        selected_object.scale = (0, 0, 0)
        selected_object.keyframe_insert(data_path="scale", frame=start_frame)

        # Set keyframes for Scale at Mid Frame with cubic interpolation
        selected_object.scale = (1, 1, 1)
        selected_object.keyframe_insert(data_path="scale", frame=mid_frame)
        
        # Redraw the UI to simulate a click
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
        
            

        return {'FINISHED'}
    
      
class CurveOperator10(BaseCurveOperator):
    bl_idname = "object.generate_curve_10"
    bl_label = "Generate Curve 10"
    bl_description = "ِAnimate the selected object alonge curve 10"
    

    
    def execute(self, context):
                      
        # Check if there is an active object
        if context.active_object is not None and context.active_object.type == 'MESH':
            selected_object = context.active_object
            
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            
            # Delete existing keyframes on angle and scale properties
            selected_object.animation_data_clear()

            if 'scale' in selected_object and selected_object['scale']:
                selected_object.keyframe_delete(data_path='["scale"]')
            
            # Check if there is a Curve Modifier on the selected object and remove it
            curve_modifier = next((modifier for modifier in selected_object.modifiers if modifier.type == 'CURVE'), None)
            if curve_modifier:
                selected_object.modifiers.remove(curve_modifier)
                
                    
            # Store the original dimensions of the selected object
            original_x_dimension = selected_object.dimensions.x
            original_y_dimension = selected_object.dimensions.y
            original_z_dimension = selected_object.dimensions.z

            # Set the origin point of the selected object to the center of its geometry
            bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')  

            # Append the curve object from the external blend file
            blend_file_path = addon_dirc + "/Assets.blend"
            curve_object_name = "Curve Twist 10"
            base_name = "Animation Curve"  # Base name for the new curve objects

            # Check if the object already exists in the scene
            existing_objects = [obj for obj in bpy.data.objects if obj.name.startswith(base_name)]
            existing_object = next((obj for obj in existing_objects if obj.name == curve_object_name), None)

            if existing_object:
                # Update the existing object
                curve_object = existing_object
                curve_object.data = bpy.data.objects[curve_object_name].data.copy()
            else:
                # Create a new object
                with bpy.data.libraries.load(blend_file_path) as (data_from, data_to):
                    if curve_object_name in data_from.objects:
                        data_to.objects = [curve_object_name]

                # Check if the object is loaded
                if curve_object_name in bpy.data.objects:
                    curve_object = bpy.data.objects[curve_object_name]

                    # Create a new object and link the data from the appended curve object
                    new_object_name = base_name + str(len(existing_objects)).zfill(3)
                    curve_object = curve_object.copy()
                    curve_object.name = new_object_name
                    bpy.context.collection.objects.link(curve_object)  # Link to the active collection
                    
                    
                    
                    
              

        curve_scale = context.scene.curve_operator_props.curve_scale
        
        if context.scene.curve_operator_props.direction == 'X':
            bpy.context.view_layer.objects.active = curve_object
            bpy.context.object.rotation_euler = (0, 0, math.radians(-90))
                    
                        
            # Set the scale factor based on x dimension
            scale_factor = (selected_object.dimensions.x / 3) * curve_scale
            curve_object.scale = (scale_factor, scale_factor, scale_factor)
                        
            curve_object.location.x = selected_object.location.x 
            curve_object.location.y = selected_object.location.y + (selected_object.dimensions.y / 2 + selected_object.dimensions.z / 2) / 2
            curve_object.location.z = selected_object.location.z - (selected_object.dimensions.y / 2 + selected_object.dimensions.z / 2) / 2

            # Set the curve modifier on the selected object
            curve_modifier = selected_object.modifiers.new(name="Curve Modifier", type='CURVE')
            curve_modifier.deform_axis = 'POS_Y'  # Set the deform axis to 'POS_Y'
            curve_modifier.object = curve_object  # Set the new curve object
                
            # Rotate the selected object 180 degrees on the y axis
            selected_object.rotation_euler.x = math.radians(90)
            selected_object.rotation_euler.y = math.radians(180)
                    
        elif context.scene.curve_operator_props.direction == 'Y':
                        
            # Set the scale factor based on y dimension
            scale_factor = (selected_object.dimensions.y / 3) * curve_scale
            curve_object.scale = (scale_factor, scale_factor, scale_factor)
                        
            curve_object.location.x = selected_object.location.x - (selected_object.dimensions.x / 2 + selected_object.dimensions.z / 2) / 2  # Half the X dimension
            curve_object.location.y = selected_object.location.y
            curve_object.location.z = selected_object.location.z - (selected_object.dimensions.x / 2 + selected_object.dimensions.z / 2) / 2
                        
            # Set the curve modifier on the selected object
            curve_modifier = selected_object.modifiers.new(name="Curve Modifier", type='CURVE')
            curve_modifier.deform_axis = 'POS_Y'  # Set the deform axis to 'POS_Y'
            curve_modifier.object = curve_object  # Set the new curve object
                
            # Rotate the selected object 180 degrees on the x axis
            selected_object.rotation_euler.x = math.radians(180)
            selected_object.rotation_euler.y = math.radians(-90)
                
        
        
        
        
        elif context.scene.curve_operator_props.direction == '-X':
            
            # Rotate the curve object -90 degrees on the Z axis
            bpy.context.view_layer.objects.active = curve_object
            bpy.context.object.rotation_euler = (0, 0, math.radians(90))
                    
                        
            # Set the scale factor based on x dimension
            scale_factor = (selected_object.dimensions.x / 3) * curve_scale
            curve_object.scale = (scale_factor, scale_factor, scale_factor)
                        
            curve_object.location.x = selected_object.location.x 
            curve_object.location.y = selected_object.location.y - (selected_object.dimensions.y / 2 + selected_object.dimensions.z / 2) / 2
            curve_object.location.z = selected_object.location.z - (selected_object.dimensions.y / 2 + selected_object.dimensions.z / 2) / 2

            # Set the curve modifier on the selected object
            curve_modifier = selected_object.modifiers.new(name="Curve Modifier", type='CURVE')
            curve_modifier.deform_axis = 'POS_Y'  # Set the deform axis to 'POS_Y'
            curve_modifier.object = curve_object  # Set the new curve object
                
            # Rotate the selected object 180 degrees on the y axis
            selected_object.rotation_euler.x = math.radians(-90)
            selected_object.rotation_euler.y = math.radians(180)
                    
        elif context.scene.curve_operator_props.direction == '-Y':
            # Rotate the curve object 180 degrees on the Z axis
            bpy.context.view_layer.objects.active = curve_object
            bpy.context.object.rotation_euler = (0, 0, math.radians(180))
                        
            # Set the scale factor based on y dimension
            scale_factor = (selected_object.dimensions.y / 3) * curve_scale
            curve_object.scale = (scale_factor, scale_factor, scale_factor)
                        
            curve_object.location.x = selected_object.location.x + (selected_object.dimensions.x / 2 + selected_object.dimensions.z / 2) / 2  # Half the X dimension
            curve_object.location.y = selected_object.location.y
            curve_object.location.z = selected_object.location.z - (selected_object.dimensions.x / 2 + selected_object.dimensions.z / 2) / 2
                        
            # Set the curve modifier on the selected object
            curve_modifier = selected_object.modifiers.new(name="Curve Modifier", type='CURVE')
            curve_modifier.deform_axis = 'POS_Y'  # Set the deform axis to 'POS_Y'
            curve_modifier.object = curve_object  # Set the new curve object
                
            # Rotate the selected object 180 degrees on the x axis
            selected_object.rotation_euler.x = math.radians(180)
            selected_object.rotation_euler.y = math.radians(90)
                
        elif context.scene.curve_operator_props.direction == 'Z':
            if original_y_dimension <= 2*original_x_dimension:
                bpy.context.view_layer.objects.active = curve_object
                bpy.context.object.rotation_euler = (math.radians(-90), 0, math.radians(180))
            else:
                bpy.context.view_layer.objects.active = curve_object
                bpy.context.object.rotation_euler = (math.radians(-90), 0, math.radians(-90))
                        
            # Set the scale factor based on z dimension
            scale_factor = (selected_object.dimensions.z / 3) * curve_scale
            curve_object.scale = (scale_factor, scale_factor, scale_factor)
                        
            curve_object.location.z = selected_object.location.z
            curve_object.location.y = selected_object.location.y
            curve_object.location.x = selected_object.location.x 
            
            # Set the curve modifier on the selected object
            curve_modifier = selected_object.modifiers.new(name="Curve Modifier", type='CURVE')
            curve_modifier.deform_axis = 'POS_Y'  # Set the deform axis to 'POS_Y'
            curve_modifier.object = curve_object  # Set the new curve object
            
            
            if original_y_dimension <= 2*original_x_dimension:
                # Rotate the selected object 180 degrees on the Y axis
                selected_object.rotation_euler.y = math.radians(180)
                selected_object.rotation_euler.z = math.radians(-90)
            else:
                # Rotate the selected object 180 degrees on the Y axis
                selected_object.rotation_euler.y = math.radians(180)
                selected_object.rotation_euler.z = math.radians(90)
            

            pass
        
        elif context.scene.curve_operator_props.direction == '-Z':
            if original_y_dimension <= 2*original_x_dimension:
                bpy.context.view_layer.objects.active = curve_object
                bpy.context.object.rotation_euler = (math.radians(90), 0, math.radians(360))
            else:
                bpy.context.view_layer.objects.active = curve_object
                bpy.context.object.rotation_euler = (math.radians(90), 0, math.radians(90))


            # Set the scale factor based on z dimension
            scale_factor = (selected_object.dimensions.z / 3) * curve_scale
            curve_object.scale = (scale_factor, scale_factor, scale_factor)

            curve_object.location.z = selected_object.location.z
            curve_object.location.y = selected_object.location.y
            curve_object.location.x = selected_object.location.x 

            # Set the curve modifier on the selected object
            curve_modifier = selected_object.modifiers.new(name="Curve Modifier", type='CURVE')
            curve_modifier.deform_axis = 'POS_Y'  # Set the deform axis to 'POS_Y'
            curve_modifier.object = curve_object  # Set the new curve object

            if original_y_dimension <= 2*original_x_dimension:
                # Rotate the selected object 180 degrees on the Y axis
                selected_object.rotation_euler.y = math.radians(180)
                selected_object.rotation_euler.z = math.radians(90)
            else:
                # Rotate the selected object 180 degrees on the Y axis
                selected_object.rotation_euler.y = math.radians(180)
                selected_object.rotation_euler.z = math.radians(-90)
            
            pass
        
        # Store the original location of the selected object
        original_location = selected_object.location.copy()
        
        

        # Calculate End Frame and Start Frame values
        end_frame = context.scene.curve_operator_props.end_frame
        start_frame = context.scene.curve_operator_props.start_frame
        mid_frame = (context.scene.curve_operator_props.start_frame + context.scene.curve_operator_props.end_frame) / 2
        move_factor = 7 * curve_scale if context.scene.curve_operator_props.direction == 'X,Y,Z' else -7 * curve_scale
        
        
        # Set keyframes
        selected_object.location = original_location
        selected_object.keyframe_insert(data_path="location", frame=end_frame)

        # Set End Frame keyframes for X/Y Direction
        if context.scene.curve_operator_props.direction == 'X':   
            selected_object.location.x += -move_factor * selected_object.dimensions.x
        elif context.scene.curve_operator_props.direction == 'Y':
                selected_object.location.y += -move_factor * selected_object.dimensions.y

        # Set End Frame keyframes for -X/-Y Direction
        elif context.scene.curve_operator_props.direction == '-X':   
            selected_object.location.x -= -move_factor * selected_object.dimensions.x
        elif context.scene.curve_operator_props.direction == '-Y':
                selected_object.location.y -= -move_factor * selected_object.dimensions.y
                
        # Set End Frame keyframes for Z Direction
        elif context.scene.curve_operator_props.direction == 'Z':
            selected_object.location.z += move_factor * selected_object.dimensions.z
            
        # Set End Frame keyframes for -Z Direction
        elif context.scene.curve_operator_props.direction == '-Z':
            selected_object.location.z -= move_factor * selected_object.dimensions.z
            
           

        # Reset location to original and set Start Frame keyframes
        selected_object.keyframe_insert(data_path="location", frame=start_frame)
        
        
        
        # Set keyframes for Scale at Start Frame
        selected_object.scale = (0, 0, 0)
        selected_object.keyframe_insert(data_path="scale", frame=start_frame)

        # Set keyframes for Scale at Mid Frame with cubic interpolation
        selected_object.scale = (1, 1, 1)
        selected_object.keyframe_insert(data_path="scale", frame=mid_frame)
        
        # Redraw the UI to simulate a click
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
        
            

        return {'FINISHED'}
    
    
class CurveOperator11(BaseCurveOperator):
    bl_idname = "object.generate_curve_11"
    bl_label = "Generate Curve 11"
    bl_description = "ِAnimate the selected object alonge curve 11"
    

    
    def execute(self, context):
                      
        # Check if there is an active object
        if context.active_object is not None and context.active_object.type == 'MESH':
            selected_object = context.active_object
            
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            
            # Delete existing keyframes on angle and scale properties
            selected_object.animation_data_clear()

            if 'scale' in selected_object and selected_object['scale']:
                selected_object.keyframe_delete(data_path='["scale"]')
            
            # Check if there is a Curve Modifier on the selected object and remove it
            curve_modifier = next((modifier for modifier in selected_object.modifiers if modifier.type == 'CURVE'), None)
            if curve_modifier:
                selected_object.modifiers.remove(curve_modifier)
                
                    
            # Store the original dimensions of the selected object
            original_x_dimension = selected_object.dimensions.x
            original_y_dimension = selected_object.dimensions.y
            original_z_dimension = selected_object.dimensions.z

            # Set the origin point of the selected object to the center of its geometry
            bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')  

            # Append the curve object from the external blend file
            blend_file_path = addon_dirc + "/Assets.blend"
            curve_object_name = "Curve Twist 11"
            base_name = "Animation Curve"  # Base name for the new curve objects

            # Check if the object already exists in the scene
            existing_objects = [obj for obj in bpy.data.objects if obj.name.startswith(base_name)]
            existing_object = next((obj for obj in existing_objects if obj.name == curve_object_name), None)

            if existing_object:
                # Update the existing object
                curve_object = existing_object
                curve_object.data = bpy.data.objects[curve_object_name].data.copy()
            else:
                # Create a new object
                with bpy.data.libraries.load(blend_file_path) as (data_from, data_to):
                    if curve_object_name in data_from.objects:
                        data_to.objects = [curve_object_name]

                # Check if the object is loaded
                if curve_object_name in bpy.data.objects:
                    curve_object = bpy.data.objects[curve_object_name]

                    # Create a new object and link the data from the appended curve object
                    new_object_name = base_name + str(len(existing_objects)).zfill(3)
                    curve_object = curve_object.copy()
                    curve_object.name = new_object_name
                    bpy.context.collection.objects.link(curve_object)  # Link to the active collection
                    
                    
                    
                    
              

        curve_scale = context.scene.curve_operator_props.curve_scale
        
        if context.scene.curve_operator_props.direction == 'X':
            bpy.context.view_layer.objects.active = curve_object
            bpy.context.object.rotation_euler = (0, 0, math.radians(-90))
                    
                        
            # Set the scale factor based on x dimension
            scale_factor = (selected_object.dimensions.x / 3) * curve_scale
            curve_object.scale = (scale_factor, scale_factor, scale_factor)
                        
            curve_object.location.x = selected_object.location.x 
            curve_object.location.y = selected_object.location.y + (selected_object.dimensions.y / 2 + selected_object.dimensions.z / 2) / 2
            curve_object.location.z = selected_object.location.z - (selected_object.dimensions.y / 2 + selected_object.dimensions.z / 2) / 2

            # Set the curve modifier on the selected object
            curve_modifier = selected_object.modifiers.new(name="Curve Modifier", type='CURVE')
            curve_modifier.deform_axis = 'POS_Y'  # Set the deform axis to 'POS_Y'
            curve_modifier.object = curve_object  # Set the new curve object
                
            # Rotate the selected object 180 degrees on the y axis
            selected_object.rotation_euler.x = math.radians(90)
            selected_object.rotation_euler.y = math.radians(180)
                    
        elif context.scene.curve_operator_props.direction == 'Y':
                        
            # Set the scale factor based on y dimension
            scale_factor = (selected_object.dimensions.y / 3) * curve_scale
            curve_object.scale = (scale_factor, scale_factor, scale_factor)
                        
            curve_object.location.x = selected_object.location.x - (selected_object.dimensions.x / 2 + selected_object.dimensions.z / 2) / 2  # Half the X dimension
            curve_object.location.y = selected_object.location.y
            curve_object.location.z = selected_object.location.z - (selected_object.dimensions.x / 2 + selected_object.dimensions.z / 2) / 2
                        
            # Set the curve modifier on the selected object
            curve_modifier = selected_object.modifiers.new(name="Curve Modifier", type='CURVE')
            curve_modifier.deform_axis = 'POS_Y'  # Set the deform axis to 'POS_Y'
            curve_modifier.object = curve_object  # Set the new curve object
                
            # Rotate the selected object 180 degrees on the x axis
            selected_object.rotation_euler.x = math.radians(180)
            selected_object.rotation_euler.y = math.radians(-90)
                
        
        
        
        
        elif context.scene.curve_operator_props.direction == '-X':
            
            # Rotate the curve object -90 degrees on the Z axis
            bpy.context.view_layer.objects.active = curve_object
            bpy.context.object.rotation_euler = (0, 0, math.radians(90))
                    
                        
            # Set the scale factor based on x dimension
            scale_factor = (selected_object.dimensions.x / 3) * curve_scale
            curve_object.scale = (scale_factor, scale_factor, scale_factor)
                        
            curve_object.location.x = selected_object.location.x 
            curve_object.location.y = selected_object.location.y - (selected_object.dimensions.y / 2 + selected_object.dimensions.z / 2) / 2
            curve_object.location.z = selected_object.location.z - (selected_object.dimensions.y / 2 + selected_object.dimensions.z / 2) / 2

            # Set the curve modifier on the selected object
            curve_modifier = selected_object.modifiers.new(name="Curve Modifier", type='CURVE')
            curve_modifier.deform_axis = 'POS_Y'  # Set the deform axis to 'POS_Y'
            curve_modifier.object = curve_object  # Set the new curve object
                
            # Rotate the selected object 180 degrees on the y axis
            selected_object.rotation_euler.x = math.radians(-90)
            selected_object.rotation_euler.y = math.radians(180)
                    
        elif context.scene.curve_operator_props.direction == '-Y':
            # Rotate the curve object 180 degrees on the Z axis
            bpy.context.view_layer.objects.active = curve_object
            bpy.context.object.rotation_euler = (0, 0, math.radians(180))
                        
            # Set the scale factor based on y dimension
            scale_factor = (selected_object.dimensions.y / 3) * curve_scale
            curve_object.scale = (scale_factor, scale_factor, scale_factor)
                        
            curve_object.location.x = selected_object.location.x + (selected_object.dimensions.x / 2 + selected_object.dimensions.z / 2) / 2  # Half the X dimension
            curve_object.location.y = selected_object.location.y
            curve_object.location.z = selected_object.location.z - (selected_object.dimensions.x / 2 + selected_object.dimensions.z / 2) / 2
                        
            # Set the curve modifier on the selected object
            curve_modifier = selected_object.modifiers.new(name="Curve Modifier", type='CURVE')
            curve_modifier.deform_axis = 'POS_Y'  # Set the deform axis to 'POS_Y'
            curve_modifier.object = curve_object  # Set the new curve object
                
            # Rotate the selected object 180 degrees on the x axis
            selected_object.rotation_euler.x = math.radians(180)
            selected_object.rotation_euler.y = math.radians(90)
                
        elif context.scene.curve_operator_props.direction == 'Z':
            if original_y_dimension <= 2*original_x_dimension:
                bpy.context.view_layer.objects.active = curve_object
                bpy.context.object.rotation_euler = (math.radians(-90), 0, math.radians(180))
            else:
                bpy.context.view_layer.objects.active = curve_object
                bpy.context.object.rotation_euler = (math.radians(-90), 0, math.radians(-90))
                        
            # Set the scale factor based on z dimension
            scale_factor = (selected_object.dimensions.z / 3) * curve_scale
            curve_object.scale = (scale_factor, scale_factor, scale_factor)
                        
            curve_object.location.z = selected_object.location.z
            curve_object.location.y = selected_object.location.y
            curve_object.location.x = selected_object.location.x 
            
            # Set the curve modifier on the selected object
            curve_modifier = selected_object.modifiers.new(name="Curve Modifier", type='CURVE')
            curve_modifier.deform_axis = 'POS_Y'  # Set the deform axis to 'POS_Y'
            curve_modifier.object = curve_object  # Set the new curve object
            
            
            if original_y_dimension <= 2*original_x_dimension:
                # Rotate the selected object 180 degrees on the Y axis
                selected_object.rotation_euler.y = math.radians(180)
                selected_object.rotation_euler.z = math.radians(-90)
            else:
                # Rotate the selected object 180 degrees on the Y axis
                selected_object.rotation_euler.y = math.radians(180)
                selected_object.rotation_euler.z = math.radians(90)
            

            pass
        
        elif context.scene.curve_operator_props.direction == '-Z':
            if original_y_dimension <= 2*original_x_dimension:
                bpy.context.view_layer.objects.active = curve_object
                bpy.context.object.rotation_euler = (math.radians(90), 0, math.radians(360))
            else:
                bpy.context.view_layer.objects.active = curve_object
                bpy.context.object.rotation_euler = (math.radians(90), 0, math.radians(90))


            # Set the scale factor based on z dimension
            scale_factor = (selected_object.dimensions.z / 3) * curve_scale
            curve_object.scale = (scale_factor, scale_factor, scale_factor)

            curve_object.location.z = selected_object.location.z
            curve_object.location.y = selected_object.location.y
            curve_object.location.x = selected_object.location.x 

            # Set the curve modifier on the selected object
            curve_modifier = selected_object.modifiers.new(name="Curve Modifier", type='CURVE')
            curve_modifier.deform_axis = 'POS_Y'  # Set the deform axis to 'POS_Y'
            curve_modifier.object = curve_object  # Set the new curve object

            if original_y_dimension <= 2*original_x_dimension:
                # Rotate the selected object 180 degrees on the Y axis
                selected_object.rotation_euler.y = math.radians(180)
                selected_object.rotation_euler.z = math.radians(90)
            else:
                # Rotate the selected object 180 degrees on the Y axis
                selected_object.rotation_euler.y = math.radians(180)
                selected_object.rotation_euler.z = math.radians(-90)
            
            pass
        
        # Store the original location of the selected object
        original_location = selected_object.location.copy()
        
        

        # Calculate End Frame and Start Frame values
        end_frame = context.scene.curve_operator_props.end_frame
        start_frame = context.scene.curve_operator_props.start_frame
        mid_frame = (context.scene.curve_operator_props.start_frame + context.scene.curve_operator_props.end_frame) / 2
        move_factor = 4.8 * curve_scale if context.scene.curve_operator_props.direction == 'X,Y,Z' else -4.8 * curve_scale
        
        
        # Set keyframes
        selected_object.location = original_location
        selected_object.keyframe_insert(data_path="location", frame=end_frame)

        # Set End Frame keyframes for X/Y Direction
        if context.scene.curve_operator_props.direction == 'X':   
            selected_object.location.x += -move_factor * selected_object.dimensions.x
        elif context.scene.curve_operator_props.direction == 'Y':
                selected_object.location.y += -move_factor * selected_object.dimensions.y

        # Set End Frame keyframes for -X/-Y Direction
        elif context.scene.curve_operator_props.direction == '-X':   
            selected_object.location.x -= -move_factor * selected_object.dimensions.x
        elif context.scene.curve_operator_props.direction == '-Y':
                selected_object.location.y -= -move_factor * selected_object.dimensions.y
                
        # Set End Frame keyframes for Z Direction
        elif context.scene.curve_operator_props.direction == 'Z':
            selected_object.location.z += move_factor * selected_object.dimensions.z
            
        # Set End Frame keyframes for -Z Direction
        elif context.scene.curve_operator_props.direction == '-Z':
            selected_object.location.z -= move_factor * selected_object.dimensions.z
            
           

        # Reset location to original and set Start Frame keyframes
        selected_object.keyframe_insert(data_path="location", frame=start_frame)
        
        
        
        # Set keyframes for Scale at Start Frame
        selected_object.scale = (0, 0, 0)
        selected_object.keyframe_insert(data_path="scale", frame=start_frame)

        # Set keyframes for Scale at Mid Frame with cubic interpolation
        selected_object.scale = (1, 1, 1)
        selected_object.keyframe_insert(data_path="scale", frame=mid_frame)
        
        # Redraw the UI to simulate a click
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
        
            

        return {'FINISHED'}
 
curve_operators_classes = (
    CurveOperator,
    CurveOperator02,
    CurveOperator03,
    CurveOperator04,
    CurveOperator05, 
    CurveOperator06,
    CurveOperator07,
    CurveOperator08,
    CurveOperator09,
    CurveOperator10,
    CurveOperator11,    
 # Add other curve operator classes here
)

