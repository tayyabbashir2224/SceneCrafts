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

class OBJECT_OT_ReverseAnimation(bpy.types.Operator):
    bl_label = "Reverse Animation"
    bl_idname = "object.Reverse_Animation"
    bl_description = "Reverse keyframes Of Selected Objects to Animate Out"

    def execute(self, context):
        # Check if there are selected objects
        if not bpy.context.selected_objects:
            raise RuntimeError("No objects are selected. Please select an object and try again.")

        # Store the current frame
        current_frame = bpy.context.scene.frame_current

        # Define the pivot frame for mirroring
        pivot_frame = context.scene.pivot_frame

        # Iterate over all selected objects
        for selected_object in bpy.context.selected_objects:
            # Check if the object has animation data
            if selected_object.animation_data:
                # Store the action if it exists
                action = selected_object.animation_data.action

                # If the selected object doesn't have an action, skip to the next object
                if not action:
                    continue

                # Iterate over all fcurves in the action
                for fcurve in action.fcurves:
                    # Iterate over all keyframes in the fcurve
                    for keyframe in fcurve.keyframe_points:
                        # Duplicate the keyframe
                        new_keyframe = keyframe.co.copy()

                        # Mirror the frame position relative to the pivot frame
                        mirrored_frame = pivot_frame - (keyframe.co.x - pivot_frame)

                        # Adjust the frame position of the duplicated keyframe
                        new_keyframe.x = mirrored_frame

                        # Insert the duplicated and mirrored keyframe
                        fcurve.keyframe_points.insert(new_keyframe.x, new_keyframe.y)

        # Restore the frame
        bpy.context.scene.frame_set(current_frame)

        return {'FINISHED'}