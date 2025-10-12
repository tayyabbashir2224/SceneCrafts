# SceneCrafts
**SceneCraft Blender Addon**

**Version:** 1.0.0 
**Author:** [MTayyab]  

---

## **Introduction:**  
SceneCraft is a Blender addon designed to simplify the animation process by providing intuitive tools for animating objects, cameras, and lights directly from the viewport. With a focus on automation and ease of use, SceneCraft accelerates workflow for artists, designers, and animators by allowing them to quickly animate scene elements with minimal effort.

SceneCraft is ideal for construction phasing animations, architectural visualizations, object motion, camera movements, and light path animations. Future updates will include enhanced rigging automation and more animation presets.

---

## **Key Features and Usage Guide:**

### 1. **SceneCraft Panel Integration**  
**Description:**  
The SceneCraft panel provides a centralized interface in Blender's 3D Viewport to control object, light, and camera animations with a simple button click.
First thing you need to do is prepare your scene:

-Subdivide any object that will be or curved or bent or twisted.

-join the parts that will be animated together as a single object.

-separate the objects that would be animated individually.

-For floor tiles, separate them, and then put them in a collection together and make sure each of the tiles has an individual origin

-Then select your object and choose a preset and your animation is ready.  

**Usage:**  
1. Open Blender and switch to the 3D Viewport.
2. Press **N** to open the sidebar.
3. Locate the **SceneCraft** tab in the sidebar.
4. Use the provided buttons to animate objects, lights, and cameras in different directions instantly.  

---

### 2. **Object Animation Controls (Directional Animation Buttons)**  
**Description:**  
Animate objects by simply clicking directional buttons. SceneCraft automatically applies transformations and keyframes without requiring manual adjustment of location, rotation, or scale.

**Usage:**  
1. Select an object in the viewport.
2. In the SceneCraft panel, choose the direction you want the object to animate (e.g., forward, backward, left, right, up, down).
3. Click the button corresponding to the desired direction.
4. The object will automatically animate in the chosen direction, with keyframes inserted automatically.

---

### 3. **Path Following (Animate Along Path)**  
**Description:**  
SceneCraft can make objects, lights, and cameras follow predefined paths by automating path constraints and applying keyframes. This feature simplifies moving scene elements along curves, making it ideal for vehicle animations, camera movement, or object pathing.

**Usage:**  
1. Select the object, light, or camera you want to animate.
2. Shift-select a curve or path.
3. In the SceneCraft panel, click **Animate Along Path**.
4. The selected item will automatically follow the chosen curve over time.

*Note: Ensure you select a curve before executing this function.*

---

### 4. **Light and Camera Animation**  
**Description:**  
SceneCraft enables easy animation of lights and cameras to enhance scene dynamics. Lights can be animated for dynamic effects, while cameras can be moved for cinematic shots.

**Usage:**  
1. Select a light or camera in the viewport.
2. In the SceneCraft panel, click the desired directional button (pan, tilt, zoom, etc.).
3. The light or camera will automatically animate in the specified direction with keyframes applied.  

---

### 5. **Automatic Keyframe Insertion**  
**Description:**  
Automate keyframe insertion by simply clicking directional animation buttons. SceneCraft handles keyframes and movement in one step.

**Usage:**  
1. Select the object, light, or camera you want to animate.
2. Click the directional animation button in the SceneCraft panel.
3. The item will animate with keyframes automatically inserted.

---

### 6. **Basic Rigging (Work in Progress)**  
**Description:**  
Preliminary rigging functions are in development, providing the foundation for automatic rigging in future releases.

*Note: This feature is currently under development and may not function as expected.*

---

## **Known Issues and Development Roadmap:**
- **Automatic Rigging** is partially implemented and will be refined in future updates.
- **Path Animation** may encounter limitations when working with complex curves.
- Users may experience unexpected behavior when multiple objects are selected simultaneously.
- Light and camera animations may need further refinement for intricate control.

---

## **Feedback and Reporting Issues:**
We value your feedback! If you encounter issues or have suggestions for improvement, please report them through the Blender Console or reach out via the provided channels. Your input helps improve SceneCraft for future releases.

Thank you for using SceneCraft!

