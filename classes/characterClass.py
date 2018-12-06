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
		inflictedStatusMsg = ""
		# [burn 0, para 1, poison 2, sleep 3, freeze 4]
		statusChanges = [[False, False, False, False, False], [False, False, False, False, False]]
		cpuCurrentStatChanges = self.cpuActivePkmn.getConditions()

		if conditions[3] == "u, 100": # if move used is rest
			for i in range(0, 5):
				cpuCurrentStatChanges[i] = False
			statusChanges[0][3] = True
			inflictedStatusMsg = ("%s fell asleep!") % (self.activePkmn)
			return [statusChanges, inflictedStatusMsg]
		
		# otherwise, check if cpu is already inflicted with a status condition;
		# if yes, no more status condition changes
		for i in cpuCurrentStatChanges:
			if i == True:
				return [statusChanges, ""]

		r = random.randint(1, 100)
		for c in range(0, len(conditions)):
			if conditions[c] != "" and r <= int(conditions[c]):
				if c == 0:
					statusChanges[1][0] = True
					inflictedStatusMsg = ("%s was burned!") % (self.cpuActivePkmn)
				elif c == 1:
					statusChanges[1][1] = True
					inflictedStatusMsg = ("%s was paralyzed!") % (self.cpuActivePkmn)
				elif c == 2:
					statusChanges[1][2] = True
					inflictedStatusMsg = ("%s was poisoned!") % (self.cpuActivePkmn)
				elif c == 3:
					statusChanges[1][3] = True
					inflictedStatusMsg = ("%s fell asleep!") % (self.cpuActivePkmn)
				elif c == 4:
					statusChanges[1][4] = True
					inflictedStatusMsg = ("%s was frozen!") % (self.cpuActivePkmn)
		for status in range(0, len(statusChanges[1])):
			if statusChanges[1][status]:
				self.cpuActivePkmn.changeConditions(status)
				break
		return [statusChanges, inflictedStatusMsg]

	def moveStats(self, changes):
		inflictedStatMsg = ""
		# [atk 0, def 1, spatk 2, spdef 3, spd 4]
		statusChanges = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
		statChanges = []
		for d in changes:
			if d != "":
				stripped = [x.strip() for x in d.split(",")]
				statChanges.append(stripped)
			else:
				statChanges.append(None)
		statsList = ["Attack", "Defense", "Sp. Attack", "Sp. Defense", "Speed", "accuracy", "evasiveness"]
		for sc in range(0, len(statChanges)):
			if statChanges[sc] == None:
				continue
			elif statChanges[sc][0] == "u": # USER STAT EFFECTS DUE TO MOVE
				statChange = int(statChanges[sc][1])
				if len(statChanges[sc]) == 2:
					statusChanges[0][sc] = statChange
					checkStatsPlyr = self.activePkmn.getStatChanges()[sc + 1] + statChange
					if self.activePkmn.getStatChanges()[sc + 1] == 6:
						inflictedStatMsg += (("%s's %s can't go any higher!") % (self.activePkmn, statsList[sc])) + "\n"
						statChanges[0][sc] = 0
					elif self.activePkmn.getStatChanges()[sc + 1] == -6:
						inflictedStatMsg += (("%s's %s can't go any lower!") % (self.activePkmn, statsList[sc])) + "\n"
						statChanges[0][sc] = 0
					elif checkStatsPlyr > 6:
						inflictedStatsMsg += (("%s's %s rose!") % (self.activePkmn, statsList[sc])) + "\n"
						statChanges[0][sc] = checkStatsPlyr - 6
						self.activePkmn.changeStats(sc, statChanges[0][sc])
					elif checkStatsPlyr < -6:
						inflictedStatsMsg += (("%s's %s fell!") % (self.activePkmn, statsList[sc])) + "\n"
						statChanges[0][sc] = checkStatsPlyr + 6
						self.activePkmn.changeStats(sc, statChanges[0][sc])
					else:
						if statChange < 0:
							inflictedStatMsg += (("%s's %s fell!") % (self.activePkmn, statsList[sc])) + "\n"
							self.activePkmn.changeStats(sc, statChange)
						elif statChange > 0:
							inflictedStatMsg += (("%s's %s rose!") % (self.activePkmn, statsList[sc])) + "\n"
							self.activePkmn.changeStats(sc, statChange)
				elif len(statChanges[sc]) == 3:
					inflictStatus = random.randint(1, 100)
					if int(statChanges[sc][2]) <= inflictStatus:
						statusChanges[0][sc] = statChange
						checkStatsPlyr = self.activePkmn.getStatChanges()[sc + 1] + statChange
						if self.activePkmn.getStatChanges()[sc + 1] == 6:
							inflictedStatMsg += (("%s's %s can't go any higher!") % (self.activePkmn, statsList[sc])) + "\n"
							statChanges[0][sc] = 0
						elif self.activePkmn.getStatChanges()[sc + 1] == -6:
							inflictedStatMsg += (("%s's %s can't go any lower!") % (self.activePkmn, statsList[sc])) + "\n"
							statChanges[0][sc] = 0
						elif checkStatsPlyr > 6:
							inflictedStatsMsg += (("%s's %s rose!") % (self.activePkmn, statsList[sc])) + "\n"
							statChanges[0][sc] = checkStatsPlyr - 6
							self.activePkmn.changeStats(sc, statChanges[0][sc])
						elif checkStatsPlyr < -6:
							inflictedStatsMsg += (("%s's %s fell!") % (self.activePkmn, statsList[sc])) + "\n"
							statChanges[0][sc] = checkStatsPlyr + 6
							self.activePkmn.changeStats(sc, statChanges[0][sc])
						else:
							if statChange < 0:
								inflictedStatMsg += (("%s's %s fell!") % (self.activePkmn, statsList[sc])) + "\n"
								self.activePkmn.changeStats(sc, statChange)
							elif statChange > 0:
								inflictedStatMsg += (("%s's %s rose!") % (self.activePkmn, statsList[sc])) + "\n"
								self.activePkmn.changeStats(sc, statChange)
			else: # CPU STAT EFFECTS DUE TO MOVE
				if len(statChanges[sc]) == 2:
					statChange = int(statChanges[sc][1])
					statusChanges[1][sc] = statChange
					checkStatsCPU = self.cpuActivePkmn.getStatChanges()[sc + 1] + statChange
					if self.cpuActivePkmn.getStatChanges()[sc + 1] == 6:
						inflictedStatMsg += (("%s's %s can't go any higher!") % (self.cpuActivePkmn, statsList[sc])) + "\n"
						statChanges[1][sc] = 0
					elif self.cpuActivePkmn.getStatChanges()[sc + 1] == -6:
						inflictedStatMsg += (("%s's %s can't go any lower!") % (self.cpuActivePkmn, statsList[sc])) + "\n"
						statChanges[1][sc] = 0
					elif checkStatsCPU > 6:
						inflictedStatsMsg += (("%s's %s rose!") % (self.cpuActivePkmn, statsList[sc])) + "\n"
						statChanges[1][sc] = checkStatsCPU - 6
						self.cpuActivePkmn.changeStats(sc, statChanges[0][sc])
					elif checkStatsCPU < -6:
						inflictedStatsMsg += (("%s's %s fell!") % (self.cpuActivePkmn, statsList[sc])) + "\n"
						statChanges[1][sc] = checkStatsCPU + 6
						self.cpuActivePkmn.changeStats(sc, statChanges[0][sc])
					else:
						if statChange < 0:
							inflictedStatMsg += (("%s's %s fell!") % (self.cpuActivePkmn, statsList[sc])) + "\n"
							self.cpuActivePkmn.changeStats(sc, statChange)
						elif statChange > 0:
							inflictedStatMsg += (("%s's %s rose!") % (self.cpuActivePkmn, statsList[sc])) + "\n"
							self.cpuActivePkmn.changeStats(sc, statChange)
				elif len(statChanges[sc]) == 3:
					inflictStatus = random.randint(1, 100)
					if int(statChanges[sc][2]) <= inflictStatus:
						statChange = int(statChanges[sc][1])
						statusChanges[1][sc] = statChange
						checkStatsCPU = self.cpuActivePkmn.getStatChanges()[sc + 1] + statChange
						if self.cpuActivePkmn.getStatChanges()[sc + 1] == 6:
							inflictedStatMsg += (("%s's %s can't go any higher!") % (self.cpuActivePkmn, statsList[sc])) + "\n"
							statChanges[1][sc] = 0
						elif self.cpuActivePkmn.getStatChanges()[sc + 1] == -6:
							inflictedStatMsg += (("%s's %s can't go any lower!") % (self.cpuActivePkmn, statsList[sc])) + "\n"
							statChanges[1][sc] = 0
						elif checkStatsCPU > 6:
							inflictedStatsMsg += (("%s's %s rose!") % (self.cpuActivePkmn, statsList[sc])) + "\n"
							statChanges[1][sc] = checkStatsCPU - 6
							self.cpuActivePkmn.changeStats(sc, statChanges[0][sc])
						elif checkStatsCPU < -6:
							inflictedStatsMsg += (("%s's %s fell!") % (self.cpuActivePkmn, statsList[sc])) + "\n"
							statChanges[1][sc] = checkStatsCPU + 6
							self.cpuActivePkmn.changeStats(sc, statChanges[0][sc])
						else:
							if statChange < 0:
								inflictedStatMsg += (("%s's %s fell!") % (self.cpuActivePkmn, statsList[sc])) + "\n"
								self.cpuActivePkmn.changeStats(sc, statChange)
							elif statChange > 0:
								inflictedStatMsg += (("%s's %s rose!") % (self.cpuActivePkmn, statsList[sc])) + "\n"
								self.cpuActivePkmn.changeStats(sc, statChange)
		return [statusChanges, inflictedStatMsg]

	def specialMoveStats(self, move):
		if move == "Ancient Power":
			r = random.randint(1, 100)
			if 10 <= r:
				return [[1, 1, 1, 1, 1, 1, 1]]

	def useMove(self, move):
		msg = ""
		currentStatusMsg = ""
		inflictedStatusMsg = ""
		inflictedStatMsg = ""
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
		if isPara and (20 <= isParaCheck): # if paralyzed, pkmn has a 20% chance of losing turn
			hit = False
			currentStatusMsg = ("%s is paralyzed! It can't move!") % (self.activePkmn)
			print(currentStatusMsg)
		elif isFrozen: # pkmn has a 20% chance of thawing out each turn
			if (20 <= isFrozenCheck):
				self.activePkmn.changeConditionsFalse(4)
				currentStatusMsg = ("%s thawed out!") % (self.activePkmn)
				hit = True
				print(currentStatusMsg)
			else:
				hit = False
				currentStatusMsg = ("%s is frozen! It can't move!") % (self.activePkmn)
				print(currentStatusMsg)
		elif isSleep: # sleeps for 1-3 turns
			if self.sleepCount == 0:
				hit = False
				self.sleepCount += 1
				currentStatusMsg = print("%s is asleep.") % (self.activePkmn)
				print(currentStatusMsg)
			elif self.sleepCount == 3:
				hit = True
				self.activePkmn.changeConditionsFalse(3)
				self.sleepCount = 0
				currentStatusMsg = ("%s woke up!") % (self.activePkmn)
				print(currentStatusMsg)
			else:
				sleepCheck = random.randint(1, 100)
				if 50 <= sleepCheck:
					hit = True
					self.activePkmn.changeConditionsFalse(3)
					self.sleepCount = 0
					currentStatusMsg = ("%s woke up!") % (self.activePkmn)
					print(currentStatusMsg)
				else:
					hit = False
					self.sleepCount += 1
					currentStatusMsg = ("%s is asleep.") % (self.activePkmn)
					print(currentStatusMsg)
		elif acc == "" or isHit <= int(acc):
			hit = True

		if hit:
			msg = "%s used %s!" % (self.activePkmn, move)
			if move.getMoveCategory() == "Physical" or move.getMoveCategory() == "Special":
				damageDealt = damageCalculator(self.activePkmn, self.cpuActivePkmn, move)
				stats = self.moveStats(statChanges)
				status = self.moveStatus(statusConds)
				statChanges = stats[0]
				statusChanges = status[0]
				statusChange = statChanges + statusChanges
				inflictedStatMsg = stats[1]
				inflictedStatusMsg = status[1]
			else:
				statusMove = statusCalculator(self.activePkmn, self.cpuActivePkmn, move)
				statusChange = statusMove[0:4]
				inflictedStatMsg = statusMove[4][1]
				inflictedStatusMsg = statusMove[4][0]
		elif not isPara and not isFrozen and not isSleep:
			msg = "%s used %s! %s's attack missed!" % (self.activePkmn, move, self.activePkmn)
		return [damageDealt, statusChange, [msg, inflictedStatMsg, inflictedStatusMsg, currentStatusMsg], move]
	
