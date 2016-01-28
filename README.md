# maya-python-imageCard
This is project is about building a workflow for creating 3D scenes from 2D images.
<img src="./img/pancake_daytime_output_083.jpg"/>

### Step 1. Photoshop
> When deciding how to paint the individual layers here, try and think of breaking down the objects in the image into pieces you might cut out of paper to build a 3D object.  I like to think of building a house out of playing cards.  The cartoon South Park is the best example of what we're going for here.

- Create an image in Photoshop with multiple layers.
- File -> Export -> Layers to files.
- Set Type to PNG-24.
- Make sure Trim Layers and Transparency are checked.

### Step 2. Maya - imageCard Importing
- Open up Maya to a blank scene.
- Load the python script [coffeeSetup.py][pySetup].
- Update the folder variable to point to your folder.

### Step 3. Maya - Scene Building
- Move each **imageCard** (2D plane) into the desired position.
- Be careful to avoid any tightly overlapping or intersecting planes whenever possible.  Although this can also produce interesting results...

### Step 4. Maya - Lighting
- Only add lights to the master/beauty render layer!
- Use whatever lights you desire, but simple spot, point and directional lights save tons of rendering time.

### Step 5. Maya - Rendering
- **Much more detail is required here**
- Use Software rendering for Z-Depth pass

### Step 6. Fusion - Compositing
- **Tons of detail here...**

   [pySetup]: <https://bitbucket.org/zklinger2000/gravmodtools/src/04fc15eee47327e9dfbd9c0c61da19d29a415315/setupCoffee.py>
