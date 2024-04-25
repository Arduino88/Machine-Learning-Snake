# import the pygame module, so you can use it
import pygame
from pygame import Color
import random
from snake_class import Segment

scale = 50 # Pixels per column
columns = 20 # Columns in the window
rows = 20 # Rows in the window
delay = 75 # milliseconds between each frame

class Food:
    def __init__(self) -> None:
        self.scale = scale
        self.respawn()
        
    def respawn(self):
        self.column = random.randint(0, columns - 1)
        self.row = random.randint(0, columns - 1)
        self.x = self.column * scale
        self.y = self.row * scale
        self.surface = pygame.Surface((self.scale, self.scale))
        self.surface.fill(Color("red"))
        self.rect = self.surface.get_rect(center=(self.x, self.y))
        
        """_summary_
        mouse parking:
        ss
    
        
        """
        
    
        


        
        

    


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

    screen = pygame.display.set_mode((columns * scale, columns * scale))
    screen.fill((100, 100, 100))
             
    
    

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
                    
        pygame.draw.rect(screen,(100, 100, 90), [0, 0 , columns * scale, columns * scale])
            
        for segment in snake.segments:
            
            if food.column == segment.column and food.row == segment.row:
                snake.grow()
                food.respawn()
        
            screen.blit(segment.surface, (segment.column * scale, segment.row * scale))
        screen.blit(food.surface, (food.x, food.y))
        pygame.display.flip()
        snake.check_collision()
        pygame.time.delay(delay)
        
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()