import sys
from typing import Set
import pygame
import settings
from pygame.constants import K_DOLLAR, K_DOWN, K_LEFT, K_RIGHT, K_UP, KEYDOWN, WINDOWHITTEST, K_a, K_s, K_w
from ship import Ship
from bullet import Bullet
from super_bullet import SuperBullet
from alien import Alien
from time import sleep
from game_stats import GameStats

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
        self.stats = GameStats(self)

    def run_game(self):
        """Start the main loop for the game."""
        self._create_fleet()
        while True:
            self._check_events()
            self._update_aliens()
            self._update_screen()




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
                if event.key == pygame.K_e:
                    self._fire_super_bullet()
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
        self._update_bullets()
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

    def _update_aliens(self):
        """ update the alien fleet """
        self._check_fleet_edge()
        self.aliens.update()
        if self._detect_alian_ship_collision():
            self._ship_hit()

    def _check_fleet_edge(self):
        """ handle aliens on edges """
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """ drop the fleet one line and change the direction """
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _fire_bullet(self):
        """A method to shoot a bullet from the spaceship"""
        bullet = Bullet(self)
        self.bullets.add(bullet)

    def _fire_super_bullet(self):
        bullet = SuperBullet (self)
        self.bullets.add(bullet)

    def _update_bullets(self):
        """ update bullets position and remove old bullets """
        for bullet in self.bullets.sprites():
            bullet.draw()
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._detect_bullet_alian_collision()
    
    def _detect_bullet_alian_collision(self):
        """ as the name sugests """
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()

    def _detect_alian_ship_collision(self):
        """ same """
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            print("Game Over")
            return True
        return False

    def _ship_hit(self):
        """ handles ship being hit """
        self.stats -= 1
        self.aliens.empty()
        self.bullets.empty()
        self._create_fleet()
        self.ship.center_ship()
        sleep(.5)

    def _check_aliens_bottom(self):
        """ checks if aliens have reached the bottom of the screen """
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()