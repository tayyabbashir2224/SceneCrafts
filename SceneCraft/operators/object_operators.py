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
from ..base_operators import BaseObjectOperator

addon_dirc = os.path.dirname(os.path.realpath(__file__))
                        #pop In/out
class OBJECT_OT_Pop_Up_Y(BaseObjectOperator):
    bl_label = "Rotate Object"
    bl_idname = "object.pop_up_y"
    bl_description = "Pop up and rotate the selected object on Y Axis while animating in or out."
    
    
    

    def execute(self, context):
        selected_object = bpy.context.object
        current_frame = bpy.context.scene.frame_current
        
        
        # Calculate End Frame and Start Frame values
        end_frame = context.scene.simple_operator_props.end_frame  # Use context.scene.simple_operator_props
        start_frame = context.scene.simple_operator_props.start_frame  # Use context.scene.simple_operator_props
    
        third_frame = start_frame + math.ceil((end_frame - start_frame) / 3 * 2)
        mid_frame = third_frame + math.ceil((end_frame - third_frame) / 2)
        
        
        
    
        bpy.ops.object.make_single_user(object=True, obdata=True, material=False, animation=False, obdata_animation=False)
        
        
        #Apply Transforms
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        
        # Store initial dimensions
        original_dimensions = selected_object.dimensions.copy()
        
        # Create bounding box around the object
        bounding_box_min, bounding_box_max = selected_object.bound_box[0], selected_object.bound_box[6]

        # Calculate the bottom center of the bounding box
        bottom_center = (
            (bounding_box_max[0] + bounding_box_min[0]) / 2,
            (bounding_box_max[1] + bounding_box_min[1]) / 2,
            bounding_box_min[2]
        )

        # Set the 3D cursor to the bottom center of the bounding box
        bpy.context.scene.cursor.location = bottom_center
        
        # Set the origin point to the 3D cursor location
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        
        # Reset delta_location
        selected_object.delta_location = (0, 0, 0)
        
        # Reset 3D cursor to the world origin
        bpy.context.scene.cursor.location = (0, 0, 0)
        
        
        # Store initial location
        original_location = selected_object.location.copy()
        original_dimensions = selected_object.dimensions.copy()
        
        
    
        
        
        # Determine the new Z location for the third frame only
        selected_object.location.z = selected_object.location.z + abs(context.scene.simple_operator_props.distance_offset)


        # Set keyframes for Third Frame with Bezier interpolation mode
        selected_object.rotation_euler = (0, 0, 0)
        selected_object.scale = (1, 1, 1)
        selected_object.keyframe_insert(data_path="location", frame=third_frame)
        location_fcurve = selected_object.animation_data.action.fcurves.find('location', index=2)  # Z-axis location
        for kp in location_fcurve.keyframe_points:
            if kp.co.x == third_frame:
                kp.interpolation = 'BEZIER'
                
        selected_object.keyframe_insert(data_path="rotation_euler", frame=third_frame)
        selected_object.keyframe_insert(data_path="scale", frame=third_frame)
        
        # Restore original frame and location
        selected_object.location = original_location
        selected_object.dimensions = original_dimensions
        bpy.context.scene.frame_set(current_frame)
        
        
        
        
        
        # Set keyframes for End Frame
        selected_object.location.z = original_location.z
        selected_object.rotation_euler = selected_object.rotation_euler
        selected_object.scale = selected_object.scale
        selected_object.keyframe_insert(data_path="location", frame=end_frame)
        selected_object.keyframe_insert(data_path="rotation_euler", frame=end_frame)
        selected_object.keyframe_insert(data_path="scale", frame=end_frame)
        
        # Set keyframes for Start Frame
        selected_object.location.z = selected_object.location.z
        selected_object.rotation_euler.y = math.radians(180)
        selected_object.scale = (0, 0, 0)
        selected_object.keyframe_insert(data_path="location", frame=start_frame)
        location_fcurve = selected_object.animation_data.action.fcurves.find('location', index=2)  # Z-axis location
        for kp in location_fcurve.keyframe_points:
            if kp.co.x == start_frame:
                kp.interpolation = 'BACK'
            else:
                kp.interpolation = 'BEZIER'
        selected_object.keyframe_insert(data_path="rotation_euler", frame=start_frame)
        selected_object.keyframe_insert(data_path="scale", frame=start_frame)
        
        

        # Set keyframes for Mid Frame
        selected_object.location.z = original_location.z
        selected_object.rotation_euler = (0, 0, 0)
        selected_object.scale = (1, 1, 0.6666666666666667)
        selected_object.keyframe_insert(data_path="location", frame=mid_frame)
        selected_object.keyframe_insert(data_path="rotation_euler", frame=mid_frame)
        selected_object.keyframe_insert(data_path="scale", frame=mid_frame)


        

        return {'FINISHED'}
        
class OBJECT_OT_Pop_Up_Y2(BaseObjectOperator):
    bl_label = "Rotate Object"
    bl_idname = "object.pop_up_y2"
    bl_description = "Pop up and rotate the selected object on Y Axis while animating in or out."
    
    
    

    def execute(self, context):
        selected_object = bpy.context.object
        current_frame = bpy.context.scene.frame_current
        
        
        # Calculate End Frame and Start Frame values
        end_frame = context.scene.simple_operator_props.end_frame  # Use context.scene.simple_operator_props
        start_frame = context.scene.simple_operator_props.start_frame  # Use context.scene.simple_operator_props
    
        third_frame = start_frame + math.ceil((end_frame - start_frame) / 3 * 2)
        mid_frame = third_frame + math.ceil((end_frame - third_frame) / 2)
        
        
        
    
        
        
        
        bpy.ops.object.make_single_user(object=True, obdata=True, material=False, animation=False, obdata_animation=False)
        
        
        #Apply Transforms
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        
        # Store initial dimensions
        original_dimensions = selected_object.dimensions.copy()
        
        # Create bounding box around the object
        bounding_box_min, bounding_box_max = selected_object.bound_box[0], selected_object.bound_box[6]

        # Calculate the bottom center of the bounding box
        bottom_center = (
            (bounding_box_max[0] + bounding_box_min[0]) / 2,
            (bounding_box_max[1] + bounding_box_min[1]) / 2,
            bounding_box_min[2]
        )

        # Set the 3D cursor to the bottom center of the bounding box
        bpy.context.scene.cursor.location = bottom_center
        
        # Set the origin point to the 3D cursor location
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        
        # Reset delta_location
        selected_object.delta_location = (0, 0, 0)
        
        # Reset 3D cursor to the world origin
        bpy.context.scene.cursor.location = (0, 0, 0)
        
        
        # Store initial location
        original_location = selected_object.location.copy()
        original_dimensions = selected_object.dimensions.copy()
        
        
    
        
        
        # Determine the new Z location for the third frame only
        selected_object.location.z = selected_object.location.z + abs(context.scene.simple_operator_props.distance_offset)

        # Set keyframes for Third Frame with Bezier interpolation mode
        selected_object.rotation_euler = (0, 0, 0)
        selected_object.scale = (1, 1, 1)
        selected_object.keyframe_insert(data_path="location", frame=third_frame)
        location_fcurve = selected_object.animation_data.action.fcurves.find('location', index=2)  # Z-axis location
        for kp in location_fcurve.keyframe_points:
            if kp.co.x == third_frame:
                kp.interpolation = 'BEZIER'
                
        selected_object.keyframe_insert(data_path="rotation_euler", frame=third_frame)
        selected_object.keyframe_insert(data_path="scale", frame=third_frame)
        
        # Restore original frame and location
        selected_object.location = original_location
        selected_object.dimensions = original_dimensions
        bpy.context.scene.frame_set(current_frame)
        
        
        
        
        
        # Set keyframes for End Frame
        selected_object.location.z = original_location.z
        selected_object.rotation_euler = selected_object.rotation_euler
        selected_object.scale = selected_object.scale
        selected_object.keyframe_insert(data_path="location", frame=end_frame)
        selected_object.keyframe_insert(data_path="rotation_euler", frame=end_frame)
        selected_object.keyframe_insert(data_path="scale", frame=end_frame)
        
        # Set keyframes for Start Frame
        selected_object.location.z = selected_object.location.z
        selected_object.rotation_euler.y = math.radians(-180)
        selected_object.scale = (0, 0, 0)
        selected_object.keyframe_insert(data_path="location", frame=start_frame)
        location_fcurve = selected_object.animation_data.action.fcurves.find('location', index=2)  # Z-axis location
        for kp in location_fcurve.keyframe_points:
            if kp.co.x == start_frame:
                kp.interpolation = 'BACK'
            else:
                kp.interpolation = 'BEZIER'
        selected_object.keyframe_insert(data_path="rotation_euler", frame=start_frame)
        selected_object.keyframe_insert(data_path="scale", frame=start_frame)
        
        

        # Set keyframes for Mid Frame
        selected_object.location.z = original_location.z
        selected_object.rotation_euler = (0, 0, 0)
        selected_object.scale = (1, 1, 0.6666666666666667)
        selected_object.keyframe_insert(data_path="location", frame=mid_frame)
        selected_object.keyframe_insert(data_path="rotation_euler", frame=mid_frame)
        selected_object.keyframe_insert(data_path="scale", frame=mid_frame)


        

        return {'FINISHED'}
        
class OBJECT_OT_Pop_Up_X(BaseObjectOperator):
    bl_label = "Rotate Object"
    bl_idname = "object.pop_up_x"
    bl_description = "Pop up and rotate the selected object on X Axis while animating in or out."
    
    
    

    def execute(self, context):
        selected_object = bpy.context.object
        current_frame = bpy.context.scene.frame_current
        
        
        # Calculate End Frame and Start Frame values
        end_frame = context.scene.simple_operator_props.end_frame  # Use context.scene.simple_operator_props
        start_frame = context.scene.simple_operator_props.start_frame  # Use context.scene.simple_operator_props
    
        third_frame = start_frame + math.ceil((end_frame - start_frame) / 3 * 2)
        mid_frame = third_frame + math.ceil((end_frame - third_frame) / 2)
        
        
        
    
        
        
        
        bpy.ops.object.make_single_user(object=True, obdata=True, material=False, animation=False, obdata_animation=False)
        
        
        #Apply Transforms
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        
        # Store initial dimensions
        original_dimensions = selected_object.dimensions.copy()
        
        # Create bounding box around the object
        bounding_box_min, bounding_box_max = selected_object.bound_box[0], selected_object.bound_box[6]

        # Calculate the bottom center of the bounding box
        bottom_center = (
            (bounding_box_max[0] + bounding_box_min[0]) / 2,
            (bounding_box_max[1] + bounding_box_min[1]) / 2,
            bounding_box_min[2]
        )

        # Set the 3D cursor to the bottom center of the bounding box
        bpy.context.scene.cursor.location = bottom_center
        
        # Set the origin point to the 3D cursor location
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        
        # Reset delta_location
        selected_object.delta_location = (0, 0, 0)
        
        # Reset 3D cursor to the world origin
        bpy.context.scene.cursor.location = (0, 0, 0)
        
        
        # Store initial location
        original_location = selected_object.location.copy()
        original_dimensions = selected_object.dimensions.copy()
        
        
    
        
        
        # Determine the new Z location for the third frame only
        selected_object.location.z = selected_object.location.z + abs(context.scene.simple_operator_props.distance_offset)

        # Set keyframes for Third Frame with Bezier interpolation mode
        selected_object.rotation_euler = (0, 0, 0)
        selected_object.scale = (1, 1, 1)
        selected_object.keyframe_insert(data_path="location", frame=third_frame)
        location_fcurve = selected_object.animation_data.action.fcurves.find('location', index=2)  # Z-axis location
        for kp in location_fcurve.keyframe_points:
            if kp.co.x == third_frame:
                kp.interpolation = 'BEZIER'
                
        selected_object.keyframe_insert(data_path="rotation_euler", frame=third_frame)
        selected_object.keyframe_insert(data_path="scale", frame=third_frame)
        
        # Restore original frame and location
        selected_object.location = original_location
        selected_object.dimensions = original_dimensions
        bpy.context.scene.frame_set(current_frame)
        
        
        
        
        
        # Set keyframes for End Frame
        selected_object.location.z = original_location.z
        selected_object.rotation_euler = selected_object.rotation_euler
        selected_object.scale = selected_object.scale
        selected_object.keyframe_insert(data_path="location", frame=end_frame)
        selected_object.keyframe_insert(data_path="rotation_euler", frame=end_frame)
        selected_object.keyframe_insert(data_path="scale", frame=end_frame)
        
        # Set keyframes for Start Frame
        selected_object.location.z = selected_object.location.z
        selected_object.rotation_euler.x = math.radians(180)
        selected_object.scale = (0, 0, 0)
        selected_object.keyframe_insert(data_path="location", frame=start_frame)
        location_fcurve = selected_object.animation_data.action.fcurves.find('location', index=2)  # Z-axis location
        for kp in location_fcurve.keyframe_points:
            if kp.co.x == start_frame:
                kp.interpolation = 'BACK'
            else:
                kp.interpolation = 'BEZIER'
        selected_object.keyframe_insert(data_path="rotation_euler", frame=start_frame)
        selected_object.keyframe_insert(data_path="scale", frame=start_frame)
        
        

        # Set keyframes for Mid Frame
        selected_object.location.z = original_location.z
        selected_object.rotation_euler = (0, 0, 0)
        selected_object.scale = (1, 1, 0.6666666666666667)
        selected_object.keyframe_insert(data_path="location", frame=mid_frame)
        selected_object.keyframe_insert(data_path="rotation_euler", frame=mid_frame)
        selected_object.keyframe_insert(data_path="scale", frame=mid_frame)


        

        return {'FINISHED'}
        
