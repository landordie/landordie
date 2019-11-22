import csv
from datetime import date
from .scene_base import *


class ResultScene(SceneBase):
    def __init__(self, player1_pts, player2_pts):
        SceneBase.__init__(self)
        self.screen_width = R_SCREEN_WIDTH
        self.screen_height = R_SCREEN_HEIGHT
        # Hold the names of the two players
        self.player1_name = ""
        self.player2_name = ""
        # Holds a value to determine which player's name is being received as input
        self.player_no = 1
        self.player1_pts = player1_pts
        self.player2_pts = player2_pts

    def store_result(self):
        # Write results to a csv file - storing Name, Score, Date
        with open('highscore_list.csv', mode='a') as csv_file:
            fieldnames = ['Name', 'Score', 'Date']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerow({'Name': self.player1_name, 'Score': self.player1_pts, 'Date': date.today()})
            writer.writerow({'Name': self.player2_name, 'Score': self.player2_pts, 'Date': date.today()})

    # A method to populate player names from user input and display them on the screen
    def get_player_name(self, event):
        if event.type == pygame.KEYDOWN:
            # If a player has finished writing their name
            if event.key == pygame.K_RETURN and self.player_no < 3:
                self.player_no += 1
            # If player 1 is writing
            elif self.player_no == 1:
                # If the pressed button corresponds to a alphabetical char (a,b,c,d...,x,y,z)
                if event.unicode.isalpha():
                    self.player1_name += event.unicode
                # If the user would like to delete a char from the screen
                elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                    self.player1_name = self.player1_name[:-1]
            # If player two is writing
            elif self.player_no == 2:
                if event.unicode.isalpha():
                    self.player2_name += event.unicode
                elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                    self.player2_name = self.player2_name[:-1]

    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if self.player_no == 1:
                    self.get_player_name(event)
                elif self.player_no == 2:
                    self.get_player_name(event)

    def Update(self):
        pass

    def Render(self, screen):
        screen.set_mode((self.screen_width, self.screen_height))
        screen.get_surface().fill(GREEN)

        # Two blocks displaying the names of the players
        block = self.font_consolas.render(self.player1_name, True, (0, 0, 0))
        rect = block.get_rect()
        rect.left = self.screen_width/2.5
        rect.top = self.screen_height/2.07

        block2 = self.font_consolas.render(self.player2_name, True, (0, 0, 0))
        rect2 = block2.get_rect()
        rect2.left = self.screen_width/2.5
        rect2.top = self.screen_height/1.28

        screen.get_surface().blit(block, rect)
        screen.get_surface().blit(block2, rect2)

        # Variable player_no changes on every press of the button Enter until it is equal to 4
        if self.player_no == 3:
            self.store_result()
            self.player_no += 1
        if self.player_no > 3:
            self.draw_text(screen, "Results have been saved successfully. Press ESCAPE to exit.",
                           (self.screen_width/2, self.screen_height/1.15), self.font_consolas, BLACK)

        # Bunch of draw methods to display instructions and guidelines on the screen
        self.draw_text(screen, "GAME RESULTS", (self.screen_width / 2, self.screen_height / 5.2),
                       self.font_arial_black_large, BLACK)
        self.draw_text(screen, f"Player 1 Score = {self.player1_pts} points",
                       (self.screen_width / 2, self.screen_height / 2.5),  self.font_verdana, BLACK)
        self.draw_text(screen, f"Player 2 Score = {self.player2_pts} points",
                       (self.screen_width/2, self.screen_height/1.5), self.font_verdana, BLACK)
        self.draw_text(screen, "Please type your name or initials.", (self.screen_width/2, self.screen_height/4), self.font_consolas, BLACK)
        self.draw_text(screen, "As you start typing, your name will appear "
                               "on the screen", (self.screen_width/2, self.screen_height/3.33), self.font_consolas, BLACK)
        self.draw_text(screen, "To confirm press ENTER | To delete a character use BACKSPACE",
                       (self.screen_width/2, self.screen_height/2.85), self.font_consolas, BLACK)
        self.draw_text(screen, "Name: ", (self.screen_width/3, self.screen_height/2), self.font_verdana, BLACK)
        self.draw_text(screen, "Name: ", (self.screen_width/3, self.screen_height/1.25), self.font_verdana, BLACK)


