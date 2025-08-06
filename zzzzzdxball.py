from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import time
import random

# ==========================
# GLOBAL GAME VARIABLES
# ==========================
diamond_x = 400  # Diamond's horizontal position
diamond_y = 600  # Diamond's vertical position
diamond_size = 15 # The size of the diamond
diamond_speed = 100 # Initial speed of the diamond (pixels per second)
score = 0
game_over = False
paused = False
last_time = time.time() # Used to calculate frame time delta

# Window dimensions
width, height = 500, 700

# Catcher properties
catcher_x = width // 2 # Start catcher in the middle
catcher_y = 50         # Position catcher near the bottom
catcher_speed = 25     # How fast the catcher moves left/right

# ==========================
# OPENGL INITIALIZATION
# ==========================
def init():
    """Initializes the OpenGL rendering context."""
    glClearColor(0.0, 0.0, 0.0, 1.0) # Set the background color to black
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, width, 0, height) # Set up a 2D orthographic projection
    glMatrixMode(GL_MODELVIEW)

def draw_pixel(x, y):
    """Draws a single pixel at the specified integer coordinates."""
    # glColor is set before calling this function
    glBegin(GL_POINTS)
    glVertex2i(x, y)
    glEnd()

# ==========================
# MIDPOINT LINE ALGORITHM
#
# This algorithm efficiently calculates which pixels to
# draw to form a line between two points. It works by
# incrementally choosing between two possible next pixels
# based on a decision variable.
# ==========================

def find_zone(x1, y1, x2, y2):
    """
    Determines which of the 8 zones the line segment falls into.
    This is the first step in converting any line to a Zone 0 line.
    """
    dx = x2 - x1
    dy = y2 - y1
    if dx >= 0 and dy >= 0: # 1st quadrant
        return 0 if abs(dx) >= abs(dy) else 1
    elif dx < 0 and dy >= 0: # 2nd quadrant
        return 2 if abs(dx) < abs(dy) else 3
    elif dx < 0 and dy < 0: # 3rd quadrant
        return 4 if abs(dx) >= abs(dy) else 5
    else: # 4th quadrant (dx >= 0 and dy < 0)
        return 6 if abs(dx) < abs(dy) else 7

def convert_to_zone0(x, y, zone):
    """Converts a point from its original zone to Zone 0."""
    if zone == 0: return x, y
    if zone == 1: return y, x
    if zone == 2: return y, -x
    if zone == 3: return -x, y
    if zone == 4: return -x, -y
    if zone == 5: return -y, -x
    if zone == 6: return -y, x
    if zone == 7: return x, -y

def convert_from_zone0(x, y, zone):
    """Converts a point from Zone 0 back to its original zone."""
    if zone == 0: return x, y
    if zone == 1: return y, x
    if zone == 2: return -y, x
    if zone == 3: return -x, y
    if zone == 4: return -x, -y
    if zone == 5: return -y, -x
    if zone == 6: return y, -x
    if zone == 7: return x, -y

def draw_midpoint_line(x1, y1, x2, y2):
    """
    Draws a line of any slope using the Midpoint Line Algorithm.
    It handles all 8 zones by converting them to and from Zone 0.
    """
    zone = find_zone(x1, y1, x2, y2)
    x1_z0, y1_z0 = convert_to_zone0(x1, y1, zone)
    x2_z0, y2_z0 = convert_to_zone0(x2, y2, zone)

    dx = x2_z0 - x1_z0
    dy = y2_z0 - y1_z0
    d = 2 * dy - dx
    incE = 2 * dy
    incNE = 2 * (dy - dx)

    x, y = x1_z0, y1_z0
    while x <= x2_z0:
        # Convert the pixel back to the original zone before drawing
        x_draw, y_draw = convert_from_zone0(x, y, zone)
        draw_pixel(x_draw, y_draw)

        if d <= 0: # Choose East
            d += incE
        else: # Choose North-East
            d += incNE
            y += 1
        x += 1

# ==========================
# GAME OBJECT DRAWING
# ==========================

def draw_diamond(cx, cy, size):
    """Draws a yellow diamond centered at (cx, cy)."""
    top = (cx, cy + size)
    right = (cx + size, cy)
    bottom = (cx, cy - size)
    left = (cx - size, cy)
    
    glColor3f(1.0, 1.0, 0.0) # Yellow color
    draw_midpoint_line(*top, *right)
    draw_midpoint_line(*right, *bottom)
    draw_midpoint_line(*bottom, *left)
    draw_midpoint_line(*left, *top)