class OBJECT_OT_Pop_Up_X2(BaseObjectOperator):
    bl_label = "Rotate Object"
    bl_idname = "object.pop_up_x2"
    bl_description = "Pop up and rotate the selected object on X Axis while animating in or out."
    
    
    

    def execute(self, context):
        selected_object = bpy.context.object
        current_frame = bpy.context.scene.frame_current
        
        
        # Calculate End Frame and Start Frame values
        end_frame = context.scene.simple_operator_props.end_frame  # Use context.scene.simple_operator_props
        start_frame = context.scene.simple_operator_props.start_frame  # Use context.scene.simple_operator_props
    
        third_frame = start_frame + math.ceil((end_frame - start_frame) / 3 * 2)
        mid_frame = third_frame + math.ceil((end_frame - third_frame) / 2)
        
        
        
    
        
        
        
        bpy.ops.object.make_single_user(object=True, obdata=True, material=False, animation=False, obdata_animation=False)
        
        
        #Apply Transforms
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        
        # Store initial dimensions
        original_dimensions = selected_object.dimensions.copy()
        
        # Create bounding box around the object
        bounding_box_min, bounding_box_max = selected_object.bound_box[0], selected_object.bound_box[6]

        # Calculate the bottom center of the bounding box
        bottom_center = (
            (bounding_box_max[0] + bounding_box_min[0]) / 2,
            (bounding_box_max[1] + bounding_box_min[1]) / 2,
            bounding_box_min[2]
        )

        # Set the 3D cursor to the bottom center of the bounding box
        bpy.context.scene.cursor.location = bottom_center
        
        # Set the origin point to the 3D cursor location
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        
        # Reset delta_location
        selected_object.delta_location = (0, 0, 0)
        
        # Reset 3D cursor to the world origin
        bpy.context.scene.cursor.location = (0, 0, 0)
        
        
        # Store initial location
        original_location = selected_object.location.copy()
        original_dimensions = selected_object.dimensions.copy()
        
        
    
        
        
        # Determine the new Z location for the third frame only
        selected_object.location.z = selected_object.location.z + abs(context.scene.simple_operator_props.distance_offset)

        # Set keyframes for Third Frame with Bezier interpolation mode
        selected_object.rotation_euler = (0, 0, 0)
        selected_object.scale = (1, 1, 1)
        selected_object.keyframe_insert(data_path="location", frame=third_frame)
        location_fcurve = selected_object.animation_data.action.fcurves.find('location', index=2)  # Z-axis location
        for kp in location_fcurve.keyframe_points:
            if kp.co.x == third_frame:
                kp.interpolation = 'BEZIER'
                
        selected_object.keyframe_insert(data_path="rotation_euler", frame=third_frame)
        selected_object.keyframe_insert(data_path="scale", frame=third_frame)
        
        # Restore original frame and location
        selected_object.location = original_location
        selected_object.dimensions = original_dimensions
        bpy.context.scene.frame_set(current_frame)
        
        
        
        
        
        # Set keyframes for End Frame
        selected_object.location.z = original_location.z
        selected_object.rotation_euler = selected_object.rotation_euler
        selected_object.scale = selected_object.scale
        selected_object.keyframe_insert(data_path="location", frame=end_frame)
        selected_object.keyframe_insert(data_path="rotation_euler", frame=end_frame)
        selected_object.keyframe_insert(data_path="scale", frame=end_frame)
        
        # Set keyframes for Start Frame
        selected_object.location.z = selected_object.location.z
        selected_object.rotation_euler.x = math.radians(-180)
        selected_object.scale = (0, 0, 0)
        selected_object.keyframe_insert(data_path="location", frame=start_frame)
        location_fcurve = selected_object.animation_data.action.fcurves.find('location', index=2)  # Z-axis location
        for kp in location_fcurve.keyframe_points:
            if kp.co.x == start_frame:
                kp.interpolation = 'BACK'
            else:
                kp.interpolation = 'BEZIER'
        selected_object.keyframe_insert(data_path="rotation_euler", frame=start_frame)
        selected_object.keyframe_insert(data_path="scale", frame=start_frame)
        
        

        # Set keyframes for Mid Frame
        selected_object.location.z = original_location.z
        selected_object.rotation_euler = (0, 0, 0)
        selected_object.scale = (1, 1, 0.6666666666666667)
        selected_object.keyframe_insert(data_path="location", frame=mid_frame)
        selected_object.keyframe_insert(data_path="rotation_euler", frame=mid_frame)
        selected_object.keyframe_insert(data_path="scale", frame=mid_frame)


        

        return {'FINISHED'}
   
class OBJECT_OT_Pop_Up(BaseObjectOperator):
    bl_label = "Rotate Object"
    bl_idname = "object.pop_up"
    bl_description = "Pop up the selected object while animating in or out."
    


    def execute(self, context):
        selected_object = bpy.context.object
        current_frame = bpy.context.scene.frame_current
        
        
        # Calculate End Frame and Start Frame values
        end_frame = context.scene.simple_operator_props.end_frame  # Use context.scene.simple_operator_props
        start_frame = context.scene.simple_operator_props.start_frame  # Use context.scene.simple_operator_props
    
        third_frame = start_frame + math.ceil((end_frame - start_frame) / 3 * 2)
        mid_frame = third_frame + math.ceil((end_frame - third_frame) / 2)
        
        
        
        
       
        
        bpy.ops.object.make_single_user(object=True, obdata=True, material=False, animation=False, obdata_animation=False)
        
        
        #Apply Transforms
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        
        # Store initial dimensions
        original_dimensions = selected_object.dimensions.copy()
        
        # Create bounding box around the object
        bounding_box_min, bounding_box_max = selected_object.bound_box[0], selected_object.bound_box[6]

        # Calculate the bottom center of the bounding box
        bottom_center = (
            (bounding_box_max[0] + bounding_box_min[0]) / 2,
            (bounding_box_max[1] + bounding_box_min[1]) / 2,
            bounding_box_min[2]
        )

        # Set the 3D cursor to the bottom center of the bounding box
        bpy.context.scene.cursor.location = bottom_center
        
        # Set the origin point to the 3D cursor location
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        
        # Reset delta_location
        selected_object.delta_location = (0, 0, 0)
        
        # Reset 3D cursor to the world origin
        bpy.context.scene.cursor.location = (0, 0, 0)
        
        
        # Store initial location
        original_location = selected_object.location.copy()
        original_dimensions = selected_object.dimensions.copy()
        
        
        
        
        
        # Determine the new Z location for the third frame only
        selected_object.location.z = selected_object.location.z + abs(context.scene.simple_operator_props.distance_offset)

        # Set keyframes for Third Frame with Bezier interpolation mode
        
        selected_object.scale = (1, 1, 1)
        selected_object.keyframe_insert(data_path="location", frame=third_frame)
        location_fcurve = selected_object.animation_data.action.fcurves.find('location', index=2)  # Z-axis location
        for kp in location_fcurve.keyframe_points:
            if kp.co.x == third_frame:
                kp.interpolation = 'BEZIER'
                
        
        selected_object.keyframe_insert(data_path="scale", frame=third_frame)
        
        # Restore original frame and location
        selected_object.location = original_location
        selected_object.dimensions = original_dimensions
        bpy.context.scene.frame_set(current_frame)
        
        
        
        
        
        # Set keyframes for End Frame
        selected_object.location.z = original_location.z
        
        selected_object.scale = selected_object.scale
        selected_object.keyframe_insert(data_path="location", frame=end_frame)
        
        selected_object.keyframe_insert(data_path="scale", frame=end_frame)
        
        # Set keyframes for Start Frame
        selected_object.location.z = selected_object.location.z
        
        selected_object.scale = (0, 0, 0)
        selected_object.keyframe_insert(data_path="location", frame=start_frame)
        location_fcurve = selected_object.animation_data.action.fcurves.find('location', index=2)  # Z-axis location
        for kp in location_fcurve.keyframe_points:
            if kp.co.x == start_frame:
                kp.interpolation = 'BACK'
            else:
                kp.interpolation = 'BEZIER'
        
        selected_object.keyframe_insert(data_path="scale", frame=start_frame)
        
        

        # Set keyframes for Mid Frame
        selected_object.location.z = original_location.z
        
        selected_object.scale = (1, 1, 0.6666666666666667)
        selected_object.keyframe_insert(data_path="location", frame=mid_frame)
        
        selected_object.keyframe_insert(data_path="scale", frame=mid_frame)
        

        return {'FINISHED'}
       
class OBJECT_OT_Pop_Up_Twist(BaseObjectOperator):
    bl_label = "Pop up and Twist"
    bl_idname = "object.pop_up_twist"
    bl_description = "Pop up the selected object while animating in or out and apply twist deform modifier."

    def execute(self, context):
        selected_object = bpy.context.object
        current_frame = bpy.context.scene.frame_current
        
        # Calculate End Frame, Start Frame, Third Frame, and Mid Frame values
        end_frame = context.scene.simple_operator_props.end_frame
        start_frame = context.scene.simple_operator_props.start_frame
        third_frame = start_frame + math.ceil((end_frame - start_frame) / 3 * 2)
        mid_frame = third_frame + math.ceil((end_frame - third_frame) / 2)
        
        
        bpy.ops.object.make_single_user(object=True, obdata=True, material=False, animation=False, obdata_animation=False)
        
        
        #Apply Transforms
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        
        # Store initial dimensions
        original_dimensions = selected_object.dimensions.copy()
        
        # Create bounding box around the object
        bounding_box_min, bounding_box_max = selected_object.bound_box[0], selected_object.bound_box[6]

        # Calculate the bottom center of the bounding box
        bottom_center = (
            (bounding_box_max[0] + bounding_box_min[0]) / 2,
            (bounding_box_max[1] + bounding_box_min[1]) / 2,
            bounding_box_min[2]
        )

        # Set the 3D cursor to the bottom center of the bounding box
        bpy.context.scene.cursor.location = bottom_center
        
        # Set the origin point to the 3D cursor location
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        
        # Reset delta_location
        selected_object.delta_location = (0, 0, 0)
        
        # Reset 3D cursor to the world origin
        bpy.context.scene.cursor.location = (0, 0, 0)
        
         # Store initial location
        original_location = selected_object.location.copy()
        

        
        # Determine the new Z location for the third frame only
        selected_object.location.z = selected_object.location.z + abs(context.scene.simple_operator_props.distance_offset)

        # Set keyframes for Third Frame with Bezier interpolation mode
        
        selected_object.scale = (1, 1, 1)
        selected_object.keyframe_insert(data_path="location", frame=third_frame)
        location_fcurve = selected_object.animation_data.action.fcurves.find('location', index=2)  # Z-axis location
        for kp in location_fcurve.keyframe_points:
            if kp.co.x == third_frame:
                kp.interpolation = 'BEZIER'
                
        
        selected_object.keyframe_insert(data_path="scale", frame=third_frame)
        
        # Restore original frame and location
        selected_object.location = original_location
        selected_object.dimensions = original_dimensions
        bpy.context.scene.frame_set(current_frame)
        
        
        
        
        
        # Set keyframes for End Frame
        selected_object.location.z = original_location.z
        
        selected_object.scale = selected_object.scale
        selected_object.keyframe_insert(data_path="location", frame=end_frame)
        
        selected_object.keyframe_insert(data_path="scale", frame=end_frame)
        
        # Set keyframes for Start Frame
        selected_object.location.z = selected_object.location.z
        
        selected_object.scale = (0, 0, 0)
        selected_object.keyframe_insert(data_path="location", frame=start_frame)
        location_fcurve = selected_object.animation_data.action.fcurves.find('location', index=2)  # Z-axis location
        for kp in location_fcurve.keyframe_points:
            if kp.co.x == start_frame:
                kp.interpolation = 'BACK'
            else:
                kp.interpolation = 'BEZIER'
        
        selected_object.keyframe_insert(data_path="scale", frame=start_frame)
        
        

        # Set keyframes for Mid Frame
        selected_object.location.z = original_location.z
        
        selected_object.scale = (1, 1, 0.6666666666666667)
        selected_object.keyframe_insert(data_path="location", frame=mid_frame)
        
        selected_object.keyframe_insert(data_path="scale", frame=mid_frame)
        
        # Delete existing Simple Deform modifier if it exists
        existing_twist_modifier = selected_object.modifiers.get("SimpleDeform")
        if existing_twist_modifier:
            selected_object.modifiers.remove(existing_twist_modifier)
        

        # Apply Twist modifier
        bpy.ops.object.modifier_add(type='SIMPLE_DEFORM')
        twist_modifier = selected_object.modifiers["SimpleDeform"]
        twist_modifier.deform_method = 'TWIST'
        twist_modifier.angle = 0
        twist_modifier.deform_axis = 'Z' 
        
        # Convert degrees to radians for angle property
        angle_degrees = -100  # Desired angle in degrees (negative for counterclockwise twist)
        angle_radians = math.radians(angle_degrees)
        
        # Keyframe Twist modifier angle at different frames
        twist_modifier.keyframe_insert(data_path="angle", frame=start_frame)
        twist_modifier.angle = angle_radians
        twist_modifier.keyframe_insert(data_path="angle", frame=third_frame)
        twist_modifier.angle = 0
        twist_modifier.keyframe_insert(data_path="angle", frame=mid_frame)

        # Restore original frame, dimensions, and location
        selected_object.dimensions = original_dimensions
        selected_object.location = original_location
        bpy.context.scene.frame_set(current_frame)

        return {'FINISHED'} 
    
