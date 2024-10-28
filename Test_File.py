from Tuple import Tuple,Color, vector,point,canvas_to_ppm,Canvas, Matrix,identity_matrix
import pytest
import math

def test_point_tuple():
    a = Tuple(4.3, -4.2, 3.1, 1.0)
    assert a.x == 4.3
    assert a.y == -4.2
    assert a.z == 3.1
    assert a.w == 1.0
    assert a.is_point()
    assert not a.is_vector()    
def test_vector_tuple():
    a = Tuple(4.3, -4.2, 3.1, 0.0)
    assert a.x == 4.3
    assert a.y == -4.2
    assert a.z == 3.1
    assert a.w == 0.0
    assert not a.is_point()
    assert a.is_vector()

def test_point_creation():
    p = point(4, -4, 3)
    assert p == Tuple(4, -4, 3, 1)

def test_vector_creation():
    v = vector(4, -4, 3)
    assert v == Tuple(4, -4, 3, 0)

def test_tuple_addition():
    a1 = Tuple(3, -2, 5, 1)
    a2 = Tuple(-2, 3, 1, 0)
    assert a1 + a2 == Tuple(1, 1, 6, 1)

def test_point_subtraction():
    p1 = point(3, 2, 1)
    p2 = point(5, 6, 7)
    assert p1 - p2 == vector(-2, -4, -6)

def test_point_vector_subtraction():
    p = point(3, 2, 1)
    v = vector(5, 6, 7)
    assert p - v == point(-2, -4, -6)

def test_vector_subtraction():
    v1 = vector(3, 2, 1)
    v2 = vector(5, 6, 7)
    assert v1 - v2 == vector(-2, -4, -6)
def test_tuple_negation():
    a = Tuple(1, -2, 3, -4)
    assert -a == Tuple(-1, 2, -3, 4)

def test_tuple_scalar_multiplication():
    a = Tuple(1, -2, 3, -4)
    assert a * 3.5 == Tuple(3.5, -7, 10.5, -14)
    assert a * 0.5 == Tuple(0.5, -1, 1.5, -2)

def test_tuple_scalar_division():
    a = Tuple(1, -2, 3, -4)
    assert a / 2 == Tuple(0.5, -1, 1.5, -2)

def test_vector_magnitude():
    v1 = vector(1, 0, 0)
    v2 = vector(0, 1, 0)
    v3 = vector(0, 0, 1)
    v4 = vector(1, 2, 3)
    v5 = vector(-1, -2, -3)

    assert v1.magnitude() == 1
    assert v2.magnitude() == 1
    assert v3.magnitude() == 1
    assert v4.magnitude() == math.sqrt(14)
    assert v5.magnitude() == math.sqrt(14)

#Chapter 2
def test_color_creation():
    c = Color(-0.5, 0.4, 1.7)
    assert c.red == -0.5
    assert c.green == 0.4
    assert c.blue == 1.7

def test_color_addition():
    c1 = Color(0.9, 0.6, 0.75)
    c2 = Color(0.7, 0.1, 0.25)  

    assert c1 + c2 == Color(1.6, 0.7, 1.0)

def test_color_subtraction():
    c1 = Color(0.9, 0.6, 0.75)
    c2 = Color(0.7, 0.1, 0.25)
    print(c1-c2)
    assert c1 - c2 == Color(0.2, 0.5, 0.5)

def test_color_scalar_multiplication():
    c = Color(0.2, 0.3, 0.4)
    assert c * 2 == Color(0.4, 0.6, 0.8)

def test_color_multiplication():
    c1 = Color(1, 0.2, 0.4)
    c2 = Color(0.9, 1, 0.1)
    print(c1*c2)
    assert c1 * c2 == Color(0.9, 0.2, 0.04)

def test_color_multiplication_type_error():
    c = Color(0.2, 0.3, 0.4)
    with pytest.raises(TypeError):
        c * "invalid"


#Canvas

def test_canvas_creation():
    canvas = Canvas(10, 20)
    assert canvas.width == 10
    assert canvas.height == 20
    for row in canvas.pixels:
        for pixel in row:
            assert pixel == Color(0, 0, 0)

def test_write_pixel():
    canvas = Canvas(10, 20)
    red = Color(1, 0, 0)
    canvas.write_pixel(2, 3, red)
    assert canvas.pixel_at(2, 3) == red