def draw_catcher(cx, cy, width, height, r, g, b):
    """Draws the player's catcher."""
    half_w = width // 2
    left_bottom  = (cx - half_w, cy)
    right_bottom = (cx + half_w, cy)
    left_top     = (cx - half_w // 2, cy + height)
    right_top    = (cx + half_w // 2, cy + height)

    glColor3f(r, g, b) # Set catcher color
    draw_midpoint_line(*left_bottom, *right_bottom)
    draw_midpoint_line(*left_top, *right_top)
    draw_midpoint_line(*left_top, *left_bottom)
    draw_midpoint_line(*right_top, *right_bottom)

def draw_buttons():
    """Draws the UI buttons (Restart, Pause, Exit) as seen in the screenshot."""
    # Restart Button (Light Blue Arrow)
    glColor3f(0.0, 1.0, 1.0) # Cyan/Light Blue
    draw_midpoint_line(50, height - 40, 20, height - 55)
    draw_midpoint_line(20, height - 55, 50, height - 70)

    # Pause/Play Button (Orange)
    glColor3f(1.0, 0.5, 0.0) # Orange
    if paused:
        # Draw Play icon (a triangle)
        draw_midpoint_line(width//2 - 10, height - 70, width//2 - 10, height - 40)
        draw_midpoint_line(width//2 - 10, height - 70, width//2 + 10, height - 55)
        draw_midpoint_line(width//2 - 10, height - 40, width//2 + 10, height - 55)
    else:
        # Draw Pause icon (two vertical bars)
        draw_midpoint_line(width//2 - 10, height - 70, width//2 - 10, height - 40)
        draw_midpoint_line(width//2 + 5, height - 70, width//2 + 5, height - 40)

    # Exit Button (Red Cross)
    glColor3f(1.0, 0.0, 0.0) # Red
    draw_midpoint_line(width - 20, height - 70, width - 50, height - 40)
    draw_midpoint_line(width - 50, height - 70, width - 20, height - 40)

# ==========================
# GAME LOGIC AND STATE
# ==========================

def check_collision():
    """Checks for AABB collision between the diamond and the catcher."""
    catcher_w, catcher_h = 100, 30
    d_left = diamond_x - diamond_size
    d_right = diamond_x + diamond_size
    d_bottom = diamond_y - diamond_size
    
    c_left = catcher_x - catcher_w // 2
    c_right = catcher_x + catcher_w // 2
    c_top = catcher_y + catcher_h

    # A simple Axis-Aligned Bounding Box (AABB) collision check
    return (d_right > c_left and d_left < c_right and d_bottom < c_top)

def reset_diamond():
    """Resets the diamond to a new random position at the top of the screen."""
    global diamond_x, diamond_y
    diamond_x = random.randint(50, width - 50)
    diamond_y = height

def increase_score():
    """Increments the score and gradually increases the diamond's speed."""
    global score, diamond_speed
    score += 1
    diamond_speed += 5 # Increase speed by a smaller amount for gradual difficulty
    print(f"Score: {score}")

def idle():
    """
    The main game loop, called continuously by GLUT.
    Handles animation and game state updates.
    """
    global diamond_y, last_time, game_over

    # If paused or game is over, do not update game state
    if paused or game_over:
        last_time = time.time()
        return

    # Calculate delta time (dt) for frame-rate independent movement
    now = time.time()
    dt = now - last_time
    last_time = now

    # Move diamond down based on speed and time
    diamond_y -= diamond_speed * dt

    # If diamond is missed, end the game
    if diamond_y + diamond_size < 0:
        game_over = True
        print(f"Game Over! Final score: {score}")

    # If diamond is caught, increase score and reset diamond
    if not game_over and check_collision():
        increase_score()
        reset_diamond()

    glutPostRedisplay() # Request a redraw of the screen

def display():
    """The main display callback function to draw everything."""
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    # Draw catcher - make it red if the game is over
    if game_over:
        draw_catcher(catcher_x, catcher_y, 100, 30, 1, 0, 0) # Red
    else:
        draw_catcher(catcher_x, catcher_y, 100, 30, 1, 1, 1) # White

    # Draw the diamond only if the game is not over
    if not game_over:
        draw_diamond(diamond_x, int(diamond_y), diamond_size)

    # Always draw the UI buttons
    draw_buttons()

    glFlush() # Ensure all drawing commands are executed

# ==========================
# USER INPUT HANDLING
# ==========================

def mouse_click(button, state, x, y):
    """Handles mouse clicks to interact with UI buttons."""
    global paused, game_over, score, diamond_speed, catcher_x

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        # Convert GLUT's top-left y-coordinate to bottom-left
        mouse_y = height - y

        # Restart button click area
        if 20 <= x <= 50 and (height - 70) <= mouse_y <= (height - 40):
            print("Restarting game...")
            game_over = False
            score = 0
            diamond_speed = 100
            catcher_x = width // 2
            reset_diamond()

        # Pause/Play button click area
        elif (width//2 - 10) <= x <= (width//2 + 10) and (height - 70) <= mouse_y <= (height - 40):
            paused = not paused
            print("Game Paused" if paused else "Game Resumed")

        # Exit button click area
        elif (width - 50) <= x <= (width - 20) and (height - 70) <= mouse_y <= (height - 40):
            print(f"Exiting. Final score: {score}")
            glutLeaveMainLoop()

def keyboard(key, x, y):
    """Handles standard keyboard presses (e.g., ESC to exit)."""
    if key == b'\x1b': # ASCII for ESC key
        glutLeaveMainLoop()

def special_keys(key, x, y):
    """Handles special keyboard presses (e.g., arrow keys for movement)."""
    global catcher_x
    if paused or game_over:
        return # Disable movement when paused or game is over

    if key == GLUT_KEY_LEFT:
        catcher_x -= catcher_speed
        if catcher_x < 50: catcher_x = 50 # Prevent moving off-screen
    elif key == GLUT_KEY_RIGHT:
        catcher_x += catcher_speed
        if catcher_x > width - 50: catcher_x = width - 50 # Prevent moving off-screen
    
    glutPostRedisplay()

# ==========================
# MAIN EXECUTION
# ==========================
def main():
    """Initializes GLUT and starts the main game loop."""
    glutInit()
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(width, height)
    glutCreateWindow(b"Catch the Diamonds!") # Set window title
    init()

    # Register all the callback functions
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(special_keys)
    glutMouseFunc(mouse_click)
    glutIdleFunc(idle)

    glutMainLoop() # Start the GLUT event processing loop

if __name__ == "__main__":
    main()