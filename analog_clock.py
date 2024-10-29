from math import pi

from Tuple import (Canvas, Color, Matrix,Tuple,canvas_to_ppm)


def main():
    c = Canvas(500, 500)

    p = Tuple(0, 0, 1,1)

    translate = Matrix.translation(250, 0, 250)
    scale = Matrix.scaling(100, 0, 100)

    for h in range(12):
        r = Matrix.rotation_y(h * pi / 6)
        transform =translate * (scale * r)
        p2 = transform * p
        print(f"position ({p2.x}, {p2.y}, {p2.z})")
        print(c.height)
        c.write_pixel(round(p2.x), c.height - round(p2.z),
                    Color(0.0, 1.0, 0.0))

    with open('clock.ppm', 'w') as out_file:
        out_file.write(canvas_to_ppm(c))


if __name__ == "__main__":
    main()