class EasyOpponent(Player):
	def __init__(self, activePkmn, party, cpuActivePkmn, cpuParty, pkmnDict, moveDict):
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
			msg = ("%s switched out for %s!") % (self.cpuActivePkmn, potentialPkmn[randPkmn])
			self.cpuActivePkmn = potentialPkmn[randPkmn]
			return [self.cpuActivePkmn, msg]
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
		inflictedStatusMsg = ""
		# [burn 0, para 1, poison 2, sleep 3, freeze 4]
		statusChanges = [[False, False, False, False, False], [False, False, False, False, False]]
		plyrCurrentStatChanges = self.activePkmn.getConditions()
		if conditions[3] == "u, 100": # if move used is rest
			statusChanges[1][3] = True
			return [statusChanges, ""]
		for i in plyrCurrentStatChanges:
			if i:
				return [statusChanges, ""]
		else:
			r = random.randint(1, 100)
			for c in range(0, len(conditions)):
				if conditions[c] != "" and r <= int(conditions[c]):
					if c == 0:
						statusChanges[0][0] = True
						inflictedStatusMsg = ("%s was burned!") % (self.activePkmn)
					elif c == 1:
						statusChanges[0][1] = True
						inflictedStatusMsg = ("%s was paralyzed!") % (self.activePkmn)
					elif c == 2:
						statusChanges[0][2] = True
						inflictedStatusMsg = ("%s was poisoned!") % (self.activePkmn)
					elif c == 3:
						statusChanges[0][3] = True
						inflictedStatusMsg = ("%s was fell asleep!") % (self.activePkmn)
					elif c == 4:
						statusChanges[0][4] = True
						inflictedStatusMsg = ("%s was frozen!") % (self.activePkmn)
		for status in range(0, len(statusChanges[1])):
			if statusChanges[0][status]:
				self.activePkmn.changeConditions(status)
				break
		return [statusChanges, inflictedStatusMsg]

	def moveStats(self, changes):
		inflictedStatMsg = ""
		# [atk 0, def 1, spatk 2, spdef 3, spd 4]
		statusChanges = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
		statChanges = []
		for d in changes:
			if d != "":
				stripped = [x.strip() for x in d.split(",")]
				statChanges.append(stripped)
			else:
				statChanges.append(None)
		statsList = ["Attack", "Defense", "Sp. Attack", "Sp. Defense", "Speed", "accuracy", "evasion"]
		for sc in range(0, len(statChanges)):
			if statChanges[sc] == None:
				continue
			elif statChanges[sc][0] == "u": # CPU STAT EFFECTS DUE TO MOVE
				statChange = int(statChanges[sc][1])
				if len(statChanges[sc]) == 2:
					statusChanges[1][sc] = statChange
					checkStatsCPU = self.cpuActivePkmn.getStatChanges()[sc + 1] + statChange
					if self.cpuActivePkmn.getStatChanges()[sc + 1] == 6:
						inflictedStatMsg += (("%s's %s can't go any higher!") % (self.cpuActivePkmn, statsList[sc])) + "\n"
						statChanges[1][sc] = 0
					elif self.cpuActivePkmn.getStatChanges()[sc + 1] == -6:
						inflictedStatMsg += (("%s's %s can't go any higher!") % (self.cpuActivePkmn, statsList[sc])) + "\n"
						statChanges[1][sc] = 0
					elif checkStatsPlyr > 6:
						inflictedStatMsg += (("%s's %s rose!") % (self.cpuActivePkmn, statsList[sc])) + "\n"
						statChanges[1][sc] = checkStatsCPU - 6
						self.cpuActivePkmn.changeStats(sc, statChanges[1][sc])
					elif checkStatsPlyr < -6:
						inflictedStatMsg += (("%s's %s rose!") % (self.cpuActivePkmn, statsList[sc])) + "\n"
						statChanges[1][sc] = checkStatsCPU + 6
						self.cpuActivePkmn.changeStats(sc, statChanges[1][sc])
					else:
						if statChange < 0:
							inflictedStatMsg += (("%s's %s fell!") % (self.cpuActivePkmn, statsList[sc])) + "\n"
							self.cpuActivePkmn.changeStats(sc, statChange)
						elif statChange > 0:
							inflictedStatMsg += (("%s's %s rose!") % (self.cpuActivePkmn, statsList[sc])) + "\n"
							self.cpuActivePkmn.changeStats(sc, statChange)
				elif len(statChanges[sc]) == 3:
					inflictStatus = random.randint(1, 100)
					if int(statChanges[sc][2]) <= inflictStatus:
						statusChanges[1][sc] = statChange
						checkStatsCPU = self.cpuActivePkmn()[sc + 1] + statChange
						if self.cpuActivePkmn.getStatChanges()[sc + 1] == 6:
							inflictedStatMsg += (("%s's %s can't go any higher!") % (self.cpuActivePkmn, statsList[sc])) + "\n"
							statChanges[1][sc] = 0
						elif self.cpuActivePkmn.getStatChanges()[sc + 1] == -6:
							inflictedStatMsg += (("%s's %s can't go any higher!") % (self.cpuActivePkmn, statsList[sc])) + "\n"
							statChanges[1][sc] = 0
						elif checkStatsPlyr > 6:
							inflictedStatMsg += (("%s's %s rose!") % (self.cpuActivePkmn, statsList[sc])) + "\n"
							statChanges[1][sc] = checkStatsCPU - 6
							self.cpuActivePkmn.changeStats(sc, statChanges[1][sc])
						elif checkStatsPlyr < -6:
							inflictedStatMsg += (("%s's %s rose!") % (self.cpuActivePkmn, statsList[sc])) + "\n"
							statChanges[1][sc] = checkStatsCPU + 6
							self.cpuActivePkmn.changeStats(sc, statChanges[1][sc])
						else:
							if statChange < 0:
								inflictedStatMsg += (("%s's %s fell!") % (self.cpuActivePkmn, statsList[sc])) + "\n"
								self.cpuActivePkmn.changeStats(sc, statChange)
							elif statChange > 0:
								inflictedStatMsg += (("%s's %s rose!") % (self.cpuActivePkmn, statsList[sc])) + "\n"
								self.cpuActivePkmn.changeStats(sc, statChange)
			else:
				statChange = int(statChanges[sc][1])
				if len(statChanges[sc]) == 2:
					statusChanges[0][sc] = statChange
					checkStatsPlyr = self.activePkmn.getStatChanges()[sc + 1] + statChange
					if self.activePkmn.getStatChanges()[sc + 1] == 6:
						inflictedStatMsg += (("%s's %s can't go any higher!") % (self.activePkmn, statsList[sc])) + "\n"
						statChanges[0][sc] = 0
					elif self.activePkmn.getStatChanges()[sc + 1] == -6:
						inflictedStatMsg += (("%s's %s can't go any lower!") % (self.activePkmn, statsList[sc])) + "\n"
						statChanges[0][sc] = 0
					elif checkStatsPlyr > 6:
						inflictedStatsMsg += (("%s's %s rose!") % (self.activePkmn, statsList[sc])) + "\n"
						statChanges[0][sc] = checkStatsPlyr - 6
						self.activePkmn.changeStats(sc, statChanges[0][sc])
					elif checkStatsPlyr < -6:
						inflictedStatsMsg += (("%s's %s fell!") % (self.activePkmn, statsList[sc])) + "\n"
						statChanges[0][sc] = checkStatsPlyr + 6
						self.activePkmn.changeStats(sc, statChanges[0][sc])
					else:
						if statChange < 0:
							inflictedStatMsg += (("%s's %s fell!") % (self.activePkmn, statsList[sc])) + "\n"
							self.activePkmn.changeStats(sc, statChange)
						elif statChange > 0:
							inflictedStatMsg += (("%s's %s rose!") % (self.activePkmn, statsList[sc])) + "\n"
							self.activePkmn.changeStats(sc, statChange)
				elif len(statChanges[sc]) == 3:
					inflictStatus = random.randint(1, 100)
					if int(statChanges[sc][2]) <= inflictStatus:
						statusChanges[0][sc] = statChange
						checkStatsPlyr = self.activePkmn.getStatChanges()[sc + 1] + statChange
						if self.activePkmn.getStatChanges()[sc + 1] == 6:
							inflictedStatMsg += (("%s's %s can't go any higher!") % (self.activePkmn, statsList[sc])) + "\n"
							statChanges[0][sc] = 0
						elif self.activePkmn.getStatChanges()[sc + 1] == -6:
							inflictedStatMsg += (("%s's %s can't go any lower!") % (self.activePkmn, statsList[sc])) + "\n"
							statChanges[0][sc] = 0
						elif checkStatsPlyr > 6:
							inflictedStatsMsg += (("%s's %s rose!") % (self.activePkmn, statsList[sc])) + "\n"
							statChanges[0][sc] = checkStatsPlyr - 6
							self.activePkmn.changeStats(sc, statChanges[0][sc])
						elif checkStatsPlyr < -6:
							inflictedStatsMsg += (("%s's %s fell!") % (self.activePkmn, statsList[sc])) + "\n"
							statChanges[0][sc] = checkStatsPlyr + 6
							self.activePkmn.changeStats(sc, statChanges[0][sc])
						else:
							if statChange < 0:
								inflictedStatMsg += (("%s's %s fell!") % (self.activePkmn, statsList[sc])) + "\n"
								self.activePkmn.changeStats(sc, statChange)
							elif statChange > 0:
								inflictedStatMsg += (("%s's %s rose!") % (self.activePkmn, statsList[sc])) + "\n"
								self.activePkmn.changeStats(sc, statChange)
		return [statusChanges, inflictedStatMsg]

	def useMove(self):
		msg = ""
		currentStatusMsg = ""
		inflictedStatusMsg = ""
		inflictedStatMsg = ""
		move = self.decideMove()
		msg = "%s used %s!" % (self.cpuActivePkmn, move)
		hit = False
		damageDealt = 0
		statusChange = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
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
			currentStatusMsg = ("%s is paralyzed! It can't move!") % (self.cpuActivePkmn)
			print(currentStatusMsg)
		elif isFrozen: # pkmn has a 20% chance of thawing out each turn
			if (isFrozenCheck <= 20):
				self.cpuActivePkmn.changeConditionsFalse(4)
				currentStatusMsg = ("%s thawed out!") % (self.cpuActivePkmn)
				hit = True
				print(currentStatusMsg)
			else:
				hit = False
				currentStatusMsg = ("%s is frozen! It can't move!") % (self.cpuActivePkmn)
				print(currentStatusMsg)
		elif isSleep: # sleeps for 1-3 turns
			if self.sleepCount == 0:
				hit = False
				self.sleepCount += 1
				currentStatusMsg = ("%s is asleep.") % (self.cpuActivePkmn)
				print(currentStatusMsg)
			elif self.sleepCount == 3:
				hit = True
				self.cpuActivePkmn.changeConditionsFalse(3)
				self.sleepCount = 0
				currentStatusMsg = ("%s woke up!") % (self.cpuActivePkmn)
				print(currentStatusMsg)
			else:
				sleepCheck = random.randint(1, 100)
				if 50 <= sleepCheck:
					hit = True
					self.cpuActivePkmn.changeConditionsFalse(3)
					self.sleepCount = 0
					currentStatusMsg = ("%s woke up!") % (self.cpuActivePkmn)
					print(currentStatusMsg)
				else:
					hit = False
					self.sleepCount += 1
					currentStatusMsg = ("%s is asleep.") % (self.cpuActivePkmn)
					print(currentStatusMsg)
		elif acc == "" or isHit <= int(acc):
			hit = True

		# THEN:
		if hit:
			msg = "%s used %s!" % (self.cpuActivePkmn, move)
			if move.getMoveCategory() == "Physical" or move.getMoveCategory() == "Special":
				damageDealt = damageCalculator(self.cpuActivePkmn, self.activePkmn, move)
				stats = self.moveStats(statChanges)
				status = self.moveStatus(statusConds)
				statChanges = stats[0]
				statusChanges = status[0]
				statusChange = statChanges + statusChanges
				inflictedStatMsg = stats[1]
				inflictedStatusMsg = status[1]
			else:
				statusMove = statusCalculator(self.cpuActivePkmn, self.activePkmn, move)
				switch1 = [statusMove[1], statusMove[0]]
				switch2 = [statusMove[3], statusMove[2]]
				statusMove = switch1 + switch2 + [statusMove[4]]
				statusChange = statusMove[0:4]
				inflictedStatMsg = statusMove[4][1]
				inflictedStatusMsg = statusMove[4][0]
		elif not isPara and not isFrozen and not isSleep:
			msg = "%s used %s! %s's attack missed!" % (self.cpuActivePkmn, move, self.cpuActivePkmn)
		return [damageDealt, statusChange, [msg, inflictedStatMsg, inflictedStatusMsg, currentStatusMsg], move]

