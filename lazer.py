import pygame
from pygame.locals import *
from constants import *
from math import *
from shot import *

def Lazer():
	return pygame.sprite.GroupSingle(LazerSprite())

class LazerSprite(pygame.sprite.Sprite):
	Height = 30
	Width = 125

	# Pulsing in and out should take about a second.
	FlashLen = FPS
	BulbNormal = 205	# Alpha

	Cooldown = 60		# Frames

	def createLazer(self):
		image = pygame.Surface((LazerSprite.Width, LazerSprite.Height), SRCALPHA)
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
		pygame.draw.circle(image, (0,255,0,LazerSprite.BulbNormal), [5, 15], 5)
		pygame.draw.arc(image, green, pygame.Rect(8,7,10,16), radians(-180), radians(0), 1)
		pygame.draw.arc(image, green, pygame.Rect(20,7,10,16), radians(0), radians(180), 1)
		pygame.draw.arc(image, green, pygame.Rect(30,7,10,16), radians(-180), radians(0), 1)
		pygame.draw.arc(image, green, pygame.Rect(40,7,10,16), radians(0), radians(180), 1)
		image.unlock()

		return image, rect

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = self.createLazer()
		
		screenRect = pygame.display.get_surface().get_rect()
		self.rect.topleft = (screenRect.width - LazerSprite.Width, (screenRect.height - LazerSprite.Height) / 2)

		self.pulseFrame = 0
		self.fireFrame = 0

	def canFire(self, shots):
		return self.fireFrame >= LazerSprite.Cooldown 

	def fire(self, shots):
		screenRect = pygame.display.get_surface().get_rect()
		left = screenRect.width - self.rect.width + 5

		shots.add(ShotSprite(left))
		self.fireFrame = 0

	def update(self, shots):
		self.pulseFrame = (self.pulseFrame+1) % LazerSprite.FlashLen
		mod = sin(radians(360*self.pulseFrame/LazerSprite.FlashLen))
		alpha = LazerSprite.BulbNormal + (50*mod)
		pygame.draw.circle(self.image, (0,255,0,alpha), [5, 15], 5)

		if self.canFire(shots):
			self.fire(shots)
		else:
			self.fireFrame += 1
