# SceneCraft/operators/camera_light_animations.py
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
import random
from mathutils import Vector, noise

class OBJECT_OT_ApplyLightAnimation(bpy.types.Operator):
    bl_idname = "scenecraft.apply_light_animation"
    bl_label = "Apply Light Animation"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.light_animation_props
        light = next((obj for obj in context.scene.objects if obj.type == 'LIGHT'), None)

        if not light:
            self.report({'WARNING'}, "No light found in the scene!")
            return {'CANCELLED'}

        start_frame, end_frame = props.start_frame, props.end_frame

        if props.light_preset == 'FLICKER':
            self.apply_flicker(light, start_frame, end_frame, props.flicker_speed)
        elif props.light_preset == 'INTENSITY':
            self.apply_dynamic_intensity(light, start_frame, end_frame)
        elif props.light_preset == 'MOVEMENT':
            self.apply_light_movement(light, start_frame, end_frame, props)
        elif props.light_preset == 'PULSE':
            self.apply_pulse_intensity(light, start_frame, end_frame, props.pulse_speed)
        elif props.light_preset == 'STROBE':
            self.apply_strobe_effect(light, start_frame, end_frame)
        elif props.light_preset == 'RANGE':
            self.apply_range_animation(light, start_frame, end_frame)
        elif props.light_preset == 'COLOR':
            self.apply_color_animation(light, start_frame, end_frame)
        elif props.light_preset == 'TRACK_TARGET':
            self.apply_spotlight_target(light, start_frame, end_frame, props.target_object)
        elif props.light_preset == 'RANDOM_FLICKER':
            self.apply_random_flicker(light, start_frame, end_frame, (10, 200))
        elif props.light_preset == 'FIRELIGHT':
            self.apply_firelight_effect(light, start_frame, end_frame)
        elif props.light_preset == 'LIGHTNING':
            self.apply_lightning_effect(light, start_frame, end_frame)
        elif props.light_preset == 'SWEEP':
            self.apply_sweep_motion(light, start_frame, end_frame, axis='X')
        elif props.light_preset == 'SPOTLIGHT_BEAM':
            self.apply_spotlight_beam(light, start_frame, end_frame)
        elif props.light_preset == 'COLOR_GRADIENT':
            colors = [color.color for color in props.gradient_colors]
            self.apply_color_gradient(light, start_frame, end_frame, colors, props.gradient_steps)
        elif props.light_preset == 'SWITCH':
            self.apply_realtime_light_switch(context)           
            
        self.report({'INFO'}, f"Applied {props.light_preset} animation!")
        return {'FINISHED'}

    def spiral_path(self, light, start_frame, end_frame, radius, steps, z_oscillation):
        initial_location = light.location.copy()
        duration = end_frame - start_frame
        if duration <= 0:
            return

        total_rotations = 3
        for i in range(steps + 1):
            progress = i / steps
            current_frame = start_frame + (progress * duration)
            bpy.context.scene.frame_set(int(round(current_frame)))

            angle = progress * total_rotations * 2 * math.pi
            x = initial_location.x + radius * math.cos(angle)
            y = initial_location.y + radius * math.sin(angle)
            z = initial_location.z + z_oscillation * math.sin(angle * 2)

            light.location = (x, y, z)
            light.keyframe_insert(data_path="location")

        bpy.context.scene.frame_set(start_frame)

    def apply_flicker(self, light, start_frame, end_frame, flicker_speed):
        for frame in range(start_frame, end_frame, int(max(1, flicker_speed * 10))):
            light.data.energy = 0 if light.data.energy > 0 else 100
            light.data.keyframe_insert(data_path="energy", frame=frame)

    def apply_dynamic_intensity(self, light, start_frame, end_frame):
        steps = 30
        for step in range(steps + 1):
            t = step / steps
            intensity = 100 + 50 * math.sin(2 * math.pi * t)
            frame = start_frame + (step * (end_frame - start_frame) // steps)
            light.data.energy = intensity
            light.data.keyframe_insert(data_path="energy", frame=frame)

    def apply_light_movement(self, light, start_frame, end_frame, props):
        movement_type = props.movement_path_type
        z_oscillation = 2.0 if props.z_oscillation else 0.0
        radius = 5.0
        steps = 36

        if movement_type == 'CIRCULAR':
            self.circular_path(light, start_frame, end_frame, radius, steps, z_oscillation)
        elif movement_type == 'SPIRAL':
            self.spiral_path(light, start_frame, end_frame, radius, steps, z_oscillation)
        elif movement_type == 'LINEAR':
            self.linear_path(light, start_frame, end_frame)

    def circular_path(self, light, start_frame, end_frame, radius, steps, z_oscillation):
        initial_location = light.location.copy()
        for step in range(steps + 1):
            angle = step * (2 * math.pi / steps)
            x = initial_location.x + radius * math.cos(angle)
            y = initial_location.y + radius * math.sin(angle)
            z = initial_location.z + (math.sin(angle) * z_oscillation)
            frame = start_frame + (step * (end_frame - start_frame) // steps)
            light.location = (x, y, z)
            light.keyframe_insert(data_path="location", frame=frame)

    def linear_path(self, light, start_frame, end_frame):
        light.keyframe_insert(data_path="location", frame=start_frame)
        light.location.x += 5.0 
        light.keyframe_insert(data_path="location", frame=end_frame)

    def apply_pulse_intensity(self, light, start_frame, end_frame, pulse_speed):
        steps = 20
        for step in range(steps + 1):
            t = step / steps
            energy = 50 + 50 * math.sin(2 * math.pi * pulse_speed * t)
            frame = start_frame + (step * (end_frame - start_frame) // steps)
            light.data.energy = energy
            light.data.keyframe_insert(data_path="energy", frame=frame)

    def apply_strobe_effect(self, light, start_frame, end_frame):
        for frame in range(start_frame, end_frame, 5):
            light.data.energy = 300
            light.data.keyframe_insert(data_path="energy", frame=frame)
            light.data.energy = 0
            light.data.keyframe_insert(data_path="energy", frame=frame + 2)

    def apply_color_animation(self, light, start_frame, end_frame):
        steps = 10
        for step in range(steps + 1):
            t = step / steps
            r = (1 - t) * 1.0 + t * 0.0
            g = (1 - t) * 0.0 + t * 1.0
            b = (1 - t) * 0.5 + t * 0.0
            frame = start_frame + (step * (end_frame - start_frame) // steps)
            light.data.color = (r, g, b)
            light.data.keyframe_insert(data_path="color", frame=frame)

    def apply_firelight_effect(self, light, start_frame, end_frame):
        steps = 50
        for step in range(steps + 1):
            t = step / steps
            intensity = 50 + random.uniform(-5, 5) * math.sin(t * 10)
            color = (1.0, 0.5 + random.uniform(-0.1, 0.1) * math.sin(t * 10), 0.3)
            frame = start_frame + (step * (end_frame - start_frame) // steps)
            light.data.energy = intensity
            light.data.keyframe_insert(data_path="energy", frame=frame)
            light.data.color = color
            light.data.keyframe_insert(data_path="color", frame=frame)

    def apply_random_flicker(self, light, start_frame, end_frame, intensity_range):
        random.seed(42)
        for frame in range(start_frame, end_frame + 1, 2):
            energy = random.uniform(*intensity_range)
            light.data.energy = energy
            light.data.keyframe_insert(data_path="energy", frame=frame)

    def apply_lightning_effect(self, light, start_frame, end_frame):
        for frame in range(start_frame, end_frame, random.randint(3, 10)):
            light.data.energy = random.uniform(500, 1000)
            light.data.keyframe_insert(data_path="energy", frame=frame)
            light.data.energy = random.uniform(50, 100)
            light.data.keyframe_insert(data_path="energy", frame=frame + 2)

    def apply_sweep_motion(self, light, start_frame, end_frame, axis='X'):
        steps = 50
        base_loc = light.location.copy()
        duration = end_frame - start_frame
        
        for step in range(steps + 1):
            t = step / steps
            offset = 5 * math.sin(2 * math.pi * t)
            frame = start_frame + int(t * duration)
            
            new_loc = base_loc.copy()
            if axis == 'X': new_loc.x += offset
            elif axis == 'Y': new_loc.y += offset
            elif axis == 'Z': new_loc.z += offset
            
            light.location = new_loc
            light.keyframe_insert(data_path="location", frame=frame)

    def apply_spotlight_beam(self, light, start_frame, end_frame):
        if light.data.type != 'SPOT':
            return
        
        steps = 30
        for step in range(steps + 1):
            t = step / steps
            cone_size = 15 + 10 * math.sin(2 * math.pi * t)
            frame = start_frame + (step * (end_frame - start_frame) // steps)
            light.data.spot_size = math.radians(cone_size)
            light.data.keyframe_insert(data_path="spot_size", frame=frame)

    def apply_color_gradient(self, light, start_frame, end_frame, colors, steps):
        if len(colors) < 2: return
        
        for step in range(steps + 1):
            t = step / steps
            color_idx = int(t * (len(colors) - 1))
            next_idx = min(color_idx + 1, len(colors) - 1)
            factor = (t * (len(colors) - 1)) - color_idx
            
            c1 = colors[color_idx]
            c2 = colors[next_idx]
            
            r = (1 - factor) * c1[0] + factor * c2[0]
            g = (1 - factor) * c1[1] + factor * c2[1]
            b = (1 - factor) * c1[2] + factor * c2[2]

            frame = start_frame + (step * (end_frame - start_frame) // steps)
            light.data.color = (r, g, b)
            light.data.keyframe_insert(data_path="color", frame=frame)

    def apply_realtime_light_switch(self, context):
        props = context.scene.light_animation_props
        collection_name = props.collection_name
        speed = props.switch_speed

        collection = bpy.data.collections.get(collection_name)
        if not collection:
            return

        lights = [obj for obj in collection.objects if obj.type == 'LIGHT']
        if not lights:
            return

        lights.sort(key=lambda x: x.name)
        frame = context.scene.frame_start
        for i, light in enumerate(lights):
            light.data.energy = 0
            light.data.keyframe_insert(data_path="energy", frame=frame)
            frame += speed
            light.data.energy = 100
            light.data.keyframe_insert(data_path="energy", frame=frame)
            frame += speed
            light.data.energy = 0
            light.data.keyframe_insert(data_path="energy", frame=frame)

    def apply_spotlight_target(self, light, start_frame, end_frame, target):
        if not target: return
        # Simple tracking via constraint logic or manual rotation calculation could be added here
        pass

    def apply_range_animation(self, light, start_frame, end_frame):
        # Animate point light radius/shadow soft size
        pass

class OBJECT_OT_ApplyCameraAnimation(bpy.types.Operator):
    bl_idname = "scenecraft.apply_camera_animation"
    bl_label = "Apply Camera Animation"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.camera_animation_props
        camera = context.scene.camera 

        if not camera:
            self.report({'WARNING'}, "No active camera in the scene!")
            return {'CANCELLED'}

        start_frame, end_frame = props.start_frame, props.end_frame

        if props.camera_preset == 'DOLLY':
            self.apply_dolly_zoom(camera, start_frame, end_frame, props)
        elif props.camera_preset == 'ZOOM':
            self.apply_zoom(camera, start_frame, end_frame)
        elif props.camera_preset == 'PAN':
            self.apply_pan(camera, start_frame, end_frame, props)
        elif props.camera_preset == 'FOCUS':
            self.apply_rack_focus(camera, start_frame, end_frame, props)
        elif props.camera_preset == 'SHAKE':
            self.apply_camera_shake(camera, start_frame, end_frame, props)
        elif props.camera_preset == 'FLY_THROUGH':
            self.apply_fly_through(camera, start_frame, end_frame, props)
        elif props.camera_preset == 'SPIRAL':
            self.apply_spiral_motion(camera, start_frame, end_frame)
        elif props.camera_preset == 'ORBIT':
            self.apply_orbit(camera, start_frame, end_frame, props)
        elif props.camera_preset == 'MULTI_SWITCH':
            self.apply_multi_camera_switch(context, start_frame, end_frame)
        elif props.camera_preset == 'FAST_SLOW':
            self.apply_fast_slow_move(camera, start_frame, end_frame, props)
        elif props.camera_preset == 'HANDHELD':
            self.apply_handheld(camera, start_frame, end_frame, props)
        elif props.camera_preset == 'CRANE':
            self.apply_crane(camera, start_frame, end_frame, props)
        elif props.camera_preset == 'POV_WALK':
            self.apply_pov_walk(camera, start_frame, end_frame, props)
        elif props.camera_preset == 'FOCUS_BREATHING':
            self.apply_focus_breathing(camera, start_frame, end_frame, props)
        elif props.camera_preset == 'WHIP_PAN':
            self.apply_whip_pan(camera, start_frame, end_frame, props)

        self.report({'INFO'}, f"Applied {props.camera_preset} animation!")
        return {'FINISHED'}

    def apply_dolly_zoom(self, camera, start_frame, end_frame, props):
        # Move forward/backward based on distance
        distance = getattr(props, "stopping_distance", 5.0)
        
        camera.keyframe_insert(data_path="location", index=2, frame=start_frame)
        
        # Simple linear move
        camera.location.z -= distance
        camera.keyframe_insert(data_path="location", index=2, frame=end_frame)

    def apply_zoom(self, camera, start_frame, end_frame):
        camera.data.lens = 20
        camera.data.keyframe_insert(data_path="lens", frame=start_frame)
        camera.data.lens = 85
        camera.data.keyframe_insert(data_path="lens", frame=end_frame)

    def apply_pan(self, camera, start_frame, end_frame, props):
        target = props.target_object
        if not target: return

        for frame in range(start_frame, end_frame + 1):
            camera.location = target.location
            camera.rotation_euler.z += 0.1
            camera.keyframe_insert(data_path="rotation_euler", index=2, frame=frame)

    def apply_rack_focus(self, camera, start_frame, end_frame, props):
        camera.data.dof.use_dof = True
        camera.data.dof.focus_distance = 1.0
        camera.data.keyframe_insert(data_path="dof.focus_distance", frame=start_frame)
        camera.data.dof.focus_distance = 10.0
        camera.data.keyframe_insert(data_path="dof.focus_distance", frame=end_frame)

    def apply_camera_shake(self, camera, start_frame, end_frame, props):
        for frame in range(start_frame, end_frame):
            camera.location.x += random.uniform(-0.1, 0.1)
            camera.location.y += random.uniform(-0.1, 0.1)
            camera.location.z += random.uniform(-0.1, 0.1)
            camera.keyframe_insert(data_path="location", frame=frame)

    def apply_fly_through(self, camera, start_frame, end_frame, props):
        steps = 100
        for i in range(steps):
            t = i / steps
            camera.location.x = 10 * t
            camera.location.y = 10 * math.sin(t * 2 * math.pi)
            camera.location.z = 5
            frame = start_frame + i * (end_frame - start_frame) // steps
            camera.keyframe_insert(data_path="location", frame=frame)

    def apply_spiral_motion(self, camera, start_frame, end_frame):
        steps = 36
        for i in range(steps):
            angle = i * (2 * math.pi / steps)
            x = 10 * math.cos(angle)
            y = 10 * math.sin(angle)
            z = 5 + i * 0.2
            frame = start_frame + i * (end_frame - start_frame) // steps
            camera.location = (x, y, z)
            camera.keyframe_insert(data_path="location", frame=frame)

    def apply_orbit(self, camera, start_frame, end_frame, props):
        target = props.target_object
        if not target: return

        steps = 36
        radius = 10
        for i in range(steps):
            angle = i * (2 * math.pi / steps)
            x = target.location.x + radius * math.cos(angle)
            y = target.location.y + radius * math.sin(angle)
            z = target.location.z
            frame = start_frame + i * (end_frame - start_frame) // steps
            camera.location = (x, y, z)
            camera.keyframe_insert(data_path="location", frame=frame)

    def apply_multi_camera_switch(self, context, start_frame, end_frame):
        cameras = [obj for obj in context.scene.objects if obj.type == 'CAMERA']
        if not cameras: return
        
        steps = len(cameras)
        step_frames = (end_frame - start_frame) // steps

        for i, cam in enumerate(cameras):
            frame = start_frame + i * step_frames
            context.scene.camera = cam
            context.scene.keyframe_insert(data_path="camera", frame=frame)

    def apply_fast_slow_move(self, camera, start_frame, end_frame, props):
        """Moves camera fast for 80% of frames, then slows down near target."""
        
        target = props.target_object
        stop_dist = getattr(props, "stopping_distance", 2.0)
        
        # Calculate Start Position
        start_pos = camera.location.copy()
        
        # Calculate Final Position
        if target:
            cam_to_target = target.location - start_pos
            distance_to_target = cam_to_target.length
            
            # Move to exactly stopping_distance away from target
            if distance_to_target > stop_dist:
                move_amount = distance_to_target - stop_dist
                direction = cam_to_target.normalized()
                final_pos = start_pos + (direction * move_amount)
            else:
                self.report({'WARNING'}, "Camera is already closer than stopping distance!")
                return
        else:
            # Fallback: Move 10 units forward if no target
            final_pos = camera.matrix_world @ Vector((0.0, 0.0, -10.0))

        # Calculate Intermediate Position (90% of travel distance)
        # This creates the "Fast" section (0% to 90% distance)
        vec_total = final_pos - start_pos
        split_pos = start_pos + (vec_total * 0.9)

        # Calculate Intermediate Frame (80% of time)
        total_frames = end_frame - start_frame
        split_frame = int(start_frame + (total_frames * 0.8))

        # Insert Keyframes
        
        # 1. Start Frame
        camera.location = start_pos
        camera.keyframe_insert(data_path="location", frame=start_frame)
        
        # 2. Split Frame (80% time, 90% distance)
        camera.location = split_pos
        camera.keyframe_insert(data_path="location", frame=split_frame)
        
        # 3. End Frame (100% time, 100% distance)
        camera.location = final_pos
        camera.keyframe_insert(data_path="location", frame=end_frame)
        
        # Apply Interpolation
        if camera.animation_data and camera.animation_data.action:
            action = camera.animation_data.action
            if hasattr(action, "fcurves"):
                for fcurve in action.fcurves:
                    if fcurve.data_path == "location":
                        for kp in fcurve.keyframe_points:
                            # Start -> Split: Linear (Fast, constant speed)
                            if int(kp.co.x) == start_frame:
                                kp.interpolation = 'LINEAR'
                            
                            # Split -> End: Bezier (Ease Out/Slow Down)
                            if int(kp.co.x) == split_frame:
                                kp.interpolation = 'BEZIER'
                                kp.easing = 'EASE_OUT'

    def apply_handheld(self, camera, start_frame, end_frame, props):
        """Applies realistic handheld camera shake using Perlin noise."""
        scale = getattr(props, "handheld_scale", 0.5)
        amp = getattr(props, "handheld_amp", 0.2)
        
        # Use delta transforms to layer on top of existing animation
        for frame in range(start_frame, end_frame + 1):
            # Generate smooth noise based on frame number
            time = frame * scale * 0.1
            
            # Location noise (XYZ)
            dx = noise.noise(Vector((time, 0, 0))) * amp
            dy = noise.noise(Vector((0, time, 0))) * amp
            dz = noise.noise(Vector((0, 0, time))) * amp
            
            # Rotation noise (Euler XYZ) - reduced amplitude
            rx = noise.noise(Vector((time + 100, 0, 0))) * amp * 0.1
            ry = noise.noise(Vector((0, time + 100, 0))) * amp * 0.1
            rz = noise.noise(Vector((0, 0, time + 100))) * amp * 0.1
            
            camera.delta_location = (dx, dy, dz)
            camera.delta_rotation_euler = (rx, ry, rz)
            
            camera.keyframe_insert(data_path="delta_location", frame=frame)
            camera.keyframe_insert(data_path="delta_rotation_euler", frame=frame)

    def apply_crane(self, camera, start_frame, end_frame, props):
        """Simulates a crane/jib shot moving vertically."""
        lift = getattr(props, "crane_height", 5.0)
        target = props.target_object
        
        # Start Position (Low)
        camera.keyframe_insert(data_path="location", frame=start_frame)
        
        # End Position (High)
        camera.location.z += lift
        camera.keyframe_insert(data_path="location", frame=end_frame)
        
        # Optional: Add Track To constraint
        if target:
            constraint = None
            for const in camera.constraints:
                if const.type == 'TRACK_TO' and const.target == target:
                    constraint = const
                    break
            
            if not constraint:
                constraint = camera.constraints.new(type='TRACK_TO')
                constraint.target = target
                constraint.track_axis = 'TRACK_NEGATIVE_Z'
                constraint.up_axis = 'UP_Y'
            
            constraint.influence = 1.0

    def apply_pov_walk(self, camera, start_frame, end_frame, props):
        """Simulates a POV walk cycle with head bobbing."""
        speed = getattr(props, "walk_speed", 10.0)
        intensity = getattr(props, "walk_intensity", 0.1)
        target = props.target_object
        stop_dist = getattr(props, "stopping_distance", 2.0)
        
        # Calculate Start and End Positions (similar to fast_slow logic)
        start_pos = camera.location.copy()
        final_pos = start_pos
        
        if target:
            cam_to_target = target.location - start_pos
            dist = cam_to_target.length
            if dist > stop_dist:
                move_amount = dist - stop_dist
                direction = cam_to_target.normalized()
                final_pos = start_pos + (direction * move_amount)
        else:
            # Move forward 10m if no target
            final_pos = camera.matrix_world @ Vector((0.0, 0.0, -10.0))

        # Animate frame by frame
        total_frames = end_frame - start_frame
        for i in range(total_frames + 1):
            frame = start_frame + i
            t = i / total_frames
            
            # Linear interpolation for base movement
            base_loc = start_pos.lerp(final_pos, t)
            
            # Add Head Bob (Sine wave on Z)
            bob_z = math.sin(frame * speed * 0.05) * intensity
            
            # Add Side Sway (Cosine wave on X, usually half frequency of Z)
            sway_x = math.cos(frame * speed * 0.025) * (intensity * 0.5)
            
            # Calculate local right vector for sway
            if target:
                forward = (target.location - base_loc).normalized()
                right = forward.cross(Vector((0,0,1)))
            else:
                # Approximate from matrix
                right = camera.matrix_world.to_3x3() @ Vector((1,0,0))
                
            final_loc = base_loc + Vector((0,0,bob_z)) + (right * sway_x)
            
            camera.location = final_loc
            camera.keyframe_insert(data_path="location", frame=frame)

    def apply_focus_breathing(self, camera, start_frame, end_frame, props):
        """Simulates rack focus with subtle lens breathing (zoom)."""
        start_dist = getattr(props, "focus_distance_start", 1.0)
        end_dist = getattr(props, "focus_distance_end", 10.0)
        breath_amt = getattr(props, "breathing_intensity", 2.0)
        
        # Ensure DOF is enabled
        camera.data.dof.use_dof = True
        
        # Initial Lens value
        base_focal_length = camera.data.lens
        
        # Keyframe Start
        camera.data.dof.focus_distance = start_dist
        camera.data.dof.keyframe_insert(data_path="focus_distance", frame=start_frame)
        
        camera.data.lens = base_focal_length
        camera.data.keyframe_insert(data_path="lens", frame=start_frame)
        
        # Keyframe End
        camera.data.dof.focus_distance = end_dist
        camera.data.dof.keyframe_insert(data_path="focus_distance", frame=end_frame)
        
        # Breathing: Focal length changes slightly when focusing closer/further
        direction = 1 if end_dist < start_dist else -1
        new_focal_length = base_focal_length + (breath_amt * direction)
        
        camera.data.lens = new_focal_length
        camera.data.keyframe_insert(data_path="lens", frame=end_frame)

    def apply_whip_pan(self, camera, start_frame, end_frame, props):
        """Creates a fast, blurred rotation transition (Whip Pan)."""
        target = props.target_object
        angle = getattr(props, "whip_pan_angle", 90.0)
        
        # Enable Motion Blur for the scene
        bpy.context.scene.render.use_motion_blur = True
        bpy.context.scene.render.motion_blur_shutter = 0.8  # Higher shutter for more blur trail
        
        # Keyframe Start Rotation
        camera.keyframe_insert(data_path="rotation_euler", frame=start_frame)
        
        # Calculate End Rotation
        if target:
            # Calculate rotation to look at target
            direction = target.location - camera.location
            rot_quat = direction.to_track_quat('-Z', 'Y')
            target_euler = rot_quat.to_euler()
            camera.rotation_euler = target_euler
        else:
            # Rotate Z axis by specific angle
            camera.rotation_euler.z += math.radians(angle)
            
        # Keyframe End Rotation
        camera.keyframe_insert(data_path="rotation_euler", frame=end_frame)
        
        # Apply Exponential Ease In/Out for the "Whip" feel (Slow start -> SUPER FAST -> Slow end)
        if camera.animation_data and camera.animation_data.action:
            action = camera.animation_data.action
            if hasattr(action, "fcurves"):
                for fcurve in action.fcurves:
                    if fcurve.data_path == "rotation_euler":
                        for kp in fcurve.keyframe_points:
                            if int(kp.co.x) == start_frame:
                                kp.interpolation = 'EXPO'
                                kp.easing = 'EASE_IN_OUT'