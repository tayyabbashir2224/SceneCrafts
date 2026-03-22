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
import os

bl_info = {
    "name": "SceneCraft",
    "author": "Tayyab Bashir",
    "version": (1, 1, 0),
    "blender": (5, 0, 0),
    "location": "3D View > Sidebar > SceneCraft",
    "description": "A range of parameters to tweak curve motion, geometry transformations, and material effects for maximum control.",
    "doc_url": "https://www.youtube.com/playlist?list=PLOZNUDZBdw_oQA2OP1hh3wl7x79AM-FNZ",
    "category": "Animation",
}

# ------------------------------------------------------------------------
# IMPORTS
# ------------------------------------------------------------------------
from .properties import (
    CameraAnimationProperties, LightAnimationProperties, SimpleOperatorProperties,
    Rotate_In_WallsOperatorProperties, Pop_In_WallsOperatorProperties,
    Fall_Down_TilesOperatorProperties, Pop_In_FloorsOperatorProperties,
    CurveOperatorProperties, CustomProperties, UniformObjectsAnimtionProperties,
    RandomObjectsAnimtionProperties, PresetAnimationProperties,
    AnimationLayer, AnimationLayerProperties,
)

from .panels.object_transforms_panel import ObjectTransformsPanel
from .panels.multi_object_transforms_panel import MultiObjectTransformsPanel
from .panels.wall_transforms_panel import WallTransformsPanel
from .panels.floor_transforms_panel import FloorTransformsPanel
from .panels.curve_transforms_panel import CurveTransformsPanel
from .panels.reverse_animation_panel import ReverseAnimationPanel
from .panels.preset_animations_panel import PresetAnimationsPanel
from .panels.animation_layers_panel import AnimationLayersPanel
from .panels.camera_light_panel import CameraLightAnimationsPanel 

from .operators.object_operators import object_operators_classes
from .operators.wall_operators import wall_operators_classes
from .operators.floor_operators import floor_operators_classes
from .operators.curve_operators import curve_operators_classes

from .operators.camera_light_animations import OBJECT_OT_ApplyCameraAnimation, OBJECT_OT_ApplyLightAnimation 
from .operators.reverse_animations import OBJECT_OT_ReverseAnimation
from .operators.preset_animations import OBJECT_OT_ApplyPresetAnimation
from .operators.animation_layers import (
    OBJECT_OT_AddAnimationLayer, 
    OBJECT_OT_DeleteAnimationLayer,
    OBJECT_OT_BakeAnimationLayers as OBJECT_OT_BakeAnimationLayers_Final 
)

# ------------------------------------------------------------------------
# REGISTRATION LISTS
# ------------------------------------------------------------------------
all_classes = (
    # Properties
    CustomProperties,
    SimpleOperatorProperties,
    Rotate_In_WallsOperatorProperties,
    Pop_In_WallsOperatorProperties,
    Fall_Down_TilesOperatorProperties,
    Pop_In_FloorsOperatorProperties,
    CurveOperatorProperties,
    UniformObjectsAnimtionProperties,
    RandomObjectsAnimtionProperties,
    PresetAnimationProperties,
    AnimationLayer,
    AnimationLayerProperties,
    CameraAnimationProperties,
    LightAnimationProperties,

    # Panels
    ObjectTransformsPanel,
    MultiObjectTransformsPanel,
    WallTransformsPanel,
    FloorTransformsPanel,
    CurveTransformsPanel,
    ReverseAnimationPanel,
    PresetAnimationsPanel,
    AnimationLayersPanel,
    CameraLightAnimationsPanel,

    # Individual Operators
    OBJECT_OT_ApplyCameraAnimation,
    OBJECT_OT_ApplyLightAnimation,
    OBJECT_OT_ReverseAnimation,
    OBJECT_OT_ApplyPresetAnimation,
    OBJECT_OT_AddAnimationLayer,
    OBJECT_OT_DeleteAnimationLayer,
    OBJECT_OT_BakeAnimationLayers_Final,
)

CLASSES_TO_REGISTER = all_classes + \
    object_operators_classes + \
    wall_operators_classes + \
    floor_operators_classes + \
    curve_operators_classes

