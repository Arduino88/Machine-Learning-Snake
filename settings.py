def init():
    global columns, rows, delay, scale, stat_coords, speed, start_length
    columns = 20
    rows = 20 # Rows in the window
    delay = 100 # milliseconds between each frame
    scale = 35 # Pixels per column
    start_coords = (2, 2)
    speed = 1
    start_length = 3