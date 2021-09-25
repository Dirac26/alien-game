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
        self.settings = ai_game.settings
    def update(self):
        """ move alian """
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x
    
    def check_edges(self):
        screen_rect = self.screen.get_rect()
        """ check if alien hits the edge """
        if self.rect.right > screen_rect.right or self.rect.left <= 0:
           return True