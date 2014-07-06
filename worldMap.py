# worldMap.py
# holds the data for the world map including tile info, etc
import common
import random
import pygame
import ConfigParser

class Map:
	def __init__(self, mapname):
		self.map = []
		self.key = {}

		parser = ConfigParser.ConfigParser()
		parser.read(mapname)
		self.tileset = parser.get("level", "tileset")

		# list of tiles
		self.tiles = self.load_tile_table(self.tileset)

		self.map = parser.get("level", "map").split("\n")
		for section in parser.sections():
			if len(section) == 1:
				desc = dict(parser.items(section))
				self.key[section] = desc

		self.portals = dict(parser.items('portals'))
		self.entries = dict(parser.items('entries'))

		self.width = len(self.map[0])
		self.height = len(self.map)

		self.start = self.find_loc(self.entries['one'])

	def __str__(self):
		result = ""
		for tile in self.map:
			result += str(tile)
		return result

	# draws the map from the top left point
	# this is calculated from within the
	# explore manager and passed here
	def draw(self, offset, screen):
		for y in range(len(self.map)):
			for x in range(len(self.map[0])):
				tX = x*common.tileSize + offset[0]
				tY = y*common.tileSize + offset[1]
				if tX > common.width or tX < -common.tileSize or tY > common.height or tY < -common.tileSize:
					continue
				curTile = self.get_tile(x, y)
				if curTile == {}:
					tile = 0,0
				else:
					tile = curTile['tile'].split(',')
					tile = int(tile[0]), int(tile[1])
				try:
					screen.blit(self.tiles[tile[0]][tile[1]], (tX, tY))
				except:
					pass

	# http://qq.readthedocs.org/en/latest/tiles.html
	def load_tile_table(self, filename):
		image = pygame.image.load(filename)
		image_width, image_height = image.get_size()
		tile_table = []
		for tile_x in range(0, image_width/common.tileSize):
			line = []
			tile_table.append(line)
			for tile_y in range(0, image_height/common.tileSize):
				rect = (tile_x*common.tileSize, tile_y*common.tileSize, common.tileSize, common.tileSize)
				line.append(image.subsurface(rect))
		return tile_table

	def get_tile(self, x, y):
		try:
			char = self.map[y][x]
		except IndexError:
			return {}
		try:
			return self.key[char]
		except KeyError:
			return {}

	def collidable(self,x, y):
		tile = self.get_tile(x, y)
		try:
			if tile['wall'] == 'True':
				return True
		except:
			pass
		return False

	def object_collision(self, x, y):
		tile = self.get_tile(x, y)
		try:
			return tile['object']
		except:
			return False

	def find_loc(self, tile):
		for y in range(len(self.map)):
			for x in range(len(self.map[0])):
				if self.map[y][x] == tile:
					return x, y
		return False

	def find_start(self, start):
		self.start = self.find_loc(self.entries[start])