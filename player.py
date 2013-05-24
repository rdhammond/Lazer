import pygame
from constants import *
from math import *

class Player(pygame.sprite.Sprite):
	height = 75
	width = 75

	minPos = 20
	maxPos = 300

	# We want to cover the entire distance in one second when
	# moving backwards. Forwards will take twice as long.
	#
	moveVel = (maxPos - minPos) / FPS

	driftVel = 1

	# Frames per normal (non-antigrav) jump
	normalJumpTime = 30
	normalSpinTime = 30

	# Initial velocity in Pixels/frame
	jumpVelZero = -0.5 * GRAVITY * normalJumpTime

	def createPlayer(self):
		image = pygame.Surface((Player.width,Player.height))
		rect = image.get_rect()

		image.set_colorkey((0,0,0))
		pygame.draw.rect(image, (0,255,0), image.get_rect(), 1)

		return image, rect

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = self.createPlayer()

		self.screenHeight = pygame.display.get_surface().get_rect().height
		self.moveTo((Player.minPos, self.screenHeight - Player.height))
		self.original = self.image.copy()

		self.angle = 0
		self.spinning = False

		self.jumpframe = 0
		self.jumpdist = 0
		self.jumping = False

		self.antigrav = False
		self.hasswitchedgrav = False

	def blitTo(self, screen):
		screen.blit(self.image, self.rect)
		return self.rect

	def rotateTo(self, angle):
		center = self.rect.center
		self.image = pygame.transform.rotate(self.original, angle)
		self.rect = self.image.get_rect(center=center)
		self.angle = angle

	def moveTo(self, pos):
		self.rect.topleft = pos

	def jump(self):
		self.rotStep = -360.0 / Player.normalSpinTime

		self.jumpframe = 0
		self.maxJump = -0.125 * GRAVITY * Player.normalJumpTime * Player.normalJumpTime

		if self.antigrav:
			self.jumpdist = self.screenHeight - 0.5*Player.height
			self.jumpVel = -Player.jumpVelZero
			self.rotStep = -self.rotStep
		else:
			self.jumpdist = 0
			self.jumpVel = Player.jumpVelZero

		self.jumping = True

	def canjump(self):
		return not self.jumping

	def canswitchgrav(self):
		if self.hasswitchedgrav:
			return False

		if self.antigrav:
			zenith = self.screenHeight - 0.5*Player.height - self.maxJump
			return zenith <= self.jumpdist <= (zenith + 20)
		else:
			return (self.maxJump - 20) <= self.jumpdist <= self.maxJump

	def update(self, direction=None):
		if self.jumping:
			if not self.antigrav:
				self.jumpdist += 0.5*GRAVITY*(2*self.jumpframe+1) + self.jumpVelZero
			else:
				self.jumpdist += -0.5*GRAVITY*(2*self.jumpframe+1) - self.jumpVelZero

			self.jumpframe += 1

			if (not self.antigrav and self.jumpdist <= 0) or (self.antigrav and self.jumpdist >= self.screenHeight):
				angle = 0
				self.jumping = False
				self.hasswitchedgrav = False

				if self.antigrav:
					y = 0
				else:
					y = self.screenHeight - Player.height
			else:
				angle = self.rotStep * self.jumpframe
				y = self.screenHeight - Player.height - self.jumpdist

			self.rotateTo(angle)
		else:
			y = self.rect.top

		x = self.rect.left

		if direction == "right":
			x += (Player.moveVel*0.5)
			if x > Player.maxPos:
				x = Player.maxPos
		elif direction == "left":
			x -= Player.moveVel
			if x < Player.minPos:
				x = Player.minPos
		else:
			x -= Player.driftVel
			if x < Player.minPos:
				x = Player.minPos

		self.moveTo((x,y))

	def switchgrav(self):
		if self.antigrav:
			distance = self.jumpdist
			v = self.jumpVel
			totalrot = -360 - self.angle
		else:
			distance = self.screenHeight - Player.height - self.jumpdist
			v = -self.jumpVel
			totalrot = 360 - self.angle

		frames = floor((-v + sqrt(v*v - 2*GRAVITY*distance))/GRAVITY)
		self.rotStep = -totalrot / frames

		self.antigrav = not self.antigrav
		self.hasswitchedgrav = False
