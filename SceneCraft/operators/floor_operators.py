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
import math
from mathutils import Vector
import os
from ..base_operators import BaseFloorOperator
addon_dirc = os.path.dirname(os.path.realpath(__file__))

class OBJECT_OT_Bend_Floors(BaseFloorOperator):
    bl_idname = "object.bend_floors"
    bl_label = "Bend Floors"

    def execute(self, context):
        # Check if there is an active object
        if bpy.context.active_object is not None:
            selected_object = bpy.context.active_object
            
            bpy.ops.object.make_single_user(object=True, obdata=True, material=False, animation=False, obdata_animation=False)
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

                
                
            # Store initial dimensions
            original_dimensions = selected_object.dimensions.copy()

        
            # Set the origin point of the selected object to the center of its geometry
            bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')
            
            # Initialize offset
            offset_x = 0.5 * original_dimensions.x
            offset_y = 0.5 * original_dimensions.y
            offset_z = 0.5 * original_dimensions.z
            
        
            # Calculate the offset to move the origin
            if context.scene.bend_direction_xyz == 'X':
                bpy.context.scene.tool_settings.use_transform_data_origin = True
            
                bpy.ops.transform.translate(value=(offset_x, 0, -offset_z), orient_type='GLOBAL')
            
                bpy.context.scene.tool_settings.use_transform_data_origin = False
            
            elif context.scene.bend_direction_xyz == '-X':
                bpy.context.scene.tool_settings.use_transform_data_origin = True
            
                bpy.ops.transform.translate(value=(-offset_x, 0, -offset_z), orient_type='GLOBAL')
            
                bpy.context.scene.tool_settings.use_transform_data_origin = False

            elif context.scene.bend_direction_xyz == 'Y':
                bpy.context.scene.tool_settings.use_transform_data_origin = True
            
                bpy.ops.transform.translate(value=(0, offset_y, -offset_z), orient_type='GLOBAL')
            
                bpy.context.scene.tool_settings.use_transform_data_origin = False
            
            elif context.scene.bend_direction_xyz == '-Y':
                bpy.context.scene.tool_settings.use_transform_data_origin = True
            
                bpy.ops.transform.translate(value=(0, -offset_y, -offset_z), orient_type='GLOBAL')
            
                bpy.context.scene.tool_settings.use_transform_data_origin = False
                

                
                
            






            # Create an empty at the origin of the selected object
            bpy.ops.object.empty_add(location=selected_object.location)
            empty = bpy.context.object
            empty.name = "Empty"

            # Adjust empty rotation and modifier.deform_axis
            if context.scene.bend_direction_xyz in {'X', '-X'}:
                empty.rotation_euler[1] = 1.5708  # 90 degrees in radians on Y-axis
                deform_axis = 'Y'
            elif context.scene.bend_direction_xyz in {'Y', '-Y'}:
                empty.rotation_euler[0] = 1.5708  # 90 degrees in radians on X-axis
                deform_axis = 'X'


            # Add SimpleDeform modifier to the selected object
            bpy.context.view_layer.objects.active = selected_object
            bpy.ops.object.modifier_add(type='SIMPLE_DEFORM')
            modifier = selected_object.modifiers[-1]
            modifier.deform_method = 'BEND'
            modifier.deform_axis = deform_axis  # Set deform axis based on direction
            modifier.origin = bpy.data.objects["Empty"]  # Set the empty as the origin of the SimpleDeform modifier
            
            
            # Set angle in the start frame based on the selected direction
            if context.scene.bend_direction == 'INWARDS':
                modifier.angle = math.radians(450)
            else:
                modifier.angle = math.radians(-450)

            # add keyframe
            modifier.keyframe_insert(data_path='angle', frame=context.scene.bend_start_frame, index=-1)

            # Set angle to end frame and add keyframe
            modifier.angle = 0  # Set angle to 0
            modifier.keyframe_insert(data_path='angle', frame=context.scene.bend_end_frame, index=-1)

            # Set scale to 0 at start frame and add keyframe
            selected_object.scale = (0, 0, 0)
            selected_object.keyframe_insert(data_path='scale', frame=context.scene.bend_start_frame, index=-1)

            # Calculate the frame for the scale keyframe as half the distance between start frame and end frame
            scale_frame = (context.scene.bend_end_frame - context.scene.bend_start_frame) // 2 + context.scene.bend_start_frame

            # Set scale to 1 at the calculated frame and add keyframe
            selected_object.scale = (1, 1, 1)
            selected_object.keyframe_insert(data_path='scale', frame=scale_frame, index=-1)

                
                
        
        else:
            print("No active object selected. Please select an object before running the script.")
            
   
        return {'FINISHED'}

