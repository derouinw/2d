# tile.py
# Holds information for a single map tile
import common
import pygame

class Tile:
	numTiles = 0
	tiles = { 	0: pygame.image.load("dirt.bmp"),
			  	1: pygame.image.load("grass.bmp") }

	def __init__(self, tile):
		Tile.numTiles += 1

		self.image = Tile.tiles[tile]

	def __str__(self):
		return Tile.tiles.indexOf(self.image)

	def draw(self, x, y, screen):
		screen.blit(self.image, (x, y))