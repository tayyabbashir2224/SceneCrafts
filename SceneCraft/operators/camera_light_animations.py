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

        # Match the preset and apply the corresponding effect
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
        elif props.light_preset == 'TRACK':
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
            self.apply_color_gradient(light, start_frame, end_frame, colors)
        elif props.light_preset == 'SWITCH':
            self.apply_realtime_light_switch(context)           
            
        self.report({'INFO'}, f"Applied {props.light_preset} animation!")
        return {'FINISHED'}

    def apply_flicker(self, light, start_frame, end_frame, flicker_speed):
        for frame in range(start_frame, end_frame, int(flicker_speed * 10)):
            light.data.energy = 0 if light.data.energy > 0 else 100
            light.data.keyframe_insert(data_path="energy", frame=frame)

    def apply_dynamic_intensity(self, light, start_frame, end_frame):
        """Animate intensity smoothly using sine wave oscillations."""
        steps = 30  # Number of steps for smooth transitions
        for step in range(steps + 1):
            t = step / steps
            intensity = 100 + 50 * math.sin(2 * math.pi * t)  # Sine wave oscillation

            # Calculate frame
            frame = start_frame + (step * (end_frame - start_frame) // steps)
            light.data.energy = intensity
            light.data.keyframe_insert(data_path="energy", frame=frame)

    def apply_light_movement(self, light, start_frame, end_frame, props):
        movement_type = props.movement_path_type
        z_oscillation = props.z_oscillation
        radius = 5.0
        steps = 36

        if movement_type == 'CIRCULAR':
            self.circular_path(light, start_frame, end_frame, radius, steps, z_oscillation)
        elif movement_type == 'SPIRAL':
            self.spiral_path(light, start_frame, end_frame, radius, steps, z_oscillation)
        elif movement_type == 'LINEAR':
            self.linear_path(light, start_frame, end_frame)

    def circular_path(self, light, start_frame, end_frame, radius, steps, z_oscillation):
        for step in range(steps + 1):
            angle = step * (2 * math.pi / steps)
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            z = light.location.z + (math.sin(angle) * 2.0 if z_oscillation else 0)
            frame = start_frame + (step * (end_frame - start_frame) // steps)
            light.location = (x, y, z)
            light.keyframe_insert(data_path="location", frame=frame)

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
        """Animate light with random flickering effect."""
        random.seed(42)  # Ensure reproducibility
        for frame in range(start_frame, end_frame + 1, 2):  # Flicker every 2 frames
            energy = random.uniform(*intensity_range)  # Random intensity
            light.data.energy = energy
            light.data.keyframe_insert(data_path="energy", frame=frame)

    def apply_lightning_effect(self, light, start_frame, end_frame):
        """Simulate sudden bursts of light like lightning strikes."""
        import random
        for frame in range(start_frame, end_frame, random.randint(3, 10)):  # Random intervals
            light.data.energy = random.uniform(500, 1000)  # Bright flashes
            light.data.keyframe_insert(data_path="energy", frame=frame)

            # Return to dimmed light after flash
            light.data.energy = random.uniform(50, 100)
            light.data.keyframe_insert(data_path="energy", frame=frame + 2)

    def apply_sweep_motion(self, light, start_frame, end_frame, axis='X'):
        """Animate light sweeping motion along an axis."""
        steps = 50
        for step in range(steps + 1):
            t = step / steps
            offset = 5 * math.sin(2 * math.pi * t)  # Oscillating motion

            frame = start_frame + (step * (end_frame - start_frame) // steps)
            if axis == 'X':
                light.location.x += offset
            elif axis == 'Y':
                light.location.y += offset
            elif axis == 'Z':
                light.location.z += offset
            
            light.keyframe_insert(data_path="location", frame=frame)

    def apply_spotlight_beam(self, light, start_frame, end_frame):
        """Animate spotlight beam size dynamically."""
        # Check if the light is a SpotLight
        if light.data.type != 'SPOT':
            self.report({'WARNING'}, "Spotlight beam effect can only be applied to SpotLights!")
            return
        
        steps = 30
        for step in range(steps + 1):
            t = step / steps
            cone_size = 15 + 10 * math.sin(2 * math.pi * t)  # Oscillate cone angle
            
            frame = start_frame + (step * (end_frame - start_frame) // steps)
            light.data.spot_size = math.radians(cone_size)  # Apply beam size
            light.data.keyframe_insert(data_path="spot_size", frame=frame)


    def apply_color_gradient(self, light, start_frame, end_frame, colors):
        """Animate light color transitions based on gradient steps."""
        steps = props.gradient_steps  # Number of steps
        for step in range(steps + 1):
            t = step / steps
            
            # Blend between colors dynamically
            r = (1 - t) * colors[0] + t * 1.0
            g = (1 - t) * colors[1] + t * 0.0
            b = (1 - t) * colors[2] + t * 1.0

            # Set keyframes for colors
            frame = start_frame + (step * (end_frame - start_frame) // steps)
            light.data.color = (r, g, b)
            light.data.keyframe_insert(data_path="color", frame=frame)
    def apply_realtime_light_switch(self, context):
        props = context.scene.light_animation_props
        collection_name = props.collection_name
        speed = props.switch_speed

        # Get the selected collection
        collection = bpy.data.collections.get(collection_name)
        if not collection:
            self.report({'WARNING'}, "No collection selected or found!")
            return

        # Get lights in the collection
        lights = [obj for obj in collection.objects if obj.type == 'LIGHT']
        if not lights:
            self.report({'WARNING'}, "No lights found in the selected collection!")
            return

        # Sort lights by name (e.g., Light01, Light02)
        lights.sort(key=lambda x: x.name)

        # Keyframe the lights to switch on/off in sequence
        frame = context.scene.frame_start
        for i, light in enumerate(lights):
            # Turn off initially
            light.data.energy = 0
            light.data.keyframe_insert(data_path="energy", frame=frame)

            # Turn on light
            frame += speed
            light.data.energy = 100
            light.data.keyframe_insert(data_path="energy", frame=frame)

            # Turn off light again
            frame += speed
            light.data.energy = 0
            light.data.keyframe_insert(data_path="energy", frame=frame)

        self.report({'INFO'}, "Realtime Light Switching Applied!")

class SCENE_OT_AddGradientColor(bpy.types.Operator):
    bl_idname = "scene.add_gradient_color"
    bl_label = "Add Gradient Color"
    
    def execute(self, context):
        props = context.scene.light_animation_props
        color = props.gradient_colors.add()
        color.color = (1.0, 1.0, 1.0)  # Default white color
        return {'FINISHED'}

class SCENE_OT_RemoveGradientColor(bpy.types.Operator):
    bl_idname = "scene.remove_gradient_color"
    bl_label = "Remove Gradient Color"
    
    def execute(self, context):
        props = context.scene.light_animation_props
        if len(props.gradient_colors) > 0:
            props.gradient_colors.remove(len(props.gradient_colors) - 1)
        return {'FINISHED'}



class OBJECT_OT_ApplyCameraAnimation(bpy.types.Operator):
    bl_idname = "scenecraft.apply_camera_animation"
    bl_label = "Apply Camera Animation"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.camera_animation_props
        camera = context.scene.camera  # Active camera in the scene

        if not camera:
            self.report({'WARNING'}, "No active camera in the scene!")
            return {'CANCELLED'}

        start_frame, end_frame = props.start_frame, props.end_frame

        if props.camera_preset == 'DOLLY':
            self.apply_dolly_zoom(camera, start_frame, end_frame)

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

        elif props.camera_preset == 'DOLLY_ZOOM':
            self.apply_dolly_zoom_effect(camera, start_frame, end_frame)

        elif props.camera_preset == 'MULTI_SWITCH':
            self.apply_multi_camera_switch(context, start_frame, end_frame)

        self.report({'INFO'}, f"Applied {props.camera_preset} animation!")
        return {'FINISHED'}

    def apply_dolly_zoom(self, camera, start_frame, end_frame):
        """Dolly zoom (Vertigo effect)."""
        camera.location.z += 5
        camera.keyframe_insert(data_path="location", index=2, frame=start_frame)
        camera.data.lens = 20
        camera.data.keyframe_insert(data_path="lens", frame=start_frame)

        camera.location.z -= 5
        camera.keyframe_insert(data_path="location", index=2, frame=end_frame)
        camera.data.lens = 85
        camera.data.keyframe_insert(data_path="lens", frame=end_frame)

    def apply_zoom(self, camera, start_frame, end_frame):
        """Simple zoom in/out effect."""
        camera.data.lens = 20
        camera.data.keyframe_insert(data_path="lens", frame=start_frame)
        camera.data.lens = 85
        camera.data.keyframe_insert(data_path="lens", frame=end_frame)

    def apply_pan(self, camera, start_frame, end_frame, props):
        """Pan camera around a target."""
        target = props.target_object
        if not target:
            self.report({'WARNING'}, "No target selected for panning!")
            return

        for frame in range(start_frame, end_frame + 1):
            camera.location = target.location
            camera.rotation_euler.z += 0.1  # Rotate around Z-axis
            camera.keyframe_insert(data_path="rotation_euler", index=2, frame=frame)

    def apply_rack_focus(self, camera, start_frame, end_frame, props):
        """Rack focus effect."""
        camera.data.dof.use_dof = True
        camera.data.dof.focus_distance = 1.0
        camera.data.keyframe_insert(data_path="dof.focus_distance", frame=start_frame)
        camera.data.dof.focus_distance = 10.0
        camera.data.keyframe_insert(data_path="dof.focus_distance", frame=end_frame)

    def apply_camera_shake(self, camera, start_frame, end_frame, props):
        """Add camera shake effect."""
        for frame in range(start_frame, end_frame):
            x_offset = random.uniform(-0.1, 0.1)
            y_offset = random.uniform(-0.1, 0.1)
            z_offset = random.uniform(-0.1, 0.1)

            camera.location.x += x_offset
            camera.location.y += y_offset
            camera.location.z += z_offset
            camera.keyframe_insert(data_path="location", frame=frame)

    def apply_fly_through(self, camera, start_frame, end_frame, props):
        """Fly-through effect."""
        steps = 100
        for i in range(steps):
            t = i / steps
            camera.location.x = 10 * t
            camera.location.y = 10 * math.sin(t * 2 * math.pi)
            camera.location.z = 5
            frame = start_frame + i * (end_frame - start_frame) // steps
            camera.keyframe_insert(data_path="location", frame=frame)

    def apply_spiral_motion(self, camera, start_frame, end_frame):
        """Spiral motion around a target."""
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
        """Orbit around an object."""
        target = props.target_object
        if not target:
            self.report({'WARNING'}, "No target selected for orbit!")
            return

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
        """Switch between multiple cameras."""
        cameras = [obj for obj in context.scene.objects if obj.type == 'CAMERA']
        steps = len(cameras)
        step_frames = (end_frame - start_frame) // steps

        for i, cam in enumerate(cameras):
            frame = start_frame + i * step_frames
            context.scene.camera = cam
            context.scene.keyframe_insert(data_path="camera", frame=frame)


