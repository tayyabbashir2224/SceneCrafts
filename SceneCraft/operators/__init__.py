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
from .preset_animations import OBJECT_OT_ApplyPresetAnimation
from .animation_layers import OBJECT_OT_AddAnimationLayer, OBJECT_OT_BakeAnimationLayers, OBJECT_OT_DeleteAnimationLayer


operators_classes = (
    OBJECT_OT_ApplyPresetAnimation,
    OBJECT_OT_AddAnimationLayer,
    OBJECT_OT_BakeAnimationLayers,    
    OBJECT_OT_DeleteAnimationLayer,
)

def register_operators():
    for cls in operators_classes:
        try:
            bpy.utils.unregister_class(cls)  # Ensure no duplicates
        except RuntimeError:
            pass
        bpy.utils.register_class(cls)

def unregister_operators():
    for cls in operators_classes:
        bpy.utils.unregister_class(cls)