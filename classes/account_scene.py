from .menu_scene import MenuScene
from .game_scene import *
from .button import Button
import pygame
from .input_box import InputBox
import pymysql.cursors


class AccountScene(SceneBase):
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if AccountScene.__instance is None:
            AccountScene()
        return AccountScene.__instance

    def __init__(self):
        if AccountScene.__instance is not None:
            raise Exception("This class is an AccountInstance!")
        else:
            AccountScene.__instance = self

        SceneBase.__init__(self)
        # Initialize buttons in the interface (menu, sign in and sign up buttons)
        self.menu_button = Button(
            (self.screen_width / 2 - (BUTTON_WIDTH / 2), self.screen_height / 1.2, BUTTON_WIDTH, BUTTON_HEIGHT),
            YELLOW, 'Main Menu')

        self.login_sc_button = Button((self.screen_width / 5.5, self.screen_height / 2.1, BUTTON_WIDTH, BUTTON_HEIGHT),
                                      GREEN, 'Sign in')

        self.reg_sc_button = Button((self.screen_width / 5.5, self.screen_height / 1.6, BUTTON_WIDTH, BUTTON_HEIGHT),
                                    RED, 'Register')

        self.login_a_sc_button = Button((self.screen_width / 1.51, self.screen_height / 2.1, BUTTON_WIDTH,
                                         BUTTON_HEIGHT), GREEN, 'Sign in')

        self.reg_a_sc_button = Button((self.screen_width / 1.51, self.screen_height / 2.1, BUTTON_WIDTH, BUTTON_HEIGHT),
                                      RED, 'Register')

        # Initialize the background
        self.background = pygame.image.load("frames/BG.png")
        self.x = 0

        # Container for credential fields
        self.button_cont_w, self.button_cont_h = self.screen_width / 2.3, self.screen_height / 4
        self.button_cont_x, self.button_cont_y = (self.screen_width / 2.1 - self.button_cont_w), (
                self.screen_height * 0.15)
        self.button_cont2_x = (self.screen_width / 1.05 - self.button_cont_w)
        self.button_cont = pygame.Surface((self.button_cont_w, self.button_cont_h)).convert_alpha()
        self.button_cont.fill(BLACK_HIGHLIGHT2)

        # Container for the database response
        self.status_cont_w, self.status_cont_h = self.screen_width / 1.2, self.screen_height / 15
        self.status_cont_x, self.status_cont_y = (self.screen_width / 2 - self.status_cont_w / 2), (
                self.screen_height / 15)
        self.status_cont = pygame.Surface((self.status_cont_w, self.status_cont_h)).convert_alpha()
        self.status_cont.fill(BLACK_HIGHLIGHT2)

        # Input boxes to handle input for username and password
        self.input_box1 = InputBox(self.button_cont_x * 4.5, self.button_cont_y * 1.3, '', 350, 33)
        self.input_box2 = InputBox(self.button_cont_x * 4.5, self.button_cont_y * 1.9, '', 350, 33)
        self.input_box3 = InputBox(self.button_cont2_x * 1.28, self.button_cont_y * 1.3, '', 350, 33)
        self.input_box4 = InputBox(self.button_cont2_x * 1.28, self.button_cont_y * 1.9, '', 350, 33)
        self.status = ''  # This variable indicates the status of the DB connection
        self.fields = [self.input_box1, self.input_box2, self.input_box3,
                       self.input_box4]  # A list used to group the input fields for cleaner code

    def ProcessInput(self, events, pressed_keys):
        for event in events:
            # Pass each event to the input boxes for handling
            for input_box in self.fields:
                input_box.handle_event(event, 2)
            # If the event is the escape button - exit game
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.Terminate()
            # Track mouse clicks for button responsiveness
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.menu_button.on_click(event):  # Go back to menu
                    menu = MenuScene.getInstance()
                    self.SwitchToScene(menu)
                elif self.reg_sc_button.on_click(event):  # Register user with DB
                    self.connect_db("register_sc", self.input_box1.text, self.input_box2.text)
                elif self.login_sc_button.on_click(event):  # Check if user in DB and sign them in if True
                    self.connect_db("login_sc", self.input_box1.text, self.input_box2.text)
                elif self.reg_a_sc_button.on_click(event):  # Register user with DB
                    self.connect_db("register_asc", self.input_box3.text, self.input_box4.text)
                elif self.login_a_sc_button.on_click(event):  # Check if user in DB and sign them in if True
                    self.connect_db("login_asc", self.input_box3.text, self.input_box4.text)

    def Update(self):
        pass

    def Render(self, screen):
        screen.set_mode((self.screen_width, self.screen_height))
        display = screen.get_surface()

        # Background parallax effect
        image_width = self.background.get_rect().width
        # The relative x of the image used for the parallax effect
        rel_x = self.x % image_width
        # Displaying the image based on the relative x and the image width
        display.blit(self.background, (rel_x - image_width, 0))
        # When the right end of the image reaches the right side of the screen
        # a new image starts displaying so we do not have any black spaces
        if rel_x < self.screen_width:
            display.blit(self.background, (rel_x, 0))
        # This decrement is what makes the image "move"
        self.x -= 1
        # Update buttons
        self.menu_button.update(display)
        self.login_sc_button.update(display)
        self.reg_sc_button.update(display)
        self.login_a_sc_button.update(display)
        self.reg_a_sc_button.update(display)

        # Display containers, input boxes and instructions
        display.blit(self.button_cont,
                     (self.button_cont_x, self.button_cont_y, self.button_cont_w, self.button_cont_h))

        display.blit(self.button_cont,
                     (self.button_cont2_x, self.button_cont_y, self.button_cont_w, self.button_cont_h))

        self.draw_text(screen, "Username:", (self.button_cont_x * 2.9, self.button_cont_y * 1.45),
                       self.font_medium, WHITE)
        self.draw_text(screen, "Password:", (self.button_cont_x * 2.9, self.button_cont_y * 2.05),
                       self.font_medium, WHITE)
        self.draw_text(screen, "Username:", (self.button_cont2_x * 1.15, self.button_cont_y * 1.45),
                       self.font_medium, WHITE)
        self.draw_text(screen, "Password:", (self.button_cont2_x * 1.15, self.button_cont_y * 2.05),
                       self.font_medium, WHITE)

        # If the status variable is changed (the value not equal to the initial one)
        if self.status != '':
            # Show the status on screen
            display.blit(self.status_cont,
                         (self.status_cont_x, self.status_cont_y, self.status_cont_w, self.status_cont_h))
            self.draw_text(screen, self.status, (self.screen_width / 2, self.screen_height / 10),
                           self.font_playernum, WHITE)

        # Draw credential fields on screen and reflect any changes to their content
        self.input_box1.draw(display)
        self.input_box2.draw(display, True)  # True here indicates that the field must be hidden (with '*')
        self.input_box3.draw(display)
        self.input_box4.draw(display, True)

    # This method is used when changing the resolutions
    # It recalculates the relative positions of all buttons on the main menu screen and puts them where they should be
    def update_all(self):
        # Container for credential fields
        self.button_cont_w, self.button_cont_h = self.screen_width / 2.3, self.screen_height / 4
        self.button_cont_x, self.button_cont_y = (self.screen_width / 2.1 - self.button_cont_w), (
                self.screen_height * 0.15)
        self.button_cont2_x = (self.screen_width / 1.05 - self.button_cont_w)
        self.button_cont = pygame.Surface((self.button_cont_w, self.button_cont_h)).convert_alpha()

        # Container for the database response
        self.status_cont_w, self.status_cont_h = self.screen_width / 1.2, self.screen_height / 15
        self.status_cont_x, self.status_cont_y = (self.screen_width / 2 - self.status_cont_w / 2), (
                self.screen_height / 15)
        self.status_cont = pygame.Surface((self.status_cont_w, self.status_cont_h)).convert_alpha()

        self.menu_button.rect.x, self.menu_button.rect.y = self.screen_width / 2 - (BUTTON_WIDTH / 2),\
                                                           self.screen_height / 1.2

        self.login_sc_button.rect.x, self.login_sc_button.rect.y = self.screen_width / 5.5, self.screen_height / 2.1

        self.reg_sc_button.rect.x, self.reg_sc_button.rect.y = self.screen_width / 5.5, self.screen_height / 1.6

        self.login_a_sc_button.rect.x, self.login_a_sc_button.rect.y = self.screen_width / 1.51, \
                                                                       self.screen_height / 2.1

        self.reg_a_sc_button.rect.x, self.reg_a_sc_button.rect.y = self.screen_width / 1.51, self.screen_height / 1.6

        # Input boxes to handle input for username and password
        self.input_box1.rect.x, self.input_box1.rect.y = self.button_cont_x * 4.5, self.button_cont_y * 1.3
        self.input_box2.rect.x, self.input_box2.rect.y = self.button_cont_x * 4.5, self.button_cont_y * 1.9
        self.input_box3.rect.x, self.input_box3.rect.y = self.button_cont2_x * 1.28, self.button_cont_y * 1.3
        self.input_box4.rect.x, self.input_box4.rect.y = self.button_cont2_x * 1.28, self.button_cont_y * 1.9

    def connect_db(self, command, name, pw):
        """The method is used to connect to a local database and make checks or register new users in it."""
        try:  # Thr try catch is used to handle cases where the DB is offline
            connection = pymysql.connect(host='localhost', user='root', password='', db='users')  # Create a connection

            for field in [name, pw]:  # Check if the credential fields are empty. If so notify user and abort action
                if field == '':
                    self.status = 'You cannot submit an empty field. Please try again!'
                    return

            if command == "login_sc":  # If the request asks the DB to check if user exists
                if not SceneBase.logged_in[0]:  # and another user is not currently logged in from the session
                    try:
                        # Create a cursor object which will be used to execute commands on the DB
                        with connection.cursor() as cursor:
                            # Create the SQL statement to get the users with the given credentials
                            sql = "SELECT `Username`, `Password` FROM `users` WHERE (Username='{0}') " \
                                  "AND (Password='{1}')".format(name, pw)
                            cursor.execute(sql)  # Execute statement
                            player = cursor.fetchone()  # And get the result of the query
                            if player:  # If the check was successful (a table entry is returned)
                                self.status = 'Spacecraft player signed in as [{0}]! Enjoy the game.'.format(name)
                                for field in [name, pw]:
                                    SceneBase.credentials.append(field)  # Update the state
                                self.logged_in[0] = True
                            else:
                                self.status = 'Wrong credentials entered. Please check the input again.'
                    finally:  # Always close the connection
                        connection.close()
                else:
                    self.status = 'You are already signed in! Please log out first.'

            elif command == "register_sc":  # If the DB has to register a new user
                if not SceneBase.logged_in[0]:  # and one is not currently logged into another account
                    try:
                        with connection.cursor() as cursor:  # Create a cursor object
                            sql = "SELECT `Username` FROM `users`"  # Define the statement in SQL
                            cursor.execute(sql)  # Execute it
                            a = [row[0] for row in cursor.fetchall()]  # Fetch all username entries from the response
                            if name in a:  # Check if a user with that name already exists
                                self.status = 'A user with that username already exists. Please try again!'
                            else:  # If not
                                # Insert the current user and commit the changes to the server
                                sql = "INSERT INTO `users` (`Username`, `Password`) VALUES (%s, %s)"
                                cursor.execute(sql, (name, pw))
                                connection.commit()
                                self.status = 'Operation executed successfully!'
                    finally:  # Always close the connection
                        connection.close()
                else:
                    self.status = 'You are already signed in! Please log out to proceed.'
            elif command == "login_asc":  # If the request asks the DB to check if user exists
                if not SceneBase.logged_in[1]:  # and another user is not currently logged in from the session
                    try:
                        # Create a cursor object which will be used to execute commands on the DB
                        with connection.cursor() as cursor:
                            # Create the SQL statement to get the users with the given credentials
                            sql = "SELECT `Username`, `Password` FROM `users` WHERE (Username='{0}') " \
                                  "AND (Password='{1}')".format(name, pw)
                            cursor.execute(sql)  # Execute statement
                            player = cursor.fetchone()  # And get the result of the query
                            if player:  # If the check was successful (a table entry is returned)
                                self.status = 'Spacecraft player signed in as [{0}]! Enjoy the game.'.format(name)
                                for field in [name, pw]:
                                    SceneBase.credentials.append(field)  # Update the state
                                self.logged_in[1] = True
                            else:
                                self.status = 'Wrong credentials entered. Please check the input again.'
                    finally:  # Always close the connection
                        connection.close()
                else:
                    self.status = 'You are already signed in! Please log out first.'

            elif command == "register_asc":  # If the DB has to register a new user
                if not SceneBase.logged_in[1]:  # and one is not currently logged into another account
                    try:
                        with connection.cursor() as cursor:  # Create a cursor object
                            sql = "SELECT `Username` FROM `users`"  # Define the statement in SQL
                            cursor.execute(sql)  # Execute it
                            a = [row[0] for row in cursor.fetchall()]  # Fetch all username entries from the response
                            if name in a:  # Check if a user with that name already exists
                                self.status = 'A user with that username already exists. Please try again!'
                            else:  # If not
                                # Insert the current user and commit the changes to the server
                                sql = "INSERT INTO `users` (`Username`, `Password`) VALUES (%s, %s)"
                                cursor.execute(sql, (name, pw))
                                connection.commit()
                                self.status = 'Operation executed successfully!'
                    finally:  # Always close the connection
                        connection.close()
                else:
                    self.status = 'You are already signed in! Please log out to proceed.'
        except pymysql.err.OperationalError:
            self.status = 'The server is currently offline. Please try again later.'
