"""
'result_scene.py' module.
Used in instantiation of a Result scene (window).
"""
import csv
from datetime import date
import pymysql
from constants import *
from .scene_base import SceneBase
from .button import Button
from .star_field import StarField
from .helper import draw_text


class ResultScene(SceneBase):
    """ResultScene subclass implementation."""

    def __init__(self, player1_pts, player2_pts):
        super().__init__()  # Call the super class (SceneBase) initialization method. This statement ensures that this
        # class inherits its behaviour from its Superclass. Abstract methods of all scenes (ProcessInput, Render,
        # Update, etc.), screen resolutions, text fonts, general text drawing methods and so on.

        self.player1_pts = player1_pts
        self.player2_pts = player2_pts
        self.background = pg.image.load('frames/splash_BG.jpg')
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
        from .accounts_scene import AccountsScene  # Avoiding circular dependencies
        self.accounts = AccountsScene.get_instance()
        if self.accounts.logged_in['Spacecraft'] or self.accounts.logged_in['Anti-spacecraft']:
            # If we are logged in and the game has finished, save the scores to the DB)
            self.connect_DB()

    # A method to populate player names from user input and display them on the screen
    def get_player_name(self, event):
        if event.type == pg.KEYDOWN:
            # If a player has finished writing their name
            if event.key == pg.K_RETURN and self.player_no < 3:
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
                elif event.key == pg.K_BACKSPACE or event.key == pg.K_DELETE:
                    self.player1_name = self.player1_name[:-1]
            # If player two is writing
            elif self.player_no == 2:
                if event.unicode.isalnum() and len(self.player2_name) < 16:
                    self.player2_name += event.unicode
                elif event.key == pg.K_BACKSPACE or event.key == pg.K_DELETE:
                    self.player2_name = self.player2_name[:-1]

    def store_result(self):  # This method saves the current scores to a local .csv file
        with open('highscore_list.csv', mode='a') as csv_file:
            fieldnames = ['Name', 'Score', 'Date']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerow({'Name': self.player1_name, 'Score': self.player1_pts, 'Date': date.today()})
            writer.writerow({'Name': self.player2_name, 'Score': self.player2_pts, 'Date': date.today()})

    def process_input(self, events, pressed_keys):
        for event in events:
            # Check for the menu button click
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and self.menu_button.on_click(event):
                from .menu_scene import MenuScene
                self.switch_to_scene(MenuScene.get_instance())
            else:
                # Otherwise get player names if local storage will be used
                if not (self.accounts.logged_in['Spacecraft'] or self.accounts.logged_in['Anti-spacecraft']):
                    if self.player_no == 1:
                        self.get_player_name(event)
                    elif self.player_no == 2:
                        self.get_player_name(event)

    def update(self):
        pass

    def render(self, screen):
        # Render the background and star field
        display = self.adjust_screen(screen)
        display.blit(self.background, (0, 0))
        self.star_field.draw_stars(display)

        self.display_scene(display)  # Display the scene specific content (depends on the storage to be used)

        # Handle the menu button
        self.menu_button.update(display)

    def display_scene(self, display):
        # Display main messages
        draw_text(display, "GAME RESULTS",
                  (self.screen_width / 2, self.screen_height / 8), FONT_BIG, CYAN)

        draw_text(display, f"Player 1 Score = {self.player1_pts} points",
                  (self.screen_width / 2, self.screen_height / 2.5), FONT_MEDIUM, CYAN)

        draw_text(display, f"Player 2 Score = {self.player2_pts} points",
                  (self.screen_width / 2, self.screen_height / 1.5), FONT_MEDIUM, CYAN)

        # If not logged in ask for user names for both players for the .cvs safe
        if not (self.accounts.logged_in['Spacecraft'] or self.accounts.logged_in['Anti-spacecraft']):
            draw_text(display, "Please, type your name or initials!",
                      (self.screen_width / 2, self.screen_height / 5.5), FONT_MEDIUM, CYAN)
            draw_text(display, "As you start typing, your name will appear on the screen.",
                      (self.screen_width / 2, self.screen_height / 4.3), FONT_MEDIUM, CYAN)
            draw_text(display, "To confirm press ENTER | To delete a character use BACKSPACE!",
                      (self.screen_width / 2, self.screen_height / 3.5), FONT_MEDIUM, CYAN)
            draw_text(display, "Name >>", (self.screen_width / 2.45, self.screen_height / 2.15), FONT_MEDIUM, CYAN)
            draw_text(display, "Name >>", (self.screen_width / 2.45, self.screen_height / 1.35), FONT_MEDIUM, CYAN)

            # Two blocks displaying the names of the players
            block = FONT_MEDIUM.render(self.player1_name, True, CYAN)
            rect = block.get_rect()
            rect.left = self.screen_width / 2.15
            rect.top = self.screen_height / 2.21

            block2 = FONT_MEDIUM.render(self.player2_name, True, CYAN)
            rect2 = block2.get_rect()
            rect2.left = self.screen_width / 2.15
            rect2.top = self.screen_height / 1.38

            display.blit(block, rect)
            display.blit(block2, rect2)

            # Variable player_no changes on every press of the button Enter until it is equal to 4
            if self.player_no == 3:
                self.store_result()
                self.player_no += 1
        else:
            # If the user decides to save scores to the DB, blit status
            draw_text(display, self.status, (self.screen_width / 2, self.screen_height / 3.33), FONT_MEDIUM, CYAN)

    def connect_DB(self):  # Method to connect to the database and update the score of the current user
        try:  # Try to connect to DB
            connection = pymysql.connect(host='localhost', user='root', password='', db='users')
            try:
                with connection.cursor() as cursor:  # Create a cursor object
                    if self.accounts.logged_in['Spacecraft'] and self.accounts.logged_in['Anti-spacecraft']:
                        self.status = 'Scores for players [%s] and [%s] updated successfully!' % \
                                      (self.accounts.credentials[0][0], self.accounts.credentials[1][0])
                    elif self.accounts.logged_in['Spacecraft']:
                        # Write SQL statement, execute and commit the changes
                        sql = "INSERT INTO `scores`(`Username`, `Spacecraft Score`, `Date`) " \
                              "VALUES ('" + self.accounts.credentials[0][0] + "'," + str(self.player1_pts) + \
                              ",CURDATE()" + ")"

                        cursor.execute(sql)
                        connection.commit()
                        self.status = 'Scores for player [%s] updated successfully!' % self.accounts.credentials[0][0]
                    elif self.accounts.logged_in['Anti-spacecraft']:
                        # Write SQL statement, execute and commit the changes
                        sql = "INSERT INTO `scores`(`Username`, `Anti-spacecraft Score`, `Date`) " \
                              "VALUES ('" + self.accounts.credentials[1][0] + "'," + str(self.player2_pts) + \
                              ",CURDATE()" + ")"
                        cursor.execute(sql)
                        connection.commit()
                        self.status = 'Scores for player [%s] updated successfully!' % self.accounts.credentials[1][0]
            finally:
                connection.close()  # Always close the connection
        except pymysql.err.OperationalError:  # If error occurs with the connection to the DB, notify user
            self.status = 'The server is currently offline. Please try again later.'
