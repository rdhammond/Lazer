import sys, pygame
from pygame.locals import *
from constants import *
from player import *
from lazer import *
from shot import *

pygame.init()
screen = pygame.display.set_mode((600, 600), HWSURFACE | DOUBLEBUF)
clock = pygame.time.Clock()

player = Player()
lazer = Lazer()
shots = Shots()

rightdown = False
leftdown = False

while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			sys.exit()

		elif event.type == KEYDOWN:
			if event.key == K_SPACE: 
				if player.sprite.canjump():
					player.sprite.jump()
				elif player.sprite.canswitchgrav():
					player.sprite.switchgrav()

			elif event.key == K_RIGHT:
				rightdown = True

			elif event.key == K_LEFT:
				leftdown = True

			elif event.unicode == "s":
				lazer.fire()

			elif event.unicode == "q":
				sys.exit()

		elif event.type == KEYUP:
			if event.key == K_RIGHT:
				rightdown = False
			elif event.key == K_LEFT:
				leftdown = False

	if rightdown:
		player.update("right")
	elif leftdown:
		player.update("left")
	else:
		player.update()
	
	lazer.update(shots)
	shots.update()

	screen.fill((0,0,0))
	player.draw(screen)
	lazer.draw(screen)
	shots.draw(screen)
	pygame.display.flip()
	clock.tick(FPS)
