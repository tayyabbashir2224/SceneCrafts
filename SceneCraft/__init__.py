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

bl_info = {
    "name": "SceneCraft",
    "author": "Tayyab Bashir",
    "version": (1, 0, 0),
    "blender": (4, 0, 2),
    "location": "3D View > Sidebar > SceneCraft",
    "description": "A range of parameters to tweak curve motion, geometry transformations, and material effects for maximum control.",
    "doc_url": "https://www.youtube.com/playlist?list=PLOZNUDZBdw_oQA2OP1hh3wl7x79AM-FNZ",
    "category": "Animation",
}

import bpy
import os

addon_dirc = os.path.dirname(os.path.realpath(__file__))

from .properties import CameraAnimationProperties, LightAnimationProperties
from .operators.camera_light_animations import OBJECT_OT_ApplyCameraAnimation, OBJECT_OT_ApplyLightAnimation 
from .panels.camera_light_panel import CameraLightAnimationsPanel 

from .panels.object_transforms_panel import ObjectTransformsPanel
from .panels.multi_object_transforms_panel import MultiObjectTransformsPanel
from .panels.wall_transforms_panel import WallTransformsPanel
from .panels.floor_transforms_panel import FloorTransformsPanel
from .panels.curve_transforms_panel import CurveTransformsPanel
from .panels.reverse_animation_panel import ReverseAnimationPanel
from .panels.preset_animations_panel import PresetAnimationsPanel
from .panels.animation_layers_panel import AnimationLayersPanel

from .operators.reverse_animations import OBJECT_OT_ReverseAnimation
from .operators.preset_animations import OBJECT_OT_ApplyPresetAnimation
from .panels import register_panels, unregister_panels
from .operators.object_operators import *
from .operators.wall_operators import *
from .operators.floor_operators import *
from .operators.curve_operators import *
from .operators import register_operators, unregister_operators

from .properties import (
    SimpleOperatorProperties,
    Rotate_In_WallsOperatorProperties,
    Pop_In_WallsOperatorProperties,
    Fall_Down_TilesOperatorProperties,
    Pop_In_FloorsOperatorProperties,
    CurveOperatorProperties,
    CustomProperties,
    UniformObjectsAnimtionProperties,
    RandomObjectsAnimtionProperties,
    PresetAnimationProperties,
    AnimationLayer,
    AnimationLayerProperties,


)

from .base_operators import register_base_operators, unregister_base_operators
from .properties import register_properties, unregister_properties

classes = (
    ObjectTransformsPanel,
    MultiObjectTransformsPanel,
    WallTransformsPanel,
    FloorTransformsPanel,
    CurveTransformsPanel,
    ReverseAnimationPanel,
    PresetAnimationsPanel,
    AnimationLayersPanel,
 #   SimplePanel,
    CustomProperties,
    SimpleOperatorProperties,
    Rotate_In_WallsOperatorProperties,
    Pop_In_WallsOperatorProperties,
    Fall_Down_TilesOperatorProperties,
    Pop_In_FloorsOperatorProperties,
    CurveOperatorProperties,
    UniformObjectsAnimtionProperties,
    RandomObjectsAnimtionProperties,
    *object_operators_classes,
    *wall_operators_classes,
    *floor_operators_classes,
    *curve_operators_classes,
    
)

def register_properties():
    print("Registering AnimationLayerProperties...")
    try:
        bpy.utils.unregister_class(PresetAnimationProperties)  # Avoid duplicate registration
        bpy.utils.unregister_class(AnimationLayerProperties)
        bpy.utils.unregister_class(AnimationLayer)
        
    except RuntimeError:
        print("AnimationLayerProperties not previously registered.")
    bpy.utils.register_class(PresetAnimationProperties)
    bpy.utils.register_class(AnimationLayer)  # Register individual layer
    bpy.utils.register_class(AnimationLayerProperties)  # Register the main property group    
    bpy.types.Scene.preset_animation_props = bpy.props.PointerProperty(type=PresetAnimationProperties)
    bpy.types.Scene.animation_layer_props = bpy.props.PointerProperty(type=AnimationLayerProperties)
    bpy.types.Scene.animation_layer_collection = bpy.props.CollectionProperty(type=AnimationLayer)

    # Add a collection for animation layers to the Scene type
    bpy.types.Scene.my_addon_animation_layer_collection = bpy.props.CollectionProperty(type=AnimationLayer)




