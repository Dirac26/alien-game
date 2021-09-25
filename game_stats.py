import pygame

class GameStats:
    """ a class to track game statistics """
    def __init__(self, ai_game):
        """ init method """
        self.settings = ai_game.settings
        self.reset_stats()
    
    def reset_stats(self):
        """ reset game status """
        self.ships_left = self.settings.ships_limit