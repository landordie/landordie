from .scene_base import *
from .menu_scene import *
from .game_scene import  *
from .button import Button
import string
import constants

class OptionsScene(SceneBase):
	def __init__(self):
		SceneBase.__init__(self)
		self.width = M_SCREEN_WIDTH
		self.height = M_SCREEN_HEIGHT

		self.menu_button = Button((self.width * 0.75 - (BUTTON_WIDTH / 2), self.height * 0.75, BUTTON_WIDTH, BUTTON_HEIGHT),
		                          YELLOW, 'Main Menu')

		self._res1 = Button((self.width * 0.25 - (BUTTON_WIDTH / 2), self.height * 0.15, BUTTON_WIDTH, BUTTON_HEIGHT),
		                    GREEN, "800x600")
		self._res2 = Button((self.width * 0.25 - (BUTTON_WIDTH / 2), self.height * 0.25, BUTTON_WIDTH, BUTTON_HEIGHT),
		                    GREEN, "1280x720")
		self._res3 = Button((self.width * 0.25 - (BUTTON_WIDTH / 2), self.height * 0.35, BUTTON_WIDTH, BUTTON_HEIGHT),
		                    GREEN, "1440x900")


	def ProcessInput(self, events, pressed_keys):
		for event in events:
			if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				self.Terminate()
			if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
				self.SwitchToScene(GameScene())
			# TODO : Fix error when trying to go back to MenuScene
			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.menu_button.on_click(event):
				self.SwitchToScene(MenuScene())
			"""
				Handling changing of resolution
			"""
			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self._res1.on_click(event):
				_res = self._res1._text.split("x")
				constants.G_SCREEN_WIDTH, constants.G_SCREEN_HEIGHT = int(_res[0]), int(_res[1])
			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self._res2.on_click(event):
				_res = self._res2._text.split("x")
				constants.G_SCREEN_WIDTH, constants.G_SCREEN_HEIGHT = int(_res[0]), int(_res[1])
			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self._res3.on_click(event):
				_res = self._res3._text.split("x")
				constants.G_SCREEN_WIDTH, constants.G_SCREEN_HEIGHT = int(_res[0]), int(_res[1])


	def Update(self):
		pass

	def Render(self, screen):
		screen.get_surface().fill(BLACK)

		self.menu_button.update(screen.get_surface())
		self._res1.update(screen.get_surface())
		self._res2.update(screen.get_surface())
		self._res3.update(screen.get_surface())