def test_canvas_to_ppm_header():
    canvas = Canvas(5, 3)
    ppm = canvas_to_ppm(canvas)
    lines = ppm.split('\n')
    assert lines[0] == 'P3'
    assert lines[1] == '5 3'
    assert lines[2] == '255'

def test_canvas_to_ppm_pixel_data():
    canvas = Canvas(5, 3)
    c1 = Color(1.5, 0, 0)
    c2 = Color(0, 0.5, 0)
    c3 = Color(-0.5, 0, 1)
    canvas.write_pixel(0, 0, c1)
    canvas.write_pixel(2, 1, c2)
    canvas.write_pixel(4, 2, c3)
    ppm = canvas_to_ppm(canvas) 
    print(ppm)
    lines = ppm.split('\n')
    assert lines[3] == '255 0 0 0 0 0 0 0 0 0 0 0 0 0 0'
    assert lines[4] == '0 0 0 0 0 0 0 127 0 0 0 0 0 0 0'
    assert lines[5] == '0 0 0 0 0 0 0 0 0 0 0 0 0 0 255'  

def test_4x4_matrix():
    m = Matrix(4, 4, [
        [1, 2, 3, 4],
        [5.5, 6.5, 7.5, 8.5],
        [9, 10, 11, 12],
        [13.5, 14.5, 15.5, 16.5]
    ])
    assert m[0, 0] == 1
    assert m[0, 3] == 4
    assert m[1, 0] == 5.5
    assert m[1, 2] == 7.5
    assert m[2, 2] == 11
    assert m[3, 0] == 13.5
    assert m[3, 2] == 15.5

def test_2x2_matrix():
    m = Matrix(2, 2, [
        [-3, 5],
        [1, -2]
    ])
    assert m[0, 0] == -3
    assert m[0, 1] == 5
    assert m[1, 0] == 1
    assert m[1, 1] == -2

def test_3x3_matrix():
    m = Matrix(3, 3, [
        [-3, 5, 0],
        [1, -2, -7],
        [0, 1, 1]
    ])
    assert m[0, 0] == -3
    assert m[1, 1] == -2
    assert m[2, 2] == 1

def test_matrix_equality(): 

    a = Matrix(4, 4, [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 8, 7, 6],
        [5, 4, 3, 2]
    ])
    b = Matrix(4, 4, [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 8, 7, 6],
        [5, 4, 3, 2]
    ])
    assert a == b

    c = Matrix(4, 4, [
        [2, 3, 4, 5],
        [6, 7, 8, 9],
        [7, 6, 5, 4],
        [3, 2, 1, 0]
    ])
    assert a != c      

def test_matrix_multiplication():
    a = Matrix(4, 4, [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 8, 7, 6],
        [5, 4, 3, 2]
    ])
    b = Matrix(4, 4, [
        [-2, 1, 2, 3],
        [3, 2, 1, -1],
        [4, 3, 6, 5],
        [1, 2, 7, 8]  

    ])
    expected = Matrix(4, 4, [
        [20, 22, 50, 48],
        [44, 54, 114, 108],
        [40, 58, 110, 102],
        [16, 26, 46, 42]
    ])
    assert a * b == expected

def test_matrix_tuple_multiplication():
    a = Matrix(4, 4, [
        [1, 2, 3, 4],
        [2, 4, 4, 2],
        [8, 6, 4, 1],
        [0, 0, 0, 1]
    ])
    b = Tuple(1, 2, 3, 1)
    expected = Tuple(18, 24, 33, 1)
    assert a * b == expected

def test_matrix_identity_multiplication():
    a = Matrix(4, 4, [
        [0, 1, 2, 4],
        [1, 2, 4, 8],
        [2, 4, 8, 16],
        [4, 8, 16, 32]
    ])
    assert a * identity_matrix == a

def test_tuple_identity_multiplication():
    a = Tuple(1, 2, 3, 4)
    assert identity_matrix * a == a

def test_matrix_transpose():
    a = Matrix(4, 4, [
        [0, 9, 3, 0],
        [9, 8, 0, 8],
        [1, 8, 5, 3],
        [0, 0, 5, 8]
    ])
    expected = Matrix(4, 4, [
        [0, 9, 1, 0],
        [9, 8, 8, 0],
        [3, 0, 5, 5],
        [0, 8, 3, 8]
    ])
    assert a.transpose() == expected

