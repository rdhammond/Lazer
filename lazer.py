import pygame
from pygame.locals import *
from constants import *
from math import *

class Lazer(pygame.sprite.Sprite):
	height = 30
	width = 125

	# Pulsing in and out should take about a second.
	flashlen = FPS
	bulbnormal = 205

	def createLazer(self):
		image = pygame.Surface((Lazer.width, Lazer.height), SRCALPHA)
		rect = image.get_rect()

		image.set_colorkey((0,0,0,0))
		green = (0,255,0)

		image.lock()
		pygame.draw.rect(image, green, pygame.Rect(50,0,76,30), 1)
		pygame.draw.line(image, green, [0,15], [50,15], 1)
		pygame.draw.rect(image, green, pygame.Rect(65,7,45,16), 1)
		pygame.draw.line(image, green, [76,7], [76,22], 1)
		pygame.draw.line(image, green, [87,7], [87,22], 1)
		pygame.draw.line(image, green, [98,7], [98,22], 1)
		pygame.draw.circle(image, (0,255,0,Lazer.bulbnormal), [5, 15], 5)
		pygame.draw.arc(image, green, pygame.Rect(8,7,10,16), radians(-180), radians(0), 1)
		pygame.draw.arc(image, green, pygame.Rect(20,7,10,16), radians(0), radians(180), 1)
		pygame.draw.arc(image, green, pygame.Rect(30,7,10,16), radians(-180), radians(0), 1)
		pygame.draw.arc(image, green, pygame.Rect(40,7,10,16), radians(0), radians(180), 1)
		image.unlock()

		return image, rect

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = self.createLazer()
		
		screenrect = pygame.display.get_surface().get_rect()
		self.rect.topleft = (screenrect.width - Lazer.width, (screenrect.height - Lazer.height) / 2)

		self.pulseframe = 0

	def blitTo(self, surface):
		surface.blit(self.image, self.rect)
		return self.rect

	def update(self):
		self.pulseframe = (self.pulseframe+1) % Lazer.flashlen
		mod = sin(radians(360*self.pulseframe/Lazer.flashlen))
		alpha = Lazer.bulbnormal + (50*mod)
		
		pygame.draw.circle(self.image, (0,255,0,alpha), [5, 15], 5)
