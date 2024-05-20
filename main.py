import pygame
from pygame import Color
import random
import settings
from queue import Queue

random.seed(9)

class Food:
    def __init__(self, gridSize):
        self.gridSize = gridSize
        self.respawn()

    def respawn(self):
        self.pos = (random.randint(0, self.gridSize), random.randint(0, self.gridSize))



settings.init()

class Snake:
    
    def __init__(self) -> None:
        self.head_coords = settings.start_coords
        self.direction = "right"
        self.speed = settings.speed
        self.length = settings.start_length
        
    def grow(self) -> None:
        self.length += 1
        
    def move(self):
        match self.direction:
            case "down":
                self.head_coords = (self.head_coords[0] + 1, self.head_coords[1])
            case "up":
                self.head_coords = (self.head_coords[0] - 1, self.head_coords[1])
            case "right":
                self.head_coords = (self.head_coords[0], self.head_coords[1] + 1)
            case "left":
                self.head_coords = (self.head_coords[0], self.head_coords[1] - 1)

    
    
        



class SnakeGame:
    def __init__(self, size):
        self.score = 0
        self.screen = pygame.display.set_mode((size * settings.scale, size * settings.scale))
        self.screen.fill((100, 100, 100))

        self.size = size
        self.grid = []
        for i in range(size):
            self.grid.append([0 for x in range(self.size)])

        self.snake = Snake()
        self.food = Food(self.size)


    def spawnFood(self):
        self.food.respawn()


    def tick(self):
        growTick = False
        self.snake.move()
        print(self.snake.head_coords)
        
        if (
            self.snake.head_coords[0] >= self.size or 
            self.snake.head_coords[0] < 0 or 
            self.snake.head_coords[1] >= self.size or 
            self.snake.head_coords[1] < 0
        ):
            self.gameOver()

        elif self.snake.head_coords == self.food.pos:
            self.spawnFood()
            self.snake.grow()
            growTick = True
            self.score += 1

        elif self.grid[self.snake.head_coords[0]][self.snake.head_coords[1]] > 0:
            self.gameOver()

        self.grid[self.snake.head_coords[0]][self.snake.head_coords[1]] = self.snake.length + 1 # +1 because immediate decrement
        
        self.grid[self.food.pos[0]][self.food.pos[1]] = -1

        for i, row in enumerate(self.grid):
            for j, tile in enumerate(row):
                if tile > 0 and not growTick:
                    self.grid[i][j] -= 1

                elif tile < -1:
                    raise Exception(f"Tile value below -1: ({i}, {j})")
                
                match tile:
                    case -1:
                        pygame.draw.rect(self.screen, (0, 255, 0), (i, j, settings.tileSize, settings.tileSize))
                    
                    case 0:
                        continue
                    
                    case _:
                        pygame.draw.rect(self.screen, (255, 0, 0), (i, j, settings.tileSize, settings.tileSize))
                    
    def gameOver(self):
        global running
        running = False
        print(f"GAME OVER! Your score is {self.score}")

                
if __name__=="__main__":

    settings.init()
    pygame.init()

    game = SnakeGame(6)
    
    pygame.display.set_caption("Snake")
    img = pygame.image.load('snake-icon.png')
    pygame.display.set_icon(img)



             
    key_queue = Queue(maxsize=10)
    
    running = True
    

    # main loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.key.key_code('d'):
                    if game.snake.direction != 'left':
                        key_queue.put('right')
                elif event.key == pygame.key.key_code('a'):
                    if game.snake.direction != 'right':
                        key_queue.put('left')
                elif event.key == pygame.key.key_code('w'):
                    if game.snake.direction != 'down':
                        key_queue.put('up')
                elif event.key == pygame.key.key_code('s'):
                    if game.snake.direction != 'up':
                        key_queue.put('down')
                
        
        if not key_queue.empty():
            #print(key_queue.qsize())
            game.snake.direction = key_queue.get()
        
        # clear screen
        pygame.draw.rect(game.screen,(100, 100, 90), [0, 0 , settings.columns * settings.scale, settings.columns * settings.scale])
                
        game.tick()
        print(game.grid)
                    
        
            # draw the segment
        pygame.display.flip()
        pygame.time.delay(settings.delay)
        