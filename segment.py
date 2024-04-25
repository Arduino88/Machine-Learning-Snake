import pygame
from pygame import Color
import random


class Segment:
    def __init__(self) -> None:
        self.lifespan = None
        self.collision = False
        self.scale = 50
        
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