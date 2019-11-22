"""
    Result Scene Module (Subclass of Scenebase)
"""
import csv
from datetime import date
from .scene_base import *


class ResultScene(SceneBase):
    """Result Scene Instance Class"""
    
    def __init__(self, player1_pts, player2_pts):
        SceneBase.__init__(self)
        
        # Set screen dimension attributes
        self.screen_width = R_SCREEN_WIDTH
        self.screen_height = R_SCREEN_HEIGHT
        
        # Player point attributes
        self.player1_pts = player1_pts
        self.player2_pts = player2_pts
        
        # Call store result static method
        self.store_result(player1_pts, player2_pts)

    @staticmethod
    def store_result(player1_pts, player2_pts):
        with open('highscore_list.csv', mode='w') as csv_file:
            fieldnames = ['Name', 'Score', 'Date']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerow({'Name': 'xXnoChance', 'Score': player1_pts, 'Date': date.today()})
            writer.writerow({'Name': 'xXyouBet', 'Score': player2_pts, 'Date': date.today()})

    def Render(self, screen):
        """Render the screen and show game results"""
        screen.set_mode((self.screen_width, self.screen_height))
        screen.get_surface().fill(GREEN)

        self.draw_text(screen, "GAME RESULTS",
                       (self.screen_width / 2, self.screen_height / 5),
                       self.font_arial_black_large, BLACK)

        self.draw_text(screen, f"Player 1 Score = {self.player1_pts} points",
                       (self.screen_width / 2, self.screen_height / 2.5),
                       self.font_arial_black, BLACK)

        self.draw_text(screen, f"Player 2 Score = {self.player2_pts} points",
                       (self.screen_width/2, self.screen_height/1.5),
                       self.font_arial_black, BLACK)
