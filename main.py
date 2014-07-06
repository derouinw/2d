# 2RAGE
# 2d rpg advanced game engine
# Main module
import sys, pygame
from pygame.locals import *
import common
import explore, player, stats, worldMap

class GameState:
	loading, menu, explore, cutscene, gameover, exit = range(6)

pygame.init()
pygame.key.set_repeat(1, 10)

gamestate = GameState.loading

# Setup important variables
screen = pygame.display.set_mode(common.window)
player = player.Player()
world = worldMap.Map("level.map")
world.find_start('one')
player.stats.position = list(world.start)
player.stats.position[0] *= common.tileSize
player.stats.position[1] *= common.tileSize
em = explore.ExploreMan(player, world, screen)
next_level = "level.map"
next_start = "one"

# Main game loop
running = True
while running:
	# Main gamestate switch
	if gamestate == GameState.loading:
		# manage loading
		world = worldMap.Map(next_level)
		world.find_start(next_start)
		player.stats.position = list(world.start)
		player.stats.position[0] *= common.tileSize
		player.stats.position[1] *= common.tileSize
		em = explore.ExploreMan(player, world, screen)

		gamestate = GameState.menu
	elif gamestate == GameState.menu:
		# manage main (and other) menu
		gamestate = GameState.explore
	elif gamestate == GameState.explore:
		# manage open world
		result = em.loop()
		if result == -1:
			gamestate = GameState.exit
		elif result == 77:
			gamestate = GameState.loading
			next_level = em.get_next()
			next_start = em.get_out()
	elif gamestate == GameState.cutscene:
		# animate cutscene
		gamestate = GameState.explore
	elif gamestate == GameState.gameover:
		# handle dying
		gamestate = GameState.explore
	else:
		# oops
		gamestate = GameState.menu
		print "ERROR: GameState not handled correctly"

	# Limit fps
	pygame.time.Clock().tick(60)

	running = gamestate != GameState.exit

# gracefully cleanup and exit
print "Thanks for playing!"