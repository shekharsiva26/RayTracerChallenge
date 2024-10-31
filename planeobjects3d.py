import math
from Tuple import *
# ... (previous definitions for `Matrix`, `Tuple`, `Color`, `Ray`, `Sphere`, `World`, `Intersection`, `Computations`, `lighting`, `prepare_computations`, `ray_for_pixel`, and `render` functions)

def main():
    # Create the world and objects
    world = World()
    light = PointLight(Tuple(-10, 10, -10, 1), Color(1, 1, 1))
    world.light = light

    # Add objects to the world
    floor = Sphere()
    floor.material = Material()
    floor.transform = Matrix.scaling(10, 0.01, 10)
    floor.material.color = Color(1, 0.9, 0.9)
    floor.material.specular = 0
    world.add_object(floor)

    left_wall = Sphere()
    left_wall.material = floor.material
    left_wall.transform = Matrix.translation(0,0,5) *  Matrix.rotation_y(-math.pi/4) * Matrix.rotation_x(math.pi/2) *Matrix.scaling(10, 0.01, 10)
   
#    world.add_object(left_wall)

    right_wall = Sphere()
    right_wall.material = floor.material
    right_wall.transform = Matrix.translation(0,0,5) *  Matrix.rotation_y(math.pi/4) * Matrix.rotation_x(math.pi/2) *Matrix.scaling(10, 0.01, 10)
   
#    world.add_object(right_wall)

    middle= Sphere()
    middle.transform = Matrix.translation(-0.5,1,0.5)
    middle.material = Material()
    middle.material.color = Color(0.1, 1, 0.5)
    middle.material.diffuse = 0.7
    middle.material.specular = 0.3
    world.add_object(middle)

    right= Sphere()
    right.transform = Matrix.translation(1.5,0.5,-0.5)*Matrix.scaling(0.5,0.5,0.5)
    right.material = Material()
    right.material.color = Color(0.5, 1, 0.1)
    right.material.diffuse = 0.7
    right.material.specular = 0.3    


    left= Sphere()
    left.transform = Matrix.translation(1.5,0.33,-0.75)*Matrix.scaling(0.33,0.33,0.33)
    left.material = Material()
    left.material.color = Color(1, 0.8, 0.1)
    left.material.diffuse = 0.7
    left.material.specular = 0.3   

    world.add_object(right)
    world.add_object(left)

    world.light = PointLight(point(-10,10,-10),Color(1,1,1))
    # Create the camera
    camera = Camera(500, 250, math.pi / 3)
    camera.transform = view_transform(Tuple(0, 1.5, -5, 1), Tuple(0, 1, 0, 1), Tuple(0, 1, 0, 0))

    # Render the scene
    canvas = render(camera, world)

    # Write the image to a PPM file
    with open("multiple3d.ppm", "w") as f:
        f.write(canvas_to_ppm(canvas))

if __name__ == "__main__":
    main()