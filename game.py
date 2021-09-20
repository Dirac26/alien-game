import sys
from typing import Set
import pygame
import settings
from pygame.constants import K_DOLLAR, K_DOWN, K_LEFT, K_RIGHT, K_UP, KEYDOWN, WINDOWHITTEST, K_a, K_s, K_w
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    """Overall class to manage game assets and behavior."""
    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = settings.Settings()
        self.screen = pygame.display.set_mode((self.settings.width, self.settings.height))
        pygame.display.set_caption("Alien Invasion")
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

    def run_game(self):
        """Start the main loop for the game."""
        self._create_fleet()
        while True:
            self._check_events()
            self._update_screen()
            self._remove_old_bullets()



    def _check_events(self):
        """A helper method that checks pygame events"""
        key_on_dict = {'right': False, 'left': False, 'up': False, 'down': False}
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_RIGHT, pygame.K_a]:
                    key_on_dict['right'] = True
                if event.key in [pygame.K_UP, pygame.K_w]:
                    key_on_dict['up'] = True
                if event.key in [pygame.K_LEFT, pygame.K_d]:
                    key_on_dict['left'] = True
                if event.key in [pygame.K_DOWN, pygame.K_s]:
                    key_on_dict['down'] = True
                if event.key == pygame.K_SPACE:
                    self._fire_bullet()
            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_RIGHT, pygame.K_a]:
                    key_on_dict['right'] = False
                if event.key in [pygame.K_UP, pygame.K_w]:
                    key_on_dict['up'] = False
                if event.key in [pygame.K_LEFT, pygame.K_d]:
                    key_on_dict['left'] = False
                if event.key in [pygame.K_DOWN, pygame.K_s]:
                    key_on_dict['down'] = False
        for direction in key_on_dict:
            if key_on_dict[direction]:
                if direction == 'right':
                    self.ship.speed = (self.ship.speed[0] + self.settings.ship_acceleration, self.ship.speed[1])
                if direction == 'up':
                    self.ship.speed = (self.ship.speed[0], self.ship.speed[1] - self.settings.ship_acceleration)
                if direction == 'left':
                    self.ship.speed = (self.ship.speed[0] -self.settings.ship_acceleration, self.ship.speed[1])
                if direction == 'down':
                    self.ship.speed = (self.ship.speed[0], self.ship.speed[1] + self.settings.ship_acceleration)
        self.ship.update()
    def _update_screen(self):
        """A helper method to update the screen with the game objects and background"""
        self.screen.fill(self.settings.background_color)
        self.bullets.update()
        self.ship.blitm()
        for bullet in self.bullets.sprites():
            bullet.draw()
        self.aliens.draw(self.screen)
        pygame.display.flip()

    def _create_fleet(self):
        """A method to create alien fleet"""

        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        ship_height = self.ship.rect.height
        available_space_y = (self.settings.height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Helper method to make one alien with index num"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien_height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _fire_bullet(self):
        """A method to shoot a bullet from the spaceship"""
        bullet = Bullet(self)
        self.bullets.add(bullet)

    def _remove_old_bullets(self):
        """delete the bullets out of the screen"""
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()