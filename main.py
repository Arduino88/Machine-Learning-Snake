import pygame
from pygame import Color
import random
import settings

random.seed(9)

class Food:
    def __init__(self, gridSize):
        self.gridSize = gridSize
        self.respawn()

    def respawn(self):
        self.pos = (random.randint(0, self.gridSize - 1), random.randint(0, self.gridSize - 1))



settings.init()

class Snake:
    
    def __init__(self) -> None:
        self.head_coords = settings.start_coords
        self.direction = settings.startDirection
        self.speed = settings.speed
        self.length = settings.start_length
        
    def grow(self) -> None:
        self.length += 1
        
    def move(self):
        match self.direction:
            case "right":
                self.head_coords = (self.head_coords[0], self.head_coords[1] + 1)
            case "up":
                self.head_coords = (self.head_coords[0] - 1, self.head_coords[1])
            case "down":
                self.head_coords = (self.head_coords[0] + 1, self.head_coords[1])
            case "left":
                self.head_coords = (self.head_coords[0], self.head_coords[1] - 1)

    
    
        



class SnakeGame:
    def __init__(self, size):
        self.running = True
        self.score = 0
        self.screen = pygame.display.set_mode((size * settings.pixelScale, size * settings.pixelScale)) #settings.scale might be unused now
        self.screen.fill((100, 100, 100))

        self.size = size
        self.grid = []
        for i in range(size):
            self.grid.append([0 for x in range(self.size)])

        self.snake = Snake()
        self.food = Food(self.size)
        self.grid[self.food.pos[0]][self.food.pos[1]] = -1

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
            print('hit border')

        elif self.snake.head_coords == self.food.pos:
            self.spawnFood()
            self.grid[self.food.pos[0]][self.food.pos[1]] = -1
            self.snake.grow()
            growTick = True
            self.score += 1

        elif self.grid[self.snake.head_coords[0]][self.snake.head_coords[1]] > 0:
            self.gameOver()
            print('hit snake')
            

        if not growTick and self.running:
            self.grid[self.snake.head_coords[0]][self.snake.head_coords[1]] = self.snake.length + 1 # +1 because immediate decrement
        
        elif self.running:
            self.grid[self.snake.head_coords[0]][self.snake.head_coords[1]] = self.snake.length
        
        if self.running:
            for i, row in enumerate(self.grid):
                for j, tile in enumerate(row):
                    if tile > 0 and not growTick:
                        self.grid[i][j] -= 1

                    elif tile < -1:
                        raise Exception(f"Tile value below -1: ({i}, {j})")
                    
                    match tile:
                        case -1:
                            pygame.draw.rect(self.screen, (0, 255, 0), (j * settings.pixelScale, i * settings.pixelScale, settings.pixelScale, settings.pixelScale))
                        
                        case 0:
                            continue
                        
                        case _:
                            pygame.draw.rect(self.screen, (255, 0, 0), (j * settings.pixelScale, i * settings.pixelScale, settings.pixelScale, settings.pixelScale))
                    
    def gameOver(self):
        self.running = False
        print(f"GAME OVER! Your score is {self.score}")
        pygame.event.post(pygame.event.Event(pygame.QUIT))

                
if __name__=="__main__":

    settings.init()
    pygame.init()

    '''
    Cursor Parking:

    
    '''

    game = SnakeGame(settings.gameSize)
    
    pygame.display.set_caption("Snake")
    img = pygame.image.load('snake-icon.png')
    pygame.display.set_icon(img)

    key_queue = []
    

    # main loop
    while game.running:
        #for row in game.grid:
            #print(row)
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.key.key_code('d'):
                    if game.snake.direction != 'left':
                        key_queue.append('right')
                elif event.key == pygame.key.key_code('a'):
                    if game.snake.direction != 'right':
                        key_queue.append('left')
                elif event.key == pygame.key.key_code('w'):
                    if game.snake.direction != 'down':
                        key_queue.append('up')
                elif event.key == pygame.key.key_code('s'):
                    if game.snake.direction != 'up':
                        key_queue.append('down')
                
        
        if key_queue:
            print(key_queue)
            game.snake.direction = key_queue.pop(-1)
            
        
        # clear screen
        pygame.draw.rect(game.screen,(100, 100, 90), [0, 0 , settings.columns * settings.scale, settings.columns * settings.scale])
                
        game.tick()
        
                    
        
            # draw the segment
        pygame.display.flip()
        pygame.time.delay(settings.delay)
        