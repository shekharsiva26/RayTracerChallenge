from Tuple import Canvas, Color, Material, PointLight, Ray, Sphere, Tuple, canvas_to_ppm, lighting, normal_at


def main():

    ray_origin = Tuple(0, 0, -5, 1)
    wall_z = 10
    wall_size = 7.0
    canvas_pixels = 100
    pixel_size = wall_size / canvas_pixels
    half = wall_size / 2
    canvas = Canvas(canvas_pixels, canvas_pixels) 

    canvas_pixels = 100
    canvas = Canvas(canvas_pixels, canvas_pixels) 
    shape = Sphere()
    material = Material()
    shape.material=material
    shape.material.color = Color(1, 0.2, 1)  # Purple color

    light_position = Tuple(-10, 10, -10, 1)
    light_color = Color(1, 1, 1)
    light = PointLight(light_position, light_color)

    for y in range(canvas_pixels):
        world_y = half - pixel_size * y
        for x in range(canvas_pixels):
            world_x = -half + pixel_size * x
            position = Tuple(world_x, world_y, wall_z, 1)
            r = Ray(ray_origin, (position - ray_origin).normalize())
            xs = shape.intersect(r)
            if hit := xs.hit():
                point = r.position(hit.t)
                normal = normal_at(hit.object, point)
                eye = -r.direction
                color = lighting(hit.object.material, light, point, eye, normal)
                canvas.write_pixel(x, y, color)

    with open('sphere.ppm', 'w') as out_file:
        out_file.write(canvas_to_ppm(canvas))      

if __name__ == "__main__":
    main()