class OBJECT_OT_Pop_Up_Z(BaseObjectOperator):
    bl_label = "Rotate Object"
    bl_idname = "object.pop_up_z"
    bl_description = "Pop up and rotate the selected object on Z Axis while animating in or out."
    


    def execute(self, context):
        selected_object = bpy.context.object
        current_frame = bpy.context.scene.frame_current
        
        
        # Calculate End Frame and Start Frame values
        end_frame = context.scene.simple_operator_props.end_frame  # Use context.scene.simple_operator_props
        start_frame = context.scene.simple_operator_props.start_frame  # Use context.scene.simple_operator_props
    
        third_frame = start_frame + math.ceil((end_frame - start_frame) / 3 * 2)
        mid_frame = third_frame + math.ceil((end_frame - third_frame) / 2)
    
        
        bpy.ops.object.make_single_user(object=True, obdata=True, material=False, animation=False, obdata_animation=False)
        
        
        #Apply Transforms
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        
        # Store initial dimensions
        original_dimensions = selected_object.dimensions.copy()
        
        # Create bounding box around the object
        bounding_box_min, bounding_box_max = selected_object.bound_box[0], selected_object.bound_box[6]

        # Calculate the bottom center of the bounding box
        bottom_center = (
            (bounding_box_max[0] + bounding_box_min[0]) / 2,
            (bounding_box_max[1] + bounding_box_min[1]) / 2,
            bounding_box_min[2]
        )

        # Set the 3D cursor to the bottom center of the bounding box
        bpy.context.scene.cursor.location = bottom_center
        
        # Set the origin point to the 3D cursor location
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        
        # Reset delta_location
        selected_object.delta_location = (0, 0, 0)
        
        # Reset 3D cursor to the world origin
        bpy.context.scene.cursor.location = (0, 0, 0)
        
        
        # Store initial Location
        original_location = selected_object.location.copy()
        original_dimensions = selected_object.dimensions.copy()
        
        
        
        
        
        # Determine the new Z location for the third frame only
        selected_object.location.z = selected_object.location.z + abs(context.scene.simple_operator_props.distance_offset)

        # Set keyframes for Third Frame with Bezier interpolation mode
        selected_object.rotation_euler = (0, 0, 0)
        selected_object.scale = (1, 1, 1)
        selected_object.keyframe_insert(data_path="location", frame=third_frame)
        location_fcurve = selected_object.animation_data.action.fcurves.find('location', index=2)  # Z-axis location
        for kp in location_fcurve.keyframe_points:
            if kp.co.x == third_frame:
                kp.interpolation = 'BEZIER'
                
        selected_object.keyframe_insert(data_path="rotation_euler", frame=third_frame)
        selected_object.keyframe_insert(data_path="scale", frame=third_frame)
        
        # Restore original frame and location
        selected_object.location = original_location
        selected_object.dimensions = original_dimensions
        bpy.context.scene.frame_set(current_frame)
        
        
        
        
        
        # Set keyframes for End Frame
        selected_object.location.z = original_location.z
        selected_object.rotation_euler = selected_object.rotation_euler
        selected_object.scale = selected_object.scale
        selected_object.keyframe_insert(data_path="location", frame=end_frame)
        selected_object.keyframe_insert(data_path="rotation_euler", frame=end_frame)
        selected_object.keyframe_insert(data_path="scale", frame=end_frame)
        
        # Set keyframes for Start Frame
        selected_object.location.z = selected_object.location.z
        selected_object.rotation_euler.z = math.radians(180)
        selected_object.scale = (0, 0, 0)
        selected_object.keyframe_insert(data_path="location", frame=start_frame)
        location_fcurve = selected_object.animation_data.action.fcurves.find('location', index=2)  # Z-axis location
        for kp in location_fcurve.keyframe_points:
            if kp.co.x == start_frame:
                kp.interpolation = 'BACK'
            else:
                kp.interpolation = 'BEZIER'
        selected_object.keyframe_insert(data_path="rotation_euler", frame=start_frame)
        selected_object.keyframe_insert(data_path="scale", frame=start_frame)
        
        

        # Set keyframes for Mid Frame
        selected_object.location.z = original_location.z
        selected_object.rotation_euler = (0, 0, 0)
        selected_object.scale = (1, 1, 0.6666666666666667)
        selected_object.keyframe_insert(data_path="location", frame=mid_frame)
        selected_object.keyframe_insert(data_path="rotation_euler", frame=mid_frame)
        selected_object.keyframe_insert(data_path="scale", frame=mid_frame)

        

        return {'FINISHED'}
    
class OBJECT_OT_Pop_Up_Z2(BaseObjectOperator):
    bl_label = "Rotate Object"
    bl_idname = "object.pop_up_z2"
    bl_description = "Pop up and rotate the selected object on Z Axis while animating in or out."
    


    def execute(self, context):
        selected_object = bpy.context.object
        current_frame = bpy.context.scene.frame_current
        
        
        # Calculate End Frame and Start Frame values
        end_frame = context.scene.simple_operator_props.end_frame  # Use context.scene.simple_operator_props
        start_frame = context.scene.simple_operator_props.start_frame  # Use context.scene.simple_operator_props
    
        third_frame = start_frame + math.ceil((end_frame - start_frame) / 3 * 2)
        mid_frame = third_frame + math.ceil((end_frame - third_frame) / 2)
    
        
        bpy.ops.object.make_single_user(object=True, obdata=True, material=False, animation=False, obdata_animation=False)
        
        
        #Apply Transforms
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        
        # Store initial dimensions
        original_dimensions = selected_object.dimensions.copy()
        
        # Create bounding box around the object
        bounding_box_min, bounding_box_max = selected_object.bound_box[0], selected_object.bound_box[6]

        # Calculate the bottom center of the bounding box
        bottom_center = (
            (bounding_box_max[0] + bounding_box_min[0]) / 2,
            (bounding_box_max[1] + bounding_box_min[1]) / 2,
            bounding_box_min[2]
        )

        # Set the 3D cursor to the bottom center of the bounding box
        bpy.context.scene.cursor.location = bottom_center
        
        # Set the origin point to the 3D cursor location
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        
        # Reset delta_location
        selected_object.delta_location = (0, 0, 0)
        
        # Reset 3D cursor to the world origin
        bpy.context.scene.cursor.location = (0, 0, 0)
        
        
        # Store initial Location
        original_location = selected_object.location.copy()
        original_dimensions = selected_object.dimensions.copy()
        
        
        
        
        
        # Determine the new Z location based on conditions for the third frame only
        longest_dimension = max(original_dimensions.x, original_dimensions.y)
        if original_dimensions.z <= longest_dimension:
            selected_object.location.z = 4 * original_dimensions.z + selected_object.location.z
        elif original_dimensions.z < 2 * longest_dimension:
            selected_object.location.z = 3 * original_dimensions.z + selected_object.location.z
        elif original_dimensions.z < 3 * longest_dimension:
            selected_object.location.z = 1.5 * original_dimensions.z + selected_object.location.z
        else:
            selected_object.location.z = original_dimensions.z + selected_object.location.z

        # Set keyframes for Third Frame with Bezier interpolation mode
        selected_object.rotation_euler = (0, 0, 0)
        selected_object.scale = (1, 1, 1)
        selected_object.keyframe_insert(data_path="location", frame=third_frame)
        location_fcurve = selected_object.animation_data.action.fcurves.find('location', index=2)  # Z-axis location
        for kp in location_fcurve.keyframe_points:
            if kp.co.x == third_frame:
                kp.interpolation = 'BEZIER'
                
        selected_object.keyframe_insert(data_path="rotation_euler", frame=third_frame)
        selected_object.keyframe_insert(data_path="scale", frame=third_frame)
        
        # Restore original frame and location
        selected_object.location = original_location
        selected_object.dimensions = original_dimensions
        bpy.context.scene.frame_set(current_frame)
        
        
        
        
        
        # Set keyframes for End Frame
        selected_object.location.z = original_location.z
        selected_object.rotation_euler = selected_object.rotation_euler
        selected_object.scale = selected_object.scale
        selected_object.keyframe_insert(data_path="location", frame=end_frame)
        selected_object.keyframe_insert(data_path="rotation_euler", frame=end_frame)
        selected_object.keyframe_insert(data_path="scale", frame=end_frame)
        
        # Set keyframes for Start Frame
        selected_object.location.z = selected_object.location.z
        selected_object.rotation_euler.z = math.radians(-180)
        selected_object.scale = (0, 0, 0)
        selected_object.keyframe_insert(data_path="location", frame=start_frame)
        location_fcurve = selected_object.animation_data.action.fcurves.find('location', index=2)  # Z-axis location
        for kp in location_fcurve.keyframe_points:
            if kp.co.x == start_frame:
                kp.interpolation = 'BACK'
            else:
                kp.interpolation = 'BEZIER'
        selected_object.keyframe_insert(data_path="rotation_euler", frame=start_frame)
        selected_object.keyframe_insert(data_path="scale", frame=start_frame)
        
        

        # Set keyframes for Mid Frame
        selected_object.location.z = original_location.z
        selected_object.rotation_euler = (0, 0, 0)
        selected_object.scale = (1, 1, 0.6666666666666667)
        selected_object.keyframe_insert(data_path="location", frame=mid_frame)
        selected_object.keyframe_insert(data_path="rotation_euler", frame=mid_frame)
        selected_object.keyframe_insert(data_path="scale", frame=mid_frame)

        

        return {'FINISHED'}

                        #scale In/out
                        
class OBJECT_OT_ScaleIn(BaseObjectOperator):
    bl_idname = "object.scale_in"
    bl_label = "Scale In"

    def execute(self, context):
        selected_object = bpy.context.object
        current_frame = bpy.context.scene.frame_current
        
        
    
        
        
        bpy.ops.object.make_single_user(object=True, obdata=True, material=False, animation=False, obdata_animation=False)
        
        
        #Apply Transforms
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        
        # Store initial dimensions
        original_dimensions = selected_object.dimensions.copy()
        
        # Create bounding box around the object
        bounding_box_min, bounding_box_max = selected_object.bound_box[0], selected_object.bound_box[6]

        # Calculate the selected origin point
        if context.scene.simple_operator_props.origin_point == 'TOP':
            origin_point = (
                (bounding_box_max[0] + bounding_box_min[0]) / 2,
                (bounding_box_max[1] + bounding_box_min[1]) / 2,
                bounding_box_max[2]
            )
        else:  # Default to 'BOTTOM'
            origin_point = (
                (bounding_box_max[0] + bounding_box_min[0]) / 2,
                (bounding_box_max[1] + bounding_box_min[1]) / 2,
                bounding_box_min[2]
            )

        # Set the 3D cursor to the selected origin point
        bpy.context.scene.cursor.location = origin_point
        
        # Set the origin point to the 3D cursor location
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        
        # Reset delta_location
        selected_object.delta_location = (0, 0, 0)
        
        # Reset 3D cursor to the world origin
        bpy.context.scene.cursor.location = (0, 0, 0)

        
        

        
        # Set keyframes for End Frame
        selected_object.keyframe_insert(data_path="scale", frame=context.scene.simple_operator_props.end_frame)
        


        # Set keyframes for Middle Frame
        middle_frame = context.scene.simple_operator_props.start_frame + ((context.scene.simple_operator_props.end_frame - context.scene.simple_operator_props.start_frame) / 2)
        selected_object.scale = (context.scene.simple_operator_props.object_scale_factor,) * 3
        selected_object.keyframe_insert(data_path="scale", frame=middle_frame)



        # Set keyframes for Start Frame
        selected_object.scale = (0, 0, 0)
        
        selected_object.keyframe_insert(data_path="scale", frame=context.scene.simple_operator_props.start_frame)
        

                
                
        # Restore original frame
        bpy.context.scene.frame_set(current_frame)

        return {'FINISHED'}

                        #animate In
                        
class OBJECT_OT_AnimateIn_Y(BaseObjectOperator):
    bl_idname = "object.animate_in_y"
    bl_label = "Animate In Y"
    bl_description = "Animate selected objects into the scene from the Y axis, or animat it out of the scene towards the Y axis"

    def execute(self, context):
        selected_object = bpy.context.object
        current_frame = bpy.context.scene.frame_current
        
        
    
        
        
        bpy.ops.object.make_single_user(object=True, obdata=True, material=False, animation=False, obdata_animation=False)
        
        
        #Apply Transforms
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        
        # Store initial dimensions
        original_dimensions = selected_object.dimensions.copy()
        
        # Create bounding box around the object
        bounding_box_min, bounding_box_max = selected_object.bound_box[0], selected_object.bound_box[6]

        # Calculate the bottom center of the bounding box
        bottom_center = (
            (bounding_box_max[0] + bounding_box_min[0]) / 2,
            (bounding_box_max[1] + bounding_box_min[1]) / 2,
            bounding_box_min[2]
        )

        # Set the 3D cursor to the bottom center of the bounding box
        bpy.context.scene.cursor.location = bottom_center
        
        # Set the origin point to the 3D cursor location
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        
        # Reset delta_location
        selected_object.delta_location = (0, 0, 0)
        
        # Reset 3D cursor to the world origin
        bpy.context.scene.cursor.location = (0, 0, 0)

        
        

        
        # Set keyframes for End Frame
        selected_object.keyframe_insert(data_path="scale", frame=context.scene.simple_operator_props.end_frame)
        selected_object.keyframe_insert(data_path="location", frame=context.scene.simple_operator_props.end_frame)
        





        # Set keyframes for Start Frame
        selected_object.scale = (0, 0, 0)
        selected_object.location.y = selected_object.location.y + context.scene.simple_operator_props.distance_offset
        selected_object.keyframe_insert(data_path="scale", frame=context.scene.simple_operator_props.start_frame)
        

        selected_object.keyframe_insert(data_path="location", frame=context.scene.simple_operator_props.start_frame)
        location_fcurve = selected_object.animation_data.action.fcurves.find('location', index=1)  # Y-axis location

        

                
        # Restore original frame
        bpy.context.scene.frame_set(current_frame)

        return {'FINISHED'}

class OBJECT_OT_AnimateIn_X(BaseObjectOperator):
    bl_idname = "object.animate_in_x"
    bl_label = "Animate In X"
    bl_description = "Animate selected objects into the scene from the Y axis, or animat it out of the scene towards the Y axis"
    def execute(self, context):
        selected_object = bpy.context.object
        current_frame = bpy.context.scene.frame_current
        
        
    
        
        
        bpy.ops.object.make_single_user(object=True, obdata=True, material=False, animation=False, obdata_animation=False)
        
        
        #Apply Transforms
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        
        # Store initial dimensions
        original_dimensions = selected_object.dimensions.copy()
        
        # Create bounding box around the object
        bounding_box_min, bounding_box_max = selected_object.bound_box[0], selected_object.bound_box[6]

        # Calculate the bottom center of the bounding box
        bottom_center = (
            (bounding_box_max[0] + bounding_box_min[0]) / 2,
            (bounding_box_max[1] + bounding_box_min[1]) / 2,
            bounding_box_min[2]
        )

        # Set the 3D cursor to the bottom center of the bounding box
        bpy.context.scene.cursor.location = bottom_center
        
        # Set the origin point to the 3D cursor location
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        
        # Reset delta_location
        selected_object.delta_location = (0, 0, 0)
        
        # Reset 3D cursor to the world origin
        bpy.context.scene.cursor.location = (0, 0, 0)

        
        

        
        # Set keyframes for End Frame
        selected_object.keyframe_insert(data_path="scale", frame=context.scene.simple_operator_props.end_frame)
        selected_object.keyframe_insert(data_path="location", frame=context.scene.simple_operator_props.end_frame)
        





        # Set keyframes for Start Frame
        selected_object.scale = (0, 0, 0)
        selected_object.location.x = selected_object.location.x + context.scene.simple_operator_props.distance_offset
        selected_object.keyframe_insert(data_path="scale", frame=context.scene.simple_operator_props.start_frame)
        

        selected_object.keyframe_insert(data_path="location", frame=context.scene.simple_operator_props.start_frame)

        

                
        # Restore original frame
        bpy.context.scene.frame_set(current_frame)

        return {'FINISHED'}

