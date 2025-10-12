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







class CameraAnimationProperties(bpy.types.PropertyGroup):
    # Preset Dropdown
    camera_preset: bpy.props.EnumProperty(
        name="Camera Preset",
        items=[
            ('DOLLY', 'Dolly', 'Move the camera forward or backward'),
            ('ZOOM', 'Zoom', 'Change the camera focal length'),
            ('PAN', 'Pan/Orbit', 'Rotate the camera around a target'),
            ('FOCUS', 'Rack Focus', 'Change focus distance for depth of field'),
            ('SHAKE', 'Camera Shake', 'Simulate shaky camera movements'),
            ('FLY_THROUGH', 'Fly Through', 'Move the camera along a path'),
            ('SPIRAL', 'Spiral Motion', 'Animate the camera in a spiral path'),
            ('ORBIT', 'Orbit', 'Orbit around a selected object'),
            ('DOLLY_ZOOM', 'Dolly Zoom', 'Create a Vertigo effect'),
            ('MULTI_SWITCH', 'Multi-Camera Switch', 'Switch between multiple cameras'),
        ],
        default='DOLLY'
    )

    # Frame Range
    start_frame: bpy.props.IntProperty(
        name="Start Frame",
        default=1,
        min=1
    )
    end_frame: bpy.props.IntProperty(
        name="End Frame",
        default=50,
        min=1
    )

    # Target Object for tracking or orbiting
    target_object: bpy.props.PointerProperty(
        type=bpy.types.Object,
        name="Target Object",
        description="Object for camera to track or orbit around"
    )

    # Focus Distance for Rack Focus
    focus_distance_start: bpy.props.FloatProperty(
        name="Focus Start",
        default=1.0,
        min=0.1,
        description="Start focus distance for rack focus animation"
    )
    focus_distance_end: bpy.props.FloatProperty(
        name="Focus End",
        default=10.0,
        min=0.1,
        description="End focus distance for rack focus animation"
    )

    # Shake Intensity
    shake_intensity: bpy.props.FloatProperty(
        name="Shake Intensity",
        default=0.1,
        min=0.01,
        description="Amount of shake applied to the camera"
    )

    # Spiral Motion Settings
    spiral_radius: bpy.props.FloatProperty(
        name="Spiral Radius",
        default=10.0,
        min=0.1,
        description="Radius for spiral motion animation"
    )
    spiral_height: bpy.props.FloatProperty(
        name="Spiral Height",
        default=5.0,
        min=0.1,
        description="Height increment for spiral motion"
    )

    # Orbit Settings
    orbit_radius: bpy.props.FloatProperty(
        name="Orbit Radius",
        default=10.0,
        min=1.0,
        description="Distance for orbit motion"
    )
    orbit_speed: bpy.props.FloatProperty(
        name="Orbit Speed",
        default=1.0,
        min=0.1,
        description="Speed for orbit rotation"
    )

    # Multi-Camera Switch Settings
    switch_interval: bpy.props.IntProperty(
        name="Switch Interval",
        default=10,
        min=1,
        description="Frame interval to switch between cameras"
    )




