import pygame as pg
import random
import copy
from classes.pokemonClass import *
from classes.moveClass import *
from classes.damageCalculator import *
from classes.hpBarClass import *
from classes.external_modules.gifImage import *

class Player:
	def __init__(self, activePkmn, party, cpuActivePkmn, pkmnDict, moveDict):
		# activePkmn is a Pokemon object
		# party is a list of Pokemon objects
		self.activePkmn = activePkmn
		if self.activePkmn != None:
			self.lvl = activePkmn.getLevel()
		self.party = party
		self.cpuActivePkmn = cpuActivePkmn
		self.pkmnDict = pkmnDict
		self.moveDict = moveDict
		self.sprite = None
		self.sleepCount = 0

	def updateOppActive(self, newPkmn):
		self.cpuActivePkmn = newPkmn

	def moveStatus(self, conditions):
		# [burn 0, para 1, poison 2, sleep 3, freeze 4]
		statusChanges = [[False, False, False, False, False], [False, False, False, False, False]]
		cpuCurrentStatChanges = self.cpuActivePkmn.getConditions()

		if conditions[3] == "u, 100": # if move used is rest
			for i in range(0, 5):
				cpuCurrentStatChanges[i] = False
			statusChanges[0][3] = True
			return statusChanges
		
		# otherwise, check if cpu is already inflicted with a status condition;
		# if yes, no more status condition changes
		print("CPU CURRENT STAT CHANGES:", cpuCurrentStatChanges)
		for i in cpuCurrentStatChanges:
			if i == True:
				return statusChanges

		r = random.randint(1, 100)
		for c in range(0, len(conditions)):
			if conditions[c] != "" and r <= int(conditions[c]):
				if c == 0:
					statusChanges[1][0] = True
				elif c == 1:
					statusChanges[1][1] = True
				elif c == 2:
					statusChanges[1][2] = True
				elif c == 3:
					statusChanges[1][3] = True
				elif c == 4:
					statusChanges[1][4] = True
		return statusChanges

	def moveStats(self, changes):
		# [atk 0, def 1, spatk 2, spdef 3, spd 4]
		statusChanges = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
		statChanges = []
		for d in changes:
			if d != "":
				stripped = [x.strip() for x in d.split(",")]
				statChanges.append(stripped)
			else:
				statChanges.append(None)
		for sc in range(0, len(statChanges)):
			if statChanges[sc] == None:
				continue
			if statChanges[sc][0] == "u":
				statChange = int(statChanges[sc][1])
				if sc == 0: # atk
					statusChanges[0][0] = statChange
				elif sc == 1: # def
					statusChanges[0][1] = statChange
				elif sc == 2: # spatk
					statusChanges[0][2] = statChange
				elif sc == 3: # spdef
					statusChanges[0][3] = statChange
				elif sc == 4: # spd
					statusChanges[0][4] = statChange
				elif sc == 5: # acc
					statusChanges[0][5] = statChange
				elif sc == 6: # eva
					statusChanges[0][6] = statChange
			else:
				if len(statChanges[sc]) == 2:
					statChange = int(statChanges[sc][1])
					if sc == 0:
						statusChanges[1][0] = statChange
					elif sc == 1:
						statusChanges[1][1] = statChange
					elif sc == 2:
						statusChanges[1][2] = statChange
					elif sc == 3:
						statusChanges[1][3] = statChange
					elif sc == 4:
						statusChanges[1][4] = statChange
					elif sc == 5: # acc
						statusChanges[1][5] = statChange
					elif sc == 6: # eva
						statusChanges[1][6] = statChange
				elif len(statChanges[sc] == 3):
					inflictStatus = random.randint(1, 100)
					if int(statChanges[sc][2]) <= inflictStatus:
						statChange = int(statChanges[sc][1])
						if sc == 0:
							statusChanges[1][0] = statChange
						elif sc == 1:
							statusChanges[1][1] = statChange
						elif sc == 2:
							statusChanges[1][2] = statChange
						elif sc == 3:
							statusChanges[1][3] = statChange
						elif sc == 4:
							statusChanges[1][4] = statChange
						elif sc == 5: # acc
							statusChanges[1][5] = statChange
						elif sc == 6: # eva
							statusChanges[1][6] = statChange
		print("PLYR STATUS CHANGES:", statusChanges)
		return statusChanges

	def specialMoveStats(self, move):
		if move == "Ancient Power":
			r = random.randint(1, 100)
			if 10 <= r:
				return [[1, 1, 1, 1, 1]]


	def useMove(self, move):
		# have the current pkmn use a move
		hit = False
		damageDealt = 0
		statusChange = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
						[False, False, False, False, False], [False, False, False, False, False]]

		# FIRST: check if the move hits
		acc = move.getMoveAccuracy()
		statusConds = move.getMoveStatus()
		statChanges = move.getMoveDStat()
		isHit = random.randint(1, 100)

		isPara = self.activePkmn.getConditions()[1]
		isParaCheck = random.randint(1, 100)
		isFrozen = self.activePkmn.getConditions()[4]
		isFrozenCheck = random.randint(1, 100)
		isSleep = self.activePkmn.getConditions()[3]

		# THEN:
		if isPara and (25 <= isParaCheck): # if paralyzed, pkmn has a 20% chance of losing turn
			hit = False
			msg = ("%s is paralyzed! It can't move!") % (self.activePkmn)
			print(msg)
		elif isFrozen: # pkmn has a 20% chance of thawing out each turn
			if (20 <= isFrozenCheck):
				self.activePkmn.changeConditionsFalse(4)
				msg = ("%s thawed out!") % (self.activePkmn)
				hit = True
				print(msg)
			else:
				hit = False
				msg = ("%s is frozen! It can't move!") % (self.activePkmn)
				print(msg)
		elif isSleep: # sleeps for 1-3 turns
			if self.sleepCount == 0:
				hit = False
				self.sleepCount += 1
				msg = print("%s is asleep.") % (self.activePkmn)
				print(msg)
			elif self.sleepCount == 3:
				hit = True
				self.activePkmn.changeConditionsFalse(3)
				self.sleepCount = 0
				msg = ("%s woke up!") % (self.activePkmn)
				print(msg)
			else:
				sleepCheck = random.randint(1, 100)
				if 50 <= sleepCheck:
					hit = True
					self.activePkmn.changeConditionsFalse(3)
					self.sleepCount = 0
					msg = ("%s woke up!") % (self.activePkmn)
					print(msg)
				else:
					hit = False
					self.sleepCount += 1
					msg = ("%s is asleep.") % (self.activePkmn)
					print(msg)
		elif isHit <= int(acc):
			hit = True

		if hit:
			msg = "%s used %s!" % (self.activePkmn, move)
			if move.getMoveCategory() == "Physical" or move.getMoveCategory() == "Special":
				damageDealt = damageCalculator(self.activePkmn, self.cpuActivePkmn, move)
				statChanges = self.moveStats(statChanges)
				statusChanges = self.moveStatus(statusConds)
				statusChange = statChanges + statusChanges
			else:
				statusChange = statusCalculator(self.activePkmn, self.cpuActivePkmn, move)
		elif not isPara or not isFrozen or not isSleep:
			msg = "%s used %s! %s's attack missed!" % (self.activePkmn, move, self.activePkmn)
			# statusChange = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0],
			# 				[False, False, False, False, False], [False, False, False, False, False]]
		print("PLYR GAVE:", statusChange)
		return [damageDealt, statusChange, msg]
	
