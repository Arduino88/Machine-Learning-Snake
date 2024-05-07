import pygame
from pygame import Color, Surface
import settings

settings.init()
class Snake:
    
    def __init__(self) -> None:
        self.head_column = settings.startposx
        self.head_row = settings.startposy
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
        if self.head_column > settings.columns - 1 or self.head_column < 0 or self.head_row > settings.columns - 1 or self.head_row < 0:
            print('Off Screen')
            exit()
        
        for segment in self.segments:
            if self.head_column == segment.column and self.head_row == segment.row:
                print('Hit itself')
                exit()

class Segment:
    def __init__(self) -> None:
        self.lifespan = None
        self.collision = False
        self.scale = settings.scale
        
    def create(self, column, row, head: bool = False) -> None:
        self.column = column
        self.row = row
        self.x = self.column * self.scale
        self.y = self.row * self.scale
        self.surface = pygame.Surface([self.scale, self.scale])
        self.surface.fill(Color("grey"))
        self.rect = self.surface.get_rect()
        self.rect = self.surface.get_rect(center=(self.x, self.y))

        self.is_head = head
        self.collision = False