def test_identity_matrix_transpose():
    assert identity_matrix.transpose() == identity_matrix

def test_determinant_2x2():
    m = Matrix(2, 2, [[1, 5], [-3, 2]])
    assert m.determinant() == 17

def test_submatrix_3x3():
    m = Matrix(3, 3, [[1, 5, 0], [-3, 2, 7], [0, 6, -3]])
    submatrix = m.submatrix(0, 2)
    assert submatrix == Matrix(2, 2, [[-3, 2], [0, 6]])

def test_submatrix_4x4():
    m = Matrix(4, 4, [[-6, 1, 1, 6], [-8, 5, 8, 6], [-1, 0, 8, 2], [-7, 1, -1, 1]])
    submatrix = m.submatrix(2, 1)
    assert submatrix == Matrix(3, 3, [[-6, 1, 6], [-8, 8, 6], [-7, -1, 1]])

def test_minor_3x3():
    m = Matrix(3, 3, [[3, 5, 0], [2, -1, -7], [6, -1, 5]])
    assert m.minor(1, 0) == 25

def test_cofactor_3x3():
    m = Matrix(3, 3, [[3, 5, 0], [2, -1, -7], [6, -1, 5]])
    assert m.cofactor(0, 0) == -12
    assert m.cofactor(1, 0) == -25

def test_determinant_3x3():
    m = Matrix(3, 3, [[1, 2, 6], [-5, 8, -4], [2, 6, 4]])
    assert m.determinant() == -196

def test_determinant_4x4():
    m = Matrix(4, 4, [[-2, -8, 3, 5], [-3, 1, 7, 3], [1, 2, -9, 6], [-6, 7, 7, -9]])
    assert m.determinant() == -4071

def test_invertible_matrix():
    a = Matrix(4, 4, [
        [6, 4, 4, 4],
        [5, 5, 7, 6],
        [4, -9, 3, -7],
        [9, 1, 7, -6]
    ])
    assert a.determinant() == -2120
    assert a.is_invertible()

def test_non_invertible_matrix():
    a = Matrix(4, 4, [
        [-4, 2, -2, -3],
        [9, 6, 2, 6],
        [0, -5, 1, -5],
        [0, 0, 0, 0]
    ])
    assert a.determinant() == 0
    assert not a.is_invertible()

def test_matrix_inverse_multiplication():
    a = Matrix(4, 4, [
        [3, -9, 7, 3],
        [3, -8, 2, -9],
        [-4, 4, 4, 1],
        [-6, 5, -1, 1]
    ])
    b = Matrix(4, 4, [
        [8, 2, 2, 2],
        [3, -1, 7, 0],
        [7, 0, 5, 4],
        [6, -2, 0, 5]
    ])
    c = a * b
    b_inv = b.inverse()
    product = c * b_inv
    assert product == a

def test_translation_matrix():
    transform = Matrix.translation(5, -3, 2)
    p = Tuple(4, -4, 3, 1)
    expected = Tuple(9, -7, 5, 1)
    assert transform * p == expected

def test_inverse_translation_matrix():
    transform = Matrix.translation(5, -3, 2)
    inv = transform.inverse()
    p = Tuple(4, -4, 3, 1)
    expected = Tuple(-1, -1, 1, 1)
    print(expected)
    print(inv*p)
    assert inv * p == expected

def test_translation_on_vector():
    transform = Matrix.translation(5, -3, 2)
    v = Tuple(4, -4, 3, 0)
    assert transform * v == v

def test_scaling_point():
    transform = Matrix.scaling(2, 3, 4)
    p = Tuple(-4, 6, 8, 1)
    expected = Tuple(-8, 18, 32, 1)
    assert transform * p == expected

def test_scaling_vector():
    transform = Matrix.scaling(2, 3, 4)
    v = Tuple(-4, 6, 8, 0)
    expected = Tuple(-8, 18, 32, 0)
    assert transform * v == expected

def test_inverse_scaling():
    transform = Matrix.scaling(2, 3, 4)
    inv = transform.inverse()
    v = Tuple(-4, 6, 8, 0)
    expected = Tuple(-2, 2, 2, 0)
    assert inv * v == expected

def test_reflection():
    transform = Matrix.scaling(-1, 1, 1)
    p = Tuple(2, 3, 4, 1)
    expected = Tuple(-2, 3, 4, 1)
    assert transform * p == expected