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