class OBJECT_OT_AnimateIn_Z(BaseObjectOperator):
    bl_idname = "object.animate_in_z"
    bl_label = "Animate In Z"
    bl_description = "Animate selected objects into the scene from the Z axis, or animat it out of the scene towards the Y axis"

    def execute(self, context):
        selected_object = bpy.context.object
        current_frame = bpy.context.scene.frame_current
        
        
    
        
        
        bpy.ops.object.make_single_user(object=True, obdata=True, material=False, animation=False, obdata_animation=False)
        
        
        #Apply Transforms
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        
        # Store initial dimensions
        original_dimensions = selected_object.dimensions.copy()
        
        # Create bounding box around the object
        bounding_box_min, bounding_box_max = selected_object.bound_box[0], selected_object.bound_box[6]

        # Calculate the bottom center of the bounding box
        bottom_center = (
            (bounding_box_max[0] + bounding_box_min[0]) / 2,
            (bounding_box_max[1] + bounding_box_min[1]) / 2,
            bounding_box_min[2]
        )

        # Set the 3D cursor to the bottom center of the bounding box
        bpy.context.scene.cursor.location = bottom_center
        
        # Set the origin point to the 3D cursor location
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        
        # Reset delta_location
        selected_object.delta_location = (0, 0, 0)
        
        # Reset 3D cursor to the world origin
        bpy.context.scene.cursor.location = (0, 0, 0)

        
        

        
        # Set keyframes for End Frame
        selected_object.keyframe_insert(data_path="scale", frame=context.scene.simple_operator_props.end_frame)
        selected_object.keyframe_insert(data_path="location", frame=context.scene.simple_operator_props.end_frame)
        





        # Set keyframes for Start Frame
        selected_object.scale = (0, 0, 0)
        selected_object.location.z = selected_object.location.z + context.scene.simple_operator_props.distance_offset
        selected_object.keyframe_insert(data_path="scale", frame=context.scene.simple_operator_props.start_frame)
        

        selected_object.keyframe_insert(data_path="location", frame=context.scene.simple_operator_props.start_frame)

        

                
        # Restore original frame
        bpy.context.scene.frame_set(current_frame)
        return {'FINISHED'}

class OBJECT_OT_B_AnimateIn_Y(BaseObjectOperator):
    bl_label = "Bounce Animate In Y"
    bl_idname = "object.b_animate_in_y"
    bl_description = "Bounce selected objects into the scene from the Y axis, or bounce it out of the scene towards the Y axis"

    def execute(self, context):
        selected_object = bpy.context.object
        current_frame = bpy.context.scene.frame_current
        
        
    
        
        
        bpy.ops.object.make_single_user(object=True, obdata=True, material=False, animation=False, obdata_animation=False)
        
        
        #Apply Transforms
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        
        # Store initial dimensions
        original_dimensions = selected_object.dimensions.copy()
        
        # Create bounding box around the object
        bounding_box_min, bounding_box_max = selected_object.bound_box[0], selected_object.bound_box[6]

        # Calculate the bottom center of the bounding box
        bottom_center = (
            (bounding_box_max[0] + bounding_box_min[0]) / 2,
            (bounding_box_max[1] + bounding_box_min[1]) / 2,
            bounding_box_min[2]
        )

        # Set the 3D cursor to the bottom center of the bounding box
        bpy.context.scene.cursor.location = bottom_center
        
        # Set the origin point to the 3D cursor location
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        
        # Reset delta_location
        selected_object.delta_location = (0, 0, 0)
        
        # Reset 3D cursor to the world origin
        bpy.context.scene.cursor.location = (0, 0, 0)

        
        

        
        # Set keyframes for End Frame
        selected_object.keyframe_insert(data_path="scale", frame=context.scene.simple_operator_props.end_frame)
        selected_object.keyframe_insert(data_path="location", frame=context.scene.simple_operator_props.end_frame)
        





        # Set keyframes for Start Frame
        selected_object.scale = (0, 0, 0)
        selected_object.location.y = selected_object.location.y + context.scene.simple_operator_props.distance_offset
        selected_object.keyframe_insert(data_path="scale", frame=context.scene.simple_operator_props.start_frame)
        
        # Set interpolation mode to "Back" for location keyframe at Start Frame
        selected_object.keyframe_insert(data_path="location", frame=context.scene.simple_operator_props.start_frame)
        location_fcurve = selected_object.animation_data.action.fcurves.find('location', index=1)  # Y-axis location
        for kp in location_fcurve.keyframe_points:
            if kp.co.x == context.scene.simple_operator_props.start_frame:
                kp.interpolation = 'BACK'

        # Set interpolation mode to "Back" for scale keyframes at Start Frame (X, Y, and Z axes)
        for i in range(3):
            scale_fcurve = selected_object.animation_data.action.fcurves.find('scale', index=i)
            for kp in scale_fcurve.keyframe_points:
                if kp.co.x == context.scene.simple_operator_props.start_frame:
                    kp.interpolation = 'BACK'
        

                
        # Restore original frame
        bpy.context.scene.frame_set(current_frame)

        return {'FINISHED'}    

class OBJECT_OT_B_AnimateIn_X(BaseObjectOperator):
    bl_label = "Bounce Animate In Y"
    bl_idname = "object.b_animate_in_x"
    bl_description = "Bounce selected objects into the scene from the X axis, or bounce it out of the scene towards the X axis."

    def execute(self, context):
        selected_object = bpy.context.object
        current_frame = bpy.context.scene.frame_current
        
        
    
        
        
        bpy.ops.object.make_single_user(object=True, obdata=True, material=False, animation=False, obdata_animation=False)
        
        
        #Apply Transforms
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        
        # Store initial dimensions
        original_dimensions = selected_object.dimensions.copy()
        
        # Create bounding box around the object
        bounding_box_min, bounding_box_max = selected_object.bound_box[0], selected_object.bound_box[6]

        # Calculate the bottom center of the bounding box
        bottom_center = (
            (bounding_box_max[0] + bounding_box_min[0]) / 2,
            (bounding_box_max[1] + bounding_box_min[1]) / 2,
            bounding_box_min[2]
        )

        # Set the 3D cursor to the bottom center of the bounding box
        bpy.context.scene.cursor.location = bottom_center
        
        # Set the origin point to the 3D cursor location
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        
        # Reset delta_location
        selected_object.delta_location = (0, 0, 0)
        
        # Reset 3D cursor to the world origin
        bpy.context.scene.cursor.location = (0, 0, 0)

        
        

        
        # Set keyframes for End Frame
        selected_object.keyframe_insert(data_path="scale", frame=context.scene.simple_operator_props.end_frame)
        selected_object.keyframe_insert(data_path="location", frame=context.scene.simple_operator_props.end_frame)
        





        # Set keyframes for Start Frame
        selected_object.scale = (0, 0, 0)
        selected_object.location.x = selected_object.location.x + context.scene.simple_operator_props.distance_offset
        selected_object.keyframe_insert(data_path="scale", frame=context.scene.simple_operator_props.start_frame)
        
        # Set interpolation mode to "Back" for location keyframe at Start Frame (X-axis)
        selected_object.keyframe_insert(data_path="location", frame=context.scene.simple_operator_props.start_frame)
        location_fcurve = selected_object.animation_data.action.fcurves.find('location', index=0)  # X-axis location
        for kp in location_fcurve.keyframe_points:
            if kp.co.x == context.scene.simple_operator_props.start_frame:
                kp.interpolation = 'BACK'


        # Set interpolation mode to "Back" for scale keyframes at Start Frame (X, Y, and Z axes)
        for i in range(3):
            scale_fcurve = selected_object.animation_data.action.fcurves.find('scale', index=i)
            for kp in scale_fcurve.keyframe_points:
                if kp.co.x == context.scene.simple_operator_props.start_frame:
                    kp.interpolation = 'BACK'
        

                
        # Restore original frame
        bpy.context.scene.frame_set(current_frame)

        return {'FINISHED'}
    
class OBJECT_OT_B_AnimateIn_Z(BaseObjectOperator):
    bl_label = "Bounce Animate In Y"
    bl_idname = "object.b_animate_in_z"
    bl_description = "Bounce selected objects into the scene from the Z axis, or bounce it out of the scene towards the Z axis."

    def execute(self, context):
        selected_object = bpy.context.object
        current_frame = bpy.context.scene.frame_current
        
        
    
        
        
        bpy.ops.object.make_single_user(object=True, obdata=True, material=False, animation=False, obdata_animation=False)
        
        
        #Apply Transforms
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        
        # Store initial dimensions
        original_dimensions = selected_object.dimensions.copy()
        
        # Create bounding box around the object
        bounding_box_min, bounding_box_max = selected_object.bound_box[0], selected_object.bound_box[6]

        # Calculate the bottom center of the bounding box
        bottom_center = (
            (bounding_box_max[0] + bounding_box_min[0]) / 2,
            (bounding_box_max[1] + bounding_box_min[1]) / 2,
            bounding_box_min[2]
        )

        # Set the 3D cursor to the bottom center of the bounding box
        bpy.context.scene.cursor.location = bottom_center
        
        # Set the origin point to the 3D cursor location
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        
        # Reset delta_location
        selected_object.delta_location = (0, 0, 0)
        
        # Reset 3D cursor to the world origin
        bpy.context.scene.cursor.location = (0, 0, 0)

        
        

        
        # Set keyframes for End Frame
        selected_object.keyframe_insert(data_path="scale", frame=context.scene.simple_operator_props.end_frame)
        selected_object.keyframe_insert(data_path="location", frame=context.scene.simple_operator_props.end_frame)
        





        # Set keyframes for Start Frame
        selected_object.scale = (0, 0, 0)
        selected_object.location.z = selected_object.location.z + context.scene.simple_operator_props.distance_offset
        selected_object.keyframe_insert(data_path="scale", frame=context.scene.simple_operator_props.start_frame)
        
        # Set interpolation mode to "Back" for location keyframe at Start Frame (Z-axis)
        selected_object.keyframe_insert(data_path="location", frame=context.scene.simple_operator_props.start_frame)
        location_fcurve = selected_object.animation_data.action.fcurves.find('location', index=2)  # Z-axis location
        for kp in location_fcurve.keyframe_points:
            if kp.co.x == context.scene.simple_operator_props.start_frame:
                kp.interpolation = 'BACK'

        # Set interpolation mode to "Back" for scale keyframes at Start Frame (X, Y, and Z axes)
        for i in range(3):
            scale_fcurve = selected_object.animation_data.action.fcurves.find('scale', index=i)
            for kp in scale_fcurve.keyframe_points:
                if kp.co.x == context.scene.simple_operator_props.start_frame:
                    kp.interpolation = 'BACK'
        

                
        # Restore original frame
        bpy.context.scene.frame_set(current_frame)
        return {'FINISHED'}        

class OBJECT_OT_Fall_Down_Z(BaseObjectOperator):
    bl_label = "Object Fall Down"
    bl_idname = "object.fall_down_z"
    bl_description = "Object Fall From the Top"

    def execute(self, context):
        selected_object = bpy.context.object
        current_frame = bpy.context.scene.frame_current
        
        
    
        
        
        bpy.ops.object.make_single_user(object=True, obdata=True, material=False, animation=False, obdata_animation=False)
        
        
        #Apply Transforms
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        
        # Store initial dimensions
        original_dimensions = selected_object.dimensions.copy()
        
        # Create bounding box around the object
        bounding_box_min, bounding_box_max = selected_object.bound_box[0], selected_object.bound_box[6]

        # Calculate the bottom center of the bounding box
        bottom_center = (
            (bounding_box_max[0] + bounding_box_min[0]) / 2,
            (bounding_box_max[1] + bounding_box_min[1]) / 2,
            bounding_box_min[2]
        )

        # Set the 3D cursor to the bottom center of the bounding box
        bpy.context.scene.cursor.location = bottom_center
        
        # Set the origin point to the 3D cursor location
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        
        # Reset delta_location
        selected_object.delta_location = (0, 0, 0)
        
        # Reset 3D cursor to the world origin
        bpy.context.scene.cursor.location = (0, 0, 0)

        
        

        
        # Set keyframes for End Frame
        selected_object.keyframe_insert(data_path="scale", frame=context.scene.simple_operator_props.end_frame)
        
        


        # Calculate middle frames
        middle_frame1 = (context.scene.simple_operator_props.start_frame + context.scene.simple_operator_props.end_frame) // 2
        middle_frame2 = (middle_frame1 + context.scene.simple_operator_props.end_frame) // 2
        
        
        
        # Set keyframes for the second middle frame with scale (1, 1, 0.5)
        selected_object.keyframe_insert(data_path="location", frame=middle_frame2)
        selected_object.scale = (1, 1, context.scene.simple_operator_props.object_min_scale_factor)
        selected_object.keyframe_insert(data_path="scale", frame=middle_frame2)
        
        # Set keyframes for the first middle frame with scale (1, 1, 1)
        selected_object.scale = (1, 1, 1)
        
        selected_object.keyframe_insert(data_path="scale", frame=middle_frame1)
        
        
        



        # Set keyframes for Start Frame
        selected_object.scale = (0, 0, 0)
        selected_object.location.z = selected_object.location.z + abs(context.scene.simple_operator_props.distance_offset)
        selected_object.keyframe_insert(data_path="scale", frame=context.scene.simple_operator_props.start_frame)
        
        selected_object.keyframe_insert(data_path="location", frame=context.scene.simple_operator_props.start_frame)


        # Set interpolation mode to "Back" for scale keyframes at Start Frame (X, Y, and Z axes)
        for i in range(3):
            scale_fcurve = selected_object.animation_data.action.fcurves.find('scale', index=i)
            for kp in scale_fcurve.keyframe_points:
                if kp.co.x == context.scene.simple_operator_props.start_frame:
                    kp.interpolation = 'BACK'
        

                
        # Restore original frame
        bpy.context.scene.frame_set(current_frame)

        return {'FINISHED'}        

