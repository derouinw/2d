# explore.py
# game manager for the explore game state
import common
import pygame
from pygame.locals import *

DIR_UP = 0
DIR_RIGHT = 1
DIR_DOWN = 2
DIR_LEFT = 3

class ExploreMan:

	def __init__(self, player, worldMap, screen):
		# player character instance
		self.player = player

		# world map instance
		self.map = worldMap

		# Surface used to draw on
		self.screen = screen

		# other things drawn on top of the normal game map
		# like messages
		self.others = pygame.Surface((common.width, common.height), pygame.SRCALPHA, 32).convert_alpha()

		self.font = pygame.font.SysFont("monospace", 15)

		# for loading next level
		# filename of map
		self.next_level = ""

	def __str__(self):
		return "Map with Player: " + str(self.player) + ", Map: " + str(self.map) + " and screen: " + str(screen)

	def draw(self):
		self.screen.fill(common.black)
		
		# calculate offset of player based on position in map
		oX = oY = 0
		if self.player.stats.position[0] > common.width / 2: 
			oX = common.width / 2 - self.player.stats.position[0]
	 	if self.player.stats.position[0] > self.map.width*common.tileSize - common.width/2:
			oX = common.width - self.map.width*common.tileSize
		if self.player.stats.position[1] > common.height / 2:
			oY = common.height / 2 - self.player.stats.position[1]
		if self.player.stats.position[1] > self.map.height*common.tileSize - common.height/2:
			oY = common.height - self.map.height*common.tileSize
		offset = (oX, oY)
		self.map.draw(offset, self.screen) # coordinate based on player location
		self.player.draw(offset, self.screen)
		self.screen.blit(self.others, (0,0))
		pygame.display.update()

	def handleInput(self, event):
		# close button
		if event.type == QUIT:
			return -1

		# keys
		if event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				return -1
			elif event.key in self.player.keys:
				if event.key == K_UP:
					self.player.stats.velocity[1] = -self.player.stats.moveSpeed
				elif event.key == K_DOWN:
					self.player.stats.velocity[1] = self.player.stats.moveSpeed
				elif event.key == K_LEFT:
					self.player.stats.velocity[0] = -self.player.stats.moveSpeed
				elif event.key == K_RIGHT:
					self.player.stats.velocity[0] = self.player.stats.moveSpeed
			elif event.key == K_f:
				tX = self.player.stats.position[0]/common.tileSize
				tY = self.player.stats.position[1] / common.tileSize
				print "Player loc: " + str(self.player.stats.position) + ", tile on loc: " + str(tX) + ", " + str(tY)
		elif event.type == KEYUP:
			if event.key in self.player.keys:
				if event.key == K_UP:
					self.player.stats.velocity[1] = 0
				elif event.key == K_DOWN:
					self.player.stats.velocity[1] = 0
				elif event.key == K_LEFT:
					self.player.stats.velocity[0] = 0
				elif event.key == K_RIGHT:
					self.player.stats.velocity[0] = 0

	def check_collision(self, character, direction):
		pos = character.stats.position
		if direction == DIR_UP:
			if pos[1] < character.stats.moveSpeed:
				return True
			# check collidable objects in map
			tX = pos[0]/common.tileSize
			tY = pos[1]/common.tileSize

			if pos[0] % common.tileSize == 0:
				above = self.map.collidable(tX, tY-1), False
			else:
				left = pos[0] % common.tileSize < common.tileSize/2
				if left:
					above = self.map.collidable(tX-1, tY-1), self.map.collidable(tX, tY-1)
				else:
					above = self.map.collidable(tX, tY-1), self.map.collidable(tX+1, tY-1)

			if (above[0] or above[1]) and pos[1]%common.tileSize < character.stats.moveSpeed:
				return True
		elif direction == DIR_RIGHT:
			if pos[0] > self.map.width*common.tileSize - 3*character.stats.moveSpeed:
				return True
			tX = pos[0]/common.tileSize
			tY = pos[1]/common.tileSize
			
			if pos[1] % common.tileSize == 0:
				right = self.map.collidable(tX+1, tY), False
			else:
				above = pos[1] % common.tileSize < common.tileSize / 2
				if above:
					right = self.map.collidable(tX+1, tY-1), self.map.collidable(tX+1, tY)
				else:
					right = self.map.collidable(tX+1, tY), self.map.collidable(tX+1, tY+1)

			if (right[0] or right[1]) and pos[0]%common.tileSize < character.stats.moveSpeed:
				return True
		elif direction == DIR_DOWN:
			if pos[1] > self.map.height*common.tileSize - 3*character.stats.moveSpeed:
				return True
			tX = pos[0]/common.tileSize
			tY = pos[1]/common.tileSize
			
			if pos[0] % common.tileSize == 0:
				below = self.map.collidable(tX, tY+1), False
			else:
				left = pos[0] % common.tileSize < common.tileSize / 2
				if left:
					below = self.map.collidable(tX-1, tY+1), self.map.collidable(tX, tY+1)
				else:
					below = self.map.collidable(tX, tY+1), self.map.collidable(tX+1, tY+1)

			if (below[0] or below[1]) and pos[1]%common.tileSize < character.stats.moveSpeed:
				return True
		elif direction == DIR_LEFT:
			if pos[0] < character.stats.moveSpeed:
				return True
			tX = pos[0]/common.tileSize
			tY = pos[1]/common.tileSize

			if pos[1] % common.tileSize == 0:
				left = self.map.collidable(tX-1, tY), False
			else:
				above = pos[1] % common.tileSize < common.tileSize / 2
				if above:
					left = self.map.collidable(tX-1, tY-1), self.map.collidable(tX-1, tY)
				else:
					left = self.map.collidable(tX-1, tY), self.map.collidable(tX-1, tY+1)

			if (left[0] or left[1]) and pos[0]%common.tileSize < character.stats.moveSpeed:
				return True
		return False

	def check_chars(self):
		# player

		# wall collisions
		if self.player.stats.velocity[0] > 0:
			if self.check_collision(self.player, DIR_RIGHT):
				self.player.stats.velocity[0] = 0
		elif self.player.stats.velocity[0] < 0:
			if self.check_collision(self.player, DIR_LEFT):
				self.player.stats.velocity[0] = 0

		if self.player.stats.velocity[1] > 0:
			if self.check_collision(self.player, DIR_DOWN):
				self.player.stats.velocity[1] = 0
		elif self.player.stats.velocity[1] < 0:
			if self.check_collision(self.player, DIR_UP):
				self.player.stats.velocity[1] = 0

		# object collisions
		obj = self.map.object_collision(self.player.stats.position[0]/common.tileSize, self.player.stats.position[1]/common.tileSize)
		if obj:
			if obj == "chest":
				label = self.font.render("Press space to open!", 1, common.white)
				self.others.blit(label, self.player.stats.position)
			elif obj == "portal":
				label = self.font.render("Press space to go through!", 1, common.white)
				self.others.blit(label, self.player.stats.position)
				if pygame.key.get_pressed()[K_SPACE]:
					# get portal from map data -> get name of new map
					tX = self.player.stats.position[0]/common.tileSize
					tY = self.player.stats.position[1]/common.tileSize
					tile = self.map.get_tile(tX,tY)
					self.next_level = self.map.portals[tile['name']]
					self.out = tile['out']
					return 77

		return 0

	def get_next(self):
		return self.next_level

	def get_out(self):
		return self.out

	# run every frame
	def loop(self):
		self.others.fill(pygame.SRCALPHA)
		for event in pygame.event.get():
			if self.handleInput(event) == -1:
				return -1
		if self.check_chars() == 77:
			return 77
		self.player.update()
		self.draw()
