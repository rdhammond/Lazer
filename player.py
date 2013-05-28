import pygame
import math
from constants import *

class Player(pygame.sprite.GroupSingle):
	def __init__(self, tunnel):
		pygame.sprite.GroupSingle.__init__(self, PlayerSprite(tunnel))

	def draw(self, surface):
		if not self.sprite.dead:
			pygame.sprite.GroupSingle.draw(self, surface)

class PlayerSprite(pygame.sprite.Sprite):
	Height = 40
	Width = 40

	MinPosX = 20
	MaxPosX = 300
	NoFlipWindow = 40

	# Death should take a second. 
	DeathFrames = FPS * 1

	# We want to cover the entire distance in one second when
	# moving backwards. Forwards will take twice as long.
	#
	MoveVel = (MaxPosX-MinPosX) / FPS
	DriftVel = 1

	# "Normal" jump, i.e. no antigrav on flat surface, should take
	# half a second.
	#
	NormalJumpTime = FPS / 2
	JumpVelBar = abs(0.5 * GRAVITY * NormalJumpTime)

	def collideTest(player, obstacle):
		return player.originalRect.colliderect(obstacle.rect)

	def createPlayer(self, color):
		image = pygame.Surface((PlayerSprite.Width,PlayerSprite.Height))
		rect = image.get_rect()

		image.set_colorkey((0,0,0))
		pygame.draw.rect(image, color, image.get_rect(), 1)

		return image, rect

	def __init__(self, tunnel):
		pygame.sprite.Sprite.__init__(self)

		self.screenHeight = pygame.display.get_surface().get_rect().height
		self.reset(tunnel)

	def rotateTo(self, angle):
		center = self.rect.center

		self.image = pygame.transform.rotate(self.original, angle)
		self.rect = self.image.get_rect(center=center)
		self.angle = angle

	def moveTo(self, pos):
		self.rect.topleft = (pos[0], self.screenHeight - pos[1])
		self.originalRect.topleft = self.rect.topleft

	def getAngle(self):
		return self.angle

	def getPos(self):
		return self.rect.left, self.screenHeight - self.rect.top

	def jump(self):
		left, top = self.getPos()

		self.jumpFrame = 0
		self.jumpStart = top

		if not self.antigrav:
			self.jumpVelZero = PlayerSprite.JumpVelBar
		else:
			self.jumpVelZero = -PlayerSprite.JumpVelBar

		g = self.gravity
		v0 = self.jumpVelZero
		midFrame = -v0 / g
		self.maxJump = 0.5*g*midFrame**2 + v0*midFrame + self.jumpStart
		self.rotVel = (-360 if not self.antigrav else 360) / midFrame*2

		self.jumping = True

	def canjump(self):
		return not self.jumping

	def canswitchgrav(self):
		if self.hasSwitchedGrav:
			return False

		left, top = self.getPos()

		if not self.antigrav:
			#return (self.maxJump - PlayerSprite.FlipWindow) <= top <= self.maxJump
			return top > PlayerSprite.NoFlipWindow
		else:
			#return self.maxJump <= top <= (self.maxJump + PlayerSprite.FlipWindow)
			return top < (self.screenHeight - PlayerSprite.NoFlipWindow)

	def calcY(self):
		g = self.gravity
		v0 = self.jumpVelZero
		t = self.jumpFrame
		y0 = self.jumpStart

		return 0.5*g*t**2 + v0*t + y0

	def jumpVel(self):
		g = self.gravity
		t = self.jumpFrame
		v0 = self.jumpVelZero

		return g*t + v0

	# TODO: Organize this nicer
	def update(self, tunnel, direction=None):
		if self.dead:
			return

		left, top = self.getPos()

		if self.dying:
			angle = self.angle + self.rotVel
			self.rotateTo(angle)
			self.dieFrame += 1

			if self.dieFrame >= PlayerSprite.DeathFrames:
				self.dead = True
			
			return

		if direction == "right":
			left += PlayerSprite.MoveVel * 0.5
		elif direction == "left":
			left -= PlayerSprite.MoveVel
		else:
			left -= PlayerSprite.DriftVel

		if left < PlayerSprite.MinPosX:
			left = PlayerSprite.MinPosX
		elif left > PlayerSprite.MaxPosX:
			left = PlayerSprite.MaxPosX

		if self.jumping:
			self.jumpFrame += 1
			top = self.calcY()

			floor, ceiling = tunnel.getBounds(int(left))
				
			if (not self.antigrav and top <= floor+PlayerSprite.Height) or (self.antigrav and top >= ceiling):
				floorAngle, ceilingAngle = tunnel.getAngle(int(left))

				if not self.antigrav:
					top = floor+PlayerSprite.Height
					angle = floorAngle
				else:
					top = ceiling
					angle = ceilingAngle

				self.jumping = False
				self.hasSwitchedGrav = False
			else:
				angle = self.angle + self.rotVel

			self.rotateTo(angle)

		self.moveTo((left, top))

	def switchgrav(self):
		left, top = self.getPos()

		self.jumpVelZero = self.jumpVel()
		self.gravity = -self.gravity

		if not self.antigrav:
			self.jumpStart += PlayerSprite.Height

		self.antigrav = not self.antigrav
		self.hasSwitchedGrav = False

	def die(self):
		self.rotVel = -15
		self.dieFrame = 0
		self.dying = True

	def reset(self, tunnel):
		self.dieFrame = 0
		self.dying = False
		self.dead = False

		self.original, self.originalRect = self.createPlayer((0,255,0))
		self.rect = self.originalRect.copy()

		floorAngle = tunnel.getAngle(PlayerSprite.MinPosX)[0]
		self.rotateTo(floorAngle)

		floor = tunnel.getBounds(PlayerSprite.MinPosX)[0]
		self.antigrav = False
		self.moveTo((PlayerSprite.MinPosX, floor+PlayerSprite.Height))

		self.jumpFrame = 0
		self.gravity = GRAVITY
		self.jumpVelZero = 0
		self.rotVel = 0
		self.jumping = False

		self.hasSwitchedGrav = False
