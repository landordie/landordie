"""
'accounts_scene.py' module.
Used in instantiating the Accounts scene.
"""
import pymysql.cursors
from .menu_scene import MenuScene
from .game_scene import *
from .button import Button
from .input_box import InputBox
from .helper import draw_text


class AccountsScene(SceneBase):
    """Accounts scene (window) singleton class implementation."""
    __instance = None

    @staticmethod
    def get_instance():
        """Static access method. Ensures the singularity of a class instance."""
        if AccountsScene.__instance is None:
            AccountsScene()
        return AccountsScene.__instance

    def __init__(self):
        """Virtually private constructor which initializes the Accounts scene."""
        super().__init__()  # Call the super class (SceneBase) initialization method. This statement ensures that this
        # class inherits its behaviour from its Superclass. Abstract methods of all scenes (ProcessInput, Render,
        # Update, etc.), screen resolutions, text fonts, general text drawing methods and so on.

        # Check if there are any instances of the class already created
        if AccountsScene.__instance is not None:
            raise Exception("This class is an AccountsInstance!")
        else:
            AccountsScene.__instance = self

        # Dictionary to show which player is logged in
        self.logged_in = {
            'Spacecraft': False,
            'Anti-spacecraft': False
        }
        self.credentials = [[], []]  # This list contains the credentials of the currently logged in user

        # Initialize buttons in the interface (menu, log in and register buttons)
        self.menu_button = Button((self.screen_width / 2 - (BUTTON_WIDTH / 2), self.screen_height / 1.2,
                                   BUTTON_WIDTH, BUTTON_HEIGHT), YELLOW, 'Main Menu')

        self.log_in_sc_button = Button((self.screen_width / 6, self.screen_height / 2.1,
                                        BUTTON_WIDTH, BUTTON_HEIGHT), GREEN, 'Log in')

        self.reg_sc_button = Button((self.screen_width / 6, self.screen_height / 1.6,
                                     BUTTON_WIDTH, BUTTON_HEIGHT), RED, 'Register')

        self.log_in_a_sc_button = Button((self.screen_width / 1.525, self.screen_height / 2.1,
                                          BUTTON_WIDTH, BUTTON_HEIGHT), GREEN, 'Log in')

        self.reg_a_sc_button = Button((self.screen_width / 1.525, self.screen_height / 1.6,
                                       BUTTON_WIDTH, BUTTON_HEIGHT), RED, 'Register')

        self.scores_button = Button((self.screen_width / 2 - (BUTTON_WIDTH / 2), self.screen_height / 1.85,
                                     BUTTON_WIDTH, BUTTON_HEIGHT), RED, 'Get scores')

        self.background = pg.image.load("Assets/frames/BG.png")  # Initialize the background

        # Container for credential fields
        self.cred_cont_w, self.cred_cont_h = self.screen_width / 2.3, self.screen_height / 4
        self.cred_cont_x, self.cred_cont_y = (self.screen_width / 2.1 - self.cred_cont_w), \
                                             (self.screen_height * 0.15)
        self.cred_cont2_x = (self.screen_width / 1.05 - self.cred_cont_w)
        self.cred_cont = pg.Surface((self.cred_cont_w, self.cred_cont_h)).convert_alpha()
        self.cred_cont.fill(BLACK_HIGHLIGHT2)

        # Container for scores
        self.score_cont_w, self.score_cont_h = self.screen_width / 1.5, self.screen_height / 1.5
        self.score_cont_x, self.score_cont_y = (self.screen_width / 2 - (self.score_cont_w / 2)), \
                                               (self.screen_height * 0.15)
        self.score_cont = pg.Surface((self.score_cont_w, self.score_cont_h)).convert_alpha()
        self.score_cont.fill(BLACK_HIGHLIGHT3)
        self.score_cont_button = Button((self.screen_width / 2 - BUTTON_WIDTH / 2, self.screen_height / 1.55,
                                         BUTTON_WIDTH, BUTTON_HEIGHT), RED, 'Close')

        # Container for the database response
        self.status_cont_w, self.status_cont_h = self.screen_width, self.screen_height / 15
        self.status_cont_x, self.status_cont_y = (self.screen_width / 2 - self.status_cont_w / 2), \
                                                 (self.screen_height / 15)
        self.status_cont = pg.Surface((self.status_cont_w, self.status_cont_h)).convert_alpha()
        self.status_cont.fill(BLACK_HIGHLIGHT2)

        # Input boxes to handle input for username and password
        self.input_box1 = InputBox(self.cred_cont_x * 4.5, self.cred_cont_y * 1.3, '', 350, 33)
        self.input_box2 = InputBox(self.cred_cont_x * 4.5, self.cred_cont_y * 1.9, '', 350, 33)
        self.input_box3 = InputBox(self.cred_cont2_x * 1.28, self.cred_cont_y * 1.3, '', 350, 33)
        self.input_box4 = InputBox(self.cred_cont2_x * 1.28, self.cred_cont_y * 1.9, '', 350, 33)
        self.fields = [self.input_box1, self.input_box2, self.input_box3, self.input_box4]  # A list used to group the
        # input fields for cleaner code

        self.status = ''  # This variable indicates the status of the DB connection
        self.cool_down = 0  # Status container cool down
        self.scores = {}  # This dictionary contains the scores for each player

    def process_input(self, events, pressed_keys):
        for event in events:
            for input_box in self.fields:  # Pass each event to the input boxes for handling
                input_box.handle_event(event, 2)
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:  # Exit program on 'Esc' button
                self.terminate()
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:  # On left mouse button click
                if self.menu_button.on_click(event):  # Go back to menu
                    for field in self.fields:  # Clear all fields
                        field.text = ""
                    menu = MenuScene.get_instance()
                    self.switch_to_scene(menu)
                # If the score table is initialized, do not check for the buttons behind the score container
                if self.scores:
                    if self.score_cont_button.on_click(event):
                        # If close container is clicked, empty the scores
                        self.scores = {}
                else:
                    if self.reg_sc_button.on_click(event):  # Register user with DB
                        self.connect_db("register", self.input_box1.text, self.input_box2.text)
                    elif self.log_in_sc_button.on_click(event):  # Check if user in DB and sign them in if True
                        self.connect_db("login_sc", self.input_box1.text, self.input_box2.text)
                    elif self.reg_a_sc_button.on_click(event):  # Register user with DB
                        self.connect_db("register", self.input_box3.text, self.input_box4.text)
                    elif self.log_in_a_sc_button.on_click(event):  # Check if user in DB and sign them in if True
                        self.connect_db("login_asc", self.input_box3.text, self.input_box4.text)
                    elif self.scores_button.on_click(event):
                        self.connect_db("get_scores", '', '')

    def update(self):
        """Recalculate and update relative positions of all buttons and input boxes."""
        # Adjust credentials fields container position
        self.cred_cont_w, self.cred_cont_h = self.screen_width / 2.3, self.screen_height / 4
        self.cred_cont_x, self.cred_cont_y = (self.screen_width / 2.1 - self.cred_cont_w), \
                                             (self.screen_height * 0.15)
        self.cred_cont2_x = (self.screen_width / 1.05 - self.cred_cont_w)
        self.cred_cont = pg.Surface((self.cred_cont_w, self.cred_cont_h)).convert_alpha()

        # Adjust database response container position
        self.status_cont_w, self.status_cont_h = self.screen_width, self.screen_height * .05
        self.status_cont_x, self.status_cont_y = (self.screen_width / 2 - self.status_cont_w / 2), \
                                                 (self.screen_height * .02)
        self.status_cont = pg.Surface((self.status_cont_w, self.status_cont_h)).convert_alpha()

        self.score_cont_x, self.score_cont_y = (self.screen_width / 2 - (self.score_cont_w / 2)), \
                                               (self.screen_height * 0.15)
        self.score_cont = pg.Surface((self.score_cont_w, self.score_cont_h)).convert_alpha()

        # Update button positions
        self.menu_button.rect.x, self.menu_button.rect.y = \
            self.screen_width / 2 - (BUTTON_WIDTH / 2), self.screen_height / 1.2

        self.log_in_sc_button.rect.x, self.log_in_sc_button.rect.y = self.screen_width / 5.7, self.screen_height / 2.1

        self.reg_sc_button.rect.x, self.reg_sc_button.rect.y = self.screen_width / 5.7, self.screen_height / 1.6

        self.log_in_a_sc_button.rect.x, self.log_in_a_sc_button.rect.y = \
            self.screen_width / 1.525, self.screen_height / 2.1

        self.reg_a_sc_button.rect.x, self.reg_a_sc_button.rect.y = self.screen_width / 1.525, self.screen_height / 1.6

        self.scores_button.rect.x, self.scores_button.rect.y = \
            self.screen_width / 2 - (BUTTON_WIDTH / 2), self.screen_height / 1.85

        self.score_cont_button.rect.x, self.score_cont_button.rect.y = \
            self.screen_width / 2 - (BUTTON_WIDTH / 2), self.screen_height / 1.55

        # Update input box positions
        self.input_box1.rect.x, self.input_box1.rect.y = self.cred_cont_x * 4.5, self.cred_cont_y * 1.3
        self.input_box2.rect.x, self.input_box2.rect.y = self.cred_cont_x * 4.5, self.cred_cont_y * 1.9
        self.input_box3.rect.x, self.input_box3.rect.y = self.cred_cont2_x * 1.28, self.cred_cont_y * 1.3
        self.input_box4.rect.x, self.input_box4.rect.y = self.cred_cont2_x * 1.28, self.cred_cont_y * 1.9

    def render(self, screen):
        display = self.adjust_screen(screen)  # Surface
        self.parallax_effect(display)  # Initialize the parallax effect

        # Display containers and container and field names
        display.blit(self.cred_cont, (self.cred_cont_x, self.cred_cont_y, self.cred_cont_w, self.cred_cont_h))
        display.blit(self.cred_cont,
                     (self.cred_cont2_x, self.cred_cont_y, self.cred_cont_w, self.cred_cont_h))

        draw_text(display, "Spacecraft player", (self.cred_cont_x * 3.9, self.cred_cont_y * 0.9),
                  FONT_MEDIUM, WHITE)
        draw_text(display, "Username:", (self.cred_cont_x * 2.9, self.cred_cont_y * 1.45), FONT_MEDIUM, WHITE)
        draw_text(display, "Password:", (self.cred_cont_x * 2.9, self.cred_cont_y * 2.05), FONT_MEDIUM, WHITE)
        draw_text(display, "Anti-spacecraft player", (self.cred_cont2_x * 1.3, self.cred_cont_y * 0.9),
                  FONT_MEDIUM, WHITE)
        draw_text(display, "Username:", (self.cred_cont2_x * 1.15, self.cred_cont_y * 1.45), FONT_MEDIUM, WHITE)
        draw_text(display, "Password:", (self.cred_cont2_x * 1.15, self.cred_cont_y * 2.05), FONT_MEDIUM, WHITE)

        # If the status variable is changed (the value not equal to the initial one)
        if self.status != '' and self.cool_down <= 120:
            # Show the status on screen
            display.blit(self.status_cont,
                         (self.status_cont_x, self.status_cont_y, self.status_cont_w, self.status_cont_h))
            draw_text(display, self.status, (self.screen_width / 2, self.screen_height * .05),
                      FONT_MEDIUM_PLUS, WHITE)
            self.cool_down += 1

        # Draw credential fields on screen and reflect any changes to their content
        self.input_box1.draw(display)
        self.input_box2.draw(display, True)  # True here indicates that the field must be hidden (with '*')
        self.input_box3.draw(display)
        self.input_box4.draw(display, True)

        # Update buttons
        self.menu_button.update(display)
        if self.scores:  # If scores are initialized display them on screen and do not update the buttons
            # Behind the container of the scores
            display.blit(self.score_cont,
                         (self.score_cont_x, self.score_cont_y, self.score_cont_w, self.score_cont_h))
            draw_text(display, "Name | Spacecraft | Anti-spacecraft | Games",
                      (self.screen_width / 2, self.score_cont_y * 1.2), FONT_MEDIUM, WHITE)

            margin = 1.4
            increment = 0.5
            for entry in self.scores:
                margin += increment
                draw_text(display, (entry + "     " + str(self.scores[entry][0]) + "     "
                                    + str(self.scores[entry][1]) + "     " + str(self.scores[entry][2])),
                          (self.screen_width / 2, self.score_cont_y * margin), FONT_MEDIUM, WHITE)
            self.score_cont_button.update(display)
        # If no scores are being displayed on screen update buttons
        else:
            self.log_in_sc_button.update(display)
            self.reg_sc_button.update(display)
            self.log_in_a_sc_button.update(display)
            self.reg_a_sc_button.update(display)
            self.scores_button.update(display)

    def connect_db(self, command, username, pw):
        """
        The method is used to connect to a local database and make checks or register new users in it.
        :param command: login or register
        :param username: player username
        :param pw: player password
        """
        try:  # Try Except is used to handle cases where the DB is offline
            connection = pymysql.connect(host='localhost', user='root', password='', db='users')  # Create a connection

            if command == "get_scores" and not self.scores:
                try:
                    # Create a cursor object which will be used to execute commands on the DB
                    with connection.cursor() as cursor:
                        if self.logged_in['Spacecraft']:
                            # Create the SQL statement to get the users with the given credentials
                            sql = "SELECT `Anti-spacecraft Score`, `Spacecraft Score` FROM `scores` WHERE " \
                                  f"(Username='{self.credentials[0][0]}')"
                            cursor.execute(sql)  # Execute statement
                            scores = cursor.fetchall()  # And get the result of the query
                            a_sc_score = 0
                            sc_score = 0
                            for score_tuple in scores:
                                a_sc_score += int(score_tuple[0])
                                sc_score += int(score_tuple[1])
                            # Add entry to the dictionary
                            self.scores[self.credentials[0][0]] = (sc_score, a_sc_score, len(scores))
                        if self.logged_in['Anti-spacecraft']:
                            # Create the SQL statement to get the users with the given credentials
                            sql = "SELECT `Anti-spacecraft Score`, `Spacecraft Score` FROM `scores` WHERE " \
                                  f"(Username='{self.credentials[1][0]}')"
                            cursor.execute(sql)  # Execute statement
                            scores = cursor.fetchall()  # And get the result of the query
                            a_sc_score = 0
                            sc_score = 0

                            for score_tuple in scores:
                                a_sc_score += int(score_tuple[0])
                                sc_score += int(score_tuple[1])
                            self.scores[self.credentials[1][0]] = (sc_score, a_sc_score, len(scores))
                finally:  # Always close the connection
                    connection.close()
                return

            # Check if the credential fields are empty. If so notify user and abort action
            for field in [username, pw]:
                if field == '':
                    self.cool_down = 0
                    self.status = 'You cannot submit an empty field. Please try again!'
                    return

            player, player_id = None, -1  # To indicate which player is trying to log in and which credentials to save
            if command == "login_sc":  # If the request asks the DB to check if user exists
                player, player_id = 'Spacecraft', 0
            elif command == "login_asc":
                player, player_id = 'Anti-spacecraft', 1
            elif command == "register":  # If the DB has to register a new user
                try:
                    with connection.cursor() as cursor:  # Create a cursor object
                        sql = "SELECT `Username` FROM `users`"  # Define the statement in SQL
                        cursor.execute(sql)  # Execute it
                        a = [row[0] for row in cursor.fetchall()]  # Fetch all username entries from the response
                        if username in a:  # Check if a user with that name already exists
                            self.status = 'A user with that username already exists. Please try again!'
                        else:  # If not
                            # Insert the current user and commit the changes to the server
                            sql = "INSERT INTO `users` (`Username`, `Password`) VALUES (%s, %s)"
                            cursor.execute(sql, (username, pw))
                            connection.commit()
                            self.status = 'Operation executed successfully!'
                        self.cool_down = 0
                finally:  # Always close the connection
                    connection.close()
                return

            if player:  # Check if the player is specified
                if not self.logged_in[player]:  # and another user is not currently logged in from the session
                    try:
                        # Create a cursor object which will be used to execute commands on the DB
                        with connection.cursor() as cursor:
                            # Create the SQL statement to get the users with the given credentials
                            sql = f"SELECT `Username`, `Password` FROM `users` WHERE (Username='{username}') " \
                                  f"AND (Password='{pw}')"
                            cursor.execute(sql)  # Execute statement
                            fetch_result = cursor.fetchone()  # And get the result of the query
                            if fetch_result:  # If the check was successful (a table entry is returned)
                                self.status = f"{player} player signed in as [{username}]! Enjoy the game."
                                self.credentials[player_id] = [username, pw]  # Update the state
                                self.logged_in[player] = True
                            else:
                                self.status = "Wrong credentials entered. Please check the input again."
                            self.cool_down = 0
                    finally:  # Always close the connection
                        connection.close()
                else:
                    self.status = "You are already signed in! Please log out first."
                    self.cool_down = 0
            else:
                print('Player not specified!')
        except pymysql.err.OperationalError:
            self.status = "The server is currently offline. Please try again later."
            self.cool_down = 0
