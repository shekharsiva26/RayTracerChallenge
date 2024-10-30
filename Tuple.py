import math
import collections

class Tuple:
    def __init__(self, x, y, z, w):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def is_point(self):
        return self.w == 1.0

    def is_vector(self):
        return self.w == 0.0
    def __eq__(self, other):
        return abs(self.x - other.x ) <0.001 and abs(self.y - other.y ) <0.001 and abs(self.z - other.z ) <0.001 and self.w == other.w

    def __repr__(self):
        return  f"Tuple({self.x}, {self.y}, {self.z}, {self.w})"
    def __add__(self, other):
        return Tuple(self.x + other.x, self.y + other.y, self.z + other.z, self.w + other.w)
    def __sub__(self, other):
        return  Tuple(self.x - other.x, self.y - other.y, self.z - other.z, self.w - other.w)
    def __neg__(self):
        return Tuple(-self.x, -self.y, -self.z, -self.w)
    def __mul__(self, scalar):
        return Tuple(self.x * scalar, self.y * scalar, self.z * scalar, self.w * scalar)
    def __truediv__(self, scalar):
        return Tuple(self.x / scalar, self.y / scalar, self.z / scalar, self.w / scalar)
    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2 + self.w**2)
    def normalize(self):
        return Tuple(self.x / self.magnitude(),self.y / self.magnitude(),self.z / self.magnitude(),self.w)
    def dot(self,b):
        return self.x *b.x + self.y *b.y +self.z *b.z 
    def cross(self, other):
        return Tuple(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,0)


