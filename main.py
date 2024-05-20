import pygame
from pygame import Color
import random
import settings
from queue import Queue

random.seed(9)

class Food:
    def __init__(self):
        self.respawn()
        
    def respawn(self, gridSize):
        self.pos = (random.randint(0, gridSize), random.randint(0, gridSize))



settings.init()

class Snake:
    
    def __init__(self) -> None:
        self.head_coords = settings.start_coords
        self.direction = "right"
        self.speed = settings.speed
        self.length = settings.start_length
        
    def grow(self) -> None:
        self.length += 1
        

    
    
        



class SnakeGame:
    def __init__(self, size):
        self.screen = pygame.display.set_mode((size * settings.scale, size * settings.scale))
        self.size = size
        self.grid = []
        for i in range(size):
            self.grid.append([0 for x in range(self.size)])

        self.snake = Snake()
        self.food = Food(self.size)





    def spawnFood():
        pass

    def tick(self): 
        for i, row in enumerate(self.grid):
            for j, tile in enumerate(row):
                if tile > 0:
                    tile -= 1
                
                match tile:
                    case -1:
                        pygame.draw.rect(self.screen, (0, 255, 0), (), )
                    case _:
                        pass
                    

                








if __name__=="__main__":

    settings.init()
    pygame.init()

    game = SnakeGame(6)
    
    pygame.display.set_caption("Snake")
    img = pygame.image.load('snake-icon.png')
    pygame.display.set_icon(img)
    snake = Snake()
    food = Food()
    for i in range(snake.length):
        snake.grow()

    screen = pygame.display.set_mode((settings.columns * settings.scale, settings.columns * settings.scale))
    screen.fill((100, 100, 100))
             
    key_queue = Queue(maxsize=10)
    
    running = True
    

    # main loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.key.key_code('d'):
                    if snake.direction != 'left':
                        key_queue.put('right')
                elif event.key == pygame.key.key_code('a'):
                    if snake.direction != 'right':
                        key_queue.put('left')
                elif event.key == pygame.key.key_code('w'):
                    if snake.direction != 'down':
                        key_queue.put('up')
                elif event.key == pygame.key.key_code('s'):
                    if snake.direction != 'up':
                        key_queue.put('down')
                
        
        if not key_queue.empty():
            #print(key_queue.qsize())
            snake.direction = key_queue.get()
        snake.move()
                    
        # clear screen
        pygame.draw.rect(screen,(100, 100, 90), [0, 0 , settings.columns * settings.scale, settings.columns * settings.scale])
            
        for segment in snake.segments:
            if food.column == segment.column and food.row == segment.row: # if segment is on food
                snake.grow()
                food.respawn()
        
            # draw the segment
            screen.blit(segment.surface, (segment.column * settings.scale, segment.row * settings.scale))
        screen.blit(food.surface, (food.x, food.y))
        pygame.display.flip()
        snake.check_collision()
        pygame.time.delay(settings.delay)
        