class OBJECT_OT_AnimateIn_Y_Rotate(BaseObjectOperator):
    bl_label = "Spiral In Y"
    bl_idname = "object.animate_in_y_rotate"
    bl_description = "Animate the selected object from the Y axis, while rotating around the Spiral Direction"

    def execute(self, context):
        selected_object = bpy.context.object
        current_frame = bpy.context.scene.frame_current
        
        
    
        
        bpy.ops.object.make_single_user(object=True, obdata=True, material=False, animation=False, obdata_animation=False)
        
        #Apply Transforms
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        
        # Store initial dimensions
        original_dimensions = selected_object.dimensions.copy()
        
        
        
        # Set the origin point of the selected object to the center of its geometry
        bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_VOLUME', center='MEDIAN')
        


        
        

        
        # Set keyframes for End Frame
        selected_object.keyframe_insert(data_path="scale", frame=context.scene.simple_operator_props.end_frame)
        selected_object.keyframe_insert(data_path="location", frame=context.scene.simple_operator_props.end_frame)
        selected_object.keyframe_insert(data_path="rotation_euler", frame=context.scene.simple_operator_props.end_frame)
        





        # Set keyframes for Start Frame
        selected_object.scale = (0, 0, 0)
                
        if context.scene.simple_operator_props.spiral_direction == 'X':
            selected_object.rotation_euler = (math.radians(context.scene.simple_operator_props.spiral_angle), 0, 0)
        elif context.scene.simple_operator_props.spiral_direction == 'Y':
            selected_object.rotation_euler = (0, math.radians(context.scene.simple_operator_props.spiral_angle), 0)
        elif context.scene.simple_operator_props.spiral_direction == 'Z':
            selected_object.rotation_euler = (0, 0, math.radians(context.scene.simple_operator_props.spiral_angle))
         
        selected_object.location.y = selected_object.location.y + context.scene.simple_operator_props.distance_offset
        selected_object.keyframe_insert(data_path="scale", frame=context.scene.simple_operator_props.start_frame)
        selected_object.keyframe_insert(data_path="rotation_euler", frame=context.scene.simple_operator_props.start_frame)
        selected_object.keyframe_insert(data_path="location", frame=context.scene.simple_operator_props.start_frame)
        

        # Set interpolation mode to "Back" for scale keyframes at Start Frame (X, Y, and Z axes)
        for i in range(3):
            scale_fcurve = selected_object.animation_data.action.fcurves.find('scale', index=i)
            for kp in scale_fcurve.keyframe_points:
                if kp.co.x == context.scene.simple_operator_props.start_frame:
                    kp.interpolation = 'BACK'
        

                
        # Restore original frame
        bpy.context.scene.frame_set(current_frame)

        return {'FINISHED'}
    
class OBJECT_OT_AnimateIn_X_Rotate(BaseObjectOperator):
    bl_label = "Spiral In X"
    bl_idname = "object.animate_in_x_rotate"
    bl_description = "Animate the selected object from the X axis, while rotating around the Spiral Direction"

    def execute(self, context):
        selected_object = bpy.context.object
        current_frame = bpy.context.scene.frame_current
        
        
        
        
        
        bpy.ops.object.make_single_user(object=True, obdata=True, material=False, animation=False, obdata_animation=False)
        
        
    
        
        
        #Apply Transforms
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        
        # Store initial dimensions
        original_dimensions = selected_object.dimensions.copy()
        
        
        
        # Set the origin point of the selected object to the center of its geometry
        bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_VOLUME', center='MEDIAN')
        


        
        

        
        # Set keyframes for End Frame
        selected_object.keyframe_insert(data_path="scale", frame=context.scene.simple_operator_props.end_frame)
        selected_object.keyframe_insert(data_path="location", frame=context.scene.simple_operator_props.end_frame)
        selected_object.keyframe_insert(data_path="rotation_euler", frame=context.scene.simple_operator_props.end_frame)
        





        # Set keyframes for Start Frame
        selected_object.scale = (0, 0, 0)
                
        if context.scene.simple_operator_props.spiral_direction == 'X':
            selected_object.rotation_euler = (math.radians(context.scene.simple_operator_props.spiral_angle), 0, 0)
        elif context.scene.simple_operator_props.spiral_direction == 'Y':
            selected_object.rotation_euler = (0, math.radians(context.scene.simple_operator_props.spiral_angle), 0)
        elif context.scene.simple_operator_props.spiral_direction == 'Z':
            selected_object.rotation_euler = (0, 0, math.radians(context.scene.simple_operator_props.spiral_angle))
         
        selected_object.location.x = selected_object.location.x + context.scene.simple_operator_props.distance_offset
        selected_object.keyframe_insert(data_path="scale", frame=context.scene.simple_operator_props.start_frame)
        selected_object.keyframe_insert(data_path="rotation_euler", frame=context.scene.simple_operator_props.start_frame)
        selected_object.keyframe_insert(data_path="location", frame=context.scene.simple_operator_props.start_frame)
        

        # Set interpolation mode to "Back" for scale keyframes at Start Frame (X, Y, and Z axes)
        for i in range(3):
            scale_fcurve = selected_object.animation_data.action.fcurves.find('scale', index=i)
            for kp in scale_fcurve.keyframe_points:
                if kp.co.x == context.scene.simple_operator_props.start_frame:
                    kp.interpolation = 'BACK'
        

                
        # Restore original frame
        bpy.context.scene.frame_set(current_frame)

        return {'FINISHED'}
        
class OBJECT_OT_AnimateIn_Z_Rotate(BaseObjectOperator):
    bl_label = "Animate In Z"
    bl_idname = "object.animate_in_z_rotate"
    bl_description = "Animate the selected object from the Z axis, while rotating around the Spiral Direction"

    def execute(self, context):
        selected_object = bpy.context.object
        current_frame = bpy.context.scene.frame_current
        
        
    
        
        bpy.ops.object.make_single_user(object=True, obdata=True, material=False, animation=False, obdata_animation=False)
        
        
        #Apply Transforms
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        
        # Store initial dimensions
        original_dimensions = selected_object.dimensions.copy()
        
        
        
        # Set the origin point of the selected object to the center of its geometry
        bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_VOLUME', center='MEDIAN')
        

        
        

        
        # Set keyframes for End Frame
        selected_object.keyframe_insert(data_path="scale", frame=context.scene.simple_operator_props.end_frame)
        selected_object.keyframe_insert(data_path="location", frame=context.scene.simple_operator_props.end_frame)
        selected_object.keyframe_insert(data_path="rotation_euler", frame=context.scene.simple_operator_props.end_frame)
        





        # Set keyframes for Start Frame
        selected_object.scale = (0, 0, 0)
        
        if context.scene.simple_operator_props.spiral_direction == 'X':
            selected_object.rotation_euler = (math.radians(context.scene.simple_operator_props.spiral_angle), 0, 0)
        elif context.scene.simple_operator_props.spiral_direction == 'Y':
            selected_object.rotation_euler = (0, math.radians(context.scene.simple_operator_props.spiral_angle), 0)
        elif context.scene.simple_operator_props.spiral_direction == 'Z':
            selected_object.rotation_euler = (0, 0, math.radians(context.scene.simple_operator_props.spiral_angle))
            
        selected_object.location.z = selected_object.location.z + context.scene.simple_operator_props.distance_offset
        selected_object.keyframe_insert(data_path="scale", frame=context.scene.simple_operator_props.start_frame)
        selected_object.keyframe_insert(data_path="rotation_euler", frame=context.scene.simple_operator_props.start_frame)
        selected_object.keyframe_insert(data_path="location", frame=context.scene.simple_operator_props.start_frame)
        

        # Set interpolation mode to "Back" for scale keyframes at Start Frame (X, Y, and Z axes)
        for i in range(3):
            scale_fcurve = selected_object.animation_data.action.fcurves.find('scale', index=i)
            for kp in scale_fcurve.keyframe_points:
                if kp.co.x == context.scene.simple_operator_props.start_frame:
                    kp.interpolation = 'BACK'
        

                
        # Restore original frame
        bpy.context.scene.frame_set(current_frame)

        return {'FINISHED'}

class OBJECT_OT_RotateIn_Z(BaseObjectOperator):
    bl_label = "Rotate In"
    bl_idname = "object.rotate_in_z"

    def execute(self, context):
        selected_object = bpy.context.object
        current_frame = bpy.context.scene.frame_current
        bl_description = "Rotate and Scale the selected object in or out."
        

        
        
        bpy.ops.object.make_single_user(object=True, obdata=True, material=False, animation=False, obdata_animation=False)
        
        
        #Apply Transforms
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        
        # Store initial dimensions
        original_dimensions = selected_object.dimensions.copy()
        
        # Create bounding box around the object
        bounding_box_min, bounding_box_max = selected_object.bound_box[0], selected_object.bound_box[6]

        # Calculate the selected origin point
        if context.scene.simple_operator_props.origin_point == 'TOP':
            origin_point = (
                (bounding_box_max[0] + bounding_box_min[0]) / 2,
                (bounding_box_max[1] + bounding_box_min[1]) / 2,
                bounding_box_max[2]
            )
        else:  # Default to 'BOTTOM'
            origin_point = (
                (bounding_box_max[0] + bounding_box_min[0]) / 2,
                (bounding_box_max[1] + bounding_box_min[1]) / 2,
                bounding_box_min[2]
            )

        # Set the 3D cursor to the selected origin point
        bpy.context.scene.cursor.location = origin_point
        
        # Set the origin point to the 3D cursor location
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        
        # Reset delta_location
        selected_object.delta_location = (0, 0, 0)
        
        # Reset 3D cursor to the world origin
        bpy.context.scene.cursor.location = (0, 0, 0)

        
        # Set keyframes for End Frame
        selected_object.keyframe_insert(data_path="scale", frame=context.scene.simple_operator_props.end_frame)
        selected_object.keyframe_insert(data_path="rotation_euler", frame=context.scene.simple_operator_props.end_frame)

        # Set keyframes for Start Frame
        selected_object.scale = (0, 0, 0)
        selected_object.rotation_euler = (0, 0, math.radians(context.scene.simple_operator_props.rotate_angle))
        selected_object.keyframe_insert(data_path="scale", frame=context.scene.simple_operator_props.start_frame)
        selected_object.keyframe_insert(data_path="rotation_euler", frame=context.scene.simple_operator_props.start_frame)

        
        
        # Restore original frame
        bpy.context.scene.frame_set(current_frame)

        return {'FINISHED'}
   
class OBJECT_OT_RotateIn_Z2(BaseObjectOperator):
    bl_label = "Rotate In"
    bl_idname = "object.rotate_in_z2"

    def execute(self, context):
        selected_object = bpy.context.object
        current_frame = bpy.context.scene.frame_current
        bl_description = "Rotate and Scale the selected object in or out."
        

        
        bpy.ops.object.make_single_user(object=True, obdata=True, material=False, animation=False, obdata_animation=False)
        
        
        #Apply Transforms
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        
        # Store initial dimensions
        original_dimensions = selected_object.dimensions.copy()
        
        
        # Create bounding box around the object
        bounding_box_min, bounding_box_max = selected_object.bound_box[0], selected_object.bound_box[6]

        # Calculate the selected origin point
        if context.scene.simple_operator_props.origin_point == 'TOP':
            origin_point = (
                (bounding_box_max[0] + bounding_box_min[0]) / 2,
                (bounding_box_max[1] + bounding_box_min[1]) / 2,
                bounding_box_max[2]
            )
        else:  # Default to 'BOTTOM'
            origin_point = (
                (bounding_box_max[0] + bounding_box_min[0]) / 2,
                (bounding_box_max[1] + bounding_box_min[1]) / 2,
                bounding_box_min[2]
            )

        # Set the 3D cursor to the selected origin point
        bpy.context.scene.cursor.location = origin_point
        
        # Set the origin point to the 3D cursor location
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        
        # Reset delta_location
        selected_object.delta_location = (0, 0, 0)
        
        # Reset 3D cursor to the world origin
        bpy.context.scene.cursor.location = (0, 0, 0)

        
        # Set keyframes for End Frame
        selected_object.keyframe_insert(data_path="scale", frame=context.scene.simple_operator_props.end_frame)
        selected_object.keyframe_insert(data_path="rotation_euler", frame=context.scene.simple_operator_props.end_frame)

        # Set keyframes for Start Frame
        selected_object.scale = (0, 0, 0)
        selected_object.rotation_euler = (0, 0, math.radians(-context.scene.simple_operator_props.rotate_angle))
        selected_object.keyframe_insert(data_path="scale", frame=context.scene.simple_operator_props.start_frame)
        selected_object.keyframe_insert(data_path="rotation_euler", frame=context.scene.simple_operator_props.start_frame)

        
        
        # Restore original frame
        bpy.context.scene.frame_set(current_frame)

        return {'FINISHED'}   
       