class SimpleOperator_Roll_Floors(BaseFloorOperator):
    bl_idname = "object.roll_floors"
    bl_label = "Roll Floors"

    def execute(self, context):
        try:
            if not (obj := context.active_object) or obj.type != 'MESH':
                self.report({'ERROR'}, "Select a mesh object")
                return {'CANCELLED'}

            apply_transforms(obj)

            # Validate and load curve asset
            asset_path = os.path.join(addon_dirc, "/Assets.blend")
            curve_name = "NurbsPath Roll"
            if not validate_asset(asset_path, curve_name, 'objects'):
                self.report({'ERROR'}, f"Missing asset: {curve_name}")
                return {'CANCELLED'}

            # Create curve with unique name
            curve = create_unique_empty(
                context,
                f"Roll_Curve_{obj.name}",
                obj.location,
                'PLAIN_AXES'
            )

            # Position curve based on direction
            direction = context.scene.roll_direction_xyz
            offset = obj.dimensions.x / 2 * 1.3 if direction in {'X', '-X'} else obj.dimensions.y / 2 * 1.3
            if direction == 'X':
                curve.location.x -= offset
            elif direction == '-X':
                curve.location.x += offset
            elif direction == 'Y':
                curve.location.y -= offset
            else:
                curve.location.y += offset

            # Configure curve rotation
            if direction == '-X':
                curve.rotation_euler.z = math.radians(180)
            elif direction == 'Y':
                curve.rotation_euler.z = math.radians(90)
            elif direction == '-Y':
                curve.rotation_euler.z = math.radians(-90)

            # Add curve modifier
            mod = get_or_create_modifier(obj, "Roll_Modifier", 'CURVE')
            mod.object = curve
            mod.deform_axis = 'POS_X'

            # Animate curve movement
            start_frame = context.scene.roll_start_frame
            end_frame = context.scene.roll_end_frame
            insert_keyframe(curve, 'location', start_frame)
            
            move_offset = obj.dimensions.x * 1.5 if direction in {'X', '-X'} else obj.dimensions.y * 1.5
            if direction in {'-X', '-Y'}:
                move_offset *= -1
                
            if direction in {'X', '-X'}:
                curve.location.x += move_offset
            else:
                curve.location.y += move_offset
                
            insert_keyframe(curve, 'location', end_frame)

        except Exception as e:
            self.report({'ERROR'}, f"Rolling failed: {str(e)}")
            return {'CANCELLED'}
        return {'FINISHED'}
