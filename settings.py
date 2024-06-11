def init():
    global columns, rows, delay, scale, start_coords, speed, start_length, tileSize, pixelScale, startDirection, gameSize, startingMoves, mutationRate
    columns = 20
    rows = 20 # Rows in the window
    delay = 100 # milliseconds between each frame
    scale = 35 # Pixels per column
    start_coords = (10, 10)
    speed = 1
    start_length = 3
    tileSize = 30
    pixelScale = 30
    startDirection = 'down'
    gameSize = 20
    startingMoves = 200
    mutationRate = 0.1