class OBJECT_OT_RotateIn_Y(BaseObjectOperator):
    bl_label = "Rotate In"
    bl_idname = "object.rotate_in_y"

    def execute(self, context):
        selected_object = bpy.context.object
        current_frame = bpy.context.scene.frame_current
        bl_description = "Rotate and Scale the selected object in or out."
        

        
        bpy.ops.object.make_single_user(object=True, obdata=True, material=False, animation=False, obdata_animation=False)

        
        
        
        #Apply Transforms
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        
        # Store initial dimensions
        original_dimensions = selected_object.dimensions.copy()
        
        
        
       # Create bounding box around the object
        bounding_box_min, bounding_box_max = selected_object.bound_box[0], selected_object.bound_box[6]

        # Calculate the selected origin point
        if context.scene.simple_operator_props.origin_point == 'TOP':
            origin_point = (
                bounding_box_max[0],  # Max X
                (bounding_box_max[1] + bounding_box_min[1]) / 2,  # Midpoint Y
                bounding_box_max[2]  # Max Z
            )
        else:  # Default to 'BOTTOM'
            origin_point = (
                bounding_box_max[0],  # Max X
                (bounding_box_max[1] + bounding_box_min[1]) / 2,  # Midpoint Y
                bounding_box_min[2]  # Min Z
            )
            
        # Set the 3D cursor to the selected origin point
        bpy.context.scene.cursor.location = origin_point

        # Set the origin point to the 3D cursor location
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

        # Reset delta_location
        selected_object.delta_location = (0, 0, 0)
        
        # Reset 3D cursor to the world origin
        bpy.context.scene.cursor.location = (0, 0, 0)


        
        # Set keyframes for End Frame
        selected_object.keyframe_insert(data_path="scale", frame=context.scene.simple_operator_props.end_frame)
        selected_object.keyframe_insert(data_path="rotation_euler", frame=context.scene.simple_operator_props.end_frame)

        # Set keyframes for Start Frame
        selected_object.scale = (0, 0, 0)
        selected_object.rotation_euler = (0, math.radians(context.scene.simple_operator_props.rotate_angle), 0)
        selected_object.keyframe_insert(data_path="scale", frame=context.scene.simple_operator_props.start_frame)
        selected_object.keyframe_insert(data_path="rotation_euler", frame=context.scene.simple_operator_props.start_frame)

        
        
        # Restore original frame
        bpy.context.scene.frame_set(current_frame)

        return {'FINISHED'}
    
class OBJECT_OT_RotateIn_Y2(BaseObjectOperator):
    bl_label = "Rotate In"
    bl_idname = "object.rotate_in_y2"

    def execute(self, context):
        selected_object = bpy.context.object
        current_frame = bpy.context.scene.frame_current
        bl_description = "Rotate and Scale the selected object in or out."
        

        
        
        bpy.ops.object.make_single_user(object=True, obdata=True, material=False, animation=False, obdata_animation=False)
        
        #Apply Transforms
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        # Store initial dimensions
        original_dimensions = selected_object.dimensions.copy()
        
        
        
        # Create bounding box around the object
        bounding_box_min, bounding_box_max = selected_object.bound_box[0], selected_object.bound_box[6]
        
        # Calculate the selected origin point
        if context.scene.simple_operator_props.origin_point == 'TOP':
            origin_point = (
                bounding_box_min[0],  # Min X
                (bounding_box_max[1] + bounding_box_min[1]) / 2,  # Midpoint Y
                bounding_box_max[2]  # Max Z
            )
        else:  # Default to 'BOTTOM'
            origin_point = (
                bounding_box_min[0],  # Min X
                (bounding_box_max[1] + bounding_box_min[1]) / 2,  # Midpoint Y
                bounding_box_min[2]  # Min Z
            )
            
        # Set the 3D cursor to the selected origin point
        bpy.context.scene.cursor.location = origin_point
        
        

        # Set the origin point to the 3D cursor location
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

        # Reset delta_location
        selected_object.delta_location = (0, 0, 0)
        
        # Reset 3D cursor to the world origin
        bpy.context.scene.cursor.location = (0, 0, 0)

        
        # Set keyframes for End Frame
        selected_object.keyframe_insert(data_path="scale", frame=context.scene.simple_operator_props.end_frame)
        selected_object.keyframe_insert(data_path="rotation_euler", frame=context.scene.simple_operator_props.end_frame)

        # Set keyframes for Start Frame
        selected_object.scale = (0, 0, 0)
        selected_object.rotation_euler = (0, math.radians(-context.scene.simple_operator_props.rotate_angle), 0)
        selected_object.keyframe_insert(data_path="scale", frame=context.scene.simple_operator_props.start_frame)
        selected_object.keyframe_insert(data_path="rotation_euler", frame=context.scene.simple_operator_props.start_frame)

        
        
        # Restore original frame
        bpy.context.scene.frame_set(current_frame)

        return {'FINISHED'}
        
class OBJECT_OT_RotateIn_X(BaseObjectOperator):
    bl_label = "Rotate In"
    bl_idname = "object.rotate_in_x"

    def execute(self, context):
        selected_object = bpy.context.object
        current_frame = bpy.context.scene.frame_current
        bl_description = "Rotate and Scale the selected object in or out."
        

        bpy.ops.object.make_single_user(object=True, obdata=True, material=False, animation=False, obdata_animation=False)
        
        
        #Apply Transforms
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        
        # Store initial dimensions
        original_dimensions = selected_object.dimensions.copy()
        
        
        # Create bounding box around the object
        bounding_box_min, bounding_box_max = selected_object.bound_box[0], selected_object.bound_box[6]
        
        
        # Calculate the selected origin point
        if context.scene.simple_operator_props.origin_point == 'TOP':
            origin_point = (
                (bounding_box_max[0] + bounding_box_min[0]) / 2,  # Midpoint X
                bounding_box_min[1],  # Min Y
                bounding_box_max[2]  # Max Z
            )
        else:  # Default to 'BOTTOM'
            origin_point = (
                (bounding_box_max[0] + bounding_box_min[0]) / 2,  # Midpoint X
                bounding_box_min[1],  # Min Y
                bounding_box_min[2]  # Min Z
            )
            
        # Set the 3D cursor to the selected origin point
        bpy.context.scene.cursor.location = origin_point
        

        # Set the origin point to the 3D cursor location
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

        # Reset delta_location
        selected_object.delta_location = (0, 0, 0)
        
        # Reset 3D cursor to the world origin
        bpy.context.scene.cursor.location = (0, 0, 0)
        
        

        
        # Set keyframes for End Frame
        selected_object.keyframe_insert(data_path="scale", frame=context.scene.simple_operator_props.end_frame)
        selected_object.keyframe_insert(data_path="rotation_euler", frame=context.scene.simple_operator_props.end_frame)

        # Set keyframes for Start Frame
        selected_object.scale = (0, 0, 0)
        selected_object.rotation_euler = (math.radians(context.scene.simple_operator_props.rotate_angle), 0, 0)
        selected_object.keyframe_insert(data_path="scale", frame=context.scene.simple_operator_props.start_frame)
        selected_object.keyframe_insert(data_path="rotation_euler", frame=context.scene.simple_operator_props.start_frame)

        
        
        # Restore original frame
        bpy.context.scene.frame_set(current_frame)

        return {'FINISHED'}

class OBJECT_OT_RotateIn_X2(BaseObjectOperator):
    bl_label = "Rotate In"
    bl_idname = "object.rotate_in_x2"

    def execute(self, context):
        selected_object = bpy.context.object
        current_frame = bpy.context.scene.frame_current
        bl_description = "Rotate and Scale the selected object in or out."
        

        
        bpy.ops.object.make_single_user(object=True, obdata=True, material=False, animation=False, obdata_animation=False) 
        
        
        #Apply Transforms
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        
        # Store initial dimensions
        original_dimensions = selected_object.dimensions.copy()
        
        
        # Create bounding box around the object
        bounding_box_min, bounding_box_max = selected_object.bound_box[0], selected_object.bound_box[6]
        
        # Calculate the selected origin point
        if context.scene.simple_operator_props.origin_point == 'TOP':
            origin_point = (
                (bounding_box_max[0] + bounding_box_min[0]) / 2,  # Midpoint X
                bounding_box_max[1],  # max Y
                bounding_box_max[2]  # Max Z
            )
        else:  # Default to 'BOTTOM'
            origin_point = (
                (bounding_box_max[0] + bounding_box_min[0]) / 2,  # Midpoint X
                bounding_box_max[1],  # max Y
                bounding_box_min[2]  # Min Z
            )
            
        # Set the 3D cursor to the selected origin point
        bpy.context.scene.cursor.location = origin_point
        

        # Set the origin point to the 3D cursor location
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

        # Reset delta_location
        selected_object.delta_location = (0, 0, 0)
        
        
        # Reset 3D cursor to the world origin
        bpy.context.scene.cursor.location = (0, 0, 0)

        
        # Set keyframes for End Frame
        selected_object.keyframe_insert(data_path="scale", frame=context.scene.simple_operator_props.end_frame)
        selected_object.keyframe_insert(data_path="rotation_euler", frame=context.scene.simple_operator_props.end_frame)

        # Set keyframes for Start Frame
        selected_object.scale = (0, 0, 0)
        selected_object.rotation_euler = (math.radians(-context.scene.simple_operator_props.rotate_angle), 0, 0)
        selected_object.keyframe_insert(data_path="scale", frame=context.scene.simple_operator_props.start_frame)
        selected_object.keyframe_insert(data_path="rotation_euler", frame=context.scene.simple_operator_props.start_frame)

        
        
        # Restore original frame
        bpy.context.scene.frame_set(current_frame)

        return {'FINISHED'} 

class OBJECT_OT_RotateIn_Bounce_Z(BaseObjectOperator):
    bl_label = "Rotate In Bounce"
    bl_idname = "object.rotate_in_bounce_z"
    bl_description = "Rotate and Scale the selected object in or out with a bounce effect."

    def execute(self, context):
        selected_object = bpy.context.object
        current_frame = bpy.context.scene.frame_current
        

        
        
        bpy.ops.object.make_single_user(object=True, obdata=True, material=False, animation=False, obdata_animation=False)
        
        
        #Apply Transforms
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        
        # Store initial dimensions
        original_dimensions = selected_object.dimensions.copy()
        
        # Create bounding box around the object
        bounding_box_min, bounding_box_max = selected_object.bound_box[0], selected_object.bound_box[6]

        # Calculate the selected origin point
        if context.scene.simple_operator_props.origin_point == 'TOP':
            origin_point = (
                (bounding_box_max[0] + bounding_box_min[0]) / 2,
                (bounding_box_max[1] + bounding_box_min[1]) / 2,
                bounding_box_max[2]
            )
        else:  # Default to 'BOTTOM'
            origin_point = (
                (bounding_box_max[0] + bounding_box_min[0]) / 2,
                (bounding_box_max[1] + bounding_box_min[1]) / 2,
                bounding_box_min[2]
            )

        # Set the 3D cursor to the selected origin point
        bpy.context.scene.cursor.location = origin_point
        
        # Set the origin point to the 3D cursor location
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        
        # Reset delta_location
        selected_object.delta_location = (0, 0, 0)
        
        # Reset 3D cursor to the world origin
        bpy.context.scene.cursor.location = (0, 0, 0)

        
        

        
        # Set keyframes for End Frame
        selected_object.keyframe_insert(data_path="scale", frame=context.scene.simple_operator_props.end_frame)
        selected_object.keyframe_insert(data_path="rotation_euler", frame=context.scene.simple_operator_props.end_frame)


        # Set keyframes for Middle Frame
        middle_frame = context.scene.simple_operator_props.start_frame + ((context.scene.simple_operator_props.end_frame - context.scene.simple_operator_props.start_frame) / 2)
        selected_object.scale = (context.scene.simple_operator_props.object_scale_factor,) * 3
        selected_object.keyframe_insert(data_path="scale", frame=middle_frame)



        # Set keyframes for Start Frame
        selected_object.scale = (0, 0, 0)
        selected_object.rotation_euler = (0, 0, math.radians(context.scene.simple_operator_props.rotate_angle))
        selected_object.keyframe_insert(data_path="scale", frame=context.scene.simple_operator_props.start_frame)
        selected_object.keyframe_insert(data_path="rotation_euler", frame=context.scene.simple_operator_props.start_frame)

        

                
                
        # Restore original frame
        bpy.context.scene.frame_set(current_frame)

        return {'FINISHED'}
        
class OBJECT_OT_RotateIn_Bounce_Z2(BaseObjectOperator):
    bl_label = "Rotate In Bounce"
    bl_idname = "object.rotate_in_bounce_z2"
    bl_description = "Rotate and Scale the selected object in or out with a bounce effect."

    def execute(self, context):
        selected_object = bpy.context.object
        current_frame = bpy.context.scene.frame_current
        

        
        
        
        
        
        
        bpy.ops.object.make_single_user(object=True, obdata=True, material=False, animation=False, obdata_animation=False)
        
        
        #Apply Transforms
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        
        # Store initial dimensions
        original_dimensions = selected_object.dimensions.copy()
        
        # Create bounding box around the object
        bounding_box_min, bounding_box_max = selected_object.bound_box[0], selected_object.bound_box[6]

        # Calculate the selected origin point
        if context.scene.simple_operator_props.origin_point == 'TOP':
            origin_point = (
                (bounding_box_max[0] + bounding_box_min[0]) / 2,
                (bounding_box_max[1] + bounding_box_min[1]) / 2,
                bounding_box_max[2]
            )
        else:  # Default to 'BOTTOM'
            origin_point = (
                (bounding_box_max[0] + bounding_box_min[0]) / 2,
                (bounding_box_max[1] + bounding_box_min[1]) / 2,
                bounding_box_min[2]
            )

        # Set the 3D cursor to the selected origin point
        bpy.context.scene.cursor.location = origin_point
        
        # Set the origin point to the 3D cursor location
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        
        # Reset delta_location
        selected_object.delta_location = (0, 0, 0)
        
        # Reset 3D cursor to the world origin
        bpy.context.scene.cursor.location = (0, 0, 0)

        
        

        
        # Set keyframes for End Frame
        selected_object.keyframe_insert(data_path="scale", frame=context.scene.simple_operator_props.end_frame)
        selected_object.keyframe_insert(data_path="rotation_euler", frame=context.scene.simple_operator_props.end_frame)


        # Set keyframes for Middle Frame
        middle_frame = context.scene.simple_operator_props.start_frame + ((context.scene.simple_operator_props.end_frame - context.scene.simple_operator_props.start_frame) / 2)
        selected_object.scale = (context.scene.simple_operator_props.object_scale_factor,) * 3
        selected_object.keyframe_insert(data_path="scale", frame=middle_frame)



        # Set keyframes for Start Frame
        selected_object.scale = (0, 0, 0)
        selected_object.rotation_euler = (0, 0, math.radians(-context.scene.simple_operator_props.rotate_angle))
        selected_object.keyframe_insert(data_path="scale", frame=context.scene.simple_operator_props.start_frame)
        selected_object.keyframe_insert(data_path="rotation_euler", frame=context.scene.simple_operator_props.start_frame)

        

                
                
        # Restore original frame
        bpy.context.scene.frame_set(current_frame)

        return {'FINISHED'}    
    