class LightAnimationProperties(bpy.types.PropertyGroup):
    light_preset: bpy.props.EnumProperty(
        name="Preset",
        items=[
            ('FLICKER', "Flicker", "Flickering Light"),
            ('INTENSITY', "Dynamic Intensity", "Intensity Animation"),
            ('MOVEMENT', "Movement", "Light Movement"),
            ('COLOR', "Color Animation", "Dynamic Color Changes"),
            ('PULSE', "Pulse", "Pulsating Light"),
            ('TRACK_TARGET', "Track Target", "Follow a Target Object"),
            ('RANDOM_FLICKER', "Random Flicker", "Chaotic Flickering"),
            ('FIRELIGHT', "Firelight", "Firelight Oscillation"),
            ('STROBE', "Strobe", "Strobe Light Effect"),
            ('LIGHTNING', "Lightning Effect", ""),
            ('SWEEP', "Sweep Motion", ""),
            ('SPOTLIGHT_BEAM', "Spotlight Beam", ""),
            ('COLOR_GRADIENT', "Color Gradient", ""),            
        ],
        default='FLICKER'
    )
    gradient_colors: bpy.props.CollectionProperty(
        type=bpy.types.PropertyGroup,
        name="Gradient Colors",
        description="Gradient color transitions"
    )

    gradient_steps: bpy.props.IntProperty(
        name="Gradient Steps",
        default=10,
        min=2,
        description="Number of steps for gradient transitions"
    )
    movement_path_type: bpy.props.EnumProperty(
        name="Path Type",
        items=[
            ('CIRCULAR', 'Circular', 'Move in a circular pattern'),
            ('SPIRAL', 'Spiral', 'Move in an expanding or contracting spiral'),
            ('LINEAR', 'Linear', 'Move in a straight line'),
            ('CUSTOM', 'Custom Path', 'Follow a user-defined path'),
        ],
        default='CIRCULAR'
    )
    z_oscillation: bpy.props.BoolProperty(name="Z Oscillation", default=False)
    enable_flicker: bpy.props.BoolProperty(name="Enable Flicker", default=False)
    start_frame: bpy.props.IntProperty(name="Start Frame", default=1, min=1)
    end_frame: bpy.props.IntProperty(name="End Frame", default=50, min=1)
    target_object: bpy.props.PointerProperty(type=bpy.types.Object, name="Target Object")

    # Add flicker_speed property
    flicker_speed: bpy.props.FloatProperty(
        name="Flicker Speed",
        description="Speed of the flickering effect",
        default=1.0,  # Set a suitable default value
        min=0.1,      # Minimum value
        max=10.0      # Maximum value
    )
    pulse_speed: bpy.props.FloatProperty(
        name="Pulse Speed",
        default=1.0,
        min=0.1
    )

    strobe_speed: bpy.props.IntProperty(
        name="Strobe Speed",
        default=5,
        min=1
    )

    intensity_range: bpy.props.FloatVectorProperty(
        name="Intensity Range",
        size=2,
        default=(50.0, 200.0)
    )

    target_object: bpy.props.PointerProperty(
        name="Target Object",
        type=bpy.types.Object
    )


class AnimationLayer(bpy.types.PropertyGroup):
    layer_name: bpy.props.StringProperty(name="Layer Name", default="New Layer")
    layer_opacity: bpy.props.FloatProperty(name="Opacity", default=1.0, min=0.0, max=1.0)
    layer_animation_type: bpy.props.EnumProperty(
        name="Animation Type",
        items=[
            ('FADE', 'Fade', 'Fade In/Out Animation'),
            ('SCALE', 'Scale', 'Scale In/Out Animation'),
            ('CURVE', 'Curve Motion', 'Motion along a curve')
        ],
        default='FADE'
    )
    start_frame: bpy.props.IntProperty(name="Start Frame", default=1, min=1)
    end_frame: bpy.props.IntProperty(name="End Frame", default=20, min=1)


class AnimationLayerProperties(bpy.types.PropertyGroup):
    active_layer_index: bpy.props.IntProperty(
        name="Active Layer Index",
        default=0,
        min=0,
        description="Index of the currently active animation layer"
    )


class PresetAnimationProperties(bpy.types.PropertyGroup):
    selected_preset: bpy.props.EnumProperty(
    name="Preset",
    items=[
        ('FADE', 'Fade In/Out', 'Apply a fading animation'),
        ('WAVE', 'Wave', 'Wave-like animation'),
        ('SPIRAL', 'Spiral', 'Spiral motion animation'),
        ('BOUNCE', 'Bounce', 'Bouncing animation'),
        ('CASCADE', 'Cascade', 'Sequential animation like a waterfall'),
        ('PULSE', 'Pulse', 'Scaling up and down rhythmically'),
        ('RANDOM', 'Random', 'Randomized motion or scaling'),
        ('EXPAND', 'Expand/Contract', 'Expand or contract objects')
    ],
    default='FADE'
    )
    target_type: bpy.props.EnumProperty(
        name="Target Type",
        description="Choose to apply animation to single object, multiple objects, or collection",
        items=[
            ('SINGLE', 'Single Object', 'Apply animation to a single object'),
            ('MULTI', 'Multiple Objects', 'Apply animation to multiple selected objects'),
            ('COLLECTION', 'Collection', 'Apply animation to objects in a collection'),
        ],
        default='SINGLE'
    )
    target_collection: bpy.props.PointerProperty(
        name="Target Collection",
        description="Collection to apply animation to",
        type=bpy.types.Collection
    )
    pattern_type: bpy.props.EnumProperty(
        name="Pattern Type",
        description="Choose the fade pattern: random or sequential",
        items=[
            ('RANDOM', 'Random', 'Apply animation in a random order'),
            ('SEQUENTIAL', 'Sequential', 'Apply animation in a sequential order'),
        ],
        default='SEQUENTIAL'
    )
    start_frame: bpy.props.IntProperty(
        name="Start Frame",
        description="Start frame for the animation",
        default=1,
        min=1
    )
    end_frame: bpy.props.IntProperty(
        name="End Frame",
        description="End frame for the animation",
        default=20,
        min=1
    )


