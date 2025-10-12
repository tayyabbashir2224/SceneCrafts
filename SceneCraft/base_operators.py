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
from bpy.props import IntProperty, FloatProperty

class BaseOperator(bpy.types.Operator):
    bl_options = {'REGISTER', 'UNDO'}
    bl_label = "Base Operator"  # Add this to avoid the error


    def invoke(self, context, event):
        # Default invoke behavior
        return self.execute(context)

class BaseObjectOperator(BaseOperator):
    """Base class for object-related operators"""
    def validate_selection(self, context):
        # Ensure an object is selected
        if not context.object:
            self.report({'WARNING'}, "No object selected!")
            return False
        return True

class BaseWallOperator(BaseOperator):
    """Base class for wall-related operators"""
    def validate_wall_selection(self, context):
        # Example validation for wall-related operations
        if not context.selected_objects:
            self.report({'WARNING'}, "No wall objects selected!")
            return False
        return True

class BaseFloorOperator(BaseOperator):
    """Base class for floor-related operators"""
    def validate_floor_selection(self, context):
        if not context.selected_objects:
            self.report({'WARNING'}, "No floor objects selected!")
            return False
        return True

    def invoke(self, context, event):
        # Call execute() by default when invoked
        return self.execute(context)


class BaseCurveOperator(BaseOperator):
    """Base class for curve-related operators"""
    def validate_curve(self, context):
        # Ensure a curve object is selected
        if not context.object or context.object.type != 'CURVE':
            self.report({'WARNING'}, "No curve object selected!")
            return False
        return True

def set_keyframe(obj, data_path, frame, value):
    """Helper function to insert a keyframe"""
    obj.keyframe_insert(data_path=data_path, frame=frame)
    obj.animation_data.action.fcurves[-1].keyframe_points[-1].co = (frame, value)

def reset_transforms(obj):
    """Helper function to reset object transforms"""
    obj.location = (0, 0, 0)
    obj.rotation_euler = (0, 0, 0)
    obj.scale = (1, 1, 1)

# Shared properties for operators
class BaseProperties:
    start_frame: IntProperty(
        name="Start Frame",
        description="Start frame of the animation",
        default=1,
        min=1,
    )
    end_frame: IntProperty(
        name="End Frame",
        description="End frame of the animation",
        default=30,
        min=1,
    )
    scale_factor: FloatProperty(
        name="Scale Factor",
        description="Scaling factor for the animation",
        default=1.0,
        min=0.1,
    )

# Registration functions
classes = [
    BaseObjectOperator,
    BaseWallOperator,
    BaseFloorOperator,
    BaseCurveOperator,
]

# DO NOT include these in the registration process
def register_base_operators():
    pass

def unregister_base_operators():
    pass
