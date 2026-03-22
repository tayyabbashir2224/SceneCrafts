import bpy
import math
import os
from mathutils import Vector, Euler
from ..base_operators import BaseWallOperator

addon_dirc = os.path.dirname(os.path.realpath(__file__))

class BaseWallOperatorExtended(BaseWallOperator):
    """Enhanced base class with common functionality for all wall operators"""
    
    def validate_scene(self, context):
        """Base validation for all operators"""
        if not context.active_object:
            self.report({'WARNING'}, "No active object selected")
            return False
        if context.active_object.type != 'MESH':
            self.report({'WARNING'}, "Selected object must be a mesh")
            return False
        return True

    def apply_transformations(self, obj):
        """Apply transformations to object"""
        try:
            bpy.ops.object.make_single_user(object=True, obdata=True, material=False, 
                                          animation=False, obdata_animation=False)
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            return True
        except Exception as e:
            self.report({'ERROR'}, f"Transform apply failed: {str(e)}")
            return False

    def create_animation_empty(self, location, name):
        """Create and return an empty with proper error handling"""
        try:
            bpy.ops.object.select_all(action='DESELECT')
            bpy.ops.object.empty_add(type='PLAIN_AXES', location=location)
            empty = bpy.context.object
            empty.name = name
            return empty
        except Exception as e:
            self.report({'ERROR'}, f"Empty creation failed: {str(e)}")
            return None

    def cleanup(self, objects):
        """Cleanup temporary objects"""
        for obj in objects:
            if obj and obj.name in bpy.data.objects:
                bpy.data.objects.remove(obj, do_unlink=True)

    def insert_keyframe(self, target, data_path, value, frame):
        """Safe keyframe insertion"""
        if target and hasattr(target, data_path):
            setattr(target, data_path, value)
            target.keyframe_insert(data_path=data_path, frame=frame)

class OBJECT_OT_Bend_Walls(BaseWallOperatorExtended):
    bl_idname = "object.bend_walls"
    bl_label = "Bend Walls"

    def execute(self, context):
        empty = None
        try:
            if not self.validate_scene(context):
                return {'CANCELLED'}

            selected_object = context.active_object
            scene = context.scene
            
            if not self.apply_transformations(selected_object):
                return {'CANCELLED'}

            original_dimensions = selected_object.dimensions.copy()
            
            # Set origin
            bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')
            offset = self.calculate_offset(original_dimensions, scene.bend_walls_direction_xyz)
            
            if offset:
                try:
                    bpy.context.scene.tool_settings.use_transform_data_origin = True
                    bpy.ops.transform.translate(value=offset, orient_type='GLOBAL')
                finally:
                    bpy.context.scene.tool_settings.use_transform_data_origin = False

            # Create empty
            empty = self.create_animation_empty(selected_object.location, "Bend_Deform_Empty")
            if not empty:
                return {'CANCELLED'}

            # Configure empty rotation
            rotation, deform_axis = self.get_deform_axis(original_dimensions, scene.bend_walls_direction_xyz)
            empty.rotation_euler = rotation

            # Add deform modifier
            try:
                bpy.context.view_layer.objects.active = selected_object
                bpy.ops.object.modifier_add(type='SIMPLE_DEFORM')
                modifier = selected_object.modifiers[-1]
                modifier.deform_method = 'BEND'
                modifier.deform_axis = deform_axis
                modifier.origin = empty
            except Exception as e:
                self.report({'ERROR'}, f"Modifier creation failed: {str(e)}")
                return {'CANCELLED'}

            # Animation setup
            start_angle = math.radians(450) if scene.bend_walls_direction == 'INWARDS' else math.radians(-450)
            self.insert_keyframe(modifier, 'angle', start_angle, scene.bend_walls_start_frame)
            self.insert_keyframe(modifier, 'angle', 0, scene.bend_walls_end_frame)

            mid_frame = (scene.bend_walls_end_frame - scene.bend_walls_start_frame) // 2 + scene.bend_walls_start_frame
            self.insert_keyframe(selected_object, 'scale', (0, 0, 0), scene.bend_walls_start_frame)
            self.insert_keyframe(selected_object, 'scale', (1, 1, 1), mid_frame)

            return {'FINISHED'}

        except Exception as e:
            self.report({'ERROR'}, f"Bend operation failed: {str(e)}")
            self.cleanup([empty] if empty else [])
            return {'CANCELLED'}

    def calculate_offset(self, dimensions, direction):
        """Calculate translation offset based on direction"""
        offsets = {
            'X/Y': (0.5*dimensions.x, 0, -0.5*dimensions.z) if dimensions.x > dimensions.y 
                   else (0, 0.5*dimensions.y, -0.5*dimensions.z),
            '-X/Y': (-0.5*dimensions.x, 0, -0.5*dimensions.z) if dimensions.x > dimensions.y 
                    else (0, -0.5*dimensions.y, -0.5*dimensions.z),
            'Z': (0, 0, 0.5*dimensions.z),
            '-Z': (0, 0, -0.5*dimensions.z)
        }
        return offsets.get(direction, None)

    def get_deform_axis(self, dimensions, direction):
        """Determine deformation axis and empty rotation"""
        if direction in {'X/Y', '-X/Y'}:
            if dimensions.x > dimensions.y:
                return (Euler((0, math.pi/2, 0)), 'X')
            return (Euler((math.pi/2, 0, 0)), 'Y')
        
        if direction in {'Z', '-Z'}:
            if dimensions.x > dimensions.y:
                return (Euler((0, math.pi/2, 0)), 'Z')
            return (Euler((0, math.pi/2, math.pi/2)), 'Z')
        
        return (Euler(), 'Z')

