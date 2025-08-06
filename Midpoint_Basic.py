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

def midpoint_line_zone0(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    d = 2 * dy - dx
    incE = 2 * dy
    incNE = 2 * (dy - dx)

    x = x1
    y = y1

    draw_pixel(x, y)
    while x < x2:               #Loop cholbe till x reaches x2
        if d <= 0:              # Choose East
            d += incE              
        else:
            d += incNE          # Choose North-East
            y += 1
        x += 1
        draw_pixel(x, y)

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    # Draw line using Midpoint Line Algorithm in Zone 0
    midpoint_line_zone0(100, 100, 300, 200)

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