def unregister_properties():

    
    del bpy.types.Scene.preset_animation_props
    bpy.utils.unregister_class(PresetAnimationProperties)
    del bpy.types.Scene.animation_layer_props
    bpy.utils.unregister_class(AnimationLayerProperties)
    del bpy.types.Scene.my_addon_animation_layer_collection
    del bpy.types.Scene.animation_layer_props

    bpy.utils.unregister_class(AnimationLayer)
    # Remove properties from Scene
    del bpy.types.Scene.animation_layer_collection

    # Unregister classes
    bpy.utils.unregister_class(AnimationLayer)
    
def register():
 
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.custom_props = bpy.props.PointerProperty(type=CustomProperties)
    bpy.types.Scene.simple_operator_props = bpy.props.PointerProperty(type=SimpleOperatorProperties)
    bpy.utils.register_class(PresetAnimationProperties)
    bpy.types.Scene.preset_animation_props = bpy.props.PointerProperty(type=PresetAnimationProperties)    
    
                        #camera/light
    bpy.utils.register_class(CameraAnimationProperties)
    bpy.utils.register_class(LightAnimationProperties)
    bpy.types.Scene.camera_animation_props = bpy.props.PointerProperty(type=CameraAnimationProperties)
    bpy.types.Scene.light_animation_props = bpy.props.PointerProperty(type=LightAnimationProperties)

    bpy.utils.register_class(OBJECT_OT_ApplyCameraAnimation)
    bpy.utils.register_class(OBJECT_OT_ApplyLightAnimation)
    bpy.utils.register_class(CameraLightAnimationsPanel)   



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
    bpy.types.Scene.rotate_in_walls = bpy.props.PointerProperty(type=Rotate_In_WallsOperatorProperties)
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
    bpy.types.Scene.pop_in_walls = bpy.props.PointerProperty(type=Pop_In_WallsOperatorProperties) 
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
    bpy.types.Scene.fall_down_tiles = bpy.props.PointerProperty(type=Fall_Down_TilesOperatorProperties)    
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
    bpy.types.Scene.pop_in_floors = bpy.props.PointerProperty(type=Pop_In_FloorsOperatorProperties)
    bpy.types.Scene.pop_start_frame = bpy.props.IntProperty(name="Start Frame", default=1, min=1)
    bpy.types.Scene.pop_end_frame = bpy.props.IntProperty(name="End Frame", default=50, min=1)
    
    
    
    bpy.types.Scene.curve_operator_props = bpy.props.PointerProperty(type=CurveOperatorProperties)
    
    bpy.types.Scene.pivot_frame = bpy.props.IntProperty(name="Pivot Frame", default=100)
    
    
    
    bpy.types.Scene.uniform_objects_animation_props = bpy.props.PointerProperty(type=UniformObjectsAnimtionProperties) 
    bpy.types.Scene.uni_animation_start_frame = bpy.props.IntProperty(name="Start Frame", default=1, min=1)
    bpy.types.Scene.uni_animation_end_frame = bpy.props.IntProperty(name="End Frame", default=30, min=1)

    bpy.types.Scene.random_objects_animation_props = bpy.props.PointerProperty(type=RandomObjectsAnimtionProperties)
    bpy.types.Scene.random_animation_start_frame = bpy.props.IntProperty(name="Start Frame", default=1, min=1)
    bpy.types.Scene.random_animation_end_frame = bpy.props.IntProperty(name="End Frame", default=30, min=1)
    #bpy.utils.register_class(SCENE_OT_AddGradientColor)
    #bpy.utils.register_class(SCENE_OT_RemoveGradientColor)


    register_properties()  # Step 1: Register properties
    register_operators()   # Step 2: Register operators
    register_panels()      # Step 3: Register panels 
    

