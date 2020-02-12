import csv
from datetime import date
from .scene_base import *
from .button import *


class ResultScene(SceneBase):
    def __init__(self, player1_pts, player2_pts):
        SceneBase.__init__(self)
        self.screen_width = R_SCREEN_WIDTH
        self.screen_height = R_SCREEN_HEIGHT
        self.player1_pts = player1_pts
        self.player2_pts = player2_pts
        self.store_result(player1_pts, player2_pts)
        self.menu_button = Button(
            (self.screen_width / 2 - (BUTTON_WIDTH / 2), self.screen_height / 2, BUTTON_WIDTH, BUTTON_HEIGHT),
            YELLOW, 'Main Menu')

    @staticmethod
    def store_result(player1_pts, player2_pts):
        with open('highscore_list.csv', mode='w') as csv_file:
            fieldnames = ['Name', 'Score', 'Date']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerow({'Name': 'xXnoChance', 'Score': player1_pts, 'Date': date.today()})
            writer.writerow({'Name': 'xXyouBet', 'Score': player2_pts, 'Date': date.today()})

    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.menu_button.on_click(event):
                from classes import MenuScene
                self.SwitchToScene(MenuScene.getInstance())

    def Update(self):
        pass

    def Render(self, screen):
        screen.set_mode((self.screen_width, self.screen_height))
        screen.get_surface().fill(GREEN)

        self.draw_text(screen, "GAME RESULTS",
                       (self.screen_width / 2, self.screen_height / 5),
                       self.press2s, BLACK)

        self.draw_text(screen, f"Player 1 Score = {self.player1_pts} points",
                       (self.screen_width / 2, self.screen_height / 2.5),
                       self.press2s, BLACK)

        self.draw_text(screen, f"Player 2 Score = {self.player2_pts} points",
                       (self.screen_width / 2, self.screen_height / 1.5),
                       self.press2s, BLACK)

        self.menu_button.update(screen.get_surface())

