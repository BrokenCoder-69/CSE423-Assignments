from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import time
import random





# ==========================
# GLOBAL VARIABLES
# ==========================
diamond_x = 400
diamond_y = 600
diamond_size = 30
diamond_speed = 100  # pixels per second
score = 0
game_over = False
last_time = time.time()
paused = False




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













def draw_diamond(cx, cy, size, r=1, g=1, b=1):
    top = (cx, cy + size)
    right = (cx + size, cy)
    bottom = (cx, cy - size)
    left = (cx - size, cy)

    draw_midpoint_line(*top, *right, r, g, b)
    draw_midpoint_line(*right, *bottom, r, g, b)
    draw_midpoint_line(*bottom, *left, r, g, b)
    draw_midpoint_line(*left, *top, r, g, b)



def draw_catcher(cx, cy, width, height, r=1, g=1, b=1):
    half_w = width // 2
    top_h = height
    bottom_h = height // 3

    # Define 4 points
    left_bottom  = (cx - half_w, cy)
    right_bottom = (cx + half_w, cy)
    left_top     = (cx - half_w // 2, cy + top_h)
    right_top    = (cx + half_w // 2, cy + top_h)

    # Draw 4 lines
    draw_midpoint_line(*left_bottom, *right_bottom, r, g, b)
    draw_midpoint_line(*left_top, *right_top, r, g, b)
    draw_midpoint_line(*left_top, *left_bottom, r, g, b)
    draw_midpoint_line(*right_top, *right_bottom, r, g, b)





catcher_x = 400  # Middle of screen
catcher_y = 50   # Near bottom
catcher_speed = 20
def keyboard(key, x, y):
    global catcher_x
    if key == b'\x1b':  # ESC key to exit
        glutLeaveMainLoop()

def special_keys(key, x, y):
    global catcher_x
    if key == GLUT_KEY_LEFT:
        catcher_x -= catcher_speed
        if catcher_x < 50:
            catcher_x = 50
    elif key == GLUT_KEY_RIGHT:
        catcher_x += catcher_speed
        if catcher_x > width - 50:
            catcher_x = width - 50

    glutPostRedisplay()  # Redraw





def idle():
    global diamond_y, last_time, game_over

    if paused or game_over:
        return

    now = time.time()
    dt = now - last_time
    last_time = now

    # Move diamond down based on speed and time passed
    diamond_y -= diamond_speed * dt

    # If missed — Game Over
    if diamond_y - diamond_size <= 0:
        game_over = True
        print(f"Game Over! Final score: {score}")

    # Collision check
    if check_collision():
        reset_diamond()
        increase_score()

    glutPostRedisplay()



def check_collision():
    catcher_w = 100
    catcher_h = 30

    # Diamond AABB
    d_left = diamond_x - diamond_size
    d_right = diamond_x + diamond_size
    d_bottom = diamond_y - diamond_size
    d_top = diamond_y + diamond_size

    # Catcher AABB
    c_left = catcher_x - catcher_w // 2
    c_right = catcher_x + catcher_w // 2
    c_bottom = catcher_y
    c_top = catcher_y + catcher_h

    return (
        d_left < c_right and
        d_right > c_left and
        d_bottom < c_top and
        d_top > c_bottom
    )

def reset_diamond():
    global diamond_x, diamond_y
    diamond_x = random.randint(100, width - 100)
    diamond_y = height

def increase_score():
    global score, diamond_speed
    score += 1
    diamond_speed += 10
    print(f"Score: {score}")


# Track pause state
paused = False

# Button bounding boxes
button_restart = {'x': 50, 'y': height - 70, 'w': 40, 'h': 40}
button_pause = {'x': 150, 'y': height - 70, 'w': 40, 'h': 40}
button_exit = {'x': 250, 'y': height - 70, 'w': 40, 'h': 40}




def draw_buttons():
    # Restart Arrow (←)
    x, y = button_restart['x'], button_restart['y']
    draw_midpoint_line(x+30, y+10, x+10, y+20, 0, 1, 1)
    draw_midpoint_line(x+30, y+30, x+10, y+20, 0, 1, 1)
    draw_midpoint_line(x+30, y+10, x+30, y+30, 0, 1, 1)

    # Pause or Play Icon
    x, y = button_pause['x'], button_pause['y']
    if not paused:
        draw_midpoint_line(x+10, y+10, x+10, y+30, 1, 0.5, 0)
        draw_midpoint_line(x+20, y+10, x+20, y+30, 1, 0.5, 0)
    else:
        draw_midpoint_line(x+10, y+10, x+10, y+30, 1, 0.5, 0)
        draw_midpoint_line(x+10, y+10, x+25, y+20, 1, 0.5, 0)
        draw_midpoint_line(x+10, y+30, x+25, y+20, 1, 0.5, 0)

    # Exit Cross
    x, y = button_exit['x'], button_exit['y']
    draw_midpoint_line(x+10, y+10, x+30, y+30, 1, 0, 0)
    draw_midpoint_line(x+30, y+10, x+10, y+30, 1, 0, 0)





def mouse_click(button, state, x, y):
    global paused, game_over, score, diamond_speed

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        # Invert y (GLUT's y=0 is top)
        y = height - y

        # Restart
        if point_in_box(x, y, button_restart):
            print("Starting Over")
            reset_diamond()
            score = 0
            diamond_speed = 100
            game_over = False

        # Pause / Play
        elif point_in_box(x, y, button_pause):
            paused = not paused
            print("Paused" if paused else "Playing")

        # Exit
        elif point_in_box(x, y, button_exit):
            print(f"Goodbye! Final score: {score}")
            glutLeaveMainLoop()



def point_in_box(x, y, box):
    return (box['x'] <= x <= box['x'] + box['w'] and
            box['y'] <= y <= box['y'] + box['h'])





















def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    if game_over:
        # Red catcher (Game Over)
        draw_catcher(catcher_x, catcher_y, 100, 30, 1, 0, 0)
    else:
        draw_catcher(catcher_x, catcher_y, 100, 30, 1, 1, 1)

    
    draw_buttons()
    draw_diamond(diamond_x, int(diamond_y), diamond_size, random.random(), random.random(), random.random())

    glFlush()





def main():
    glutInit()
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(width, height)
    glutCreateWindow(b"Midpoint Line Drawing")
    init()
    glutDisplayFunc(display)
    glutMouseFunc(mouse_click)

    glutKeyboardFunc(keyboard)
    glutSpecialFunc(special_keys)
    glutIdleFunc(idle)

    glutMainLoop()



if __name__ == "__main__":
    main()