class OBJECT_OT_Wipe_Floors(BaseFloorOperator):
    bl_idname = "object.wipe_floors"
    bl_label = "Wipe Floors"

    def execute(self, context):
        # Check if there is an active object
        if bpy.context.active_object is not None:
            selected_object = bpy.context.active_object
            
            bpy.ops.object.make_single_user(object=True, obdata=True, material=False, animation=False, obdata_animation=False)
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

                
           
                
 
            
            
            # Store initial dimensions
            original_dimensions = selected_object.dimensions.copy()

        
            # Set the origin point of the selected object to the center of its geometry
            bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')
            
            # Initialize offset
            offset_x = 0.5 * original_dimensions.x
            offset_y = 0.5 * original_dimensions.y
            offset_z = 0.5 * original_dimensions.z
            
        
            # Calculate the offset to move the origin
            if context.scene.wipe_direction_xyz == 'X':
                bpy.context.scene.tool_settings.use_transform_data_origin = True
            
                bpy.ops.transform.translate(value=(offset_x, 0, -offset_z), orient_type='GLOBAL')
            
                bpy.context.scene.tool_settings.use_transform_data_origin = False
            
            elif context.scene.wipe_direction_xyz == '-X':
                bpy.context.scene.tool_settings.use_transform_data_origin = True
            
                bpy.ops.transform.translate(value=(-offset_x, 0, -offset_z), orient_type='GLOBAL')
            
                bpy.context.scene.tool_settings.use_transform_data_origin = False

            elif context.scene.wipe_direction_xyz == 'Y':
                bpy.context.scene.tool_settings.use_transform_data_origin = True
            
                bpy.ops.transform.translate(value=(0, offset_y, -offset_z), orient_type='GLOBAL')
            
                bpy.context.scene.tool_settings.use_transform_data_origin = False
            
            elif context.scene.wipe_direction_xyz == '-Y':
                bpy.context.scene.tool_settings.use_transform_data_origin = True
            
                bpy.ops.transform.translate(value=(0, -offset_y, -offset_z), orient_type='GLOBAL')
            
                bpy.context.scene.tool_settings.use_transform_data_origin = False
                
                 
                 
                 
                 
            # Calculate frame numbers for keyframes
            frame_start = context.scene.wipe_start_frame
            frame_Utility = frame_start + 1
            frame_end = context.scene.wipe_end_frame  
            
            
            
            # Set keyframes based on the selected direction
            if context.scene.wipe_direction_xyz in {'X', '-X'}:
                    start_scale = (0, 1, 0)
                    utility_scale = (0, 1, 1)
                    end_scale = (1, 1, 1)
                    
            if context.scene.wipe_direction_xyz in {'Y', '-Y'}:

                start_scale = (1, 0, 0)
                utility_scale = (1, 0, 1)
                end_scale = (1, 1, 1)
                                    

                
                
            # Set keyframes for Start Frame
            selected_object.scale = start_scale
            selected_object.keyframe_insert(data_path="scale", frame=frame_start, index=0)  # Keyframe X scale
            selected_object.keyframe_insert(data_path="scale", frame=frame_start, index=1)  # Keyframe Y scale
            selected_object.keyframe_insert(data_path="scale", frame=frame_start, index=2)  # Keyframe Z scale

            # Set keyframes for Utility Keyframe
            selected_object.scale = utility_scale
            selected_object.keyframe_insert(data_path="scale", frame=frame_Utility, index=0)  # Keyframe X scale
            selected_object.keyframe_insert(data_path="scale", frame=frame_Utility, index=1)  # Keyframe Y scale
            selected_object.keyframe_insert(data_path="scale", frame=frame_Utility, index=2)  # Keyframe Z scale

            # Set keyframes for End Frame
            selected_object.scale = end_scale
            selected_object.keyframe_insert(data_path="scale", frame=frame_end, index=0)  # Keyframe X scale
            selected_object.keyframe_insert(data_path="scale", frame=frame_end, index=1)  # Keyframe Y scale
            selected_object.keyframe_insert(data_path="scale", frame=frame_end, index=2)  # Keyframe Z scale
    
            # Set interpolation mode to Cubic
            for fcurve in selected_object.animation_data.action.fcurves:
                if fcurve.data_path == "scale":
                    for keyframe_point in fcurve.keyframe_points:
                        keyframe_point.interpolation = 'CUBIC'  


            print("Keyframes set successfully.")
        else:
            print("No active object selected.")

        return {'FINISHED'}

