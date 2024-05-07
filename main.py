import pygame
from pygame import Color
import random
from snake_class import Snake
import settings
from queue import Queue

class Food:
    def __init__(self) -> None:
        self.scale = settings.scale
        self.respawn()
        
    def respawn(self):
        self.column = random.randint(0, settings.columns - 1)
        self.row = random.randint(0, settings.columns - 1)
        self.x = self.column * settings.scale
        self.y = self.row * settings.scale
        self.surface = pygame.Surface((self.scale, self.scale))
        self.surface.fill(Color("red"))
        self.rect = self.surface.get_rect(center=(self.x, self.y))
        '''
        CURSOR PARKING
        
        '''


def main():
    
    settings.init()
    pygame.init()
    
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
        
if __name__=="__main__":
    main()