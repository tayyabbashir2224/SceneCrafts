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
        empty = None
        try:
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
                empty.name = "Bend_Floor_Empty"

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
                modifier.origin = empty  # Set the empty as the origin
                
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
                self.report({'WARNING'}, "No active object selected.")
                return {'CANCELLED'}
                
            return {'FINISHED'}
        
        except Exception as e:
            self.report({'ERROR'}, f"Bend Floors operation failed: {e}")
            return {'CANCELLED'}
        finally:
            # Clean up the temporary empty object
            if empty and empty.name in bpy.data.objects:
                bpy.data.objects.remove(empty, do_unlink=True)

class SimpleOperator_Roll_Floors(BaseFloorOperator):
    bl_idname = "object.roll_floors"
    bl_label = "Roll Floors"

    def execute(self, context):
        curve = None
        try:
            if not (obj := context.active_object) or obj.type != 'MESH':
                self.report({'ERROR'}, "Select a mesh object")
                return {'CANCELLED'}

            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

            # Load curve asset
            blend_path = os.path.join(addon_dirc, "Assets.blend")
            curve_name = "NurbsPath Roll"
            
            with bpy.data.libraries.load(blend_path) as (data_from, data_to):
                if curve_name in data_from.objects:
                    data_to.objects = [curve_name]
            
            if curve_name in bpy.data.objects:
                curve = bpy.data.objects[curve_name].copy()
                curve.name = f"Roll_Curve_{obj.name}"
                context.collection.objects.link(curve)
            else:
                # Fallback creation
                bpy.ops.curve.primitive_nurbs_path_add(location=obj.location)
                curve = context.active_object
                curve.name = f"Roll_Curve_{obj.name}"

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
            mod = obj.modifiers.new(name="Roll_Modifier", type='CURVE')
            mod.object = curve
            mod.deform_axis = 'POS_X'

            # Animate curve movement
            start_frame = context.scene.roll_start_frame
            end_frame = context.scene.roll_end_frame
            curve.keyframe_insert(data_path='location', frame=start_frame)
            
            move_offset = obj.dimensions.x * 1.5 if direction in {'X', '-X'} else obj.dimensions.y * 1.5
            if direction in {'-X', '-Y'}:
                move_offset *= -1
                
            if direction in {'X', '-X'}:
                curve.location.x += move_offset
            else:
                curve.location.y += move_offset
                
            curve.keyframe_insert(data_path='location', frame=end_frame)

            return {'FINISHED'}

        except Exception as e:
            self.report({'ERROR'}, f"Rolling failed: {str(e)}")
            return {'CANCELLED'}
        finally:
            if curve and curve.name in bpy.data.objects:
                bpy.data.objects.remove(curve, do_unlink=True)

class OBJECT_OT_Wipe_Floors(BaseFloorOperator):
    bl_idname = "object.wipe_floors"
    bl_label = "Wipe Floors"

    def execute(self, context):
        if bpy.context.active_object is not None:
            selected_object = bpy.context.active_object
            
            bpy.ops.object.make_single_user(object=True, obdata=True, material=False, animation=False, obdata_animation=False)
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

            # Store initial dimensions
            original_dimensions = selected_object.dimensions.copy()

            # Set the origin point
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
            start_scale = (1, 1, 1)
            utility_scale = (1, 1, 1)
            end_scale = (1, 1, 1)

            if context.scene.wipe_direction_xyz in {'X', '-X'}:
                    start_scale = (0, 1, 0)
                    utility_scale = (0, 1, 1)
                    end_scale = (1, 1, 1)
            if context.scene.wipe_direction_xyz in {'Y', '-Y'}:
                start_scale = (1, 0, 0)
                utility_scale = (1, 0, 1)
                end_scale = (1, 1, 1)
                
            # Set keyframes
            selected_object.scale = start_scale
            selected_object.keyframe_insert(data_path="scale", frame=frame_start)
            selected_object.scale = utility_scale
            selected_object.keyframe_insert(data_path="scale", frame=frame_Utility)
            selected_object.scale = end_scale
            selected_object.keyframe_insert(data_path="scale", frame=frame_end)
    
            # Set interpolation mode to Cubic
            if selected_object.animation_data and selected_object.animation_data.action:
                for fcurve in selected_object.animation_data.action.fcurves:
                    if fcurve.data_path == "scale":
                        for keyframe_point in fcurve.keyframe_points:
                            keyframe_point.interpolation = 'CUBIC'  

        else:
            self.report({'WARNING'}, "No active object selected.")
            return {'CANCELLED'}

        return {'FINISHED'}

