from classes.pokemonClass import *
from classes.moveClass import *

def specialMoveEffects(pkmn, oppPkmn, move):
	power = move.getMovePower()
	statusChange = None
	if move.getName() == "Eruption" or move.getName() == "Water Spout":
		power = 150 * ((pkmn.getBattleStats()[0] - pkmn.getStatChanges()[0]) / pkmn.getBattleStats()[0])
		if power < 1:
			power = 1
	if move.getName() == "Venoshock":
		if oppPkmn.getConditions()[2] == True:
			power = 130
	return [power, statusChange]