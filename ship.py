import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """A class that represents the star ship"""
    def __init__(self, ai_game):
        """init method"""
        super().__init__()
        self.boundaries = [ai_game.settings.width, ai_game.settings.height]
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.acceleration = ai_game.settings.ship_acceleration

        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom
        self.speed = (0, 0)
    def update(self):
        """A method to update the ship position dpeending on its speed"""
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]
        if self.rect.y <= 0:
            self.speed = (self.speed[0], 0)
            self.rect.y = 0
        if self.rect.x <= 0:
            self.speed = (0, self.speed[1])
            self.rect.x = 0
        if self.rect.y >= self.boundaries[1] - self.image.get_height():
            self.speed = (self.speed[0], 0)
            self.rect.y = self.boundaries[1] - self.image.get_height() - 1
        if self.rect.x >= self.boundaries[0] - self.image.get_width():
            self.speed = (0, self.speed[1])
            self.rect.x = self.boundaries[0] - self.image.get_width() - 1

    def blitm(self):
        """Method to draw the ship"""
        self.screen.blit(self.image, self.rect)
    
    def center_ship(self):
        """ move the ship back to center """
        self.rect.midbottom = self.screen.midbottom
        self.x = float(self.rect.x)