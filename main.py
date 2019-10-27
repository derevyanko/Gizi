import pygame
from objects import *

pygame.init()
pygame.font.init()

clock = pygame.time.Clock()

window = Window(
	size = (1000, 800),
	name = 'Game',
	run = True
)

user = User(
	name = "",
	level = '1'
)

while window.run:
	clock.tick(60)
	print(user.name)
	if window.status == 'gameplay':
		if window.windows['gameplay'].status is 'winWindow':
			window.windows['gameplay'].winWindow(window)
		elif window.windows['gameplay'].status is 'gameOver':
			window.windows['gameplay'].gameOverWindow(window)
		else:
			window.windows['gameplay'].gamePlay(window)
	elif window.status == 'startWindow':
		window.windows['startWindow'].draw(window, user)
	elif window.status == 'Menu':
		window.windows['Menu'].draw(window)

pygame.quit()