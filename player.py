import pygame
from constants import *
from math import *

def Player():
	return pygame.sprite.GroupSingle(PlayerSprite())

class PlayerSprite(pygame.sprite.Sprite):
	Height = 40
	Width = 40

	MinPos = 20
	MaxPos = 300
	FlipWindow = 40

	# We want to cover the entire distance in one second when
	# moving backwards. Forwards will take twice as long.
	#
	MoveVel = (MaxPos - MinPos) / FPS

	DriftVel = 1

	# Frames per normal (non-antigrav) jump
	NormalJumpTime = 30
	NormalSpinTime = 30

	# Initial velocity in Pixels/frame
	JumpVelZero = -0.5 * GRAVITY * NormalJumpTime

	def createPlayer(self):
		image = pygame.Surface((PlayerSprite.Width,PlayerSprite.Height))
		rect = image.get_rect()

		image.set_colorkey((0,0,0))
		pygame.draw.rect(image, (0,255,0), image.get_rect(), 1)

		return image, rect

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = self.createPlayer()

		self.screenHeight = pygame.display.get_surface().get_rect().height
		self.moveTo((PlayerSprite.MinPos, self.screenHeight - PlayerSprite.Height))
		self.original = self.image.copy()

		self.angle = 0
		self.spinning = False

		self.jumpFrame = 0
		self.jumpDist = 0
		self.jumping = False

		self.antigrav = False
		self.hasSwitchedGrav = False

	def rotateTo(self, angle):
		center = self.rect.center
		self.image = pygame.transform.rotate(self.original, angle)
		self.rect = self.image.get_rect(center=center)
		self.angle = angle

	def moveTo(self, pos):
		self.rect.topleft = pos

	def jump(self):
		self.rotStep = -360.0 / PlayerSprite.NormalSpinTime

		self.jumpFrame = 0
		self.maxJump = -0.125 * GRAVITY * PlayerSprite.NormalJumpTime * PlayerSprite.NormalJumpTime

		if self.antigrav:
			self.jumpDist = self.screenHeight - 0.5*PlayerSprite.Height
			self.jumpVel = -PlayerSprite.JumpVelZero
			self.rotStep = -self.rotStep
		else:
			self.jumpDist = 0
			self.jumpVel = PlayerSprite.JumpVelZero

		self.jumping = True

	def canjump(self):
		return not self.jumping

	def canswitchgrav(self):
		if self.hasSwitchedGrav:
			return False

		if self.antigrav:
			zenith = self.screenHeight - 0.5*PlayerSprite.Height - self.maxJump
			return zenith <= self.jumpDist <= (zenith + PlayerSprite.FlipWindow)
		else:
			return (self.maxJump - PlayerSprite.FlipWindow) <= self.jumpDist <= self.maxJump

	def update(self, direction=None):
		if self.jumping:
			if not self.antigrav:
				self.jumpDist += 0.5*GRAVITY*(2*self.jumpFrame+1) + PlayerSprite.JumpVelZero
			else:
				self.jumpDist += -0.5*GRAVITY*(2*self.jumpFrame+1) - PlayerSprite.JumpVelZero

			self.jumpFrame += 1

			if (not self.antigrav and self.jumpDist <= 0) or (self.antigrav and self.jumpDist >= self.screenHeight):
				angle = 0
				self.jumping = False
				self.hasSwitchedGrav = False

				if self.antigrav:
					y = 0
				else:
					y = self.screenHeight - PlayerSprite.Height
			else:
				angle = self.rotStep * self.jumpFrame
				y = self.screenHeight - PlayerSprite.Height - self.jumpDist

			self.rotateTo(angle)
		else:
			y = self.rect.top

		x = self.rect.left

		if direction == "right":
			x += (PlayerSprite.MoveVel*0.5)
		elif direction == "left":
			x -= PlayerSprite.MoveVel
		else:
			x -= PlayerSprite.DriftVel

		if x < PlayerSprite.MinPos:
			x = PlayerSprite.MinPos
		elif x > PlayerSprite.MaxPos:
			x = PlayerSprite.MaxPos

		self.moveTo((x,y))

	def switchgrav(self):
		if self.antigrav:
			distance = self.jumpDist
			v = self.jumpVel
			totalRot = -360 - self.angle
		else:
			distance = self.screenHeight - PlayerSprite.Height - self.jumpDist
			v = -self.jumpVel
			totalRot = 360 - self.angle

		frames = floor((-v + sqrt(v*v - 2*GRAVITY*distance))/GRAVITY)
		self.rotStep = -totalRot / frames

		self.antigrav = not self.antigrav
		self.hasSwitchedGrav = False