class SimpleOperatorProperties(bpy.types.PropertyGroup):

    start_frame: bpy.props.IntProperty(
        name="Start Frame",
        description="Reversing the frame range will animate out instead of in.",
        default=1,
        min=1,
    )
    
    end_frame: bpy.props.IntProperty(
        name="End Frame",
        description="Reversing the frame range will animate out instead of in.",
        default=30,
        min=1,
    )
    show_transform: bpy.props.BoolProperty(
        name="Show Transform",
        default=False,
    )    
    show_scale: bpy.props.BoolProperty(
        name="Scale In/Out:",
        default=False,
    )
    show_fall: bpy.props.BoolProperty(
        name="Fall Down",
        default=False,
    )
    show_spiral: bpy.props.BoolProperty(
        name="Spiral In/Out",
        default=False,
    )
    show_rotate: bpy.props.BoolProperty(
        name="Rotate In/Out",
        default=False,
    )
    show_popup: bpy.props.BoolProperty(
        name="Pop Up",
        default=False,
    )
    show_wallbend: bpy.props.BoolProperty(
        name="Bend Walls In/Out",
        default=False,
    )
    show_wallroll: bpy.props.BoolProperty(
        name="Roll Walls In/Out",
        default=False,
    )
    show_wallwipe: bpy.props.BoolProperty(
        name="Wipe Walls In/Out",
        default=False,
    )
    show_wallpop: bpy.props.BoolProperty(
        name="Pop In Wall Tiles",
        default=False,
    )
    show_wallrotate: bpy.props.BoolProperty(
        name="Rotate In Wall Tiles",
        default=False,
    )
    show_tilepopfloor: bpy.props.BoolProperty(
        name="Floor Tiles Pop In",
        default=False,
    )
    show_tilefallfloor: bpy.props.BoolProperty(
        name="Floor Tiles Fall Down",
        default=False,
    )
    show_wipefloor: bpy.props.BoolProperty(
        name="Wipe Floors In/Out",
        default=False,
    )
    show_rollfloor: bpy.props.BoolProperty(
        name="Roll Floor In/Out",
        default=False,
    )
    show_bendfloor: bpy.props.BoolProperty(
        name="Bend Floor In/Out",
        default=False,
    )
    show_uniobj: bpy.props.BoolProperty(
        name="Uniform Objects Animation",
        default=False,
    )
    show_ranobj: bpy.props.BoolProperty(
        name="Random Objects Animation",
        default=False,
    )
    show_cam: bpy.props.BoolProperty(
        name="Camera Animation",
        default=False,
    )
    show_light: bpy.props.BoolProperty(
        name="Light Animation",
        default=False,
    )    
    spiral_direction_items = [
        ('X', 'X', 'X Direction'),
        ('Y', 'Y', 'Y Direction'),
        ('Z', 'Z', 'Z Direction'),
    ]

    spiral_direction: bpy.props.StringProperty(
        items=spiral_direction_items,
        name="Spiral Direction",
        description="Choose the spiral direction",
        default='X'
    )
    
    distance_offset: bpy.props.FloatProperty(
        name="Distance & Diretion",
        description="The distance the object travels, and the direction - or +.",
        default=3.0,
    )
    
    object_min_scale_factor: bpy.props.FloatProperty(
        name="Min Scale",
        description="Scale factor for the object",
        default=0.5,
        min=0.1,
        max=1,
    )
    
    object_scale_factor: bpy.props.FloatProperty(
        name="Scale Factor",
        description="Scale factor for the object",
        default=1.2,
        min=0.1,
    )
    
    spiral_angle: bpy.props.FloatProperty(
    name="Spiral Angle",
    description="Rotation angle for the spiral",
    default=270.0,
    )
    
    rotate_angle: bpy.props.FloatProperty(
    name="Rotate Angle",
    description="Rotation angle",
    default=180.0,
    min=0.0,
    )
    
    
    origin_point_items = [
        ('BOTTOM', 'Bottom', 'Set origion point to bottom center'),
        ('TOP', 'Top', 'Set origion point to top center'),
    ]

    origin_point: bpy.props.EnumProperty(
        items=origin_point_items,
        name="Origin Point",
        description="Choose the origin point of the object",
        default='BOTTOM'
    )
    

    
    
    

