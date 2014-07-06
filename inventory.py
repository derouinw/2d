# inventory.py
# holds all the items and equipped for a character
import common

class Inventory:
	def __init__(self):
		# list of Items that are currently equipped
		self.equipped = []

		# list of Items that are currently held in inventory space
		self.items = []

	def __str__(self):
		result = "Equipped: "
		for item in self.equipped:
			result += str(item) + ", "
		result += "Held: "
		for item in self.items:
			result += str(item) + ", "
		return result