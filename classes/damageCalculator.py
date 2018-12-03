import random
from classes.pokemonClass import *
from classes.moveClass import *
import csv

def damageCalculator(atkPkmn, defPkmn, move):
	typeEffDict = {}
	file = "classes/spreadsheets/typeEffectiveness.csv"
	lst = open(file)
	csvReader = csv.reader(lst, delimiter = ",")
	for line in csvReader:
		if line[0] not in typeEffDict:
			typeEffDict[line[0]] = [[line[1], line[2]]]
		else:
			typeEffDict[line[0]] = typeEffDict[line[0]] + [[line[1], line[2]]]
	lst.close()

	# level
	lvl = int(atkPkmn.getLevel())

	# pkmn relevant stats
	atkPkmnAtk = int(atkPkmn.getBattleStats()[1])
	atkPkmnSpAtk = int(atkPkmn.getBattleStats()[3])
	defPkmnDef = int(defPkmn.getBattleStats()[2])
	defPkmnSpDef = int(defPkmn.getBattleStats()[4])

	# move power
	movePower = int(move.getMovePower())

	# move category: physical/special?
	moveCat = move.getMoveCategory()

	# move high crit?
	moveHiCrit = move.getMoveAddedEffects()[0]

	# pkmn/move relevant types
	atkPkmnType = atkPkmn.getType()
	defPkmnType = defPkmn.getType()
	moveType = move.getMoveType()

	stab = 1
	for i in atkPkmnType:
		if i == moveType:
			stab = 1.5
			break

	superEff = 1
	for match in typeEffDict[moveType]:
		if match[0] == defPkmnType[0]:
			superEff *= float(match[1])
	if len(defPkmnType) == 2:
		for match in typeEffDict[moveType]:
			if match[0] == defPkmnType[1]:
				superEff *= float(match[1])
	if move.getMoveName() == "Freeze-Dry" and ("Water" in defPkmnType):
		superEff = 2
	elif move.getMoveName() == "Thousand Arrows" and ("Flying" in defPkmnType):
		superEff = 1

	# is burned?
	burn = 1
	if atkPkmn.getConditions()[0] == True and moveCat == "Physical":
		burn = 0.5

	# random factor
	rand = random.randint(85, 100) / 100

	# crit?
	crit = 1
	critProbability = 4
	if moveHiCrit == 1:
		critProbability = 12
	num = random.randint(1, 100)
	if num <= critProbability or move.getMoveName() == "Frost Breath":
		crit = 1.5

	if moveCat == "Physical":
		a = atkPkmnAtk
		d = defPkmnDef
	else:
		a = atkPkmnSpAtk
		d = defPkmnSpDef

	primaryFormula = ((((2 * lvl) / 5 + 2) * movePower * (a / d)) / 50) + 2
	modifier = rand * stab * superEff * burn * crit
	formula = primaryFormula * modifier
	return int(formula)

def statusCalculator(atkPkmn, defPkmn, move):
	statusConds = move.getMoveStatus()
	statChanges = move.getMoveDStat()

	print(move, statusConds)

	for status in range(0, len(statusConds)):
		if statusConds[status] != "":
			if statusConds[status].isdigit():
				defPkmn.changeConditions(status)
			else:
				atkPkmn.changeConditions(status)

	for stat in range(0, len(statChanges)):
		if statChanges[stat] != "":
			lst = statChanges[stat].split(",")
			if lst[0] == "t":
				defPkmn.changeStats(stat, int(lst[1]))
			else:
				atkPkmn.changeStats(stat, int(lst[1]))

	atkPkmnStatChanges = atkPkmn.getStatChanges()[1:]
	defPkmnStatChanges = defPkmn.getStatChanges()[1:]
	atkPkmnCond = atkPkmn.getConditions()
	defPkmnCond = defPkmn.getConditions()

	return [atkPkmnStatChanges, defPkmnStatChanges, atkPkmnCond, defPkmnCond]