class SimpleOperator_Roll_Walls(BaseWallOperatorExtended):
    bl_idname = "object.roll_walls"
    bl_label = "Roll Walls"

    def execute(self, context):
        curve_object = None
        try:
            if not self.validate_scene(context):
                return {'CANCELLED'}

            selected_object = context.active_object
            scene = context.scene
            
            if not self.apply_transformations(selected_object):
                return {'CANCELLED'}

            original_dimensions = selected_object.dimensions.copy()
            
            # Create curve
            curve_object = self.setup_curve(selected_object, original_dimensions, scene)
            if not curve_object:
                return {'CANCELLED'}

            # Add curve modifier
            if not self.add_curve_modifier(selected_object, curve_object):
                self.cleanup([curve_object])
                return {'CANCELLED'}

            # Setup animations
            self.setup_animations(selected_object, curve_object, scene)
            return {'FINISHED'}

        except Exception as e:
            self.report({'ERROR'}, f"Roll operation failed: {str(e)}")
            self.cleanup([curve_object] if curve_object else [])
            return {'CANCELLED'}

    def setup_curve(self, obj, dimensions, scene):
        """Create and configure curve object"""
        try:
            curve = self.load_or_create_curve(obj, dimensions, scene)
            if not curve:
                return None

            self.position_curve(curve, obj, dimensions, scene)
            self.rotate_curve(curve, dimensions, scene)
            self.scale_curve(curve, dimensions, scene)
            
            return curve
        except Exception as e:
            self.report({'ERROR'}, f"Curve setup failed: {str(e)}")
            return None

    def load_or_create_curve(self, obj, dimensions, scene):
        """Load or create curve"""
        blend_path = os.path.join(addon_dirc, "Assets.blend")
        base_name = "Roll_Curve"
        existing = [o for o in bpy.data.objects if o.name.startswith(base_name)]
        new_name = f"{base_name}_{len(existing):03d}"

        try:
            with bpy.data.libraries.load(blend_path) as (data_from, data_to):
                if "NurbsPath Roll" in data_from.objects:
                    data_to.objects = ["NurbsPath Roll"]

            if "NurbsPath Roll" in bpy.data.objects:
                new_curve = bpy.data.objects["NurbsPath Roll"].copy()
                new_curve.name = new_name
                bpy.context.collection.objects.link(new_curve)
                return new_curve
                
            return self.create_fallback_curve(new_name, obj.location)
        except Exception as e:
            self.report({'WARNING'}, f"Asset load failed: {str(e)}")
            return self.create_fallback_curve(new_name, obj.location)

    def create_fallback_curve(self, name, location):
        """Create fallback curve"""
        try:
            bpy.ops.curve.primitive_nurbs_path_add()
            curve = bpy.context.object
            curve.name = name
            curve.location = location
            return curve
        except Exception as e:
            self.report({'ERROR'}, f"Curve creation failed: {str(e)}")
            return None

    def position_curve(self, curve, obj, dimensions, scene):
        """Position curve"""
        direction = scene.roll_walls_direction_xyz
        offset = 1.3 * 0.5
        loc = obj.location.copy()

        if direction == 'X/Y':
            if dimensions.x > dimensions.y:
                loc.x += dimensions.x * offset
            else:
                loc.y += dimensions.y * offset
        elif direction == '-X/Y':
            if dimensions.x > dimensions.y:
                loc.x -= dimensions.x * offset
            else:
                loc.y -= dimensions.y * offset
        elif direction == 'Z':
            loc.z += dimensions.z * offset
        elif direction == '-Z':
            loc.z -= dimensions.z * offset

        curve.location = loc

    def rotate_curve(self, curve, dimensions, scene):
        """Rotate curve"""
        direction = scene.roll_walls_direction_xyz
        rotation = Euler()

        if direction in {'X/Y', '-X/Y'}:
            if dimensions.x > dimensions.y:
                rotation.x = math.radians(-90)
                rotation.z = math.radians(180)
            else:
                rotation.z = math.radians(-90)
                rotation.x = math.radians(-90)
        elif direction == '-Z':
            rotation.x = math.radians(90)
            rotation.y = math.radians(-90) if dimensions.x > dimensions.y else math.radians(180)
        elif direction == 'Z':
            rotation.x = math.radians(-90)
            rotation.y = math.radians(90)
            rotation.z = math.radians(180)

        curve.rotation_euler = rotation

    def scale_curve(self, curve, dimensions, scene):
        """Scale curve"""
        direction = scene.roll_walls_direction_xyz
        if direction in {'X/Y', '-X/Y'}:
            scale = dimensions.x if dimensions.x > dimensions.y else dimensions.y
        else:
            scale = dimensions.z
        curve.scale = (scale * 0.5,) * 3

    def add_curve_modifier(self, obj, curve):
        """Add curve modifier"""
        try:
            modifier = obj.modifiers.new(name="Curve_Modifier", type='CURVE')
            modifier.deform_axis = 'POS_X'
            modifier.object = curve
            return True
        except Exception as e:
            self.report({'ERROR'}, f"Modifier creation failed: {str(e)}")
            return False

    def setup_animations(self, obj, curve, scene):
        """Setup animations"""
        frame_start = scene.roll_walls_start_frame
        frame_end = scene.roll_walls_end_frame
        frame_mid = frame_start + (frame_end - frame_start) // 3

        # Curve animation
        self.insert_keyframe(curve, 'location', curve.location, frame_mid)
        self.animate_curve_movement(curve, obj, scene, frame_end)
        
        # Object scale animation
        self.animate_object_scale(obj, scene, frame_start, frame_mid)

    def animate_curve_movement(self, curve, obj, scene, frame_end):
        """Animate curve movement"""
        new_loc = curve.location.copy()
        direction = scene.roll_walls_direction_xyz
        dimensions = obj.dimensions
        offset = 1.2

        if direction == 'X/Y':
            if dimensions.x > dimensions.y:
                new_loc.x -= dimensions.x * offset
            else:
                new_loc.y -= dimensions.y * offset
        elif direction == '-X/Y':
            if dimensions.x > dimensions.y:
                new_loc.x += dimensions.x * offset
            else:
                new_loc.y += dimensions.y * offset
        elif direction == 'Z':
            new_loc.z -= dimensions.z * offset
        elif direction == '-Z':
            new_loc.z += dimensions.z * offset

        curve.location = new_loc
        self.insert_keyframe(curve, 'location', new_loc, frame_end)

    def animate_object_scale(self, obj, scene, frame_start, frame_mid):
        """Animate object scale"""
        initial_scale = self.get_initial_scale(obj.dimensions, scene)
        obj.scale = initial_scale
        self.insert_keyframe(obj, 'scale', initial_scale, frame_start)
        obj.scale = (1, 1, 1)
        self.insert_keyframe(obj, 'scale', (1, 1, 1), frame_mid)
        
        if obj.animation_data:
            for fc in obj.animation_data.action.fcurves:
                if fc.data_path == "scale":
                    for kp in fc.keyframe_points:
                        kp.interpolation = 'BACK'

    def get_initial_scale(self, dimensions, scene):
        """Get initial scale"""
        direction = scene.roll_walls_direction_xyz
        if direction in {'X/Y', '-X/Y'}:
            return (1, 1, 0)
        return (0, 1, 1) if dimensions.x > dimensions.y else (1, 0, 1)