class Matrix:
    def __init__(self, rows, cols, elements):
        self.rows = rows
        self.cols = cols
        self.elements = elements

    @staticmethod
    def translation(x, y, z):
        return Matrix(4, 4, [
            [1, 0, 0, x],
            [0, 1, 0, y],
            [0, 0, 1, z],
            [0, 0, 0, 1]
        ])

    @staticmethod
    def scaling(x, y, z):
        return Matrix(4, 4, [
            [x, 0, 0, 0],
            [0, y, 0, 0],
            [0, 0, z, 0],
            [0, 0, 0, 1]
        ])

    @staticmethod
    def rotation_x(radians):
        c = math.cos(radians)
        s = math.sin(radians)
        return Matrix(4, 4, [
            [1, 0, 0, 0],
            [0, c, -s, 0],
            [0, s, c, 0],
            [0, 0, 0, 1]
        ])

    @staticmethod
    def rotation_y(radians):
        c = math.cos(radians)
        s = math.sin(radians)
        return Matrix(4, 4, [
            [c, 0, s, 0],
            [0, 1, 0, 0],
            [-s, 0, c, 0],
            [0, 0, 0, 1]
        ])

    @staticmethod
    def rotation_z(radians):
        c = math.cos(radians)
        s = math.sin(radians)
        return Matrix(4, 4, [
            [c, -s, 0, 0],
            [s, c, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
    
    @staticmethod
    def shearing(xy, xz, yx, yz, zx, zy):
        return Matrix(4, 4, [
            [1, xy, xz, 0],
            [yx, 1, yz, 0],
            [zx, zy, 1, 0],
            [0, 0, 0, 1]
        ])

    def determinant(self):
        if self.rows != self.cols:
            raise ValueError("Matrix must be square")
        
        if self.rows == 2:
            return self.elements[0][0] * self.elements[1][1] - self.elements[0][1] * self.elements[1][0]

        determinant = 0
        for i in range(self.cols):
            determinant += self.elements[0][i] * self.cofactor(0, i)
        return determinant

    def submatrix(self, row, col):
        submatrix = []
        for i in range(self.rows):
            if i == row:
                continue
            subrow = []
            for j in range(self.cols):
                if j == col:
                    continue
                subrow.append(self.elements[i][j])
            submatrix.append(subrow)
        return Matrix(self.rows - 1, self.cols - 1, submatrix)
    def __truediv__(self, scalar):
        if scalar == 0:
            raise ValueError("Division by zero")
        return Matrix(self.rows, self.cols, [[element / scalar for element in row] for row in self.elements])
    def inverse(self):
        if self.rows != self.cols:
            raise ValueError("Matrix must be square")
        
        if self.rows == 4 and self.cols == 4 and self.elements[0][3] != 0 and self.elements[1][3] != 0 and self.elements[2][3] != 0:
            return Matrix.translation(-self.elements[0][3], -self.elements[1][3], -self.elements[2][3])
        else:
            determinant = self.determinant()
            if determinant == 0:
                raise ValueError("Matrix is not invertible")

            cofactor_matrix = [[self.cofactor(i, j) for j in range(self.cols)] for i in range(self.rows)]
            adjugate = Matrix(self.rows, self.cols, cofactor_matrix).transpose()

            return adjugate / determinant
    
    def minor(self, row, col):
        submatrix = self.submatrix(row, col)
        return submatrix.determinant()

    def cofactor(self, row, col):
        minor = self.minor(row, col)
        return (-1) ** (row + col) * minor

    def __getitem__(self, index):
        row, col = index
        return self.elements[row][col]
    
    def is_invertible(self):
        return self.determinant() != 0

    def __eq__(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            return False
        for i in range(self.rows):
            for j in range(self.cols):
                if abs(self.elements[i][j] - other.elements[i][j])> 0.01:
                    return False
        return True
    def __mul__(self, other):
        if isinstance(other, Matrix):
            if self.cols != other.rows:
                raise ValueError("Matrix dimensions are incompatible for multiplication")
            result = [[0 for _ in range(other.cols)] for _ in range(self.rows)]
            for i in range(self.rows):
                for j in range(other.cols):
                    for k in range(self.cols):
                        result[i][j] += self.elements[i][k] * other.elements[k][j]
            return Matrix(self.rows, other.cols, result)
        elif isinstance(other, Tuple):
            if self.cols != 4:
                raise ValueError("Matrix must be 4x4 to multiply with a tuple")
            result = Tuple (0,0,0,0)
            result.x += self.elements[0][0] * other.x + self.elements[0][1] * other.y   + self.elements[0][2] * other.z + self.elements[0][3] * other.w
            result.y += self.elements[1][0] * other.x + self.elements[1][1] * other.y   + self.elements[1][2] * other.z + self.elements[1][3] * other.w
            result.z += self.elements[2][0] * other.x + self.elements[2][1] * other.y   + self.elements[2][2] * other.z + self.elements[2][3] * other.w
            result.w += self.elements[3][0] * other.x + self.elements[3][1] * other.y   + self.elements[3][2] * other.z + self.elements[3][3] * other.w
            return result

    def transpose(self):
        return Matrix(self.cols, self.rows, [[self.elements[j][i] for j in range(self.rows)] for i in range(self.cols)])


identity_matrix = Matrix(4, 4, [
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
])
class Color:
    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue

    def __repr__(self):
        return f"Color(red={self.red}, green={self.green}, blue={self.blue})" 


    def __add__(self, other):
        if not isinstance(other, Color):
            raise TypeError("Can only add Color objects")
        return Color(self.red + other.red, self.green + other.green, self.blue + other.blue)

    def __sub__(self, other):
        if not isinstance(other, Color):
            raise TypeError("Can only subtract Color objects")
        return Color(self.red - other.red, self.green - other.green, self.blue - other.blue)
    
    def __eq__(self, other):
        return abs(self.red - other.red) <= 0.001 and abs(self.green - other.green) <=0.001 and abs(self.blue - other.blue) <=0.001 

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Color(self.red * other, self.green * other, self.blue * other)
        elif isinstance(other, Color):
            return Color(self.red * other.red, self.green * other.green, self.blue * other.blue)
        else:
            raise TypeError("Can only multiply Color by a number or another Color")


class PointLight:
    def __init__(self, position, intensity):
        self.position = position
        self.intensity = intensity
    def __eq__(self, other):
        return self.intensity == other.intensity  and self.position == other.position

class Material:
    def __init__(self, color=Color(1, 1, 1), ambient=0.1, diffuse=0.9, specular=0.9, shininess=200):
        self.color = color
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.shininess = shininess


class Sphere:
    def __init__(self, center=Tuple(0, 0, 0, 1), radius=1):
        self.center = center
        self.radius = radius
    def material(self):
        return self._material

    def set_material(self, material):
        self._material = material
    def __init__(self, transform=identity_matrix,center=Tuple(0, 0, 0, 1),radius=1):
        self.transform = transform
        self.center = center
        self.radius = radius

    def set_transform(self, t):
        self.transform = t

    def intersect(self, ray):
        sphere_to_ray = ray.origin - self.center
        a = ray.direction.dot(ray.direction)
        b = 2 * sphere_to_ray.dot(ray.direction)
        c = sphere_to_ray.dot(sphere_to_ray) - self.radius * self.radius

        discriminant = b * b - 4 * a * c
        if discriminant < 0: 
            return Intersections()  # No intersections
        else:
            t1 = (-b - math.sqrt(discriminant)) / (2 * a)
            t2 = (-b + math.sqrt(discriminant)) / (2 * a)
            return Intersections(Intersection(t1, self), Intersection(t2, self))

class Intersection:
    def __init__(self, t, object):
        self.t = t
        self.object = object

class Intersections(collections.MutableSequence):
    def __init__(self, *intersections):
        self.intersections = list(intersections)

    def __len__(self):
        return len(self.intersections)

    def __getitem__(self, index):
        return self.intersections[index]
    
    def append(self,intersection):
        self.intersections.append(intersection) 

    def __delitem__(self, i): del self.intersections[i]

    def __setitem__(self, i, v):
        #self.check(v)
        self.intersections[i] = v


    def extend(self,intersections):
        self.intersections.extend(intersections)
        self.intersections.sort(key = intersect_sort_function)

    def insert(self, i, v):
#        self.check(v)
        self.intersections.insert(i, v)

    def hit(self):
        hit = None
        for i in self.intersections:
            if i.t >= 0 and (hit is None or i.t < hit.t):
                hit = i
        return hit



class Ray:
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction

    def position(self, t):
        return self.origin + self.direction * t
    
    def transform(self, m):
        return Ray(m * self.origin, m * self.direction)



    
def point(x, y, z):
    return Tuple(x, y, z, 1)

def vector(x, y, z):
    return Tuple(x, y, z, 0)


class Canvas:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.pixels = [[Color(0, 0, 0) for _ in range(width)] for _ in range(height)]

    def write_pixel(self, x, y, color):
        self.pixels[y][x] = color

    def pixel_at(self, x, y):
        return self.pixels[y][x]

def canvas_to_ppm(canvas):
    ppm_lines = []
    ppm_lines.append("P3")
    ppm_lines.append(f"{canvas.width} {canvas.height}")
    ppm_lines.append("255")

    for row in canvas.pixels:
        pixel_line = ""
        for pixel in row:
            red = int(max(0, min(255, pixel.red * 255)))
            green = int(max(0, min(255, pixel.green * 255)))
            blue = int(max(0, min(255, pixel.blue * 255)))
            pixel_line += f"{red} {green} {blue} "
        ppm_lines.append(pixel_line.strip())
    
    ppm_lines.append("")

    return "\n".join(ppm_lines)

def intersect(sphere, ray):
    transformed_ray = ray.transform(sphere.transform.inverse())
    return sphere.intersect(transformed_ray)

def normal_at(sphere, world_point):
    object_point = sphere.transform.inverse() * world_point
    object_normal = object_point - Tuple(0, 0, 0, 1)
    world_normal = sphere.transform.inverse().transpose() * object_normal
    world_normal.w = 0
    return world_normal.normalize()

def reflect(v, n):
    return v - n * 2 * v.dot(n)

def lighting(material, light, point, eyev, normalv):
    effective_color = light.intensity * material.color
    
    # Ambient lighting
    ambient = effective_color * material.ambient

    # Diffuse lighting
    light_v = (light.position - point).normalize()
    light_dot_normal = light_v.dot(normalv)
    diffuse = effective_color * material.diffuse * max(light_dot_normal, 0)

    # Specular lighting
    reflect_v = reflect(-light_v, normalv)
    reflect_dot_eye = reflect_v.dot(eyev)
    specular = effective_color * material.specular * pow(max(reflect_dot_eye, 0), material.shininess)

    return ambient + diffuse + specular

class World:
    def __init__(self, objects=[], light=None):
        self.objects = objects
        self.light = light

def default_world():
    light = PointLight(Tuple(-10, 10, -10, 1), Color(1, 1, 1))
    s1 = Sphere()
    s1.material = Material()
    s1.material.color = Color(0.8, 1.0, 0.6)
    s1.material.diffuse = 0.7
    s1.material.specular = 0.2
    s2 = Sphere()
    s2.material = Material()
    s2.set_transform(Matrix.scaling(0.5,0.5, 0.5))
    return World([s1, s2], light)

def intersect_world(world, ray):
    xs = Intersections()
    for obj in world.objects:
        intersections = intersect(obj,ray)
        xs.extend(intersections)
    return xs




class Computations:
    def __init__(self, t, object, point, eyev, normalv):
        self.t = t
        self.object = object
        self.point = point
        self.eyev = eyev
        self.normalv = normalv

def prepare_computations(intersection, ray):
    t = intersection.t
    object = intersection.object
    point = ray.position(t)
    eyev = -ray.direction
    normalv = normal_at(object, point)
    inside = False
    if normalv.dot(eyev) < 0:
        inside = True
        normalv = -normalv

    return Computations(t, object, point, eyev, normalv)

def shade_hit(world, comps):
    return lighting(comps.object.material, world.light, comps.point, comps.eyev, comps.normalv)

def color_at(world, ray):
    xs = intersect_world(world,ray)
    hit = xs.hit()
    if hit:
        comps = prepare_computations(hit, ray)
        return shade_hit(world, comps)
    else:
        return Color(0, 0, 0)

def intersect_sort_function(intersection):
  return intersection.t