class OBJECT_OT_RotateIn_Bounce_X(BaseObjectOperator):
    bl_label = "Rotate In Bounce"
    bl_idname = "object.rotate_in_bounce_x"
    bl_description = "Rotate and Scale the selected object in or out with a bounce effect."

    def execute(self, context):
        selected_object = bpy.context.object
        current_frame = bpy.context.scene.frame_current
        

        
        
        
        
        
        
        bpy.ops.object.make_single_user(object=True, obdata=True, material=False, animation=False, obdata_animation=False)
        
        
        #Apply Transforms
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        
        # Store initial dimensions
        original_dimensions = selected_object.dimensions.copy()
        
        
        # Create bounding box around the object
        bounding_box_min, bounding_box_max = selected_object.bound_box[0], selected_object.bound_box[6]

        # Calculate the selected origin point
        if context.scene.simple_operator_props.origin_point == 'TOP':
            origin_point = (
                (bounding_box_max[0] + bounding_box_min[0]) / 2,  # Midpoint X
                bounding_box_min[1],  # Min Y
                bounding_box_max[2]  # Max Z
            )
        else:  # Default to 'BOTTOM'
            origin_point = (
                (bounding_box_max[0] + bounding_box_min[0]) / 2,  # Midpoint X
                bounding_box_min[1],  # Min Y
                bounding_box_min[2]  # Min Z
            )
            
        # Set the 3D cursor to the selected origin point
        bpy.context.scene.cursor.location = origin_point

        # Set the origin point to the 3D cursor location
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

        # Reset delta_location
        selected_object.delta_location = (0, 0, 0)
        
        # Reset 3D cursor to the world origin
        bpy.context.scene.cursor.location = (0, 0, 0)

        
        

        
        # Set keyframes for End Frame
        selected_object.keyframe_insert(data_path="scale", frame=context.scene.simple_operator_props.end_frame)
        selected_object.keyframe_insert(data_path="rotation_euler", frame=context.scene.simple_operator_props.end_frame)


        # Set keyframes for Middle Frame
        middle_frame = context.scene.simple_operator_props.start_frame + ((context.scene.simple_operator_props.end_frame - context.scene.simple_operator_props.start_frame) / 2)
        selected_object.scale = (context.scene.simple_operator_props.object_scale_factor,) * 3
        selected_object.keyframe_insert(data_path="scale", frame=middle_frame)



        # Set keyframes for Start Frame
        selected_object.scale = (0, 0, 0)
        selected_object.rotation_euler = (math.radians(context.scene.simple_operator_props.rotate_angle), 0, 0)
        selected_object.keyframe_insert(data_path="scale", frame=context.scene.simple_operator_props.start_frame)
        selected_object.keyframe_insert(data_path="rotation_euler", frame=context.scene.simple_operator_props.start_frame)

        

                
                
        # Restore original frame
        bpy.context.scene.frame_set(current_frame)

        return {'FINISHED'}
    
class OBJECT_OT_RotateIn_Bounce_X2(BaseObjectOperator):
    bl_label = "Rotate In Bounce"
    bl_idname = "object.rotate_in_bounce_x2"
    bl_description = "Rotate and Scale the selected object in or out with a bounce effect."

    def execute(self, context):
        selected_object = bpy.context.object
        current_frame = bpy.context.scene.frame_current
        

        
        
        
        
        
        
        bpy.ops.object.make_single_user(object=True, obdata=True, material=False, animation=False, obdata_animation=False) 
        
        
        #Apply Transforms
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        
        # Store initial dimensions
        original_dimensions = selected_object.dimensions.copy()
        
        
        # Create bounding box around the object
        bounding_box_min, bounding_box_max = selected_object.bound_box[0], selected_object.bound_box[6]

        # Calculate the selected origin point
        if context.scene.simple_operator_props.origin_point == 'TOP':
            origin_point = (
                (bounding_box_max[0] + bounding_box_min[0]) / 2,  # Midpoint X
                bounding_box_max[1],  # max Y
                bounding_box_max[2]  # Max Z
            )
        else:  # Default to 'BOTTOM'
            origin_point = (
                (bounding_box_max[0] + bounding_box_min[0]) / 2,  # Midpoint X
                bounding_box_max[1],  # max Y
                bounding_box_min[2]  # Min Z
            )
            
        # Set the 3D cursor to the selected origin point
        bpy.context.scene.cursor.location = origin_point

        # Set the origin point to the 3D cursor location
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

        # Reset delta_location
        selected_object.delta_location = (0, 0, 0)
        
        
        # Reset 3D cursor to the world origin
        bpy.context.scene.cursor.location = (0, 0, 0)

        
        

        
        # Set keyframes for End Frame
        selected_object.keyframe_insert(data_path="scale", frame=context.scene.simple_operator_props.end_frame)
        selected_object.keyframe_insert(data_path="rotation_euler", frame=context.scene.simple_operator_props.end_frame)


        # Set keyframes for Middle Frame
        middle_frame = context.scene.simple_operator_props.start_frame + ((context.scene.simple_operator_props.end_frame - context.scene.simple_operator_props.start_frame) / 2)
        selected_object.scale = (context.scene.simple_operator_props.object_scale_factor,) * 3
        selected_object.keyframe_insert(data_path="scale", frame=middle_frame)



        # Set keyframes for Start Frame
        selected_object.scale = (0, 0, 0)
        selected_object.rotation_euler = (math.radians(-context.scene.simple_operator_props.rotate_angle), 0, 0)
        selected_object.keyframe_insert(data_path="scale", frame=context.scene.simple_operator_props.start_frame)
        selected_object.keyframe_insert(data_path="rotation_euler", frame=context.scene.simple_operator_props.start_frame)

        

                
                
        # Restore original frame
        bpy.context.scene.frame_set(current_frame)

        return {'FINISHED'}
    
class OBJECT_OT_RotateIn_Bounce_Y(BaseObjectOperator):
    bl_label = "Rotate In Bounce"
    bl_idname = "object.rotate_in_bounce_y"
    bl_description = "Rotate and Scale the selected object in or out with a bounce effect."

    def execute(self, context):
        selected_object = bpy.context.object
        current_frame = bpy.context.scene.frame_current
        

        
        
        
        
        
        
        bpy.ops.object.make_single_user(object=True, obdata=True, material=False, animation=False, obdata_animation=False)

        
        
        
        #Apply Transforms
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        
        # Store initial dimensions
        original_dimensions = selected_object.dimensions.copy()
        
        
        
       # Create bounding box around the object
        bounding_box_min, bounding_box_max = selected_object.bound_box[0], selected_object.bound_box[6]

        # Calculate the selected origin point
        if context.scene.simple_operator_props.origin_point == 'TOP':
            origin_point = (
                bounding_box_max[0],  # Max X
                (bounding_box_max[1] + bounding_box_min[1]) / 2,  # Midpoint Y
                bounding_box_max[2]  # Max Z
            )
        else:  # Default to 'BOTTOM'
            origin_point = (
                bounding_box_max[0],  # Max X
                (bounding_box_max[1] + bounding_box_min[1]) / 2,  # Midpoint Y
                bounding_box_min[2]  # Min Z
            )
            
        # Set the 3D cursor to the selected origin point
        bpy.context.scene.cursor.location = origin_point

        # Set the origin point to the 3D cursor location
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

        # Reset delta_location
        selected_object.delta_location = (0, 0, 0)
        
        # Reset 3D cursor to the world origin
        bpy.context.scene.cursor.location = (0, 0, 0)

        
        

        
        # Set keyframes for End Frame
        selected_object.keyframe_insert(data_path="scale", frame=context.scene.simple_operator_props.end_frame)
        selected_object.keyframe_insert(data_path="rotation_euler", frame=context.scene.simple_operator_props.end_frame)


        # Set keyframes for Middle Frame
        middle_frame = context.scene.simple_operator_props.start_frame + ((context.scene.simple_operator_props.end_frame - context.scene.simple_operator_props.start_frame) / 2)
        selected_object.scale = (context.scene.simple_operator_props.object_scale_factor,) * 3
        selected_object.keyframe_insert(data_path="scale", frame=middle_frame)



        # Set keyframes for Start Frame
        selected_object.scale = (0, 0, 0)
        selected_object.rotation_euler = (0, math.radians(context.scene.simple_operator_props.rotate_angle), 0)
        selected_object.keyframe_insert(data_path="scale", frame=context.scene.simple_operator_props.start_frame)
        selected_object.keyframe_insert(data_path="rotation_euler", frame=context.scene.simple_operator_props.start_frame)

        

                
                
        # Restore original frame
        bpy.context.scene.frame_set(current_frame)

        return {'FINISHED'}
    
class OBJECT_OT_RotateIn_Bounce_Y2(BaseObjectOperator):
    bl_label = "Rotate In Bounce"
    bl_idname = "object.rotate_in_bounce_y2"
    bl_description = "Rotate and Scale the selected object in or out with a bounce effect."

    def execute(self, context):
        selected_object = bpy.context.object
        current_frame = bpy.context.scene.frame_current
        

        
        
        
        
        
        
        bpy.ops.object.make_single_user(object=True, obdata=True, material=False, animation=False, obdata_animation=False)
        
        #Apply Transforms
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        # Store initial dimensions
        original_dimensions = selected_object.dimensions.copy()
        
        
        
        # Create bounding box around the object
        bounding_box_min, bounding_box_max = selected_object.bound_box[0], selected_object.bound_box[6]

        # Calculate the selected origin point
        if context.scene.simple_operator_props.origin_point == 'TOP':
            origin_point = (
                bounding_box_min[0],  # Min X
                (bounding_box_max[1] + bounding_box_min[1]) / 2,  # Midpoint Y
                bounding_box_max[2]  # Max Z
            )
        else:  # Default to 'BOTTOM'
            origin_point = (
                bounding_box_min[0],  # Min X
                (bounding_box_max[1] + bounding_box_min[1]) / 2,  # Midpoint Y
                bounding_box_min[2]  # Min Z
            )
            
        # Set the 3D cursor to the selected origin point
        bpy.context.scene.cursor.location = origin_point

        # Set the origin point to the 3D cursor location
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

        # Reset delta_location
        selected_object.delta_location = (0, 0, 0)
        
        # Reset 3D cursor to the world origin
        bpy.context.scene.cursor.location = (0, 0, 0)

        
        

        
        # Set keyframes for End Frame
        selected_object.keyframe_insert(data_path="scale", frame=context.scene.simple_operator_props.end_frame)
        selected_object.keyframe_insert(data_path="rotation_euler", frame=context.scene.simple_operator_props.end_frame)


        # Set keyframes for Middle Frame
        middle_frame = context.scene.simple_operator_props.start_frame + ((context.scene.simple_operator_props.end_frame - context.scene.simple_operator_props.start_frame) / 2)
        selected_object.scale = (context.scene.simple_operator_props.object_scale_factor,) * 3
        selected_object.keyframe_insert(data_path="scale", frame=middle_frame)



        # Set keyframes for Start Frame
        selected_object.scale = (0, 0, 0)
        selected_object.rotation_euler = (0, math.radians(-context.scene.simple_operator_props.rotate_angle), 0)
        selected_object.keyframe_insert(data_path="scale", frame=context.scene.simple_operator_props.start_frame)
        selected_object.keyframe_insert(data_path="rotation_euler", frame=context.scene.simple_operator_props.start_frame)

        

                
                
        # Restore original frame
        bpy.context.scene.frame_set(current_frame)

        return {'FINISHED'}

