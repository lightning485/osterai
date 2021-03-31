# Tested in Blender 2.92. Licensing: MIT License

import bpy
import math as m
import random

random.seed(123) # to make it reproducable each time when the script is called. Use 123 for generating training data and 321 for generating what is called "known unknown" in the notebook.

nums_eggs = [0,1,2,3,4,5,6,7] # list with desired number of eggs
num_images = 2000 # images per number of eggs
x_range = [-5.0, 5.0] # where to spawn eggs
y_range = [-11.8, 9.2] # where to spawn eggs
min_d = 2.0 # minimum distance between two egg positions. CAREFUL: If you set this too high, spawning might not be possible at all and the script might freeze. Then, Ctrl-C in the Blender System Console to abort
    
filepath_object = bpy.path.abspath('//egg.obj') # path of the object to spawn. // brings us in directory of *.blend file
    
# helper function: Euclidean distance between two points
def dist(x,y, x0,y0):
    return m.sqrt((x-x0)**2+(y-y0)**2)

# helper function: Minimum distance from one point to a list of points
def closest_dist(x,y, xs,ys):
    if len(xs) == 0:
        return float(m.inf)
    d = []
    for k in range(len(xs)):
        d_k = dist(xs[k],ys[k],x,y)
        d.append(d_k)
    return min(d)

# Main part
# =========

grass_seed = 0
for num_eggs in nums_eggs:
    for i in range(num_images):
        spawned_objs = []

        # List of already existing egg coordinates, initially empty:
        xs_existing = []
        ys_existing = []
        for n in range(num_eggs):
            # Spawn egg
            # ---------
            bpy.ops.import_scene.obj(filepath=filepath_object)
            obj = bpy.context.selected_objects[0] # new object is selected after creation
            #bpy.ops.object.modifier_add(type='COLLISION') # this should prevent hair from growing through the object, but it doesn't seem to work always
            
            done = False
            while not done:
                x_new = random.uniform(x_range[0], x_range[1])
                y_new = random.uniform(y_range[0], y_range[1])
                if closest_dist(x_new,y_new, xs_existing,ys_existing) >= min_d:
                    done = True
             
            obj.location.x = x_new
            obj.location.y = y_new
            obj.rotation_euler[2] = random.random()*m.pi
            
            spawned_objs.append(obj)
            
            xs_existing.append(x_new)
            ys_existing.append(y_new)
            
        # Vary context
        # ------------
        
        # Change grass randomly:
        bpy.data.objects['Plane'].particle_systems["ParticleSettings"].seed = grass_seed
        grass_seed = grass_seed + 1

        # Rotate light randomly around origin:
        angle = random.random()*m.pi
        R = m.sqrt(bpy.data.objects['Light'].location.x**2 + bpy.data.objects['Light'].location.y**2)
        bpy.data.objects['Light'].location.x = R*m.cos(angle)
        bpy.data.objects['Light'].location.y = R*m.sin(angle)
        
        # Render
        # ------
        
        bpy.context.scene.render.filepath = bpy.path.abspath('//images\\'+str(num_eggs)+'\\'+str(i)+'.png') # // brings us in directory of *.blend file
        bpy.ops.render.render(write_still=True)

        # Clean up
        # --------
        
        # Delete all previously spawned objects:
        for obj in bpy.context.selected_objects:
            obj.select_set(False)
        for obj in spawned_objs:
            obj.select_set(True)
            bpy.ops.object.delete()
