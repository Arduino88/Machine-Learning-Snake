import pygame
from pygame import Color
import random
import settings
from NeuralNetwork import NeuralNetwork, DenseLayer, Perceptron, sigmoid, relu, softmax
import numpy as np

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


    def isValid(self, coords):
        
        if (
            coords[0] >= self.size or 
            coords[0] < 0 or 
            coords[1] >= self.size or 
            coords[1] < 0
        ):
            return False
        
        if self.grid[coords[0]][coords[1]] > 0:
            return False
        
        return True
    


    def tick(self):
        growTick = False
        self.snake.move()
        print(self.snake.head_coords)
        
        if not self.isValid(self.snake.head_coords):
            self.gameOver()

        elif self.snake.head_coords == self.food.pos:
            self.spawnFood()
            self.grid[self.food.pos[0]][self.food.pos[1]] = -1
            self.snake.grow()
            growTick = True
            self.score += 1


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

    def snakeDistToFood(self):
        return abs(self.snake.head_coords[0] - self.food.pos[0]) + abs(self.snake.head_coords[1] - self.food.pos[1])
    
    def getDanger(self) -> tuple:
        danger = [0, 0, 0, 0]

    
        if not self.isValid((self.snake.head_coords[0] - 1, self.snake.head_coords[1])):
            danger[0] = 1
        
        if not self.isValid((self.snake.head_coords[0] + 1, self.snake.head_coords[1])):
            danger[1] = 1

        if not self.isValid((self.snake.head_coords[0], self.snake.head_coords[1] - 1)):
            danger[2] = 1

        if not self.isValid((self.snake.head_coords[0], self.snake.head_coords[1] + 1)):
            danger[3] = 1

        match self.snake.direction:
            case 'up':
                danger[0] = 0
            case 'down':
                danger[1] = 0
            case 'right':
                danger[2] = 0
            case 'left':
                danger[3] = 0

        return tuple(danger)



    def getState(self):
        up = 0
        down = 0
        left = 0
        right = 0
        dangerLeft, dangerRight, dangerUp, dangerDown = self.getDanger()
        foodDist = self.snakeDistToFood()
        match self.snake.direction:
            case 'up':
                up = 1
            case 'down':
                down = 1
            case 'right':
                right = 1
            case 'left':
                left = 1

        return (dangerLeft, dangerRight, dangerUp, dangerDown, foodDist, up, down, left, right)

class Agent:
    def __init__(self) -> None:
        self.brain = NeuralNetwork()
        self.brain.addLayer(DenseLayer(18, 9, activation='sigmoid'))
        self.brain.addLayer(DenseLayer(10, 18, activation='sigmoid'))
        self.brain.addLayer(DenseLayer(10, 10, activation='sigmoid'))
        self.brain.addLayer(DenseLayer(4, 10, activation='softmax'))

    def action(self, state): 
        return self.brain.forwardPropagate(state)
                
if __name__=="__main__":

    testAgent = Agent()

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


                                
        state = np.array(game.getState())
        action = testAgent.action(state)
        print(action)
        selectedActionIndex = np.argmax(action)
        print(selectedActionIndex)

        match selectedActionIndex:
            case 0:
                game.snake.direction = 'up'
            case 1:
                game.snake.direction = 'down'
            case 2:
                game.snake.direction = 'left'
            case 3:
                game.snake.direction = 'right'

        
        # clear screen
        pygame.draw.rect(game.screen,(100, 100, 90), [0, 0 , settings.columns * settings.scale, settings.columns * settings.scale])
                
        game.tick()
        
                    
        
            # draw the segment
        pygame.display.flip()
        #pygame.time.delay(settings.delay)
        