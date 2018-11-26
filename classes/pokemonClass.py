import csv

class Pokemon:
    def __init__(self, pkmn, lv, ev, moves, isFainted, statChanges, statusConditions,
                 isActive = False):
        pkmnAttributes = []
        file = "classes/spreadsheets/pokemon.csv"
        pkmnList = open(file)
        csvReader = csv.reader(pkmnList, delimiter = ",")
        for line in csvReader:
            if line[0] == pkmn:
                pkmnAttributes = line
                break
        pkmnList.close()
        
        # ATTRIBUTES
        self.pkmnName = pkmn # str
        if pkmnAttributes[2] == "":
            self.pkmnType = [pkmnAttributes[1]]
        else:
            self.pkmnType = [pkmnAttributes[1]] + [pkmnAttributes[2]]
        self.baseStats = []
        for stat in range(3, 9):
            attr = int(pkmnAttributes[stat])
            self.baseStats.append(attr)
        self.ev = ev # [hp, atk, def, sp. atk, sp. def, spd] int (max 252 per stat, max 510 overall)
        self.moves = moves # [move1, move2, move3, move4] str
        self.level = lv # int
        self.isFainted = isFainted
        self.statChanges = statChanges
        self.ppChanges = [0, 0, 0, 0]
        self.statusConditions = statusConditions # [burn, freeze, para, poison, sleep]
        self.isActive = isActive
        self.stagesDict = {-6: 0.25, -5: 0.28, -4: 0.33, -3: 0.2, -2: 0.5, -1: 0.66, 0: 1, 1: 1.5, 2: 2, 3: 2.5, 4: 3, 5: 3.5, 6: 4}
    
    def __repr__(self):
        return "%s" % self.pkmnName
    
    # change to active
    def activeTrue(self):
        self.isActive = True

    def activeFalse(self):
        self.isActive = False

    def getIsActive(self):
        return self.isActive

    # get pkmn name
    def getName(self):
        if self.pkmnName == "Nidoran-F":
            return "Nidoran (F)"
        elif self.pkmnName == "Nidoran-M":
            return "Nidoran (M)"
        return self.pkmnName

    # get pkmn type
    def getType(self):
        return self.pkmnType
    
    # get pkmn level
    def getLevel(self):
        return self.level

    # change pkmn level
    def changeLevel(self, newLvl):
        self.level = newLvl
    
    # get base stats
    def getBaseStats(self):
        return self.baseStats

    # get BATTLE pkmn stats (NOT base stats! these are dependent on level and EVs)
    # assume 31 IVs for each stat bc why would you do anything else
    # formulae retrieved from https://bulbapedia.bulbagarden.net/wiki/Statistic#In_Generation_III_onward
    def getBattleStats(self):
        iv = 31
        evDivisor = 4
        hpFormula = int((((2 * self.baseStats[0] + iv + self.ev[0]/evDivisor) * \
                    self.level) / 100) + self.level + 10)
        adjStats = [hpFormula]
        for stat in range(1, len(self.baseStats)): # atk, def, sp. atk, sp. def, spd
            base = int((((2 * self.baseStats[stat] + iv + \
                      self.ev[stat]/evDivisor) * self.level) / 100) + 5)
            formula = base * self.stagesDict[self.statChanges[stat]]
            adjStats.append(formula)
        return adjStats
    
    # get pkmn moves
    def getMoves(self):
        return self.moves
    
    # use a move
    def useMove(self, usedMove):
        return "%s used %s." % (self.pkmnName, usedMove)

    def changeToFainted(self):
        self.isFainted = True

    def changeNotFainted(self):
        self.isFainted = False

    # get is fainted
    def getIsFainted(self):
        return self.isFainted

    # get stat changes
    def getStatChanges(self):
        return self.statChanges

    # change stats
    def changeStats(self, stat, stage):
        if stat == 0:
            self.statChanges[1] += stage
        elif stat == 1:
            self.statChanges[2] += stage
        elif stat == 2:
            self.statChanges[3] += stage
        elif stat == 3:
            self.statChanges[4] += stage
        elif stat == 4:
            self.statChanges[5] += stage

    def getPPChanges(self):
        return self.ppChanges

    # reset stats
    def resetStatConds(self):
        self.statChanges = [0, 0, 0, 0, 0, 0]
        self.statusConditions = [False, False, False, False, False]

    # get status
    def getConditions(self):
        return self.statusConditions

    def changeConditions(self, cond):
        if cond == 0:
            self.statusConditions[0] = True
        elif cond == 1:
            self.statusConditions[1] = True
        elif cond == 2:
            self.statusConditions[2] = True
        elif cond == 3:
            self.statusConditions[3] = True
        elif cond == 4:
            self.statusConditions[4] = True