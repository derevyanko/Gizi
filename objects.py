import pygame
import time
from math import ceil, fabs
from pygame import draw, Rect, key, font
from time import clock
from pygame import MOUSEBUTTONDOWN, KEYDOWN, K_BACKSPACE, K_RETURN
from keywords import colors
import json
import os, sys, subprocess

class Window():
	def __init__(self, **kwargs):
		self.run = kwargs['run']
		self.status = 'startWindow'
		self.windows = {'startWindow': StartWindow(kwargs['size']),'Menu': Menu(kwargs['size']), 'gameplay': GamePlayWindow(kwargs['size'])}
		self.caption = pygame.display.set_caption(kwargs['name'])

class Text():
	def __init__(self, text, coords):
		self.text = text
		self.coords = coords

class Texts():
	def __init__(self, texts):
		self.texts = texts
		self.pointer = 0

class Menu():
	def __init__(self, size):
		x = size[0] // 10
		y = size[1] // 5
		self.size = size
		self.texts = Texts([Text('Играть', (x, y)), Text('Рекорды', (x, y + 50)), 
			Text('Помощь', (x, y + 100)), Text('Выход', (x, y + 150))])
		self.screen = pygame.display.set_mode(size)

	def draw(self, window):
		self.get_events(window)
		window.windows[window.status].screen.fill((0, 0, 0))

		font = pygame.font.Font(None, 50)
		
		for i in range(len(self.texts.texts)):
			if self.texts.pointer != i:
				coords = self.texts.texts[i].coords
				text = font.render(self.texts.texts[i].text, 5, (255, 255, 255))
				window.windows[window.status].screen.blit(text, coords)
			else:
				coords = self.texts.texts[i].coords
				text = font.render(self.texts.texts[i].text, 5, (0, 0, 0))
				rect_text = text.get_rect()
				surf = pygame.Surface((rect_text.width, rect_text.height))
				surf.fill((255, 255, 255))
				window.windows[window.status].screen.blit(surf, coords)
				window.windows[window.status].screen.blit(text, coords)

		pygame.display.update()

	def get_events(self, window):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				window.run = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
					if event.key == pygame.K_UP:
						self.texts.pointer -= 1
						if self.texts.pointer < 0:
							self.texts.pointer = 3
					else:
						self.texts.pointer += 1
					self.texts.pointer %= 4
				elif event.key == pygame.K_RETURN:
					if self.texts.pointer == 0:
						window.status = 'gameplay'
					elif self.texts.pointer == 1:
						open_file('highscores.json')
					elif self.texts.pointer == 2:
						open_file('instruction.html')
					else:
						window.run = False

	def open_file(self, filename):
		if sys.platform == "win32":
			os.startfile(filename)
			print("Windows")
		else:
			print("Not Windows")
			opener ="open" if sys.platform == "darwin" else "xdg-open"
			subprocess.call([opener, filename])