class Fall_Down_Tiles(BaseFloorOperator):
    bl_idname = "object.fall_down_tiles"
    bl_label = "Fall Down Tiles"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Make floor tiles collection fall down from center"
    
    def execute(self, context):
        
        fall_down_tiles_props = context.scene.fall_down_tiles
        collection_name = fall_down_tiles_props.collection_name
        empty_name = fall_down_tiles_props.empty_name
        fade_in_value = fall_down_tiles_props.fade_in_value
        
        
        start_frame = context.scene.fade_start_frame
        end_frame = context.scene.fade_end_frame
        
        
        

        

        
        
        # Get all objects in the collection
        collection = bpy.data.collections.get(collection_name)
        objects_in_collection = [obj for obj in collection.objects if obj.type == 'MESH']

        # Initialize bounding box min and max values
        min_x, min_y, min_z = float('inf'), float('inf'), float('inf')
        max_x, max_y, max_z = float('-inf'), float('-inf'), float('-inf')

        # Calculate the bounding box of the collection
        for obj in objects_in_collection:
            for vert in obj.data.vertices:
                world_coord = obj.matrix_world @ vert.co
                min_x = min(min_x, world_coord.x)
                min_y = min(min_y, world_coord.y)
                min_z = min(min_z, world_coord.z)
                max_x = max(max_x, world_coord.x)
                max_y = max(max_y, world_coord.y)
                max_z = max(max_z, world_coord.z)

        # Calculate the center of the collection
        center_x = (min_x + max_x) / 2
        center_y = (min_y + max_y) / 2
        center_z = (min_z + max_z) / 2
        
        
        
        
        # Calculate the longest dimension in X and Y dimensions
        longest_dimension_x = max_x - min_x
        longest_dimension_y = max_y - min_y

        # Use the longer dimension for your calculation
        longest_dimension = max(longest_dimension_x, longest_dimension_y)
        




        # Calculate the scaling factor
        # Calculate the scaling factor
        scaling_factor = (longest_dimension_x + longest_dimension_y) / 2


        # Create a sphere empty named "Tiles Empty" at the center of the chosen collection
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = None
        bpy.ops.object.empty_add(type='SPHERE', align='WORLD', location=(center_x, center_y, center_z))
        empty = bpy.context.object
        empty.name = "Tiles Empty"
        
        # Calculate the frame number for keyframing (one-third distance between start and end frames)
        keyframe_frame = start_frame + (end_frame - start_frame) / 3

        # Keyframe the location at the calculated frame
        empty.keyframe_insert(data_path="location", frame=keyframe_frame)


        # Move the empty 1 meter in the Z-axis
        empty.location.z += 1.0

        # Set keyframe for the new location at the start frame
        empty.keyframe_insert(data_path="location", frame=start_frame)

        
        # Import the geometry node from an external file
        filepath = addon_dirc + "/Assets.blend"
        node_group_name = "Fall Down"

        # Append the node group
        with bpy.data.libraries.load(filepath) as (data_from, data_to):
            data_to.node_groups = [node for node in data_from.node_groups if node == node_group_name]

        # Check if the node group was successfully appended
        if node_group_name in bpy.data.node_groups:
            fall_down = bpy.data.node_groups[node_group_name]
        else:
            self.report({'ERROR'}, f"Failed to append node group: {node_group_name} from {filepath}")
            return {'CANCELLED'}


        # Create a new cube object after setting the properties
        bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=(center_x, center_y, center_z))
        cube_object = bpy.context.object
        cube_object.name = "Fall Down Floor Preset"  

        name = bpy.context.object.name
        obj = bpy.data.objects[name]
        mod = obj.modifiers.new(name = "Fall Down", type = 'NODES')
        mod.node_group = fall_down
        
        
        # Add the Empty & Collection to the modifier
        bpy.context.object.modifiers["Fall Down"]["Input_2"] = empty
        
        bpy.context.object.modifiers["Fall Down"]["Input_1"] = collection


        # Assuming you have the modifier already created and added to the object
        modifier_name = "Fall Down"
        property_name = "Input_3"

        # Set the property value
        bpy.context.object.modifiers[modifier_name][property_name] = 0.0
        # Keyframe the property at the end frame
        bpy.context.object.keyframe_insert(data_path=f'modifiers["{modifier_name}"]["{property_name}"]', frame=start_frame)

        # Set the property value based on the scaling factor
        # Check if longest dimensions are less than or equal to 10 meters
        if longest_dimension <= 5:
            bpy.context.object.modifiers[modifier_name][property_name] = scaling_factor / 1.5
        elif longest_dimension <= 10:
            bpy.context.object.modifiers[modifier_name][property_name] = scaling_factor / 1.475
        else:
            bpy.context.object.modifiers[modifier_name][property_name] = scaling_factor / 1.4
        

        # Keyframe the property at the end frame
        bpy.context.object.keyframe_insert(data_path=f'modifiers["{modifier_name}"]["{property_name}"]', frame=end_frame)
        
        
        return {'FINISHED'}
