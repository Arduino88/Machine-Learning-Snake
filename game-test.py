# import the pygame module, so you can use it
import pygame
from pygame import Color
import random

startposx = 2
startposy = 2
scale = 50 # Pixels per column

class Food:
    def __init__(self) -> None:
        self.respawn()
    
    def respawn(self):
        self.column = random.randint(1, 20)
        self.row = random.randint(1, 20)
        self.x = self.column * 50
        self.y = self.row * 50
        self.surface = pygame.Surface((50, 50))
        self.surface.fill(Color("red"))
        self.rect = self.surface.get_rect()
        self.rect.topleft = (self.x, self.y)
        
    

class Segment:
    def __init__(self) -> None:
        self.lifespan = None
        self.collision = False
        
    def create(self, column, row, head: bool = False) -> None:
        self.column = column
        self.row = row
        self.x = self.column * 50
        self.y = self.row * 50
        self.surface = pygame.Surface([30,30])
        self.surface.fill(Color("grey"))
        self.rect = self.surface.get_rect()
        self.rect.center = (self.x, self.y)
        self.is_head = head
        self.collision = False
        
    
        

class Snake:
    def __init__(self) -> None:
        self.head_column = startposx
        self.head_row = startposy
        self.segments = []
        self.direction = "right"
        self.speed = 1
        self.length = 3
        
    def grow(self) -> None:
        self.length += 1
        
        
    def move(self) -> None:
        
        self.segments.append(Segment())
        self.segments[-1].create(column=self.head_column, row=self.head_row, head=False)
        
        
        if self.direction == "right":
            self.head_column += self.speed
        elif self.direction == "left":
            self.head_column -= self.speed
        elif self.direction == "up":
            self.head_row -= self.speed
        elif self.direction == "down":
            self.head_row += self.speed
        
        if len(self.segments) > self.length:
            self.segments.pop(0)

    
    
    
    def check_collision(self):
        if self.head_column > 20 or self.head_column < 0 or self.head_row > 20 or self.head_row < 0:
            print('Off Screen')
            exit()
        
        for segment in self.segments:
            if self.head_column == segment.column and self.head_row == segment.row:
                print('Hit itself')
                exit()
        
        

    


# define a main function
def main():
    
    # initialize the pygame module
    pygame.init()
    # load and set the logo
    pygame.display.set_caption("minimal program")
    snake = Snake()
    food = Food()
    for i in range(snake.length):
        snake.grow()
    # create a surface on screen that has the size of 240 x 180
    screen = pygame.display.set_mode((1000,1000))
    screen.fill((100, 100, 100))
    
    
    # define the position of the sprite
    # how many pixels to move the each frame
    step_x = 0
    step_y = 0
             
    
    

    # define a variable to control the main loop
    running = True
    

    # main loop
    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
            

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.key.key_code('d'):
                    if snake.direction != 'left':
                        snake.direction = 'right'
                elif event.key == pygame.key.key_code('a'):
                    if snake.direction != 'right':
                        snake.direction = 'left'
                elif event.key == pygame.key.key_code('w'):
                    if snake.direction != 'down':
                        snake.direction = 'up'
                elif event.key == pygame.key.key_code('s'):
                    if snake.direction != 'up':
                        snake.direction = 'down'
                
        
                
            # check if the smiley is still on screen, if not change direction

        

        snake.move()
                        

                    
        
        pygame.draw.rect(screen,(100, 100, 90), [0, 0 , 1000, 1000])
            
        for segment in snake.segments:
            
            if food.column == segment.column and food.row == segment.row:
                snake.grow()
                food.respawn()
        
            screen.blit(segment.surface, (segment.column * scale, segment.row * scale))
        screen.blit(food.surface, (food.x, food.y))
        pygame.display.flip()
        snake.check_collision()
        pygame.time.delay(75)
        
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()