class OBJECT_OT_Wipe_Walls(BaseWallOperatorExtended):
    bl_idname = "object.wipe_walls"
    bl_label = "Wipe Walls"

    def execute(self, context):
        try:
            if not self.validate_scene(context):
                return {'CANCELLED'}

            selected_object = context.active_object
            scene = context.scene
            
            if not self.apply_transformations(selected_object):
                return {'CANCELLED'}

            original_dimensions = selected_object.dimensions.copy()
            
            # Set origin
            bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')
            self.adjust_origin_position(selected_object, original_dimensions, scene)
            
            # Setup animation
            self.setup_wipe_animation(selected_object, original_dimensions, scene)
            return {'FINISHED'}

        except Exception as e:
            self.report({'ERROR'}, f"Wipe operation failed: {str(e)}")
            return {'CANCELLED'}

    def adjust_origin_position(self, obj, dimensions, scene):
        """Adjust origin position"""
        offset = self.calculate_offset(dimensions, scene.wipe_walls_direction_xyz)
        if offset:
            try:
                bpy.context.scene.tool_settings.use_transform_data_origin = True
                bpy.ops.transform.translate(value=offset, orient_type='GLOBAL')
            finally:
                bpy.context.scene.tool_settings.use_transform_data_origin = False

    def calculate_offset(self, dimensions, direction):
        """Calculate offset"""
        offset_map = {
            'X/Y': (dimensions.x/2, 0, -dimensions.z/2) if dimensions.x > dimensions.y 
                   else (0, dimensions.y/2, -dimensions.z/2),
            '-X/Y': (-dimensions.x/2, 0, -dimensions.z/2) if dimensions.x > dimensions.y 
                    else (0, -dimensions.y/2, -dimensions.z/2),
            'Z': (0, 0, dimensions.z/2),
            '-Z': (0, 0, -dimensions.z/2)
        }
        return offset_map.get(direction, None)

    def setup_wipe_animation(self, obj, dimensions, scene):
        """Setup wipe animation"""
        scales = self.get_animation_scales(dimensions, scene.wipe_walls_direction_xyz)
        frames = (
            scene.wipe_walls_start_frame,
            scene.wipe_walls_start_frame + 1,
            scene.wipe_walls_end_frame
        )
        
        for frame, scale in zip(frames, scales):
            self.insert_keyframe(obj, 'scale', scale, frame)
        
        self.set_scale_interpolation(obj, 'CUBIC')

    def get_animation_scales(self, dimensions, direction):
        """Get animation scales"""
        if direction in {'X/Y', '-X/Y'}:
            if dimensions.x > dimensions.y:
                return [(0, 1, 0), (0, 1, 1), (1, 1, 1)]
            return [(1, 0, 0), (1, 0, 1), (1, 1, 1)]
        
        if direction in {'Z', '-Z'}:
            return [(1, 0, 0), (1, 1, 0), (1, 1, 1)]
        
        return [(1, 1, 1)] * 3

    def set_scale_interpolation(self, obj, interpolation):
        """Set scale interpolation"""
        if obj.animation_data and obj.animation_data.action:
            for fc in obj.animation_data.action.fcurves:
                if fc.data_path == "scale":
                    for kp in fc.keyframe_points:
                        kp.interpolation = interpolation