class Rotate_In_WallsOperatorProperties(bpy.types.PropertyGroup):
    collection_name: bpy.props.StringProperty(
        name="Collection",
        description="Choose Collection",
    )
    
    
    empty_name: bpy.props.StringProperty(
        name="Empty",
    )
    

class Pop_In_WallsOperatorProperties(bpy.types.PropertyGroup):
    collection_name: bpy.props.StringProperty(
        name="Collection",
        description="Choose Collection",
    )
    
    
    empty_name: bpy.props.StringProperty(
        name="Empty",
    )
    

    
class Fall_Down_TilesOperatorProperties(bpy.types.PropertyGroup):
    collection_name: bpy.props.StringProperty(
        name="Collection",
        description="Choose Collection",
    )
    
    
    empty_name: bpy.props.StringProperty(
        name="Empty",
    )
    
    fade_in_value: bpy.props.FloatProperty(
        name="Fade In",
        default=2.0,
        min=-10000.0,
        max=10000.0,
        description="Animation input value for the geometry node",
    )
    



class Pop_In_FloorsOperatorProperties(bpy.types.PropertyGroup):
    collection_name: bpy.props.StringProperty(
        name="Collection",
        description="Choose Collection",
    )
    
    
    empty_name: bpy.props.StringProperty(
        name="Empty",
    )
    
    
    
    

class CurveOperatorProperties(bpy.types.PropertyGroup):
    direction_items = [
        ('X', 'X', 'X Direction'),
        ('-X', '-X', '-X Direction'),
        ('Y', 'Y', 'Y Direction'),
        ('-Y', '-Y', '-Y Direction'),
        ('Z', 'Z', 'Z Direction'),
        ('-Z', '-Z', '-Z Direction')
    ]

    direction: bpy.props.EnumProperty(
        items=direction_items,
        name="Direction",
        description="Choose the direction",
        default='X'
    )
    
    
    start_frame: bpy.props.IntProperty(
        name="Start Frame",
        description="Reversing the frame range will animate out instead of in",
        default=1,
        min=1,
    )
    
    end_frame: bpy.props.IntProperty(
        name="End Frame",
        description="Reversing the frame range will animate out instead of in",
        default=50,
        min=1,
    )
    
    
    curve_scale: bpy.props.FloatProperty(
        name="Curve Scale",
        description="Scale factor for the curve",
        default=1,
        min=0.1,  
    )
    
    


    
    
    


class CustomProperties(bpy.types.PropertyGroup):
    active_panel: bpy.props.EnumProperty(
        items=[
            ("Object_Transforms", "Object Transforms", "Show Object Transforms"),
            ("Multi_Object_Transforms", "Multi Object Transforms", "Show Multi Object Transforms"),
            ("Wall_Transforms", "Wall Transforms", "Show Wall Transforms"),
            ("Floor_Transforms", "Floor Transforms", "Show Floor Transforms"),
            ("Animate_Along_A_Curve", "Animate Along A Curve", "Show Animate Along A Curve"),
            ("Reverse_Animation", "Reverse Animation/Animate Out", "Show Reverse Animation"),
        ],
        default="Object_Transforms"
    )
    
    
    
    
    
    