class GamePlayWindow():
	def __init__(self, size):
		x = size[0] // 10
		y = size[0] // 5
		self.status = 'notStart'
		self.size = size
		self.score = 0
		self.surfTexts = []
		self.texts = {'winWindow': Texts([Text('Начать заново', (x, y)), Text('Выход в меню', (x, y + 50))]), 
			'gameOver': Texts([Text('Начать заново', (x, y)), Text('Выход в меню', (x, y + 50))])}
		self.screen = pygame.display.set_mode(size)

	def gamePlay(self, window):
		self.get_eventsGamePlay(window)
		
		if window.status == 'startWindow':
			window.windows[window.status].draw(window)
		else:
			window.windows['gameplay'].drawGame(window)

	def winWindow(self, window):
		self.get_eventsWinWindow(window)
		window.windows['gameplay'].drawWinWindow(window)

	def gameOverWindow(self, window):
		self.get_eventsGameOverWindow(window)
		window.windows['gameplay'].drawGameOverWindow(window)

	def drawGameOverWindow(self, window):
		window.windows[window.status].screen.fill((0, 0, 0))

		font = pygame.font.Font(None, 50)

		for i in range(len(self.texts['gameOver'].texts)):
			if self.texts['gameOver'].pointer != i:
				coords = self.texts['gameOver'].texts[i].coords
				text = font.render(self.texts['gameOver'].texts[i].text, 5, (255, 255, 255))
				window.windows[window.status].screen.blit(text, coords)
			else:
				coords = self.texts['gameOver'].texts[i].coords
				text = font.render(self.texts['gameOver'].texts[i].text, 5, (0, 0, 0))
				rect_text = text.get_rect()
				surf = pygame.Surface((rect_text.width, rect_text.height))
				surf.fill((255, 255, 255))
				window.windows[window.status].screen.blit(surf, coords)
				window.windows[window.status].screen.blit(text, coords)

		pygame.display.update()

	def drawWinWindow(self, window):
		window.windows[window.status].screen.fill((0, 0, 0))

		font = pygame.font.Font(None, 50)

		for i in range(len(self.texts['winWindow'].texts)):
			if self.texts['winWindow'].pointer != i:
				coords = self.texts['winWindow'].texts[i].coords
				text = font.render(self.texts['winWindow'].texts[i].text, 5, (255, 255, 255))
				window.windows[window.status].screen.blit(text, coords)
			else:
				coords = self.texts['winWindow'].texts[i].coords
				text = font.render(self.texts['winWindow'].texts[i].text, 5, (0, 0, 0))
				rect_text = text.get_rect()
				surf = pygame.Surface((rect_text.width, rect_text.height))
				surf.fill((255, 255, 255))
				window.windows[window.status].screen.blit(surf, coords)
				window.windows[window.status].screen.blit(text, coords)

		pygame.display.update()

	def drawGame(self, window):
		window.windows[window.status].screen.fill((0, 0, 0))
		pygame.display.update()

	def get_eventsGameOverWindow(self, window):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				window.run = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
					if event.key == pygame.K_UP:
						self.texts['gameOver'].pointer -= 1
					else:
						self.texts['gameOver'].pointer += 1
					self.texts['gameOver'].pointer = fabs(self.texts['gameOver'].pointer)
					self.texts['gameOver'].pointer %= 2
				elif event.key == pygame.K_RETURN:
					if self.texts['gameOver'].pointer == 0:
						window.windows[window.status].lastStatus = 'notStart'
						window.windows[window.status].status = 'notStart'
					else:
						window.windows[window.status].lastStatus = 'notStart'
						window.windows[window.status].status = 'notStart'
						window.status = 'startWindow'

	def get_eventsWinWindow(self, window):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				window.run = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
					if event.key == pygame.K_UP:
						self.texts['winWindow'].pointer -= 1
					else:
						self.texts['winWindow'].pointer += 1
					self.texts['winWindow'].pointer = fabs(self.texts['winWindow'].pointer)
					self.texts['winWindow'].pointer %= 2
				elif event.key == pygame.K_RETURN:
					if self.texts['winWindow'].pointer == 0:
						window.windows[window.status].status = 'notStart'
					else:
						window.windows[window.status].status = 'notStart'
						window.status = 'startWindow'

	def get_eventsGamePlay(self, window):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				window.run = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					window.windows[window.status] = 'notStart'
					window.status = 'startWindow'

		keys = pygame.key.get_pressed()

	def load_level(self, filename):
		file = open(filename, 'r')
		# read file
		file.close()

class Timer():
	def __init__(self, **kwargs):
		self.timer_seconds = kwargs['timer_seconds']
		self.coords = kwargs['coords']
		self.start_seconds = kwargs['start_seconds']
		self.seconds = kwargs['timer_seconds']

	def update(self):
		seconds = ceil(self.timer_seconds - (time.time() - self.start_seconds))
		self.seconds = seconds

	def draw(self, window):
		window.windows[window.status].screen.fill((0, 0, 0))

		self.update()
		font = pygame.font.Font(None, 50)
		text = font.render(str(self.seconds), 5, (255, 255, 255))
		window.windows[window.status].screen.blit(text, self.coords)

		pygame.display.update()

