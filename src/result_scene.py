"""
'result_scene.py' module.
Used in instantiation of a Result scene (window).
"""
import csv
from datetime import date
import pymysql
from src.constants import *
from .scene_base import SceneBase
from .button import Button
from .star_field import StarField
from .helper import draw_text


class ResultScene(SceneBase):
    """ResultScene subclass implementation."""

    def __init__(self, sc_pts, a_sc_pts):
        super().__init__()  # Call the super class (SceneBase) initialization method. This statement ensures that this
        # class inherits its behaviour from its Superclass. Abstract methods of all scenes (ProcessInput, Render,
        # Update, etc.), screen resolutions, text fonts, general text drawing methods and so on.

        self.sc_pts = sc_pts  # Spacecraft game points
        self.a_sc_pts = a_sc_pts  # Anti-spacecraft game points
        self.background = pg.image.load('assets/frames/splash_BG.jpg')
        self.star_field = StarField(self.screen_width, self.screen_height)

        self.menu_button = Button(
            (self.screen_width / 2 - (BUTTON_WIDTH / 2), self.screen_height / 1.2, BUTTON_WIDTH, BUTTON_HEIGHT),
            YELLOW, 'Main Menu')
        # Hold the names of the two players
        self.sc_name = ""
        self.a_sc_name = ""
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
                if self.player_no == 1 and len(self.sc_name) == 0:
                    self.sc_name = "DEFAULT_PLAYER1"
                elif self.player_no == 2 and len(self.a_sc_name) == 0:
                    self.a_sc_name = "DEFAULT_PLAYER2"
                self.player_no += 1
            # If player 1 is writing
            elif self.player_no == 1:
                # If the pressed button corresponds to a alphabetical char (a,b,c,d...,x,y,z)
                if event.unicode.isalnum() and len(self.sc_name) < 16:
                    self.sc_name += event.unicode
                # If the user would like to delete a char from the screen
                elif event.key == pg.K_BACKSPACE or event.key == pg.K_DELETE:
                    self.sc_name = self.sc_name[:-1]
            # If player two is writing
            elif self.player_no == 2:
                if event.unicode.isalnum() and len(self.a_sc_name) < 16:
                    self.a_sc_name += event.unicode
                elif event.key == pg.K_BACKSPACE or event.key == pg.K_DELETE:
                    self.a_sc_name = self.a_sc_name[:-1]

    def store_result(self):
        """Save the current scores to a local .csv file."""
        with open('highscore_list.csv', mode='a') as csv_file:
            fieldnames = ['Name', 'Score', 'Date']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerow({'Name': self.sc_name, 'Score': self.sc_pts, 'Date': date.today()})
            writer.writerow({'Name': self.a_sc_name, 'Score': self.a_sc_pts, 'Date': date.today()})

    def process_input(self, events, pressed_keys):
        for event in events:
            # On 'Main Menu' button click or 'Enter' key press switch to the Menu scene
            if (event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and self.menu_button.on_click(event))\
                    or (event.type == pg.KEYDOWN and event.key == pg.K_RETURN and self.player_no > 2):
                from .menu_scene import MenuScene  # Avoiding circular dependencies
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
        """
        Show the Result scene indicators and instruction messages.
        :param display: Pygame screen surface
        """
        # Display main messages
        draw_text(display, "GAME RESULTS",
                  (self.screen_width / 2, self.screen_height / 8), FONT_BIG, CYAN)

        draw_text(display, f"Player 1 Score = {self.sc_pts} points",
                  (self.screen_width / 2, self.screen_height / 2.5), FONT_MEDIUM, CYAN)

        draw_text(display, f"Player 2 Score = {self.a_sc_pts} points",
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
            block = FONT_MEDIUM.render(self.sc_name, True, CYAN)
            rect = block.get_rect()
            rect.left = self.screen_width / 2.15
            rect.top = self.screen_height / 2.21

            block2 = FONT_MEDIUM.render(self.a_sc_name, True, CYAN)
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
                    # Check for the login status of both players and get their credentials
                    sc_logged, sc_cred = self.accounts.logged_in['Spacecraft'], self.accounts.credentials[0][0]
                    a_sc_logged, a_sc_cred = self.accounts.logged_in['Anti-spacecraft'], self.accounts.credentials[1][0]

                    if sc_logged:  # If the spacecraft player is logged in insert their score in the db
                        # Write SQL statement, execute and commit the changes
                        sql = "INSERT INTO `scores`(`Username`, `Spacecraft Score`, `Date`) " \
                              f"VALUES ('{sc_cred}', {self.sc_pts}, CURDATE())"
                        cursor.execute(sql)
                        connection.commit()
                        self.status = f'Scores for player [{sc_cred}] updated successfully!'
                    if a_sc_logged:  # If the anti-spacecraft player is logged in insert their score in the db
                        # Write SQL statement, execute and commit the changes
                        sql = "INSERT INTO `scores`(`Username`, `Anti-spacecraft Score`, `Date`) " \
                              f"VALUES ('{a_sc_cred}', {self.a_sc_pts}, CURDATE())"
                        cursor.execute(sql)
                        connection.commit()
                        self.status = f'Scores for player [{a_sc_cred}] updated successfully!'
                    if sc_logged and a_sc_logged:  # If both players are logged in then notify for both insertions
                        self.status = f'Scores for players [{sc_cred}] and [{a_sc_cred}] updated successfully!'
            finally:
                connection.close()  # Always close the connection
        except pymysql.err.OperationalError:  # If error occurs with the connection to the DB, notify user
            self.status = 'The server is currently offline. Please try again later.'