class BasePresetOperator(BaseWallOperator):
    """Base class for preset wall animation operators"""
    
    node_group_prefix = ""
    preset_name = ""
    direction_prop = ""
    start_frame_prop = ""
    end_frame_prop = ""
    
    def get_properties(self, context):
        """Placeholder for getting the correct property group"""
        return None 
    
    def execute(self, context):
        empty = None
        try:
            if not self.validate_scene(context):
                return {'CANCELLED'}

            props = self.get_properties(context)
            collection = self.get_collection(props.collection_name)
            dimensions, center = self.calculate_collection_bounds(collection)
            empty = self.create_animation_empty(center, props.empty_name)
            
            self.animate_empty(empty, dimensions, center, context)
            self.setup_geometry_nodes(
                context, 
                collection, 
                empty, 
                center,
                self.node_group_prefix,
                self.preset_name
            )
            
            return {'FINISHED'}
            
        except Exception as e:
            self.report({'ERROR'}, f"{self.bl_label} failed: {str(e)}")
            self.cleanup(empty if 'empty' in locals() else None)
            return {'CANCELLED'}

    def validate_scene(self, context):
        """Base validation logic"""
        if not hasattr(context.scene, self.direction_prop):
            self.report({'ERROR'}, "Missing required scene properties")
            return False
        return True

    def get_collection(self, collection_name):
        """Get and validate collection"""
        collection = bpy.data.collections.get(collection_name)
        if not collection:
            raise ValueError(f"Collection '{collection_name}' not found")
        return collection

    def calculate_collection_bounds(self, collection):
        """Calculate collection bounding box"""
        min_coords = Vector((float('inf'),)*3)
        max_coords = Vector((float('-inf'),)*3)

        for obj in collection.objects:
            if obj.type != 'MESH':
                continue
                
            for vert in obj.data.vertices:
                world_co = obj.matrix_world @ vert.co
                min_coords = Vector(map(min, zip(min_coords, world_co)))
                max_coords = Vector(map(max, zip(max_coords, world_co)))

        dimensions = max_coords - min_coords
        center = (min_coords + max_coords) / 2
        
        return dimensions, center

    def create_animation_empty(self, location, name):
        """Create animation control empty"""
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.empty_add(
            type='PLAIN_AXES', 
            location=location
        )
        empty = bpy.context.object
        empty.name = name
        return empty

    def animate_empty(self, empty, dimensions, center, context):
        """Animate empty movement based on direction"""
        direction = getattr(context.scene, self.direction_prop)
        shift_amount = dimensions / 1.2
        frame_start = getattr(context.scene, self.start_frame_prop)
        frame_end = getattr(context.scene, self.end_frame_prop)

        # Calculate initial position based on direction
        start_pos, end_pos = self.calculate_movement(
            direction, 
            dimensions, 
            center, 
            shift_amount
        )

        # Set keyframes
        empty.location = start_pos
        empty.keyframe_insert("location", frame=frame_start)
        empty.location = end_pos
        empty.keyframe_insert("location", frame=frame_end)

    def calculate_movement(self, direction, dimensions, center, shift):
        """Calculate empty movement path"""
        dir_map = {
            'X/Y': {
                'start': (-shift.x, 0, 0) if dimensions.x > dimensions.y else (0, -shift.y, 0),
                'end': (shift.x, 0, 0) if dimensions.x > dimensions.y else (0, shift.y, 0)
            },
            '-X/Y': {
                'start': (shift.x, 0, 0) if dimensions.x > dimensions.y else (0, shift.y, 0),
                'end': (-shift.x, 0, 0) if dimensions.x > dimensions.y else (0, -shift.y, 0)
            },
            'Z': {'start': (0, 0, -shift.z), 'end': (0, 0, shift.z)},
            '-Z': {'start': (0, 0, shift.z), 'end': (0, 0, -shift.z)}
        }
        
        base = Vector(center)
        offsets = dir_map.get(direction, {'start': (0,0,0), 'end': (0,0,0)})
        return base + Vector(offsets['start']), base + Vector(offsets['end'])

    def setup_geometry_nodes(self, context, collection, empty, center, prefix, preset_name):
        """Setup geometry nodes modifier"""
        direction = getattr(context.scene, self.direction_prop)
        mesh_obj = next((obj for obj in collection.objects if obj.type == 'MESH'), None)
        dimensions = mesh_obj.dimensions if mesh_obj else Vector((1,1,1))
        
        suffix = self.get_node_group_suffix(direction, dimensions)
        node_group_name = f"{prefix} {suffix}"
        
        node_group = self.append_node_group(node_group_name)
        if not node_group:
            raise ValueError(f"Failed to load node group: {node_group_name}")
            
        preset_obj = self.create_preset_object(center, preset_name)
        self.add_geometry_node_modifier(
            preset_obj, 
            node_group, 
            collection, 
            empty
        )

    def get_node_group_suffix(self, direction, dimensions):
        """Determine node group suffix based on direction and dimensions"""
        if direction in {'X/Y', '-X/Y'}:
            return 'X' if dimensions.x > dimensions.y else 'Y'
        return 'ZX' if dimensions.x > dimensions.y else 'ZY'

    def append_node_group(self, name):
        """Append node group from assets"""
        filepath = os.path.join(addon_dirc, "Assets.blend")
        
        try:
            with bpy.data.libraries.load(filepath) as (data_from, data_to):
                data_to.node_groups = [g for g in data_from.node_groups if g.startswith(name)] 
                
            return bpy.data.node_groups.get(name) or bpy.data.node_groups.get(data_to.node_groups[0])
        except Exception as e:
            self.report({'ERROR'}, f"Asset load failed: {str(e)}")
            return None

    def create_preset_object(self, location, name):
        """Create preset cube object"""
        bpy.ops.mesh.primitive_cube_add(size=2, location=location)
        obj = bpy.context.object
        obj.name = name
        return obj

    def add_geometry_node_modifier(self, obj, node_group, collection, empty):
        """Add and configure geometry node modifier"""
        mod_name = f"{node_group.name}_Modifier"
        modifier = obj.modifiers.get(mod_name) or obj.modifiers.new(mod_name, 'NODES')
        
        modifier.node_group = node_group
        modifier["Input_1"] = collection
        modifier["Input_2"] = empty
        
        return modifier

    def cleanup(self, empty):
        """Remove temporary objects"""
        if empty and empty.name in bpy.data.objects:
            bpy.data.objects.remove(empty, do_unlink=True)