class EasyOpponent(Player):
	def __init__(self, activePkmn, party, cpuActivePkmn, pkmnDict, moveDict, cpuParty):
		super().__init__(activePkmn, party, cpuActivePkmn, pkmnDict, moveDict)
		self.cpuParty = cpuParty
		self.sleepCount = 0

	def updateOppActive(self, newPkmn):
		self.activePkmn = newPkmn

	def updateCPUSprite(self, newPkmn, pkmnDict):
		activeName = newPkmn.getName()
		properName = str(activeName).title()
		if properName == "Farfetch'D":
			properName = "Farfetch'd"
		folderPath = "images/pkmn_sprites_front/"
		pkmnLower = str(activeName).lower()
		if pkmnLower == "mr. mime":
			pkmnLower = "mrmime"
		pkmnFolderPath = folderPath + pkmnLower + "/"
		frameNum = pkmnDict[properName][9]

		# MAKE SPRITE OBJECT
		spriteInit = GifSprite(pkmnFolderPath, frameNum, pkmnLower, (460, 140))
		cpuActiveSprite = pygame.sprite.Group(spriteInit)

		return cpuActiveSprite

	def switchOut(self):
		potentialPkmn = []
		for pkmn in self.cpuParty:
			if pkmn != None and pkmn.getIsFainted():
				continue
			elif pkmn != None:
				potentialPkmn.append(pkmn)
		if len(potentialPkmn) != 0:
			randPkmn = random.randint(0, len(potentialPkmn) - 1)
			self.cpuActivePkmn = potentialPkmn[randPkmn]
			return self.cpuActivePkmn
		else:
			return 0

	def decideMove(self):
		rlMoves = self.cpuActivePkmn.getMoves()
		oppPkmnTypes = self.activePkmn.getType()
		# DELETE LATER BUT CHANGE ABOVE rlMOVES TO "moves"
		moves = []
		for i in rlMoves:
			if i == None:
				continue
			else:
				moves.append(i)
		# CHECK FOR SUPER EFFECTIVE MOVE
		# load type effectiveness dict
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
		# try to find which of ur attacking moves are super-effective...
		potentialMoves = []
		for ty in moves:
			if ty.getMoveCategory() == "Physical" or ty.getMoveCategory() == "Special":
				mvType = ty.getMoveType()
				if len(oppPkmnTypes) == 1:
					for defType in typeEffDict[mvType]:
						if defType[0] == oppPkmnTypes[0] and defType[1] == 2:
							potentialMoves.append(ty)
				elif len(oppPkmnTypes) == 2:
					eff = 1
					for defType in typeEffDict[mvType]:
						if defType[0] == oppPkmnTypes[0]:
							eff *= float(defType[1])
						elif defType[0] == oppPkmnTypes[1]:
							eff *= float(defType[1])
					if eff >= 2:
						potentialMoves.append(ty)
		# ...if one move in the list of potential moves, just set move to that one...
		if len(potentialMoves) == 1:
			move = potentialMoves[0]
		# ...otherwise, find the move with the greatest power...
		elif len(potentialMoves) > 1:
			currentPower = 0
			currentMove = None
			for m in potentialMoves:
				if int(m.getMovePower()) > currentPower:
					currentMove = m
			move = currentMove
		# ...if none, pick randomly and hope for the best! ¯\_(ツ)_/¯
		elif len(potentialMoves) == 0:
			moveNum = random.randint(0, len(moves) - 1)
			move = moves[moveNum]
		return move

	def moveStatus(self, conditions):
		# [burn 0, para 1, poison 2, sleep 3, freeze 4]
		statusChanges = [[False, False, False, False, False], [False, False, False, False, False]]
		if conditions[3] == "u, 100": # if move used is rest
			statusChanges[1][3] = True
			return statusChanges
		else:
			r = random.randint(1, 100)
			for c in range(0, len(conditions)):
				if conditions[c] != "" and r <= int(conditions[c]):
					if c == 0:
						statusChanges[0][0] = True
					elif c == 1:
						statusChanges[0][1] = True
					elif c == 2:
						statusChanges[0][2] = True
					elif c == 3:
						statusChanges[0][3] = True
					elif c == 4:
						statusChanges[0][4] = True
		return statusChanges

	def moveStats(self, changes):
		# [atk 0, def 1, spatk 2, spdef 3, spd 4]
		statusChanges = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
		statChanges = []
		for d in changes:
			if d != "":
				stripped = [x.strip() for x in d.split(",")]
				statChanges.append(stripped)
			else:
				statChanges.append(None)
		for sc in range(0, len(statChanges)):
			if statChanges[sc] == None:
				continue
			if statChanges[sc][0] == "u":
				statChange = int(statChanges[sc][1])
				if sc == 0:
					statusChanges[1][0] = statChange
				elif sc == 1:
					statusChanges[1][1] = statChange
				elif sc == 2:
					statusChanges[1][2] = statChange
				elif sc == 3:
					statusChanges[1][3] = statChange
				elif sc == 4:
					statusChanges[1][4] = statChange
			else:
				if len(statChanges[sc]) == 2:
					statChange = int(statChanges[sc][1])
					if sc == 0:
						statusChanges[0][0] = statChange
					elif sc == 1:
						statusChanges[0][1] = statChange
					elif sc == 2:
						statusChanges[0][2] = statChange
					elif sc == 3:
						statusChanges[0][3] = statChange
					elif sc == 4:
						statusChanges[0][4] = statChange
				elif len(statChanges[sc]) == 3:
					inflictStatus = random.randint(1, 100)
					if int(statChanges[sc][2]) <= inflictStatus:
						statChange = int(statChanges[sc][1])
						if sc == 0:
							statusChanges[0][0] = statChange
						elif sc == 1:
							statusChanges[0][1] = statChange
						elif sc == 2:
							statusChanges[0][2] = statChange
						elif sc == 3:
							statusChanges[0][3] = statChange
						elif sc == 4:
							statusChanges[0][4] = statChange
		return statusChanges

	def useMove(self):
		move = self.decideMove()
		msg = "%s used %s!" % (self.cpuActivePkmn, move)
		hit = False
		damageDealt = 0
		statusChange = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0],
							[False, False, False, False, False], [False, False, False, False, False]]

		# FIRST: check if the move hitss
		acc = move.getMoveAccuracy()
		statusConds = move.getMoveStatus()
		statChanges = move.getMoveDStat()
		isHit = random.randint(1, 100)

		# CHECK STATUSES
		isPara = self.cpuActivePkmn.getConditions()[1]
		isParaCheck = random.randint(1, 100)
		isFrozen = self.cpuActivePkmn.getConditions()[4]
		isFrozenCheck = random.randint(1, 100)
		isSleep = self.cpuActivePkmn.getConditions()[3]

		# THEN:
		if isPara and (isParaCheck <= 25): # if paralyzed, pkmn has a 25% chance of losing turn
			print(isParaCheck)
			hit = False
			msg = ("%s is paralyzed! It can't move!") % (self.cpuActivePkmn)
			print(msg)
		elif isFrozen: # pkmn has a 20% chance of thawing out each turn
			if (isFrozenCheck <= 20):
				self.cpuActivePkmn.changeConditionsFalse(4)
				msg = ("%s thawed out!") % (self.cpuActivePkmn)
				hit = True
				print(msg)
			else:
				hit = False
				msg = ("%s is frozen! It can't move!") % (self.cpuActivePkmn)
				print(msg)
		elif isSleep: # sleeps for 1-3 turns
			if self.sleepCount == 0:
				hit = False
				self.sleepCount += 1
				msg = ("%s is asleep.") % (self.cpuActivePkmn)
				print(msg)
			elif self.sleepCount == 3:
				hit = True
				self.cpuActivePkmn.changeConditionsFalse(3)
				self.sleepCount = 0
				msg = ("%s woke up!") % (self.cpuActivePkmn)
				print(msg)
			else:
				sleepCheck = random.randint(1, 100)
				if 50 <= sleepCheck:
					hit = True
					self.cpuActivePkmn.changeConditionsFalse(3)
					self.sleepCount = 0
					msg = ("%s woke up!") % (self.cpuActivePkmn)
					print(msg)
				else:
					hit = False
					self.sleepCount += 1
					msg = ("%s is asleep.") % (self.cpuActivePkmn)
					print(msg)
		elif isHit <= int(acc):
			hit = True

		# THEN:
		if hit:
			msg = "%s used %s!" % (self.cpuActivePkmn, move)
			if move.getMoveCategory() == "Physical" or move.getMoveCategory() == "Special":
				damageDealt = damageCalculator(self.cpuActivePkmn, self.activePkmn, move)
				statusChange = self.moveStats(statChanges) + self.moveStatus(statusConds)
			else:
				statusChange = statusCalculator(self.cpuActivePkmn, self.activePkmn, move)
				switch1 = [statusChange[1], statusChange[0]]
				switch2 = [statusChange[3], statusChange[2]]
				statusChange = switch1 + switch2
		elif not isPara or not isFrozen or not isSleep:
			msg = "%s used %s! %s's attack missed!" % (self.cpuActivePkmn, move, self.cpuActivePkmn)
			# statusChange = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0],
			# 				[False, False, False, False, False], [False, False, False, False, False]]
		return [damageDealt, statusChange, msg]