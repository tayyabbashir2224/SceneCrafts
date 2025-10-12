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
from .panels.object_transforms_panel import ObjectTransformsPanel
from .panels.multi_object_transforms_panel import MultiObjectTransformsPanel
from .panels.wall_transforms_panel import WallTransformsPanel
from .panels.floor_transforms_panel import FloorTransformsPanel
from .panels.curve_transforms_panel import CurveTransformsPanel
from .panels.reverse_animation_panel import ReverseAnimationPanel
from .panels.preset_animations_panel import PresetAnimationsPanel
panels_classes = (
    ObjectTransformsPanel,
    MultiObjectTransformsPanel,
    WallTransformsPanel,
    FloorTransformsPanel,
    CurveTransformsPanel,
    ReverseAnimationPanel,
    PresetAnimationsPanel,
)

def register_panels():
    for cls in panels_classes:
        bpy.utils.register_class(cls)

def unregister_panels():
    for cls in panels_classes:
        bpy.utils.unregister_class(cls)
