from Tuple import Tuple,Color,Canvas,Sphere,Ray,Intersection,Intersections, canvas_to_ppm

def main():
    ray_origin = Tuple(0, 0, -5, 1)
    wall_z = 10
    wall_size = 7.0
    canvas_pixels = 100
    pixel_size = wall_size / canvas_pixels
    half = wall_size / 2
    canvas = Canvas(canvas_pixels, canvas_pixels) 

    color = Color(1, 0, 0)  # Red
    shape = Sphere()

    for y in range(canvas_pixels):
        world_y = half - pixel_size * y
        for x in range(canvas_pixels):
            world_x = -half + pixel_size * x
            position = Tuple(world_x, world_y, wall_z, 1)
            r = Ray(ray_origin, (position - ray_origin).normalize())
            xs = shape.intersect(r)
            if xs.hit():
                canvas.write_pixel( x, y, color)

    
    with open('output.ppm', 'w') as out_file:
        out_file.write(canvas_to_ppm(canvas))            

  

if __name__ == "__main__":
    main()