class Pop_In_Floors(BaseFloorOperator):
    bl_idname = "object.pop_in_floors"
    bl_label = "Pop In Floors"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Pop in or out floor tiles collection from any direction"
    
    def execute(self, context):
        
        pop_in_floors_props = context.scene.pop_in_floors
        collection_name = pop_in_floors_props.collection_name
        empty_name = pop_in_floors_props.empty_name
     
        start_frame = context.scene.pop_start_frame
        end_frame = context.scene.pop_end_frame
        
        
        
        
        # Get all objects in the collection
        collection = bpy.data.collections.get(collection_name)
        objects_in_collection = [obj for obj in collection.objects if obj.type == 'MESH']

        # Initialize bounding box min and max values
        min_x, min_y, min_z = float('inf'), float('inf'), float('inf')
        max_x, max_y, max_z = float('-inf'), float('-inf'), float('-inf')

        # Calculate the bounding box of the collection
        for obj in objects_in_collection:
            for vert in obj.data.vertices:
                world_coord = obj.matrix_world @ vert.co
                min_x = min(min_x, world_coord.x)
                min_y = min(min_y, world_coord.y)
                min_z = min(min_z, world_coord.z)
                max_x = max(max_x, world_coord.x)
                max_y = max(max_y, world_coord.y)
                max_z = max(max_z, world_coord.z)

        # Calculate the center of the collection
        center_x = (min_x + max_x) / 2
        center_y = (min_y + max_y) / 2
        center_z = (min_z + max_z) / 2
        
        # Calculate the dimensions of the bounding box
        dimension_x = max_x - min_x
        dimension_y = max_y - min_y
        dimension_z = max_z - min_z
        
        
        # Calculate the shift amounts
        shift_amount_x = dimension_x / 1.2
        shift_amount_y = dimension_y / 1.2


        
        
        
        # Create an empty named "Pop In Empty" at the adjusted location
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = None
        bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=(center_x, center_y, center_z))
        empty = bpy.context.object
        empty.name = "Pop In Empty"
        

            
            
        # Set keyframes based on pop_direction
        if context.scene.pop_direction_xyz == 'X':
            empty.location = (center_x - shift_amount_x, center_y, center_z)
            empty.keyframe_insert(data_path="location", frame=start_frame)

            empty.location = (center_x + shift_amount_x, center_y, center_z)
            empty.keyframe_insert(data_path="location", frame=end_frame)


        elif context.scene.pop_direction_xyz == 'Y':
            empty.location = (center_x, center_y - shift_amount_y, center_z)
            empty.keyframe_insert(data_path="location", frame=start_frame)

            empty.location = (center_x, center_y + shift_amount_y, center_z)
            empty.keyframe_insert(data_path="location", frame=end_frame)
            
        elif context.scene.pop_direction_xyz == '-X':
            empty.location = (center_x + shift_amount_x, center_y, center_z)
            empty.keyframe_insert(data_path="location", frame=start_frame)

            empty.location = (center_x - shift_amount_x, center_y, center_z)
            empty.keyframe_insert(data_path="location", frame=end_frame)


        elif context.scene.pop_direction_xyz == '-Y':
            empty.location = (center_x, center_y + shift_amount_y, center_z)
            empty.keyframe_insert(data_path="location", frame=start_frame)

            empty.location = (center_x, center_y - shift_amount_y, center_z)
            empty.keyframe_insert(data_path="location", frame=end_frame)


        
        

        if context.scene.pop_direction_xyz == 'X':
            # Import the geometry node from an external file
            filepath = addon_dirc + "/Assets.blend"
            node_group_name = "Pop In X"

            # Append the node group
            with bpy.data.libraries.load(filepath) as (data_from, data_to):
                data_to.node_groups = [node for node in data_from.node_groups if node == node_group_name]

            # Check if the node group was successfully appended
            if node_group_name in bpy.data.node_groups:
                pop_in_x = bpy.data.node_groups[node_group_name]
            else:
                self.report({'ERROR'}, f"Failed to append node group: {node_group_name} from {filepath}")
                return {'CANCELLED'}
            
            
            # Create a new cube object after setting the properties
            bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=(center_x, center_y, center_z))
            cube_object = bpy.context.object
            cube_object.name = "Pop In Floor Preset"  

         
            name = bpy.context.object.name
            obj = bpy.data.objects[name]
            mod = obj.modifiers.new(name = "Pop In X", type = 'NODES')
            mod.node_group = pop_in_x
            
            
            # Add the Empty to the modifier
            bpy.context.object.modifiers["Pop In X"]["Input_1"] = empty
            
            bpy.context.object.modifiers["Pop In X"]["Input_0"] = collection
            
            
            
            
        elif context.scene.pop_direction_xyz == '-X':
            # Import the geometry node from an external file
            filepath = addon_dirc + "/Assets.blend"
            node_group_name = "Pop In X2"

            # Append the node group
            with bpy.data.libraries.load(filepath) as (data_from, data_to):
                data_to.node_groups = [node for node in data_from.node_groups if node == node_group_name]

            # Check if the node group was successfully appended
            if node_group_name in bpy.data.node_groups:
                pop_in_x2 = bpy.data.node_groups[node_group_name]
            else:
                self.report({'ERROR'}, f"Failed to append node group: {node_group_name} from {filepath}")
                return {'CANCELLED'}
            
            
            # Create a new cube object after setting the properties
            bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=(center_x, center_y, center_z))
            cube_object = bpy.context.object
            cube_object.name = "Pop In Floor Preset"  

         
            name = bpy.context.object.name
            obj = bpy.data.objects[name]
            mod = obj.modifiers.new(name = "Pop In X2", type = 'NODES')
            mod.node_group = pop_in_x2
            
            
            # Add the Empty to the modifier
            bpy.context.object.modifiers["Pop In X2"]["Input_1"] = empty
            
            bpy.context.object.modifiers["Pop In X2"]["Input_0"] = collection
            
            
        elif context.scene.pop_direction_xyz == 'Y':
            # Import the geometry node from an external file
            filepath = addon_dirc + "/Assets.blend"
            node_group_name = "Pop In Y"

            # Append the node group
            with bpy.data.libraries.load(filepath) as (data_from, data_to):
                data_to.node_groups = [node for node in data_from.node_groups if node == node_group_name]

            # Check if the node group was successfully appended
            if node_group_name in bpy.data.node_groups:
                pop_in_y = bpy.data.node_groups[node_group_name]
            else:
                self.report({'ERROR'}, f"Failed to append node group: {node_group_name} from {filepath}")
                return {'CANCELLED'}
            
            
            # Create a new cube object after setting the properties
            bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=(center_x, center_y, center_z))
            cube_object = bpy.context.object
            cube_object.name = "Pop In Floor Preset"  

         
            name = bpy.context.object.name
            obj = bpy.data.objects[name]
            mod = obj.modifiers.new(name = "Pop In Y", type = 'NODES')
            mod.node_group = pop_in_y
            
            
            # Add the Empty to the modifier
            bpy.context.object.modifiers["Pop In Y"]["Input_1"] = empty
            
            bpy.context.object.modifiers["Pop In Y"]["Input_0"] = collection
            
            
            
            
        elif context.scene.pop_direction_xyz == '-Y':
            # Import the geometry node from an external file
            filepath = addon_dirc + "/Assets.blend"
            node_group_name = "Pop In Y2"

            # Append the node group
            with bpy.data.libraries.load(filepath) as (data_from, data_to):
                data_to.node_groups = [node for node in data_from.node_groups if node == node_group_name]

            # Check if the node group was successfully appended
            if node_group_name in bpy.data.node_groups:
                pop_in_y2 = bpy.data.node_groups[node_group_name]
            else:
                self.report({'ERROR'}, f"Failed to append node group: {node_group_name} from {filepath}")
                return {'CANCELLED'}
            
            
            # Create a new cube object after setting the properties
            bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=(center_x, center_y, center_z))
            cube_object = bpy.context.object
            cube_object.name = "Pop In Floor Preset"  

         
            name = bpy.context.object.name
            obj = bpy.data.objects[name]
            mod = obj.modifiers.new(name = "Pop In Y2", type = 'NODES')
            mod.node_group = pop_in_y2
            
            
            # Add the Empty to the modifier
            bpy.context.object.modifiers["Pop In Y2"]["Input_1"] = empty
            
            bpy.context.object.modifiers["Pop In Y2"]["Input_0"] = collection
            
            
        return {'FINISHED'}  
    
    
               

floor_operators_classes = (
    OBJECT_OT_Bend_Floors,
    SimpleOperator_Roll_Floors,
    OBJECT_OT_Wipe_Floors,
    Fall_Down_Tiles,
    Pop_In_Floors,
)