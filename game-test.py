# import the pygame module, so you can use it
import pygame
from pygame import Color
import random

distance = 50
startposx = 100
startposy = 100

class Food:
    def __init__(self) -> None:
        self.x = 50*random.randint(1, 20)
        self.y = 50*random.randint(1, 20)
        self.surface = pygame.Surface([50,50])
        self.surface.fill(Color("red"))
        self.rect = self.surface.get_rect()
        self.rect.topleft = (self.x, self.y)
        
        pass
    
    
    def respawn(self):
        self.column = random.randint(1, 20)
        self.row = random.randint(1, 20)
        self.x = 50 * self.column
        self.y = 50 * self.row
        self.surface.fill(Color("red"))
        self.rect = self.surface.get_rect()
        self.rect.topleft = (self.x, self.y)
        pass
        
    
    

class Segment:
    def __init__(self) -> None:
        self.lifespan = None
        self.collision = False
        
    def create(self, lifespan: int, x, y, head: bool = False) -> None:
        self.column: int
        self.row: int
        self.x = self.column * 50
        self.y = self.row * 50
        self.lifespan = lifespan
        self.surface = pygame.Surface([50,50])
        self.surface.fill(Color("orange"))
        self.rect = self.surface.get_rect()
        self.is_head = head
        self.collision = False

    def activate_collision(self):
        if not self.is_head:
            self.collision = True
            self.surface.fill(Color('green'))
        
        
    def is_alive(self) -> bool:
        self.lifespan -= 1
        if self.lifespan <= 0:
            return False
        else:
            return True
        
        

class Snake:
    def __init__(self) -> None:
        self.head = Segment()
        self.head.create(lifespan=None, x=startposx, y=startposy, head=True) 
        self.segments = []
        self.direction = "right"
        self.speed = 50
        self.length = 3
        
    def grow(self) -> None:
        self.length += 1
        for segment in self.segments: #Iterate through all segments and extend their lifespan by one tick
            segment.lifespan += 1
        
        
    def move(self) -> None:
        for segment in self.segments:
            if not segment.is_alive():
                self.segments.pop(0)
        
        self.segments.append(Segment())
        self.segments[-1].create(lifespan=self.length, x=self.head.x, y=self.head.y, head=False)
        
        
        
        if self.direction == "right":
            self.head.x += self.speed
        elif self.direction == "left":
            self.head.x -= self.speed
        elif self.direction == "up":
            self.head.y -= self.speed
        elif self.direction == "down":
            self.head.y += self.speed
        
        
        pass
    
    
    
    def check_collision(self):
        if self.head.x > 1000 or self.head.x < 0 or self.head.y > 1000 or self.head.y < 0:
            print('Collision')
            exit()
        
        for segment in self.segments:
            if self.head.rect.colliderect(segment.rect) and segment.collision:
                print('Collision with snake body')
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
             
    
    
    
    screen.blit(snake.head.surface, (50,50))
    # define a variable to control the main loop
    running = True
    
    
    pygame.display.flip()
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
        snake.check_collision()
        
        if snake.head.rect.colliderect(food.rect):
            food.respawn()
            snake.grow()
        
        pygame.draw.rect(screen,(200, 180, 90), [0, 0 , 1000, 1000])
        screen.blit(snake.head.surface, (snake.head.x,snake.head.y))
            
        for segment in snake.segments:
            screen.blit(segment.surface, (segment.x, segment.y))
        screen.blit(food.surface, (food.x, food.y))
        pygame.display.flip()
        pygame.time.delay(100)
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()