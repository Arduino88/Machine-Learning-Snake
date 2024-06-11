import pygame
from pygame import Color
import random
import math
import copy
import settings
from NeuralNetwork import NeuralNetwork, DenseLayer, Perceptron, sigmoid, relu, softmax
import numpy as np

import torch
import torch.nn as nn
import torch.optim as optim

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
    def __init__(self):
        self.reset()

    def reset(self):
        self.step = 0
        size = settings.gameSize
        self.running = True
        self.score = 0
        self.screen = pygame.display.set_mode((size * settings.pixelScale, size * settings.pixelScale)) #settings.scale might be unused now
        self.screen.fill((100, 100, 100))
        self.moves = settings.startingMoves

        self.size = size
        self.grid = []
        for _ in range(size):
            self.grid.append([0 for _ in range(self.size)])

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
        self.step += 1
        self.moves -= 1
        if self.moves < 0:
            self.running = False
            return

        growTick = False
        self.snake.move()
        #print(self.snake.head_coords)
        
        if not self.isValid(self.snake.head_coords):
            self.gameOver()

        elif self.snake.head_coords == self.food.pos:
            self.spawnFood()
            self.grid[self.food.pos[0]][self.food.pos[1]] = -1
            self.snake.grow()
            growTick = True
            self.score += 5


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
        #print(f"GAME OVER! Your score is {self.score}")
        pygame.event.post(pygame.event.Event(pygame.QUIT))




    def getState(self):
        def snakeDistToFood(row, col):
            return math.sqrt((abs(row - self.food.pos[0])) ** 2 + (abs(col - self.food.pos[1])) ** 2)

        def safeDist(direction: tuple):
            row, col = self.snake.head_coords[0] + direction[0], self.snake.head_coords[1] + direction[1]
            counter = 1
            while 0 <= row < len(self.grid) and 0 <= col < len(self.grid[0]):
                if self.grid[row][col] > 0:
                    break

                row += direction[0]
                col += direction[1]
                counter += 1

            return counter


        directions = ((-1, 0), (1, 0), (0, -1), (0, 1), (1, 1), (-1, -1), (1, -1), (-1, 1))

        foodDistances = []
        for direction in directions:
            foodDistances.append(snakeDistToFood(self.snake.head_coords[0] + direction[0], self.snake.head_coords[1] + direction[1]))

        safeDistances = []
        for direction in directions:
            safeDistances.append(safeDist(direction))
        
        #foodDistances: input list with len 8
        #safeDistances: input list with len 8
        #Total: input list with len 16

        returnList = safeDistances + foodDistances
        return returnList

class Agent:
    def __init__(self, inputCount) -> None:
        self.fitness = 0
        self.brain = NeuralNetwork()
        self.brain.addLayer(DenseLayer(16, inputCount, activation='sigmoid'))
        self.brain.addLayer(DenseLayer(10, 16, activation='sigmoid'))
        self.brain.addLayer(DenseLayer(10, 10, activation='sigmoid'))
        self.brain.addLayer(DenseLayer(4, 10, activation='softmax'))

    def action(self, state): 
        return self.brain.forwardPropagate(state)
                
if __name__=="__main__":

    batchSize = 50
    epochs = 200
    games = [SnakeGame() for _ in range(batchSize)]
    inputCount = 16 # + settings.rows * settings.columns
    agents = [Agent(inputCount) for _ in range(batchSize)]
    
    print(agents, games)

    fitnesses = []

    
    for epoch in range(epochs):
        # EPOCH LOOP
        for i in range(batchSize):

            settings.init()
            pygame.init()

            '''
            Cursor Parking:

            
            '''
            
            pygame.display.set_caption("Snake")
            img = pygame.image.load('snake-icon.png')
            pygame.display.set_icon(img)

            key_queue = []
            

            # main loop
            while games[i].running:
                #for row in game.grid:
                    #print(row)
                
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        games[i].running = False

                initialState = games[i].getState()
                #for x in games[i].grid:
                #   initialState.extend(x)
                state = np.array(initialState)
                #print('agent', i, agents[i])
                action = agents[i].action(state)
                #print(action)
                selectedActionIndex = np.argmax(action)
                #print(selectedActionIndex)

                match selectedActionIndex:
                    case 0:
                        games[i].snake.direction = 'up'
                    case 1:
                        games[i].snake.direction = 'down'
                    case 2:
                        games[i].snake.direction = 'left'
                    case 3:
                        games[i].snake.direction = 'right'

                
                # clear screen
                pygame.draw.rect(games[i].screen,(100, 100, 90), [0, 0 , settings.columns * settings.scale, settings.columns * settings.scale])
                        
                games[i].tick()
                
                            
                
                    # draw the segment
                pygame.display.flip()

                agents[i].fitness = max(games[i].score * 5 + games[i].step / 2, 1)
                #pygame.time.delay(settings.delay)
            
            fitnesses.append(float(agents[i].fitness))

        print(fitnesses)
        print(f'ENDING EPOCH {epoch}')
        for game in games:
            game.reset()


        maxReward = max(fitnesses)
        fitnessSum = sum(fitnesses)
        print('fitness sum', fitnessSum)
        for i in range(len(fitnesses)):
            fitnesses[i] /= fitnessSum


        print('fitness percentages', fitnesses)
        print('sum of fitnesses', sum(fitnesses))
        print('maxReward', maxReward)
        

        #for i in range(1, len(fitnesses)):
        #    fitnesses[i] += fitnesses[i - 1]

        #print(fitnesses)

        newGeneration = []
        for i in range(len(agents)):
            #select parent
            parent = random.choices(agents, weights = fitnesses)[0]

            newGeneration.append(copy.deepcopy(parent))

            newGeneration[-1].brain.mutate()


        agents.clear()
        agents = newGeneration





        fitnesses.clear()
        