class Fall_Down_Tiles(BaseFloorOperator):
    bl_idname = "object.fall_down_tiles"
    bl_label = "Fall Down Tiles"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Make floor tiles collection fall down from center"
    
    def execute(self, context):
        fall_down_tiles_props = context.scene.fall_down_tiles
        collection_name = fall_down_tiles_props.collection_name
        start_frame = context.scene.fade_start_frame
        end_frame = context.scene.fade_end_frame
        
        collection = bpy.data.collections.get(collection_name)
        if not collection:
            self.report({'ERROR'}, "Collection not found")
            return {'CANCELLED'}

        objects_in_collection = [obj for obj in collection.objects if obj.type == 'MESH']
        if not objects_in_collection:
            self.report({'WARNING'}, "No mesh objects in collection")
            return {'CANCELLED'}

        # Calculate bounding box center
        min_x, min_y, min_z = float('inf'), float('inf'), float('inf')
        max_x, max_y, max_z = float('-inf'), float('-inf'), float('-inf')

        for obj in objects_in_collection:
            for vert in obj.data.vertices:
                world_coord = obj.matrix_world @ vert.co
                min_x = min(min_x, world_coord.x)
                min_y = min(min_y, world_coord.y)
                min_z = min(min_z, world_coord.z)
                max_x = max(max_x, world_coord.x)
                max_y = max(max_y, world_coord.y)
                max_z = max(max_z, world_coord.z)

        center_x = (min_x + max_x) / 2
        center_y = (min_y + max_y) / 2
        center_z = (min_z + max_z) / 2
        
        longest_dimension = max(max_x - min_x, max_y - min_y)
        scaling_factor = (max_x - min_x + max_y - min_y) / 2

        # Create temporary objects
        empty = None
        cube_object = None
        
        try:
            bpy.ops.object.select_all(action='DESELECT')
            bpy.ops.object.empty_add(type='SPHERE', location=(center_x, center_y, center_z))
            empty = bpy.context.object
            empty.name = "Tiles_Fall_Empty"
            
            keyframe_frame = start_frame + (end_frame - start_frame) / 3
            empty.keyframe_insert(data_path="location", frame=keyframe_frame)
            empty.location.z += 1.0
            empty.keyframe_insert(data_path="location", frame=start_frame)

            # Load Node Group
            filepath = os.path.join(addon_dirc, "Assets.blend")
            node_group_name = "Fall Down"
            
            with bpy.data.libraries.load(filepath) as (data_from, data_to):
                if node_group_name in data_from.node_groups:
                    data_to.node_groups = [node_group_name]
            
            fall_down_group = bpy.data.node_groups.get(node_group_name)
            if not fall_down_group:
                self.report({'ERROR'}, f"Failed to load node group: {node_group_name}")
                return {'CANCELLED'}

            bpy.ops.mesh.primitive_cube_add(size=2, location=(center_x, center_y, center_z))
            cube_object = bpy.context.object
            cube_object.name = "Fall_Down_Floor_Preset"  

            mod = cube_object.modifiers.new(name="Fall Down", type='NODES')
            mod.node_group = fall_down_group
            mod["Input_2"] = empty
            mod["Input_1"] = collection

            # Animate modifier property
            mod["Input_3"] = 0.0
            cube_object.keyframe_insert(data_path='modifiers["Fall Down"]["Input_3"]', frame=start_frame)

            if longest_dimension <= 5:
                mod["Input_3"] = scaling_factor / 1.5
            elif longest_dimension <= 10:
                mod["Input_3"] = scaling_factor / 1.475
            else:
                mod["Input_3"] = scaling_factor / 1.4
            
            cube_object.keyframe_insert(data_path='modifiers["Fall Down"]["Input_3"]', frame=end_frame)
            
            return {'FINISHED'}

        except Exception as e:
            self.report({'ERROR'}, f"Operation failed: {e}")
            return {'CANCELLED'}
        finally:
            if empty and empty.name in bpy.data.objects:
                bpy.data.objects.remove(empty, do_unlink=True)