class StopWatch():
	def __init__(self, **kwargs):
		self.timer_seconds = kwargs['timer_seconds']
		self.coords = kwargs['coords']
		self.start_seconds = kwargs['start_seconds']
		self.seconds = 0

	def update(self):
		seconds = ceil(time.time() - self.start_seconds)
		self.seconds = seconds

	def draw(self, window):
		window.windows[window.status].screen.fill((0, 0, 0))

		self.update()
		font = pygame.font.Font(None, 50)
		text = font.render(str(self.seconds), 5, (255, 255, 255))
		window.windows[window.status].screen.blit(text, self.coords)

		pygame.display.update()

class Unit:

	def __init__(self, **kwargs):
		self.width = kwargs['width']
		self.height = kwargs['height']
		self.color = kwargs['color']
		self.x = kwargs['coordinates'][0]
		self.y = kwargs['coordinates'][1]
		self.speed = kwargs['speed']
		self.bullet_speed = kwargs['bullet_speed']
		self.sprite = kwargs['sprite']
		self.bullet_color = kwargs['bullet_color']
		self.bullet_width = kwargs['bullet_width']
		self.bullet_height = kwargs['bullet_height']
		self.bullets = []
		self.fire_rate = kwargs['fire_rate']
		self.health = 100
		self.side = kwargs['side']
		self.last_bullet = clock() - self.fire_rate
		self.form = kwargs['form']

	def draw(self, window):
		if self.sprite is None:
			if self.form == 'rect':
				pygame.draw.rect(window.windows[window.status].screen, self.color, (self.x, self.y, self.width, self.height))
		else:
			window.windows[window.status].screen.blit(self.sprite, (self.x, self.y))

	def add_bullet(self):
		t = clock()
		if t - self.last_bullet > self.fire_rate:
			self.last_bullet = t
			if self.side == 'enemy':
				bullet = Bullet(self.screen,
								width=self.bullet_width,
								height=self.bullet_height,
								speed=self.bullet_speed,
								color=self.bullet_color,
								coordinates=(self.x + self.width // 2, self.y + self.height)
								)
			else:
				bullet = Bullet(self.screen,
								width=self.bullet_width,
								height=self.bullet_height,
								speed=self.bullet_speed,
								color=self.bullet_color,
								coordinates=(self.x + self.width // 2, self.y)
								)
			self.bullets.append(bullet)

	def move_right(self):
		self.x += self.speed

	def move_left(self):
		self.x -= self.speed

	def move_up(self):
		self.y -= self.speed

	def move_down(self):
		self.y += self.speed

	def check_border(self, window):
		w = window.windows[window.status].screen.get_width()
		h = window.windows[window.status].screen.get_height()
		if self.x < -1 * self.width:
			self.x = w
		if self.x > w:
			self.x = -1 * self.width

	def health_bar(self):
		if self.health > 0:
			height = self.height // 7
			width = int(self.width * (self.health / 100))
			color = (255, 0, 0)
			if self.side == 'ally':
				draw.rect(window.windows[window.status].screen, color, (self.x, self.y - self.height//10 - height, width, height))
			else:
				draw.rect(window.windows[window.status].screen, color, (self.x, self.y + self.height + self.height // 10, width, height))

class Bullet:

	def __init__(self, screen, **kwargs):
		self.width = kwargs['width']
		self.height = kwargs['height']
		self.speed = kwargs['speed']
		self.color = kwargs['color']
		self.x = kwargs['coordinates'][0]
		self.y = kwargs['coordinates'][1]

	def draw(self, window):
		self.move_up()
		draw.rect(window.windows[window.status].screen, self.color, (self.x, self.y, self.width, self.height))

	def move_up(self):
		self.y -= self.speed

	def move_down(self):
		self.y += self.speed

	def move_left(self):
		self.x -= self.speed

	def move_right(self):
		self.x += self.speed

class Button:

	def __init__(self, **kwargs):
		self.width = kwargs['width']
		self.height = kwargs['height']
		self.text = kwargs['text']
		self.x = kwargs['coordinates'][0]
		self.y = kwargs['coordinates'][1]
		self.font_size = kwargs['font_size']
		self.text_color = kwargs['text_color']
		self.background_color = kwargs['background_color']
		self.sprite = kwargs['sprite']

	def write_text(self, window):
		font = pygame.font.Font(None, self.font_size)
		text = font.render(self.text, 0, self.text_color)
		window.windows[window.status].screen.blit(text, (self.x, self.y))

	def draw_background(self, window):
		draw.rect(window.windows[window.status].screen, self.background_color, (self.x, self.y, self.width, self.height))

	def draw(self, window):
		if self.sprite is None:
			self.draw_background(window)
			self.write_text(window)
		else:
			window.windows[window.status].screen.blit(self.sprite, (self.x, self.y))

	def collision_mouse(self, event):
		if event.type == MOUSEBUTTONDOWN:
			rect = Rect(self.x, self.y, self.width, self.height)
			if rect.collidepoint(event.pos[0], event.pos[1]):
				return True


def collision_rect(object1, object2):
	tl1x = object1.x
	tl1y = object1.y
	tr1x = object1.x + object1.width
	tr1y = object1.y
	bl1x = object1.x
	bl1y = object1.y + object1.height
	br1x = object1.x + object1.width
	br1y = object1.y + object1.height

	tl2x = object2.x
	tl2y = object2.y
	tr2x = object2.x + object2.width
	tr2y = object2.y
	bl2x = object2.x
	bl2y = object2.y + object2.height
	br2x = object2.x + object2.width
	br2y = object2.y + object2.height

	if tl1x < br2x and tl1y < br2y and tl1x > bl2x and tl1y > tr2y:
		return True
	elif tr1x > bl2x and tr1x < br2x and tr1y < br2y and tr1y > tr2y:
		return True
	elif bl1x < tr2x and bl1x > tl2x and bl1y > tl2y and bl1y < bl2y:
		return True
	elif br1x > tl2x and br1x < tr2x and br1y > tl2y and br1y < bl2y:
		return True
	elif tl2x < br1x and tl2y < br1y and tl2x > bl1x and tl2y > tr1y:
		return True
	elif tr2x > bl1x and tr2x < br1x and tr2y < br1y and tr2y > tr1y:
		return True
	elif bl2x < tr1x and bl2x > tl1x and bl2y > tl1y and bl2y < bl1y:
		return True
	elif br2x > tl1x and br2x < tr1x and br2y > tl1y and br2y < bl1y:
		return True
	else:
		return False


def window_resize(size):
	return display.set_mode(size)

class InputBox:

	def __init__(self, **kwargs):
		self.width = kwargs['width']
		self.height = kwargs['height']
		self.color = kwargs['color']
		self.border_width = kwargs['border_width']
		self.active_color = kwargs['active_color']
		self.no_active_color = kwargs['no_active_color']
		self.x = kwargs['coordinates'][0]
		self.y = kwargs['coordinates'][1]
		self.font_size = kwargs['font_size']
		self.text = ''
		self.text_color = kwargs['text_color']
		self.active = False
		self.Rect = Rect(self.x, self.y, self.width, self.height)
		self.border_color = self.no_active_color
		self.text_surface = None
		self.field_name = kwargs['field_name']
		self.enter = False

	def draw(self, window):
		font2 = font.Font(None, self.font_size)
		font1 = font.Font(None, self.font_size)
		text = font1.render(self.text, 0, self.text_color)
		text2 = font2.render(self.field_name, 0, self.border_color)
		self.text_surface = text
		draw.rect(window.windows[window.status].screen, (0, 0, 0), (self.x, self.y, self.width, self.height))
		window.windows[window.status].screen.blit(text, (self.x + self.border_width, self.y + self.border_width))
		window.windows[window.status].screen.blit(text2, (self.x + text2.get_width() // 2, self.y - text2.get_height()))
		draw.rect(window.windows[window.status].screen, self.border_color, (self.x, self.y, self.width, self.height), self.border_width)

	def check_event(self, event):
		if event.type == MOUSEBUTTONDOWN:
			if self.Rect.collidepoint(event.pos[0], event.pos[1]):
				if self.active:
					self.active = False
					self.border_color = self.no_active_color
				else:
					self.active = True
					self.border_color = self.active_color
			else:
				self.active = False
				self.border_color = self.no_active_color
		elif event.type == KEYDOWN:
			if self.active:
				if event.key == K_BACKSPACE:
					self.text = self.text[:-1]
				else:
					if self.text_surface.get_width() < self.width - 30:
						self.text += event.unicode
				if event.key == K_RETURN:
					self.enter = True

class User():
	def __init__(self, **kwargs):
		self.score = {}
		self.name = kwargs["name"]
		self.time = {}
		self.cur_level = kwargs['level']

	def save_results(self, level):
		# save results to current user in file
		with open('highscores.json', 'r') as json_file:
			data = json.load(json_file)
			try:
				user_data = data[self.name]
				try:
					data_level = user_data[level]
					data[self.name][level]['score'] = self.score[level]
					data[self.name][level]['time'] = self.time[level]
				except:
					data[self.name][level] = []
					data[self.name][level].append({
						'score': self.score[level],
						'time': self.time[level]
					})
			except:
				# add new user and save him results
				data[self.name] = {}
				data[self.name][level] = []
				data[self.name][level].append({
					'score': self.score[level],
					'time': self.time[level]
				})
			
			with open('highscores.json', 'w') as file:
				json.dump(data, file)

	def add_result(self, **kwargs):
		# save result to class
		level = str(kwargs['level'])
		self.score[level] = kwargs['score']
		self.time[level] = kwargs['time']
		self.save_results(level)

class StartWindow():
	def __init__(self, size):
		self.size = size
		self.InputBox = InputBox(
			width = int(size[0] * 0.8),
			height = int(size[1] * 0.2),
			coordinates = (int(size[0] * 0.1), int(size[1] * 0.2)),
			field_name = 'Ваше имя',
			font_size = 50,
			text_color = (0, 255, 0),
			color = (0, 0, 0),
			border_width = 5,
			active_color = (0, 0, 255),
			no_active_color = (255, 255, 0)
		)
		self.buttonContinue = Button(
			width = int(size[0] * 0.3),
			height = int(size[1] * 0.2),
			coordinates = (int(size[0] * 0.1), int(size[1] * 0.6)),
			font_size = 50,
			text_color = (0, 0, 0),
			background_color = (255, 255, 255),
			text = "Продолжить",
			sprite = None
		)
		self.buttonExit = Button(
			width = int(size[0] * 0.3),
			height = int(size[1] * 0.2),
			coordinates = (int(size[0] * 0.6), int(size[1] * 0.6)),
			font_size = 50,
			text_color = (0, 0, 0),
			background_color = (255, 255, 255),
			text = "Выйти",
			sprite = None
		)
		self.screen = pygame.display.set_mode(size)

	def draw(self, window, user):
		self.get_events(window, user)
		window.windows['startWindow'].screen.fill((0, 0, 0))

		self.InputBox.draw(window)
		self.buttonContinue.draw(window)
		self.buttonExit.draw(window)

		pygame.display.update()

	def get_events(self, window, user):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				window.run = False
			self.InputBox.check_event(event)
			if self.buttonContinue.collision_mouse(event) and self.InputBox.text != "":
				window.status = "Menu"
				user.name = self.InputBox.text
			if self.buttonExit.collision_mouse(event):
				window.run = False