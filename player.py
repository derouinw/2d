# player.py
# includes the main user player class
import common
import pygame
import stats, inventory
from pygame.locals import *

class Player:
	def __init__(self):
		# character attributes and such
		self.stats = stats.Stats()

		# character's inventory
		# includes info like equipped and customization as well
		self.inventory = inventory.Inventory()

		self.image = pygame.image.load("player.png").convert_alpha()

		# tuple of keys used
		self.keys = (K_UP, K_DOWN, K_LEFT, K_RIGHT, K_SPACE)

	def __str__(self):
		return "Player with Stats: " + str(self.stats) + " and Inventory: " + str(self.inventory)

	def draw(self, offset, screen):
		# offset represents where to actually draw the player on the screen
		# versus its actual map position
		# (determined by explore man)
		pX = self.stats.position[0] + offset[0]
		pY = self.stats.position[1] + offset[1]
		screen.blit(self.image, (pX, pY))

	def handleInput(self, event):
		if event.key == K_UP:
			self.move((0,-self.stats.moveSpeed))
			#self.stats.velocity[1] = -self.stats.moveSpeed
		elif event.key == K_DOWN:
			self.move((0, self.stats.moveSpeed))
			#self.stats.velocity[1] = self.stats.moveSpeed
		elif event.key == K_RIGHT:
			self.move((self.stats.moveSpeed, 0))
			#self.stats.velocity[0] = self.stats.moveSpeed
		elif event.key == K_LEFT:
			self.move((-self.stats.moveSpeed, 0))
			#self.stats.velocity[0] = -self.stats.moveSpeed
		elif event.key == K_SPACE:
			self.stats.moveSpeed = 32 if self.stats.moveSpeed == 16 else 16

		#self.move(self.stats.velocity)

	def move(self, vec):
		self.stats.position[0] += vec[0]
		self.stats.position[1] += vec[1]

	def update(self):
		self.stats.position[0] += self.stats.velocity[0]
		self.stats.position[1] += self.stats.velocity[1]
