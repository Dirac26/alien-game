import pygame
from pygame import sprite
from pygame.sprite import Sprite

class SuperBullet(Sprite):
    def __init__(self, ai_game):
        """Init method"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color
        self.rect = pygame.Rect(0, 0, 800, 100)
        self.rect.midtop = ai_game.ship.rect.midtop
        self.y = float(self.rect.y)
    
    def update(self):
        """Update the bulit position"""
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y
    
    def draw(self):
        """Draw the bullet"""
        pygame.draw.rect(self.screen, self.color, self.rect)