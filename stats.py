# stats.py
# includes information about a character's attributes
# therefore, should have an instance in every character, player and npc
import common

class Stats:
	def __init__(self):
		self.attr1 = 10
		self.attr2 = 10
		self.attr3 = 10
		self.position = [128,128]
		self.velocity = [0,0]
		self.moveSpeed = 16
		# etc

	def __str__(self):
		return "Attr1: " + str(self.attr1) + " Attr2: " + str(self.attr2) + " Attr2: " + str(self.attr3) + " Position: " + str(self.position) + " Move speed: " + str(self.moveSpeed)

	def reset(attr1, attr2, attr3, position):
		self.attr1 = attr1
		self.attr2 = attr2
		self.attr3 = attr3
		self.position = position