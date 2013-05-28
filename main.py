import sys, pygame
from pygame.locals import *
from constants import *
from tunnel import *
from player import *
from lazer import *
from shot import *

DeathDelay = 1000

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), HWSURFACE | DOUBLEBUF)
clock = pygame.time.Clock()

tunnel = Tunnel()
player = Player(tunnel)
lazer = Lazer()
shots = Shots()

rightdown = False
leftdown = False
paused = False

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

			elif event.unicode == "p":
				paused = not paused

			elif event.unicode == "q":
				sys.exit()

		elif event.type == KEYUP:
			if event.key == K_RIGHT:
				rightdown = False
			elif event.key == K_LEFT:
				leftdown = False

	if paused:
		clock.tick(FPS)
		continue

	# TODO: Organize this nicer
	if not player.sprite.dying:
		collideShots = pygame.sprite.spritecollide(player.sprite, shots, False, PlayerSprite.collideTest)
	
		if len(collideShots) > 0:
			player.sprite.die()

	if not player.sprite.dying:
		tunnel.update()
	
		if rightdown:
			player.update(tunnel, "right")
		elif leftdown:
			player.update(tunnel, "left")
		else:
			player.update(tunnel)
		
		lazer.update(shots)
		shots.update()

	elif not player.sprite.dead:
		player.update(tunnel)

	screen.fill((0,0,0))
	tunnel.draw(screen)
	player.draw(screen)
	lazer.draw(screen)
	shots.draw(screen)
	pygame.display.flip()

	if player.sprite.dead:
		pygame.time.wait(DeathDelay)
		player.sprite.reset(tunnel)
	else:
		clock.tick(FPS)