# ------------------------------------------------------------------------
# REGISTER / UNREGISTER
# ------------------------------------------------------------------------

def register():
    # 1. Register Classes
    for cls in CLASSES_TO_REGISTER:
        bpy.utils.register_class(cls)

    # 2. Register Scene Properties
    bpy.types.Scene.custom_props = bpy.props.PointerProperty(type=CustomProperties)
    bpy.types.Scene.simple_operator_props = bpy.props.PointerProperty(type=SimpleOperatorProperties)
    bpy.types.Scene.preset_animation_props = bpy.props.PointerProperty(type=PresetAnimationProperties)    
    bpy.types.Scene.camera_animation_props = bpy.props.PointerProperty(type=CameraAnimationProperties)
    bpy.types.Scene.light_animation_props = bpy.props.PointerProperty(type=LightAnimationProperties)
    bpy.types.Scene.animation_layer_collection = bpy.props.CollectionProperty(type=AnimationLayer)
    bpy.types.Scene.animation_layer_props = bpy.props.PointerProperty(type=AnimationLayerProperties)
    
    bpy.types.Scene.rotate_in_walls = bpy.props.PointerProperty(type=Rotate_In_WallsOperatorProperties)
    bpy.types.Scene.pop_in_walls = bpy.props.PointerProperty(type=Pop_In_WallsOperatorProperties) 
    bpy.types.Scene.fall_down_tiles = bpy.props.PointerProperty(type=Fall_Down_TilesOperatorProperties)    
    bpy.types.Scene.pop_in_floors = bpy.props.PointerProperty(type=Pop_In_FloorsOperatorProperties)
    bpy.types.Scene.curve_operator_props = bpy.props.PointerProperty(type=CurveOperatorProperties)
    bpy.types.Scene.uniform_objects_animation_props = bpy.props.PointerProperty(type=UniformObjectsAnimtionProperties) 
    bpy.types.Scene.random_objects_animation_props = bpy.props.PointerProperty(type=RandomObjectsAnimtionProperties)
    
    # Direct Scene Properties
    bpy.types.Scene.bend_walls_direction = bpy.props.EnumProperty(
        name="Direction",
        items=[('OUTWARDS', 'Outwards', 'Bend Outwards'), ('INWARDS', 'Inwards', 'Bend Inwards')],
        default='OUTWARDS'
    )
    bpy.types.Scene.bend_walls_direction_xyz = bpy.props.EnumProperty(
        name="Direction XYZ",
        items=[('X/Y', 'X/Y', 'Bend in X or Y direction'),
               ('-X/Y', '-X/Y', 'Bend in -X or -Y direction'),
               ('Z', 'Z', 'Bend in Z direction'),
               ('-Z', '-Z', 'Bend in -Z direction')],
        default='X/Y'
    )
    bpy.types.Scene.bend_walls_start_frame = bpy.props.IntProperty(name="Start Frame", default=1, min=1)
    bpy.types.Scene.bend_walls_end_frame = bpy.props.IntProperty(name="End Frame", default=30, min=1)
    bpy.types.Scene.roll_walls_start_frame = bpy.props.IntProperty(default=1)
    bpy.types.Scene.roll_walls_end_frame = bpy.props.IntProperty(default=30)   
    bpy.types.Scene.roll_walls_direction_xyz = bpy.props.EnumProperty(
        name="Direction XYZ",
        items=[('X/Y', 'X/Y', 'Roll in X or Y direction'),
               ('-X/Y', '-X/Y', 'Roll in -X or -Y direction'),
               ('Z', 'Z', 'Roll in Z direction'),
               ('-Z', '-Z', 'Roll -Z direction')],
        default='X/Y'
    ) 
    bpy.types.Scene.wipe_walls_direction_xyz = bpy.props.EnumProperty(
        name="Direction XYZ",
        items=[('X/Y', 'X/Y', 'Wipe in X or Y direction'),
               ('-X/Y', '-X/Y', 'Wipe in -X or -Y direction'),
               ('Z', 'Z', 'Wipe in Z direction'),
               ('-Z', '-Z', 'Wipe in -Z direction')],
        default='X/Y'
    )  
    bpy.types.Scene.wipe_walls_start_frame = bpy.props.IntProperty(default=1)
    bpy.types.Scene.wipe_walls_end_frame = bpy.props.IntProperty(default=30) 
    bpy.types.Scene.rotate_w_direction_xyz = bpy.props.EnumProperty(
        name="Direction XYZ",
        items=[('X/Y', 'X/Y', 'pop in X/Y direction'),
               ('-X/Y', '-X/Y', 'pop in -X/Y direction'),
               ('Z', 'Z', 'pop in Z direction'),
               ('-Z', '-Z', 'pop in -Z direction'),],
        default='X/Y'
    ) 
    bpy.types.Scene.rotate_w_start_frame = bpy.props.IntProperty(name="Start Frame", default=1, min=1)
    bpy.types.Scene.rotate_w_end_frame = bpy.props.IntProperty(name="End Frame", default=50, min=1)
    bpy.types.Scene.pop_w_direction_xyz = bpy.props.EnumProperty(
        name="Direction XYZ",
        items=[('X/Y', 'X/Y', 'pop in X/Y direction'),
               ('-X/Y', '-X/Y', 'pop in -X/Y direction'),
               ('Z', 'Z', 'pop in Z direction'),
               ('-Z', '-Z', 'pop in -Z direction'),],
        default='X/Y'
    )    
    bpy.types.Scene.pop_w_start_frame = bpy.props.IntProperty(name="Start Frame", default=1, min=1)
    bpy.types.Scene.pop_w_end_frame = bpy.props.IntProperty(name="End Frame", default=40, min=1)
    bpy.types.Scene.bend_direction = bpy.props.EnumProperty(
        name="Direction",
        items=[('OUTWARDS', 'Outwards', 'Bend Outwards'), ('INWARDS', 'Inwards', 'Bend Inwards')],
        default='OUTWARDS'
    )    
    bpy.types.Scene.bend_direction_xyz = bpy.props.EnumProperty(
        name="Direction XYZ",
        items=[('X', 'X', 'Bend in X direction'),
               ('Y', 'Y', 'Bend in Y direction'),
               ('-X', '-X', 'Bend in -X direction'),
               ('-Y', '-Y', 'Bend in -Y direction'),],
        default='X'
    )
    bpy.types.Scene.bend_start_frame = bpy.props.IntProperty(name="Start Frame", default=1, min=1)
    bpy.types.Scene.bend_end_frame = bpy.props.IntProperty(name="End Frame", default=30, min=1)   
    bpy.types.Scene.roll_start_frame = bpy.props.IntProperty(default=1)
    bpy.types.Scene.roll_end_frame = bpy.props.IntProperty(default=30)    
    bpy.types.Scene.roll_direction_xyz = bpy.props.EnumProperty(
        name="Direction XYZ",
        items=[('X', 'X', 'Roll in X direction'),
               ('Y', 'Y', 'Roll in Y direction'),
               ('-X', '-X', 'Roll in -X direction'),
               ('-Y', '-Y', 'Roll -Y direction')],
        default='X'
    )  
    bpy.types.Scene.wipe_direction_xyz = bpy.props.EnumProperty(
        name="Direction XYZ",
        items=[('X', 'X', 'Wipe in X direction'),
               ('Y', 'Y', 'Wipe in Y direction'),
               ('-X', '-X', 'Wipe in -X direction'),
               ('-Y', '-Y', 'Wipe in -Y direction'),],
        default='X'
    )    
    bpy.types.Scene.wipe_start_frame = bpy.props.IntProperty(default=1)
    bpy.types.Scene.wipe_end_frame = bpy.props.IntProperty(default=20)    
    bpy.types.Scene.fade_start_frame = bpy.props.IntProperty(name="Start Frame", default=1, min=1)
    bpy.types.Scene.fade_end_frame = bpy.props.IntProperty(name="End Frame", default=40, min=1)
    bpy.types.Scene.pop_direction_xyz = bpy.props.EnumProperty(
        name="Direction XYZ",
        items=[('X', 'X', 'pop in X direction'),
               ('Y', 'Y', 'pop in Y direction'),
               ('-X', '-X', 'pop in -X direction'),
               ('-Y', '-Y', 'pop in -Y direction'),],
        default='X'
    )   
    bpy.types.Scene.pop_start_frame = bpy.props.IntProperty(name="Start Frame", default=1, min=1)
    bpy.types.Scene.pop_end_frame = bpy.props.IntProperty(name="End Frame", default=50, min=1)
    bpy.types.Scene.pivot_frame = bpy.props.IntProperty(name="Pivot Frame", default=100)
    bpy.types.Scene.uni_animation_start_frame = bpy.props.IntProperty(name="Start Frame", default=1, min=1)
    bpy.types.Scene.uni_animation_end_frame = bpy.props.IntProperty(name="End Frame", default=30, min=1)
    bpy.types.Scene.random_animation_start_frame = bpy.props.IntProperty(name="Start Frame", default=1, min=1)
    bpy.types.Scene.random_animation_end_frame = bpy.props.IntProperty(name="End Frame", default=30, min=1)