class MediumOpponent(EasyOpponent):
	def __init__(self, activePkmn, party, cpuActivePkmn, cpuParty, pkmnDict, moveDict):
		super().__init__(activePkmn, party, cpuActivePkmn, cpuParty, pkmnDict, moveDict)
		self.sleepCount = 0
		# load type effectiveness dict
		self.typeEffDict = {}
		file = "classes/spreadsheets/typeEffectiveness.csv"
		lst = open(file)
		csvReader = csv.reader(lst, delimiter = ",")
		for line in csvReader:
			if line[0] not in self.typeEffDict:
				self.typeEffDict[line[0]] = [[line[1], line[2]]]
			else:
				self.typeEffDict[line[0]] = self.typeEffDict[line[0]] + [[line[1], line[2]]]
		lst.close()

	def switchOut(self):
		# checks if there's any super-effective pkmn in the party atm
		oppPkmnTypes = self.activePkmn.getType()
		bestPotentialPkmn = []
		otherPotentialPkmn = []
		lastResortPkmn = []
		for pkmn in self.cpuParty:
			if pkmn != None and pkmn.getIsFainted():
				continue
			elif pkmn != None:
				if self.checkEffectivenessAgainstOpp(oppPkmnTypes, pkmn.getType()) >= 2:
					bestPotentialPkmn.append(pkmn)
				elif self.checkOppEffectiveness(oppPkmnTypes, pkmn.getType()) <= 1:
					otherPotentialPkmn.append(pkmn)
				else:
					lastResortPkmn.append(pkmn)
		if len(bestPotentialPkmn) != 0:
			if len(bestPotentialPkmn) > 1:
				randPkmn = random.randint(0, len(bestPotentialPkmn) - 1)
				msg = ("%s switched out for %s!") % (self.cpuActivePkmn, bestPotentialPkmn[randPkmn])
				self.cpuActivePkmn = bestPotentialPkmn[randPkmn]
				return [self.cpuActivePkmn, msg]
			else:
				msg = ("%s switched out for %s!") % (self.cpuActivePkmn, bestPotentialPkmn[0])
				self.cpuActivePkmn = bestPotentialPkmn[0]
				return [self.cpuActivePkmn, msg]
		elif len(otherPotentialPkmn) != 0:
			if len(otherPotentialPkmn) > 1:
				randPkmn = random.randint(0, len(bestPotentialPkmn) - 1)
				msg = ("%s switched out for %s!") % (self.cpuActivePkmn, otherPontentialPkmn[randPkmn])
				self.cpuActivePkmn = otherPotentialPkmn[randPkmn]
				return [self.cpuActivePkmn, msg]
			else:
				msg = ("%s switched out for %s!") % (self.cpuActivePkmn, otherPotentialPkmn[0])
				self.cpuActivePkmn = otherPotentialPkmn[0]
				return [self.cpuActivePkmn, msg]
		elif len(lastResortPkmn) != 0:
			if len(lastResortPkmn) > 1:
				randPkmn = random.randint(0, len(bestPotentialPkmn) - 1)
				msg = ("%s switched out for %s!") % (self.cpuActivePkmn, lastResortPkmn[randPkmn])
				self.cpuActivePkmn = lastResortPkmn[randPkmn]
				return [self.cpuActivePkmn, msg]
			else:
				msg = ("%s switched out for %s!") % (self.cpuActivePkmn, lastResortPkmn[0])
				self.cpuActivePkmn = lastResortPkmn[0]
				return [self.cpuActivePkmn, msg]
		else:
			return 0

	def switchOutInTurn(self, pkmn):
		self.cpuActivePkmn = pkmn
		return self.cpuActivePkmn

	def checkEffectivenessAgainstOpp(self, oppPkmnTypes, cpuPkmnTypes):
		effectiveness = 1
		for pkmnType in cpuPkmnTypes:
			checkEffectiveness = self.typeEffDict[pkmnType]
			if len(oppPkmnTypes) == 1:
				for oppType in checkEffectiveness:
					if oppType[0] == oppPkmnTypes[0]:
						effectiveness *= float(oppType[1])
			elif len(oppPkmnTypes) == 2:
				for oppType in checkEffectiveness:
					if oppType[0] == oppPkmnTypes[0]:
						effectiveness *= float(oppType[1])
					elif oppType[0] == oppPkmnTypes[1]:
						effectiveness *= float(oppType[1])
		return effectiveness

	def checkOppEffectiveness(self, oppPkmnTypes, cpuPkmnTypes):
		effectiveness = 1
		for pkmnType in oppPkmnTypes:
			checkEffectiveness = self.typeEffDict[pkmnType]
			if len(cpuPkmnTypes) == 1:
				for cpuType in checkEffectiveness:
					if cpuType[0] == cpuPkmnTypes[0]:
						effectiveness *= float(cpuType[1])
			elif len(cpuPkmnTypes) == 2:
				for cpuType in checkEffectiveness:
					if cpuType[0] == cpuPkmnTypes[0]:
						effectiveness *= float(cpuType[1])
					elif cpuType[0] == cpuPkmnTypes[1]:
						effectiveness *= float(cpuType[1])
		return effectiveness

	def inflictWhichStatus(self, move):
		moveStatuses = move.getMoveStatus()
		# based on base stats bc CPU doesn't necessarily know player's EV spread
		# on their pkmn, just like you wouldn't irl
		oppPkmnStats = self.activePkmn.getBaseStats()
		# ...except for speed
		checkSpeed = self.cpuActivePkmn.getBattleStats()[5] > self.activePkmn.getBattleStats()[5]
		for status in range(0, len(moveStatuses)):
			if moveStatuses[status] != "":
				if status == 0: # burn
					if oppPkmnStats[1] > oppPkmnStats[3]: # atk vs spatk
						return move
				if status == 1: # para
					if not checkSpeed:
						return move
				else: # poison or sleep (no moves exist that directly freeze)
					return move

	def inflictWhichStatChange(self, move):
		moveStats = move.getMoveDStat() # [atk, def, spatk, spdef, spd, acc, eva]
		# give the "high" determinator a buffer of 3 points
		hiAtk = self.activePkmn.getBaseStats()[1] >= self.cpuActivePkmn.getBaseStats()[2] - 3 # atk > def?
		hiDef = self.activePkmn.getBaseStats()[2] >= self.cpuActivePkmn.getBaseStats()[1] - 3 # def > atk?
		hiSpAtk = self.activePkmn.getBaseStats()[3] >= self.cpuActivePkmn.getBaseStats()[4] - 3 # spatk > spdef?
		hiSpDef = self.activePkmn.getBaseStats()[4] >= self.cpuActivePkmn.getBaseStats()[3] - 3 # spdef > spatk?
		hiSpd = self.activePkmn.getBaseStats()[5] >= self.cpuActivePkmn.getBaseStats()[5] - 5 # spd > spd?
		for stat in range(0, len(moveStats)):
			if moveStats[stat] != "":
				specificChanges = [x.strip() for x in moveStats[stat].split(",")]
				if specificChanges[0] == "u":
					if stat == 0 and hiDef: # atk
						return move
					elif stat == 1 and hiAtk: # def
						return move
					elif stat == 2 and hiSpDef: # spatk
						return move
					elif stat == 3 and hiSpAtk: # spdef
						return move
					elif stat == 4 and hiSpd: # spd
						return move
					else:
						randomInt = random.randint(0, 2) # 33% odds to reduce opponent's accuracy/evasion, as this is not strictly necessary
						if randomInt == 0:
							return move
						else:
							return None

	def decideMove(self):
		rlMoves = self.cpuActivePkmn.getMoves()
		cpuPkmnTypes = self.cpuActivePkmn.getType()
		oppPkmnTypes = self.activePkmn.getType()
		# DELETE LATER BUT CHANGE ABOVE rlMOVES TO "moves"
		moves = []
		for i in rlMoves:
			if i == None:
				continue
			else:
				moves.append(i)
		# check if cpu should switch out or not
		effectiveness = self.checkOppEffectiveness(oppPkmnTypes, cpuPkmnTypes)
		oppRemainingHP = self.activePkmn.getBattleStats()[0] - self.activePkmn.getStatChanges()[0]
		oppRemainingHPDec = oppRemainingHP / (self.activePkmn.getBattleStats()[0])
		cpuRemainingHP = self.cpuActivePkmn.getBattleStats()[0] - self.cpuActivePkmn.getStatChanges()[0]
		cpuRemainingHPDec = cpuRemainingHP / (self.cpuActivePkmn.getBattleStats()[0])
		if effectiveness >= 2:
			bestSwitchOuts = []
			otherSwitchOuts = []
			for pkmn in self.cpuParty:
				if pkmn != self.cpuActivePkmn and pkmn != None:
					checkEff = self.checkOppEffectiveness(oppPkmnTypes, pkmn.getType())
					if checkEff == 1:
						otherSwitchOuts.append(pkmn)
					elif checkEff <= 0.5:
						bestSwitchOuts.append(pkmn)
			if oppRemainingHPDec >= 0.3:
				if bestSwitchOuts != []:
					if len(bestSwitchOuts) == 1:
						return ["switch", bestSwitchOuts[0]]
					else:
						randPkmn = random.randint(0, len(bestSwitchOuts) - 1)
						return ["switch", bestSwitchOuts[randPkmn]]
				elif otherSwitchOuts != []:
					if len(otherSwitchOuts) == 1:
						return ["switch", otherSwitchOuts[0]]
					else:
						randPkmn = random.randint(0, len(otherSwitchOuts) - 1)
						return ["switch", otherSwitchOuts[randPkmn]]
		potentialMoves = []
		checkSpeed = self.cpuActivePkmn.getBattleStats()[5] > self.activePkmn.getBattleStats()[5]
		# CHECK IF CPU WILL USE A STATUS MOVE
		if (cpuRemainingHPDec >= 0.8) or (cpuRemainingHPDec <= 0.2 and checkSpeed):
			for ty in moves:
				if ty.getMoveCategory() == "Status":
					if not all(item is "" for item in ty.getMoveStatus()): # check if move inflicts status conditions...
						if not any(self.activePkmn.getConditions()): # check if plyr pkmn has any status conditions
							move = self.inflictWhichStatus(ty)
							if move != None:
								return move
					else: # ...otherwise, we know that the move changes the plyr pkmn's stats
						move = self.inflictWhichStatChange(ty)
						if move != None:
							return move
		# IF NO STATUS MOVES APPLY, THEN CHECK FOR SUPER EFFECTIVE MOVE
		# try to find which of ur attacking moves are super-effective...
		for ty in moves:
			if ty.getMoveCategory() == "Physical" or ty.getMoveCategory() == "Special":
				mvType = ty.getMoveType()
				if len(oppPkmnTypes) == 1:
					for defType in self.typeEffDict[mvType]:
						if defType[0] == oppPkmnTypes[0] and defType[1] == 2:
							potentialMoves.append(ty)
				elif len(oppPkmnTypes) == 2:
					eff = 1
					for defType in self.typeEffDict[mvType]:
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
			# cull move list of status condition moves, just in case
			culledMoves = []
			for mv in moves:
				if mv.getMoveCategory() == "Status" and all(item is "" for item in mv.getMoveDStat()):
					continue
				else:
					culledMoves.append(mv)
			moveNum = random.randint(0, len(culledMoves) - 1)
			move = culledMoves[moveNum]
		return move

	def useMove(self):
		msg = ""
		currentStatusMsg = ""
		inflictedStatusMsg = ""
		inflictedStatMsg = ""
		move = self.decideMove()
		if type(move) != Move and move[0] == "switch":
			return move
		msg = "%s used %s!" % (self.cpuActivePkmn, move)
		hit = False
		damageDealt = 0
		statusChange = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
							[False, False, False, False, False], [False, False, False, False, False]]

		# FIRST: check if the move hits
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
		elif acc == "" or isHit <= int(acc):
			hit = True

		# THEN:
		if hit:
			msg = "%s used %s!" % (self.cpuActivePkmn, move) # e.g. "Raichu used Thunderbolt!"
			# if a move deals damage, then return the damage it deals + any status changes
			if move.getMoveCategory() == "Physical" or move.getMoveCategory() == "Special":
				damageDealt = damageCalculator(self.cpuActivePkmn, self.activePkmn, move)
				stats = self.moveStats(statChanges)
				status = self.moveStatus(statusConds)
				statChanges = stats[0]
				statusChanges = status[0]
				statusChange = statChanges + statusChanges
				inflictedStatMsg = stats[1]
				inflictedStatusMsg = status[1]
			else:
				statusMove = statusCalculator(self.cpuActivePkmn, self.activePkmn, move)
				switch1 = [statusMove[1], statusMove[0]]
				switch2 = [statusMove[3], statusMove[2]]
				statusMove = switch1 + switch2 + [statusMove[4]]
				statusChange = statusMove[0:4]
				inflictedStatMsg = statusMove[4][1]
				inflictedStatusMsg = statusMove[4][0]
		elif not isPara and not isFrozen and not isSleep:
			msg = "%s used %s! %s's attack missed!" % (self.cpuActivePkmn, move, self.cpuActivePkmn)
		return [damageDealt, statusChange, [msg, inflictedStatMsg, inflictedStatusMsg, currentStatusMsg], move]