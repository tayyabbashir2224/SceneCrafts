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
import random
import math

class OBJECT_OT_ApplyPresetAnimation(bpy.types.Operator):
    bl_idname = "object.apply_preset_animation"
    bl_label = "Apply Preset Animation"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        props = scene.preset_animation_props
        layer = scene.animation_layer_collection.add()
        layer.layer_name = "Preset Animation"
        layer.layer_animation_type = 'FADE'
        # Get selected preset and animation properties
        selected_preset = props.selected_preset
        target_type = props.target_type
        pattern_type = props.pattern_type
        start_frame = props.start_frame
        end_frame = props.end_frame
    #print(f"Preset: {selected_preset}, Start Frame: {start_frame}, End Frame: {end_frame}")
        # Get target objects based on user selection
        objects = self.get_target_objects(context, props.target_type, props.target_collection)
        if not objects:
            self.report({'WARNING'}, "No valid objects found!")
            return {'CANCELLED'}


        # Apply the selected preset
        if selected_preset == 'FADE':
            self.apply_fade(objects, start_frame, end_frame, pattern_type)
        elif selected_preset == 'WAVE':
            self.apply_wave(objects, start_frame, end_frame)
        elif selected_preset == 'SPIRAL':
            self.apply_spiral(objects, start_frame, end_frame)
        elif selected_preset == 'BOUNCE':
            self.apply_bounce(objects, start_frame, end_frame)
        elif selected_preset == 'CASCADE':
            self.apply_cascade(objects, start_frame, end_frame)
        elif selected_preset == 'PULSE':
            self.apply_pulse(objects, start_frame, end_frame)
        elif selected_preset == 'RANDOM':
            self.apply_random(objects, start_frame, end_frame)
        elif selected_preset == 'EXPAND':
            self.apply_expand_contract(objects, start_frame, end_frame, expand=True)

        # Confirm the animation has been applied
        self.report({'INFO'}, f"Applied {selected_preset} animation!")
        return {'FINISHED'}
    def get_target_objects(self, context, target_type, target_collection):
        """Fetch target objects based on the user's selection."""
        if target_type == 'SINGLE':
            return [context.object] if context.object else []
        elif target_type == 'MULTI':
            return context.selected_objects
        elif target_type == 'COLLECTION' and target_collection:
            return list(target_collection.objects)
        return []

    def apply_fade(self, objects, start_frame, end_frame, pattern_type):
    #print(f"Applying fade to {len(objects)} objects from frame {start_frame} to {end_frame}")
        """Apply fade-in/out animation to objects."""
        # Randomize order if pattern is RANDOM
        if pattern_type == 'RANDOM':
            random.shuffle(objects)

        frame_interval = (end_frame - start_frame) // len(objects) if len(objects) > 0 else 0
        for i, obj in enumerate(objects):
            obj_start = start_frame + (i * frame_interval)
            obj_end = obj_start + frame_interval

            # Ensure object has material with alpha support
            if not obj.data.materials:
                mat = bpy.data.materials.new(name="FadeMaterial")
                mat.use_nodes = True
                obj.data.materials.append(mat)
            mat = obj.data.materials[0]
            mat.use_nodes = True

            nodes = mat.node_tree.nodes
            links = mat.node_tree.links
            bsdf_node = nodes.get("Principled BSDF") or nodes.new("ShaderNodeBsdfPrincipled")
            output_node = nodes.get("Material Output") or nodes.new("ShaderNodeOutputMaterial")
            links.new(bsdf_node.outputs["BSDF"], output_node.inputs["Surface"])

            # Animate alpha
            bsdf_node.inputs["Alpha"].default_value = 0.0  # Transparent
            bsdf_node.inputs["Alpha"].keyframe_insert(data_path="default_value", frame=obj_start)
            bsdf_node.inputs["Alpha"].default_value = 1.0  # Opaque
            bsdf_node.inputs["Alpha"].keyframe_insert(data_path="default_value", frame=obj_end)








    def apply_wave(self, objects, start_frame, end_frame, wave_height=1.0):
        frame_interval = (end_frame - start_frame) // len(objects) if len(objects) > 0 else 1
        for i, obj in enumerate(objects):
            wave_frame = start_frame + (i * frame_interval)
        
            # Animate object position in wave
            obj.location.z += wave_height
            obj.keyframe_insert(data_path="location", index=2, frame=wave_frame)
            obj.location.z -= wave_height
            obj.keyframe_insert(data_path="location", index=2, frame=wave_frame + frame_interval)


    def apply_spiral(self, objects, start_frame, end_frame, radius=2.0, rotation_steps=5):
        frame_interval = (end_frame - start_frame) // len(objects) if len(objects) > 0 else 1
        for i, obj in enumerate(objects):
        # Calculate spiral position
            angle = (i / len(objects)) * (rotation_steps * 2 * math.pi)  # Convert steps to radians
            x = radius * (i / len(objects)) * math.cos(angle)
            y = radius * (i / len(objects)) * math.sin(angle)

        # Animate the object's location
            obj.location = (x, y, obj.location.z)
            obj.keyframe_insert(data_path="location", frame=start_frame + (i * frame_interval))


    def apply_bounce(self, objects, start_frame, end_frame, bounce_height=1.5):
        frame_interval = (end_frame - start_frame) // len(objects) if len(objects) > 0 else 1
        for i, obj in enumerate(objects):
            bounce_frame = start_frame + (i * frame_interval)
        
        # Animate bouncing
            obj.location.z += bounce_height
            obj.keyframe_insert(data_path="location", index=2, frame=bounce_frame)
            obj.location.z -= bounce_height
            obj.keyframe_insert(data_path="location", index=2, frame=bounce_frame + frame_interval)



    def apply_cascade(self, objects, start_frame, end_frame):
        frame_interval = (end_frame - start_frame) // len(objects) if len(objects) > 0 else 1
        for i, obj in enumerate(objects):
            obj_start = start_frame + (i * frame_interval)
            obj.location.x += 1.0  # Example: move along X-axis
            obj.keyframe_insert(data_path="location", index=0, frame=obj_start)


    def apply_pulse(self, objects, start_frame, end_frame, pulse_scale=1.5):
        frame_interval = (end_frame - start_frame) // len(objects) if len(objects) > 0 else 1
        for i, obj in enumerate(objects):
            pulse_frame = start_frame + (i * frame_interval)
        
        # Animate pulsing
            obj.scale = (pulse_scale, pulse_scale, pulse_scale)
            obj.keyframe_insert(data_path="scale", frame=pulse_frame)
            obj.scale = (1.0, 1.0, 1.0)
            obj.keyframe_insert(data_path="scale", frame=pulse_frame + frame_interval)



    def apply_random(self, objects, start_frame, end_frame):
        for obj in objects:
            random_offset = random.uniform(-1.0, 1.0)
        
        # Animate random movement
            obj.location.x += random_offset
            obj.keyframe_insert(data_path="location", index=0, frame=start_frame)
            obj.location.y += random_offset
            obj.keyframe_insert(data_path="location", index=1, frame=end_frame)

    def apply_expand_contract(self, objects, start_frame, end_frame, expand=True):
        factor = 1 if expand else -1
        for obj in objects:
            obj.location.x += factor * obj.location.x * 0.5
            obj.location.y += factor * obj.location.y * 0.5
            obj.location.z += factor * obj.location.z * 0.5
            obj.keyframe_insert(data_path="location", frame=start_frame)