def unregister():
    # 1. Delete Scene Properties
    del bpy.types.Scene.random_animation_end_frame
    del bpy.types.Scene.random_animation_start_frame
    del bpy.types.Scene.uni_animation_end_frame
    del bpy.types.Scene.uni_animation_start_frame
    del bpy.types.Scene.pivot_frame
    del bpy.types.Scene.pop_end_frame
    del bpy.types.Scene.pop_start_frame
    del bpy.types.Scene.pop_direction_xyz
    del bpy.types.Scene.fade_end_frame
    del bpy.types.Scene.fade_start_frame
    del bpy.types.Scene.wipe_end_frame
    del bpy.types.Scene.wipe_start_frame
    del bpy.types.Scene.wipe_direction_xyz
    del bpy.types.Scene.roll_direction_xyz
    del bpy.types.Scene.roll_end_frame
    del bpy.types.Scene.roll_start_frame
    del bpy.types.Scene.bend_end_frame
    del bpy.types.Scene.bend_start_frame
    del bpy.types.Scene.bend_direction_xyz
    del bpy.types.Scene.bend_direction
    del bpy.types.Scene.pop_w_end_frame
    del bpy.types.Scene.pop_w_start_frame
    del bpy.types.Scene.pop_w_direction_xyz
    del bpy.types.Scene.rotate_w_end_frame
    del bpy.types.Scene.rotate_w_start_frame
    del bpy.types.Scene.rotate_w_direction_xyz
    del bpy.types.Scene.wipe_walls_end_frame
    del bpy.types.Scene.wipe_walls_start_frame
    del bpy.types.Scene.wipe_walls_direction_xyz
    del bpy.types.Scene.roll_walls_end_frame
    del bpy.types.Scene.roll_walls_start_frame
    del bpy.types.Scene.roll_walls_direction_xyz
    del bpy.types.Scene.bend_walls_end_frame
    del bpy.types.Scene.bend_walls_start_frame
    del bpy.types.Scene.bend_walls_direction_xyz
    del bpy.types.Scene.bend_walls_direction

    # 2. Delete Pointers
    del bpy.types.Scene.random_objects_animation_props
    del bpy.types.Scene.uniform_objects_animation_props
    del bpy.types.Scene.curve_operator_props
    del bpy.types.Scene.pop_in_floors
    del bpy.types.Scene.fall_down_tiles
    del bpy.types.Scene.pop_in_walls
    del bpy.types.Scene.rotate_in_walls
    del bpy.types.Scene.animation_layer_props
    del bpy.types.Scene.animation_layer_collection
    del bpy.types.Scene.light_animation_props
    del bpy.types.Scene.camera_animation_props
    del bpy.types.Scene.preset_animation_props
    del bpy.types.Scene.simple_operator_props
    del bpy.types.Scene.custom_props
    
    # 3. Unregister Classes
    for cls in reversed(CLASSES_TO_REGISTER):
        try:
            bpy.utils.unregister_class(cls)
        except RuntimeError:
            pass

if __name__ == "__main__":
    register()