class Pop_In_Floors(BaseFloorOperator):
    bl_idname = "object.pop_in_floors"
    bl_label = "Pop In Floors"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Pop in or out floor tiles collection from any direction"
    
    def execute(self, context):
        pop_in_floors_props = context.scene.pop_in_floors
        collection_name = pop_in_floors_props.collection_name
        start_frame = context.scene.pop_start_frame
        end_frame = context.scene.pop_end_frame
        
        collection = bpy.data.collections.get(collection_name)
        if not collection:
            return {'CANCELLED'}

        objects_in_collection = [obj for obj in collection.objects if obj.type == 'MESH']
        if not objects_in_collection:
            return {'CANCELLED'}

        # Bounding box calc
        min_x, min_y, min_z = float('inf'), float('inf'), float('inf')
        max_x, max_y, max_z = float('-inf'), float('-inf'), float('-inf')

        for obj in objects_in_collection:
            for vert in obj.data.vertices:
                world_coord = obj.matrix_world @ vert.co
                min_x = min(min_x, world_coord.x)
                min_y = min(min_y, world_coord.y)
                min_z = min(min_z, world_coord.z)
                max_x = max(max_x, world_coord.x)
                max_y = max(max_y, world_coord.y)
                max_z = max(max_z, world_coord.z)

        center_x = (min_x + max_x) / 2
        center_y = (min_y + max_y) / 2
        center_z = (min_z + max_z) / 2
        
        shift_amount_x = (max_x - min_x) / 1.2
        shift_amount_y = (max_y - min_y) / 1.2

        empty = None
        cube_object = None

        try:
            bpy.ops.object.select_all(action='DESELECT')
            bpy.ops.object.empty_add(type='PLAIN_AXES', location=(center_x, center_y, center_z))
            empty = bpy.context.object
            empty.name = "Pop_In_Floor_Empty"
            
            direction = context.scene.pop_direction_xyz
            
            if direction == 'X':
                empty.location = (center_x - shift_amount_x, center_y, center_z)
                empty.keyframe_insert("location", frame=start_frame)
                empty.location = (center_x + shift_amount_x, center_y, center_z)
                empty.keyframe_insert("location", frame=end_frame)
            elif direction == 'Y':
                empty.location = (center_x, center_y - shift_amount_y, center_z)
                empty.keyframe_insert("location", frame=start_frame)
                empty.location = (center_x, center_y + shift_amount_y, center_z)
                empty.keyframe_insert("location", frame=end_frame)
            elif direction == '-X':
                empty.location = (center_x + shift_amount_x, center_y, center_z)
                empty.keyframe_insert("location", frame=start_frame)
                empty.location = (center_x - shift_amount_x, center_y, center_z)
                empty.keyframe_insert("location", frame=end_frame)
            elif direction == '-Y':
                empty.location = (center_x, center_y + shift_amount_y, center_z)
                empty.keyframe_insert("location", frame=start_frame)
                empty.location = (center_x, center_y - shift_amount_y, center_z)
                empty.keyframe_insert("location", frame=end_frame)

            # Determine Node Group
            node_group_name = "Pop In X"
            if direction == '-X': node_group_name = "Pop In X2"
            elif direction == 'Y': node_group_name = "Pop In Y"
            elif direction == '-Y': node_group_name = "Pop In Y2"

            filepath = os.path.join(addon_dirc, "Assets.blend")
            with bpy.data.libraries.load(filepath) as (data_from, data_to):
                if node_group_name in data_from.node_groups:
                    data_to.node_groups = [node_group_name]
            
            node_group = bpy.data.node_groups.get(node_group_name)
            
            bpy.ops.mesh.primitive_cube_add(size=2, location=(center_x, center_y, center_z))
            cube_object = bpy.context.object
            cube_object.name = "Pop_In_Floor_Preset"

            mod = cube_object.modifiers.new(name=node_group_name, type='NODES')
            mod.node_group = node_group
            mod["Input_1"] = empty
            mod["Input_0"] = collection
            
            return {'FINISHED'}

        except Exception as e:
            self.report({'ERROR'}, f"Operation failed: {e}")
            return {'CANCELLED'}
        finally:
            if empty and empty.name in bpy.data.objects:
                bpy.data.objects.remove(empty, do_unlink=True)

floor_operators_classes = (
    OBJECT_OT_Bend_Floors,
    SimpleOperator_Roll_Floors,
    OBJECT_OT_Wipe_Floors,
    Fall_Down_Tiles,
    Pop_In_Floors,
)