class UniformObjectsAnimtionProperties(bpy.types.PropertyGroup):
    
    collection_name: bpy.props.StringProperty(
        name="Collection",
        description="Choose Collection",
    )
    
    animate_from_z: bpy.props.FloatProperty(
        name="Animate From Z",
        description="Set animation distance from Z direction",
        default=0.0,
    )
    
    animate_from_y: bpy.props.FloatProperty(
        name="Animate From Y",
        description="Set animation distance from Y direction",
        default=0.0,
    )
    
    animate_from_x: bpy.props.FloatProperty(
        name="Animate From X",
        description="Set animation distance from X direction",
        default=0.0,
    )
    
    
    rotation_x: bpy.props.FloatProperty(
        name="Rotation X",
        description="Set Rotation X",
        default=0.0,
        subtype='ANGLE',
    )
    
    rotation_y: bpy.props.FloatProperty(
        name="Rotation Y",
        description="Set Rotation Y",
        default=0.0,
        subtype='ANGLE',
    )
    
    rotation_z: bpy.props.FloatProperty(
        name="Rotation Z",
        description="Set Rotation Z",
        default=0.0,
        subtype='ANGLE',
    )
    
    
class RandomObjectsAnimtionProperties(bpy.types.PropertyGroup):
    
    collection_name: bpy.props.StringProperty(
        name="Collection",
        description="Choose Collection",
    )
    
    min_z_distance: bpy.props.FloatProperty(
        name="Min Z Distance",
        description="Minimum Z distance",
        default=0.0,
    )

    max_z_distance: bpy.props.FloatProperty(
        name="Max Z Distance",
        description="Maximum Z distance",
        default=0.0,
    )

    min_y_distance: bpy.props.FloatProperty(
        name="Min Y Distance",
        description="Minimum Y distance",
        default=0.0,
    )

    max_y_distance: bpy.props.FloatProperty(
        name="Max Y Distance",
        description="Maximum Y distance",
        default=0.0,
    )
    
    
    min_x_distance: bpy.props.FloatProperty(
        name="Min X Distance",
        description="Minimum X distance",
        default=0.0,
    )

    max_x_distance: bpy.props.FloatProperty(
        name="Max X Distance",
        description="Maximum X distance",
        default=0.0,
    )

    min_x_rotation: bpy.props.FloatProperty(
        name="Min X Rotation",
        description="Minimum X rotation",
        default=0.0,
        subtype='ANGLE',
    )

    max_x_rotation: bpy.props.FloatProperty(
        name="Max X Rotation",
        description="Maximum X rotation",
        default=0.0,
        subtype='ANGLE',
    )

    min_y_rotation: bpy.props.FloatProperty(
        name="Min Y Rotation",
        description="Minimum Y rotation",
        default=0.0,
        subtype='ANGLE',
    )

    max_y_rotation: bpy.props.FloatProperty(
        name="Max Y Rotation",
        description="Maximum Y rotation",
        default=0.0,
        subtype='ANGLE',
    )

    min_z_rotation: bpy.props.FloatProperty(
        name="Min Z Rotation",
        description="Minimum Z rotation",
        default=0.0,
        subtype='ANGLE',
    )

    max_z_rotation: bpy.props.FloatProperty(
        name="Max Z Rotation",
        description="Maximum Z rotation",
        default=0.0,
        subtype='ANGLE',
    )
    
    
    
def register_properties():



    bpy.utils.register_class(AnimationLayer)
    bpy.utils.register_class(AnimationLayerProperties)
    bpy.types.Scene.animation_layer_collection = bpy.props.CollectionProperty(type=AnimationLayer)
    bpy.types.Scene.animation_layer_props = bpy.props.PointerProperty(type=AnimationLayerProperties)

def unregister_properties():


    del bpy.types.Scene.animation_layer_collection
    del bpy.types.Scene.animation_layer_props
    bpy.utils.unregister_class(AnimationLayerProperties)
    bpy.utils.unregister_class(AnimationLayer)    

    
__all__ = [
    "register_properties",
    "unregister_properties",
    "AnimationLayer",
    "AnimationLayerProperties"
]
