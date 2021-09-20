import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """Class for alien ships"""
    def __init__(self, ai_game):
        """init method"""
        super().__init__()
        self.screen = ai_game.screen
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()
        self.width = self.rect.width
        self.height = self.rect.height
        self.x = self.rect.x