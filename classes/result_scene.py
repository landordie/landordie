"""
Result scene class
"""
import csv
from datetime import date

import pymysql

from .scene_base import *
from .button import *
from .star_field import StarField


class ResultScene(SceneBase):
    def __init__(self, player1_pts, player2_pts):
        SceneBase.__init__(self)
        self.player1_pts = player1_pts
        self.player2_pts = player2_pts
        self.background = pygame.image.load('frames/splash_BG.jpg')
        self.star_field = StarField(self.screen_width, self.screen_height)

        self.menu_button = Button(
            (self.screen_width / 2 - (BUTTON_WIDTH / 2), self.screen_height / 1.2, BUTTON_WIDTH, BUTTON_HEIGHT),
            YELLOW, 'Main Menu')
        # Hold the names of the two players
        self.player1_name = ""
        self.player2_name = ""
        # Holds a value to determine which player's name is being received as input
        self.player_no = 1
        self.status = ''

        if SceneBase.logged_in[0] or SceneBase.logged_in[1]:  # If we are logged in and the game has finished, save the scores to the DB)
            self.connect_DB()

    # A method to populate player names from user input and display them on the screen
    def get_player_name(self, event):
        if event.type == pygame.KEYDOWN:
            # If a player has finished writing their name
            if event.key == pygame.K_RETURN and self.player_no < 3:
                if self.player_no == 1 and len(self.player1_name) == 0:
                    self.player1_name = "DEFAULT_PLAYER1"
                elif self.player_no == 2 and len(self.player2_name) == 0:
                    self.player2_name = "DEFAULT_PLAYER2"
                self.player_no += 1
            # If player 1 is writing
            elif self.player_no == 1:
                # If the pressed button corresponds to a alphabetical char (a,b,c,d...,x,y,z)
                if event.unicode.isalnum() and len(self.player1_name) < 16:
                    self.player1_name += event.unicode
                # If the user would like to delete a char from the screen
                elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                    self.player1_name = self.player1_name[:-1]
            # If player two is writing
            elif self.player_no == 2:
                if event.unicode.isalnum() and len(self.player2_name) < 16:
                    self.player2_name += event.unicode
                elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                    self.player2_name = self.player2_name[:-1]

    def store_result(self):  # This method saves the current scores to a local .csv file
        with open('highscore_list.csv', mode='a') as csv_file:
            fieldnames = ['Name', 'Score', 'Date']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerow({'Name': self.player1_name, 'Score': self.player1_pts, 'Date': date.today()})
            writer.writerow({'Name': self.player2_name, 'Score': self.player2_pts, 'Date': date.today()})

    def ProcessInput(self, events, pressed_keys):
        for event in events:
            # Check for the menu button click
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.menu_button.on_click(event):
                from classes import MenuScene
                self.SwitchToScene(MenuScene.getInstance())
            else:
                # Otherwise get player names if local storage will be used
                if not SceneBase.logged_in:
                    if self.player_no == 1:
                        self.get_player_name(event)
                    elif self.player_no == 2:
                        self.get_player_name(event)

    def Update(self):
        pass

    def Render(self, screen):
        # Render the background and star field
        screen.set_mode((self.screen_width, self.screen_height))
        screen.get_surface().blit(self.background, (0, 0))
        self.star_field.draw_stars(screen.get_surface())

        self.display_scene(screen)  # Display the scene specific content (depends on the storage to be used)

        # Handle the menu button
        self.menu_button.update(screen.get_surface())

    def display_scene(self, screen):
        # Display main messages
        self.draw_text(screen, "GAME RESULTS",
                       (self.screen_width / 2, self.screen_height / 5),
                       self.press2s, CYAN)

        self.draw_text(screen, f"Player 1 Score = {self.player1_pts} points",
                       (self.screen_width / 2, self.screen_height / 2.5),
                       self.press2s, CYAN)

        self.draw_text(screen, f"Player 2 Score = {self.player2_pts} points",
                       (self.screen_width / 2, self.screen_height / 1.5),
                       self.press2s, CYAN)

        # If not logged in ask for user names for both players for the .cvs safe
        if not SceneBase.logged_in:
            self.draw_text(screen, "Please type your name or initials.", (self.screen_width / 2, self.screen_height / 4),
                           self.font_medium, CYAN)
            self.draw_text(screen, "As you start typing, your name will appear "
                                   "on the screen", (self.screen_width / 2, self.screen_height / 3.33), self.font_medium,
                           CYAN)
            self.draw_text(screen, "To confirm press ENTER | To delete a character use BACKSPACE",
                           (self.screen_width / 2, self.screen_height / 2.85), self.font_medium, CYAN)
            self.draw_text(screen, "Name >>", (self.screen_width / 2.45, self.screen_height / 2.15), self.font_medium, CYAN)
            self.draw_text(screen, "Name >>", (self.screen_width / 2.45, self.screen_height / 1.35), self.font_medium, CYAN)

            # Two blocks displaying the names of the players
            block = self.font_medium.render(self.player1_name, True, CYAN)
            rect = block.get_rect()
            rect.left = self.screen_width / 2.15
            rect.top = self.screen_height / 2.21

            block2 = self.font_medium.render(self.player2_name, True, CYAN)
            rect2 = block2.get_rect()
            rect2.left = self.screen_width / 2.15
            rect2.top = self.screen_height / 1.38

            screen.get_surface().blit(block, rect)
            screen.get_surface().blit(block2, rect2)

            # Variable player_no changes on every press of the button Enter until it is equal to 4
            if self.player_no == 3:
                self.store_result()
                self.player_no += 1
        else:
            # If the user decides to save scores to the DB, blit status
            self.draw_text(screen, self.status,
                           (self.screen_width / 2, self.screen_height / 3.33), self.font_medium, CYAN)

    def connect_DB(self):  # Method to connect to the database and update the score of the current user
        try:  # Try to connect to DB
            connection = pymysql.connect(host='localhost', user='root', password='', db='users')
            try:
                with connection.cursor() as cursor:  # Create a cursor object
                    # Write SQL statement, execute and commit the changes
                    sql = "UPDATE `users` SET `Score`=%s WHERE Username='%s'" % (self.player1_pts, SceneBase.credentials[0])
                    cursor.execute(sql)
                    connection.commit()
                    self.status = 'Scores for player [%s] updated successfully!' % SceneBase.credentials[0]
            finally:
                connection.close()  # Always close the connection
        except pymysql.err.OperationalError:  # If error occurs with the connection to the DB, notify user
            self.status = 'The server is currently offline. Please try again later.'