class OBJECT_OT_Pop_In_Walls(BasePresetOperator):
    bl_idname = "object.pop_in_walls"
    bl_label = "Pop In Wall Tiles"
    node_group_prefix = "NTPop In Walls"
    preset_name = "Pop_In_Walls_Preset"
    direction_prop = "pop_w_direction_xyz"
    start_frame_prop = "pop_w_start_frame"
    end_frame_prop = "pop_w_end_frame"

    def get_properties(self, context):
        return context.scene.pop_in_walls

class OBJECT_OT_Rotate_In_Walls(BasePresetOperator):
    bl_idname = "object.rotate_in_walls"
    bl_label = "Rotate In Wall Tiles"
    node_group_prefix = "NTRotate Walls"
    preset_name = "Rotate_In_Walls_Preset"
    direction_prop = "rotate_w_direction_xyz"
    start_frame_prop = "rotate_w_start_frame"
    end_frame_prop = "rotate_w_end_frame"

    def get_properties(self, context):
        return context.scene.rotate_in_walls

wall_operators_classes = (
    OBJECT_OT_Bend_Walls,
    SimpleOperator_Roll_Walls,
    OBJECT_OT_Wipe_Walls,
    OBJECT_OT_Pop_In_Walls,
    OBJECT_OT_Rotate_In_Walls,
)