class OBJECT_OT_RandomObjectsAnimtion(BaseObjectOperator):
    bl_idname = "object.random_objects_animation"
    bl_label = "Random Objects Fall Down"
    bl_description = "Randomly Animate a Collection of Objects"
    
  
    def execute(self, context):
        
        start_frame = context.scene.random_animation_start_frame
        end_frame = context.scene.random_animation_end_frame

        
        # Create a cube
        bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0))
        cube_object = bpy.context.active_object
        cube_object.name = "Objects Animation Preset"

        # Import the geometry node from an external file
        filepath = addon_dirc + "/Assets.blend"
        node_group_name = "Random Objects Animation"

        # Append the node group
        with bpy.data.libraries.load(filepath) as (data_from, data_to):
            data_to.node_groups = [node for node in data_from.node_groups if node == node_group_name]

        # Check if the node group was successfully appended
        if node_group_name in bpy.data.node_groups:
            random_objects_animations = bpy.data.node_groups[node_group_name]
        else:
            self.report({'ERROR'}, f"Failed to append node group: {node_group_name} from {filepath}")
            return {'CANCELLED'}

        # Create a modifier and assign the node group
        name = bpy.context.object.name
        obj = bpy.data.objects[name]
        mod = obj.modifiers.new(name="Random Objects Animation", type='NODES')
        mod.node_group = random_objects_animations

        # Assign the collection to the modifier's socket
        collection_name = context.scene.random_objects_animation_props.collection_name
        collection = bpy.data.collections.get(collection_name)
        mod["Socket_6"] = collection

        # Assign values to modifier sockets
        mod["Socket_11"] = context.scene.random_objects_animation_props.min_z_distance
        mod["Socket_12"] = context.scene.random_objects_animation_props.max_z_distance
        mod["Socket_33"] = context.scene.random_objects_animation_props.min_y_distance
        mod["Socket_34"] = context.scene.random_objects_animation_props.max_y_distance
        mod["Socket_30"] = context.scene.random_objects_animation_props.min_x_distance
        mod["Socket_31"] = context.scene.random_objects_animation_props.max_x_distance
        
        mod["Socket_17"] = context.scene.random_objects_animation_props.min_x_rotation
        mod["Socket_18"] = context.scene.random_objects_animation_props.max_x_rotation
        mod["Socket_21"] = context.scene.random_objects_animation_props.min_y_rotation
        mod["Socket_22"] = context.scene.random_objects_animation_props.max_y_rotation
        mod["Socket_24"] = context.scene.random_objects_animation_props.min_z_rotation
        mod["Socket_25"] = context.scene.random_objects_animation_props.max_z_rotation

        node_group = bpy.data.node_groups.get("Random Objects Animation")
        if node_group:
            interface = node_group.interface
            if interface:
                items_tree = interface.items_tree
                items_tree[15].subtype = 'ANGLE'
                


               
        # Keyframe Scale
        mod["Socket_4"] = 0.0
        bpy.context.object.keyframe_insert(data_path=f'modifiers["Random Objects Animation"]["Socket_4"]', frame=start_frame)
        
        mod["Socket_4"] = 1.0
        bpy.context.object.keyframe_insert(data_path=f'modifiers["Random Objects Animation"]["Socket_4"]', frame=end_frame)


        # Keyframe Animation 
        if mod["Socket_11"] != 0.0:
            mod["Socket_11"] = context.scene.random_objects_animation_props.min_z_distance
            bpy.context.object.keyframe_insert(data_path=f'modifiers["Random Objects Animation"]["Socket_11"]', frame=start_frame)
            
            mod["Socket_11"] = 0.0
            bpy.context.object.keyframe_insert(data_path=f'modifiers["Random Objects Animation"]["Socket_11"]', frame=end_frame)
            
            
        if mod["Socket_12"] != 0.0:
            mod["Socket_12"] = context.scene.random_objects_animation_props.max_z_distance
            bpy.context.object.keyframe_insert(data_path=f'modifiers["Random Objects Animation"]["Socket_12"]', frame=start_frame)
            
            mod["Socket_12"] = 0.0
            bpy.context.object.keyframe_insert(data_path=f'modifiers["Random Objects Animation"]["Socket_12"]', frame=end_frame)
    
        
        # Keyframe Socket_33
        if mod["Socket_33"] != 0.0:
            mod["Socket_33"] = context.scene.random_objects_animation_props.min_y_distance
            bpy.context.object.keyframe_insert(data_path=f'modifiers["Random Objects Animation"]["Socket_33"]', frame=start_frame)
            mod["Socket_33"] = 0.0
            bpy.context.object.keyframe_insert(data_path=f'modifiers["Random Objects Animation"]["Socket_33"]', frame=end_frame)

        # Keyframe Socket_34
        if mod["Socket_34"] != 0.0:
            mod["Socket_34"] = context.scene.random_objects_animation_props.max_y_distance
            bpy.context.object.keyframe_insert(data_path=f'modifiers["Random Objects Animation"]["Socket_34"]', frame=start_frame)
            mod["Socket_34"] = 0.0
            bpy.context.object.keyframe_insert(data_path=f'modifiers["Random Objects Animation"]["Socket_34"]', frame=end_frame)

        # Keyframe Socket_30
        if mod["Socket_30"] != 0.0:
            mod["Socket_30"] = context.scene.random_objects_animation_props.min_x_distance
            bpy.context.object.keyframe_insert(data_path=f'modifiers["Random Objects Animation"]["Socket_30"]', frame=start_frame)
            mod["Socket_30"] = 0.0
            bpy.context.object.keyframe_insert(data_path=f'modifiers["Random Objects Animation"]["Socket_30"]', frame=end_frame)

        # Keyframe Socket_31
        if mod["Socket_31"] != 0.0:
            mod["Socket_31"] = context.scene.random_objects_animation_props.max_x_distance
            bpy.context.object.keyframe_insert(data_path=f'modifiers["Random Objects Animation"]["Socket_31"]', frame=start_frame)
            mod["Socket_31"] = 0.0
            bpy.context.object.keyframe_insert(data_path=f'modifiers["Random Objects Animation"]["Socket_31"]', frame=end_frame)

        # Keyframe Socket_17
        if mod["Socket_17"] != 0.0:
            mod["Socket_17"] = context.scene.random_objects_animation_props.min_x_rotation
            bpy.context.object.keyframe_insert(data_path=f'modifiers["Random Objects Animation"]["Socket_17"]', frame=start_frame)
            mod["Socket_17"] = 0.0
            bpy.context.object.keyframe_insert(data_path=f'modifiers["Random Objects Animation"]["Socket_17"]', frame=end_frame)

        # Keyframe Socket_18
        if mod["Socket_18"] != 0.0:
            mod["Socket_18"] = context.scene.random_objects_animation_props.max_x_rotation
            bpy.context.object.keyframe_insert(data_path=f'modifiers["Random Objects Animation"]["Socket_18"]', frame=start_frame)
            mod["Socket_18"] = 0.0
            bpy.context.object.keyframe_insert(data_path=f'modifiers["Random Objects Animation"]["Socket_18"]', frame=end_frame)

        # Keyframe Socket_21
        if mod["Socket_21"] != 0.0:
            mod["Socket_21"] = context.scene.random_objects_animation_props.min_y_rotation
            bpy.context.object.keyframe_insert(data_path=f'modifiers["Random Objects Animation"]["Socket_21"]', frame=start_frame)
            mod["Socket_21"] = 0.0
            bpy.context.object.keyframe_insert(data_path=f'modifiers["Random Objects Animation"]["Socket_21"]', frame=end_frame)

        # Keyframe Socket_22
        if mod["Socket_22"] != 0.0:
            mod["Socket_22"] = context.scene.random_objects_animation_props.max_y_rotation
            bpy.context.object.keyframe_insert(data_path=f'modifiers["Random Objects Animation"]["Socket_22"]', frame=start_frame)
            mod["Socket_22"] = 0.0
            bpy.context.object.keyframe_insert(data_path=f'modifiers["Random Objects Animation"]["Socket_22"]', frame=end_frame)

        # Keyframe Socket_24
        if mod["Socket_24"] != 0.0:
            mod["Socket_24"] = context.scene.random_objects_animation_props.min_z_rotation
            bpy.context.object.keyframe_insert(data_path=f'modifiers["Random Objects Animation"]["Socket_24"]', frame=start_frame)
            mod["Socket_24"] = 0.0
            bpy.context.object.keyframe_insert(data_path=f'modifiers["Random Objects Animation"]["Socket_24"]', frame=end_frame)

        # Keyframe Socket_25
        if mod["Socket_25"] != 0.0:
            mod["Socket_25"] = context.scene.random_objects_animation_props.max_z_rotation
            bpy.context.object.keyframe_insert(data_path=f'modifiers["Random Objects Animation"]["Socket_25"]', frame=start_frame)
            mod["Socket_25"] = 0.0
            bpy.context.object.keyframe_insert(data_path=f'modifiers["Random Objects Animation"]["Socket_25"]', frame=end_frame)

        return {'FINISHED'}

class OBJECT_OT_UniformObjectsAnimtion(BaseObjectOperator):
    bl_idname = "object.uniform_objects_animation"
    bl_label = "Uniform Objects animation"
    bl_description = "Animate a Collection of Objects together"
    
  
    def execute(self, context):
        
        start_frame = context.scene.uni_animation_start_frame
        end_frame = context.scene.uni_animation_end_frame

        
        # Create a cube
        bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0))
        cube_object = bpy.context.active_object
        cube_object.name = "Objects Animation Preset"

        # Import the geometry node from an external file
        filepath = addon_dirc + "/Assets.blend"
        node_group_name = "Uniform Objects Animation"

        # Append the node group
        with bpy.data.libraries.load(filepath) as (data_from, data_to):
            data_to.node_groups = [node for node in data_from.node_groups if node == node_group_name]

        # Check if the node group was successfully appended
        if node_group_name in bpy.data.node_groups:
            uniform_objects_animations = bpy.data.node_groups[node_group_name]
        else:
            self.report({'ERROR'}, f"Failed to append node group: {node_group_name} from {filepath}")
            return {'CANCELLED'}
        
        # Create a modifier and assign the node group
        name = bpy.context.object.name
        obj = bpy.data.objects[name]
        mod = obj.modifiers.new(name="Uniform Objects Animation", type='NODES')
        mod.node_group = uniform_objects_animations

        # Assign the collection to the modifier's socket
        collection_name = context.scene.uniform_objects_animation_props.collection_name
        collection = bpy.data.collections.get(collection_name)
        mod["Socket_6"] = collection

        
        # Assign values to the modifier's socket
        mod["Socket_5"] = context.scene.uniform_objects_animation_props.animate_from_z
        mod["Socket_14"] = context.scene.uniform_objects_animation_props.animate_from_x
        mod["Socket_15"] = context.scene.uniform_objects_animation_props.animate_from_y
        
        # Assign the float values to the modifier's sockets
        mod["Socket_7"] = context.scene.uniform_objects_animation_props.rotation_x
        mod["Socket_8"] = context.scene.uniform_objects_animation_props.rotation_y
        mod["Socket_9"] = context.scene.uniform_objects_animation_props.rotation_z

        # Set the subtype of socket 7 to 'ANGLE'
        node_group = bpy.data.node_groups.get("Uniform Objects Animation")
        if node_group:
            interface = node_group.interface
            if interface:
                items_tree = interface.items_tree
                items_tree[5].subtype = 'ANGLE'
                
        # Keyframe Scale
        mod["Socket_4"] = 0.0
        bpy.context.object.keyframe_insert(data_path=f'modifiers["Uniform Objects Animation"]["Socket_4"]', frame=start_frame)
        
        mod["Socket_4"] = 1.0
        bpy.context.object.keyframe_insert(data_path=f'modifiers["Uniform Objects Animation"]["Socket_4"]', frame=end_frame)



        # Keyframe Z Animation 
        if mod["Socket_5"] != 0.0:
            mod["Socket_5"] = context.scene.uniform_objects_animation_props.animate_from_z
            bpy.context.object.keyframe_insert(data_path=f'modifiers["Uniform Objects Animation"]["Socket_5"]', frame=start_frame)
            
            mod["Socket_5"] = 0.0
            bpy.context.object.keyframe_insert(data_path=f'modifiers["Uniform Objects Animation"]["Socket_5"]', frame=end_frame)
    
    
        # Keyframe X Animation 
        if mod["Socket_14"] != 0.0:
            mod["Socket_14"] = context.scene.uniform_objects_animation_props.animate_from_x
            bpy.context.object.keyframe_insert(data_path=f'modifiers["Uniform Objects Animation"]["Socket_14"]', frame=start_frame)
            
            mod["Socket_14"] = 0.0
            bpy.context.object.keyframe_insert(data_path=f'modifiers["Uniform Objects Animation"]["Socket_14"]', frame=end_frame)


        # Keyframe Y Animation 
        if mod["Socket_15"] != 0.0:
            mod["Socket_15"] = context.scene.uniform_objects_animation_props.animate_from_y
            bpy.context.object.keyframe_insert(data_path=f'modifiers["Uniform Objects Animation"]["Socket_15"]', frame=start_frame)
            
            mod["Socket_15"] = 0.0
            bpy.context.object.keyframe_insert(data_path=f'modifiers["Uniform Objects Animation"]["Socket_15"]', frame=end_frame)

        
        # Keyframe Rotation X 
        if mod["Socket_7"] != 0.0:
            mod["Socket_7"] = context.scene.uniform_objects_animation_props.rotation_x
            bpy.context.object.keyframe_insert(data_path=f'modifiers["Uniform Objects Animation"]["Socket_7"]', frame=start_frame)
            
            mod["Socket_7"] = 0.0
            bpy.context.object.keyframe_insert(data_path=f'modifiers["Uniform Objects Animation"]["Socket_7"]', frame=end_frame)

        
        # Keyframe Rotation Y
        if mod["Socket_8"] != 0.0:
            mod["Socket_8"] = context.scene.uniform_objects_animation_props.rotation_y
            bpy.context.object.keyframe_insert(data_path=f'modifiers["Uniform Objects Animation"]["Socket_8"]', frame=start_frame)
         
            mod["Socket_8"] = 0.0
            bpy.context.object.keyframe_insert(data_path=f'modifiers["Uniform Objects Animation"]["Socket_8"]', frame=end_frame)



        # Keyframe Rotation Z
        if mod["Socket_9"] != 0.0:
            mod["Socket_9"] = context.scene.uniform_objects_animation_props.rotation_z
            bpy.context.object.keyframe_insert(data_path=f'modifiers["Uniform Objects Animation"]["Socket_9"]', frame=start_frame)

            mod["Socket_9"] = 0.0
            bpy.context.object.keyframe_insert(data_path=f'modifiers["Uniform Objects Animation"]["Socket_9"]', frame=end_frame)


        return {'FINISHED'}


        
object_operators_classes = (
    OBJECT_OT_Pop_Up_Y,
    OBJECT_OT_Pop_Up_Y2,    
    OBJECT_OT_Pop_Up_X,
    OBJECT_OT_Pop_Up_X2,
    OBJECT_OT_Pop_Up_Z,
    OBJECT_OT_Pop_Up_Z2,
    OBJECT_OT_Pop_Up,
    OBJECT_OT_Pop_Up_Twist,
    OBJECT_OT_ScaleIn,
    OBJECT_OT_AnimateIn_Y,
    OBJECT_OT_AnimateIn_X,
    OBJECT_OT_AnimateIn_Z,
    OBJECT_OT_B_AnimateIn_Y,
    OBJECT_OT_B_AnimateIn_X,
    OBJECT_OT_B_AnimateIn_Z,
    OBJECT_OT_Fall_Down_Z,    
    OBJECT_OT_AnimateIn_Y_Rotate,
    OBJECT_OT_AnimateIn_X_Rotate,
    OBJECT_OT_AnimateIn_Z_Rotate,
    OBJECT_OT_RotateIn_Z,
    OBJECT_OT_RotateIn_Z2,
    OBJECT_OT_RotateIn_Y,
    OBJECT_OT_RotateIn_Y2,
    OBJECT_OT_RotateIn_X,
    OBJECT_OT_RotateIn_X2,
    OBJECT_OT_RotateIn_Bounce_Z,
    OBJECT_OT_RotateIn_Bounce_Z2,
    OBJECT_OT_RotateIn_Bounce_X,
    OBJECT_OT_RotateIn_Bounce_X2,
    OBJECT_OT_RotateIn_Bounce_Y,
    OBJECT_OT_RotateIn_Bounce_Y2,
    OBJECT_OT_RandomObjectsAnimtion,
    OBJECT_OT_UniformObjectsAnimtion,
    # Add other object operator classes here
)