def unregister():
   
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.custom_props
    del bpy.types.Scene.simple_operator_props
    del bpy.types.Scene.preset_animation_props
    bpy.utils.unregister_class(PresetAnimationProperties)    

                #camera/light
    del bpy.types.Scene.camera_animation_props
    del bpy.types.Scene.light_animation_props

    bpy.utils.unregister_class(CameraAnimationProperties)
    bpy.utils.unregister_class(LightAnimationProperties)
    bpy.utils.unregister_class(OBJECT_OT_ApplyCameraAnimation)
    bpy.utils.unregister_class(OBJECT_OT_ApplyLightAnimation)
    bpy.utils.unregister_class(CameraLightAnimationsPanel)
    
    
    
    del bpy.types.Scene.bend_walls_start_frame
    del bpy.types.Scene.bend_walls_end_frame  
    del bpy.types.Scene.bend_walls_direction 
    del bpy.types.Scene.bend_walls_direction_xyz 

    del bpy.types.Scene.roll_walls_start_frame
    del bpy.types.Scene.roll_walls_end_frame
    del bpy.types.Scene.roll_walls_direction_xyz   

    del bpy.types.Scene.wipe_walls_direction   
    del bpy.types.Scene.wipe_walls_start_frame
    del bpy.types.Scene.wipe_walls_end_frame    
    del bpy.types.Scene.rotate_w_direction_xyz   

    del bpy.types.Scene.rotate_in_walls    
    del bpy.types.Scene.rotate_w_start_frame
    del bpy.types.Scene.rotate_w_end_frame   
    del bpy.types.Scene.pop_w_direction_xyz    

    del bpy.types.Scene.pop_in_walls    
    del bpy.types.Scene.pop_w_start_frame
    del bpy.types.Scene.pop_w_end_frame 
    
    del bpy.types.Scene.rotate_in_walls    
    del bpy.types.Scene.rotate_w_start_frame
    del bpy.types.Scene.rotate_w_end_frame   
    del bpy.types.Scene.pop_w_direction_xyz 
    
    del bpy.types.Scene.pop_in_walls    
    del bpy.types.Scene.pop_w_start_frame
    del bpy.types.Scene.pop_w_end_frame
    
    
    
    del bpy.types.Scene.bend_start_frame
    del bpy.types.Scene.bend_end_frame    
    del bpy.types.Scene.bend_direction    
    del bpy.types.Scene.bend_direction_xyz  
    
    del bpy.types.Scene.roll_start_frame
    del bpy.types.Scene.roll_end_frame
    del bpy.types.Scene.roll_direction_xyz  
    
    del bpy.types.Scene.wipe_direction    
    del bpy.types.Scene.wipe_start_frame
    del bpy.types.Scene.wipe_wipe_end_frame 
    
    del bpy.types.Scene.fall_down_tiles    
    del bpy.types.Scene.fade_start_frame
    del bpy.types.Scene.fade_end_frame    
    del bpy.types.Scene.pop_direction_xyz 
    
    del bpy.types.Scene.pop_in_floors    
    del bpy.types.Scene.pop_start_frame
    del bpy.types.Scene.pop_end_frame
    
    
    
    del bpy.types.Scene.curve_operator_props
    
    del bpy.types.Scene.pivot_frame
    
    

    del bpy.types.Scene.uniform_objects_animation_props
    del bpy.types.Scene.uni_animation_start_frame
    del bpy.types.Scene.uni_animation_end_frame
    
    

    del bpy.types.Scene.random_objects_animation_props
    del bpy.types.Scene.random_animation_start_frame
    del bpy.types.Scene.random_animation_end_frame

    #bpy.utils.unregister_class(SCENE_OT_AddGradientColor)
    #bpy.utils.unregister_class(SCENE_OT_RemoveGradientColor)
    unregister_panels()    # Step 1: Unregister panels
    unregister_operators() # Step 2: Unregister operators
    unregister_properties() # Step 3: Unregister properties
if __name__ == "__main__":
    register()
