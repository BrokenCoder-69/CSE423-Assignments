from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

# ==========================
# GLOBAL VARIABLES
# ==========================
plate_speed = 3         # Initial speed of plate
speed = 1               # Speed of falling diamond
plate_x = 200           # Initial X position of plate
pause = False           # Pause/resume flag
animation_speed = 10    # Frame delay/speed control
diamond_x, diamond_y = 300, 500  # Initial position of diamond


# ==========================
# DRAWING FUNCTIONS
# ==========================
def plate():
    """Draw the catching plate."""
    global plate_x
    x = plate_x
    r, g, b = 0, 1, 1
    line_algo(x, 50, x + 200, 50, r, g, b)
    line_algo(x + 25, 25, x + 175, 25, r, g, b)
    line_algo(x, 50, x + 25, 25, r, g, b)
    line_algo(x + 175, 25, x + 200, 50, r, g, b)


def diamond():
    """Draw and drop the diamond. Handle collision with plate."""
    global diamond_x, diamond_y, speed, plate_x, pause, plate_speed

    # Successful catch
    if diamond_y < 110 and plate_x <= diamond_x <= plate_x + 200:
        diamond_y = 500
        print('Score =', plate_speed - 2)
        plate_speed += 1
        speed += plate_speed * 0.01
        diamond_x = random.randint(25, 575)

    # Missed catch
    elif diamond_y < 110 and (diamond_x > (plate_x + 200) or diamond_x < plate_x):
        restart()
        return

    # Move diamond
    diamond_y -= speed
    if pause:
        diamond_y += speed  # Cancel movement if paused

    x, y = diamond_x, diamond_y
    r, g, b = 1, 1, 0
    line_algo(x, y, x - 20, y - 30, r, g, b)
    line_algo(x, y, x + 20, y - 30, r, g, b)
    line_algo(x - 20, y - 30, x, y - 60, r, g, b)
    line_algo(x + 20, y - 30, x, y - 60, r, g, b)

    glutPostRedisplay()


def back():
    """Draw the restart button."""
    r, g, b = 0, 1, 0
    x, y = 25, 550
    line_algo(x, y, x + 50, y, r, g, b)
    line_algo(x, y, x + 25, y + 25, r, g, b)
    line_algo(x, y, x + 25, y - 25, r, g, b)


def pause_play():
    """Draw the pause/resume button."""
    global pause
    r, g, b = 1, 0.2, 1
    x, y = 275, 575

    if pause:
        # Resume icon
        line_algo(x, y, x + 50, y - 25, r, g, b)
        line_algo(x, y - 50, x + 50, y - 25, r, g, b)
        line_algo(x, y, x, y - 50, r, g, b)
    else:
        # Pause icon
        line_algo(x + 10, y, x + 10, y - 50, r, g, b)
        line_algo(x + 40, y, x + 40, y - 50, r, g, b)


def cross():
    """Draw the close button."""
    r, g, b = 1, 0, 0
    x, y = 525, 575
    line_algo(x, y, x + 50, y - 50, r, g, b)
    line_algo(x, y - 50, x + 50, y, r, g, b)


# ==========================
# UTILITY FUNCTIONS
# ==========================
def convert_coordinate(x, y):
    """Convert mouse coordinates to OpenGL coordinates."""
    return x, 600 - y


def zone(x1, y1, x2, y2):
    """Determine the zone of the line from (x1,y1) to (x2,y2)."""
    dx = x2 - x1
    dy = y2 - y1

    if abs(dx) > abs(dy):
        if dx > 0 and dy >= 0: return 0
        elif dx < 0 and dy > 0: return 3
        elif dx < 0 and dy < 0: return 4
        else: return 7
    else:
        if dx > 0 and dy >= 0: return 1
        elif dx < 0 and dy > 0: return 2
        elif dx < 0 and dy < 0: return 5
        else: return 6


def zone02z(x, y, z):
    """Convert a point from zone 0 to zone z."""
    transforms = [
        (x, y), (y, x), (-y, x), (-x, y),
        (-x, -y), (-y, -x), (y, -x), (x, -y)
    ]
    return transforms[z]


def z2zone0(x, y, z):
    """Convert a point from zone z to zone 0."""
    # Reverse of zone02z
    return zone02z(x, y, z)


def line_algo(x1, y1, x2, y2, r=1, g=1, b=1):
    """Draw a line using Midpoint algorithm and zone transformation."""
    z = zone(x1, y1, x2, y2)
    x1, y1 = z2zone0(x1, y1, z)
    x2, y2 = z2zone0(x2, y2, z)
    dx = x2 - x1
    dy = y2 - y1
    d = 2 * dy - dx

    glBegin(GL_POINTS)
    glColor3f(r, g, b)
    glVertex2f(*zone02z(x1, y1, z))

    while x1 < x2:
        if d > 0:
            d += 2 * (dy - dx)
            x1 += 1
            y1 += 1
        else:
            d += 2 * dy
            x1 += 1
        draw_x, draw_y = zone02z(x1, y1, z)
        glVertex2f(draw_x, draw_y)
    glEnd()


def restart():
    """Reset all variables to initial state."""
    global plate_x, diamond_x, diamond_y, speed, pause, plate_speed
    pause = True
    plate_x = 200
    diamond_x, diamond_y = 300, 500
    speed = 0
    plate_speed = 3
    print('Restart!')
    glutPostRedisplay()


# ==========================
# INPUT HANDLERS
# ==========================
def keyboardListener(key, x, y):
    """Keyboard spacebar for pause/resume toggle."""
    global speed, pause
    if key == b' ':
        pause = not pause
        speed = 0 if pause else 1
        glutPostRedisplay()


def specialKeyListener(key, x, y):
    """Left and Right arrow keys to move the plate."""
    global plate_x, plate_speed
    if pause:
        return
    if key == GLUT_KEY_RIGHT:
        plate_x += plate_speed * 2
        if plate_x > 400:
            plate_x -= plate_speed * 2
    elif key == GLUT_KEY_LEFT:
        plate_x -= plate_speed * 2
        if plate_x < 0:
            plate_x += plate_speed * 2


def mouseListener(button, state, x, y):
    """Mouse click handler for restart, pause/resume, and exit."""
    global pause, speed
    x, y = convert_coordinate(x, y)
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if 0 <= x <= 100 and 500 <= y <= 600:
            restart()
        elif 500 <= x <= 600 and 500 <= y <= 600:
            glutLeaveMainLoop()
        elif 250 <= x <= 350 and 500 <= y <= 600:
            pause = not pause
            speed = 0 if pause else 1
            glutPostRedisplay()


# ==========================
# RENDERING & MAIN LOOP
# ==========================
def iterate():
    """Set up the projection for 2D rendering."""
    glViewport(0, 0, 600, 600)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 600, 0.0, 600, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def showScreen():
    """Main display function."""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glPointSize(1)
    iterate()
    plate()
    diamond()
    back()
    pause_play()
    cross()
    glutSwapBuffers()


# ==========================
# INIT GLUT & START GAME
# ==========================
glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(600, 600)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"OpenGL Coding Practice")
glutDisplayFunc(showScreen)
glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)
glutMainLoop()
