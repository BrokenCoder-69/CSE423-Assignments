from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Window dimensions
width, height = 800, 600

def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Black background
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, width, 0, height)  # Origin at bottom-left
    glMatrixMode(GL_MODELVIEW)

def draw_pixel(x, y, r=1, g=1, b=1):
    glColor3f(r, g, b)
    glBegin(GL_POINTS)
    glVertex2i(x, y)
    glEnd()





def find_zone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    abs_dx = abs(dx)
    abs_dy = abs(dy)

    if dx >= 0 and dy >= 0:
        if abs_dx >= abs_dy:
            return 0
        else:
            return 1
    elif dx < 0 and dy >= 0:
        if abs_dx < abs_dy:
            return 2
        else:
            return 3
    elif dx < 0 and dy < 0:
        if abs_dx >= abs_dy:
            return 4
        else:
            return 5
    elif dx >= 0 and dy < 0:
        if abs_dx < abs_dy:
            return 6
        else:
            return 7



def convert_to_zone0(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return y, -x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return -y, x
    elif zone == 7:
        return x, -y



def convert_from_zone0(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return -y, x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return y, -x
    elif zone == 7:
        return x, -y




















def draw_midpoint_line(x1, y1, x2, y2, r=1, g=1, b=1):
    zone = find_zone(x1, y1, x2, y2)

    x1_zone0, y1_zone0 = convert_to_zone0(x1, y1, zone)
    x2_zone0, y2_zone0 = convert_to_zone0(x2, y2, zone)

    dx = x2_zone0 - x1_zone0
    dy = y2_zone0 - y1_zone0

    d = 2 * dy - dx
    incE = 2 * dy
    incNE = 2 * (dy - dx)

    x = x1_zone0
    y = y1_zone0

    x_draw, y_draw = convert_from_zone0(x, y, zone)
    draw_pixel(x_draw, y_draw, r, g, b)

    while x < x2_zone0:
        if d <= 0:
            d += incE
        else:
            d += incNE
            y += 1
        x += 1
        x_draw, y_draw = convert_from_zone0(x, y, zone)
        draw_pixel(x_draw, y_draw, r, g, b)


def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    # Test in different zones
    draw_midpoint_line(100, 100, 300, 200)   # Zone 0
    draw_midpoint_line(100, 100, 200, 300)   # Zone 1
    draw_midpoint_line(300, 100, 200, 300)   # Zone 2
    draw_midpoint_line(300, 100, 100, 200)   # Zone 3
    draw_midpoint_line(300, 300, 100, 100)   # Zone 4
    draw_midpoint_line(200, 300, 100, 100)   # Zone 5
    draw_midpoint_line(100, 300, 200, 100)   # Zone 6
    draw_midpoint_line(100, 300, 300, 200)   # Zone 7

    glFlush()


def main():
    glutInit()
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(width, height)
    glutCreateWindow(b"Midpoint Line Drawing")
    init()
    glutDisplayFunc(display)
    glutMainLoop()

if __name__ == "__main__":
    main()
