import random

class Move:
    def __init__(self, moveName, moveType, moveCategory, movePower, moveAccuracy, movePP, movePriority, moveAddedEffects):
        self.moveName = moveName
        self.moveType = moveType
        self.moveCategory = moveCategory # physical/special/status
        self.movePower = movePower
        self.moveAccuracy = moveAccuracy
        self.movePP = movePP
        self.movePriority = movePriority
        # 0: [burn, freeze, para, poison, sleep]
        # 1: [datk, ddef, dspatk, dspdef, dspd, dacc, deva]
        # 2: [other]
        self.moveAddedEffects = moveAddedEffects
    
    def __eq__(self, other):
        return (isinstance(other, Move)) and (self.moveName == other.moveName) and \
               (self.moveType == other.moveType) and (self.moveCategory == other.moveCategory) and \
               (self.movePower == other.movePower) and (self.moveAccuracy == other.moveAccuracy) and \
               (self.movePP == other.movePP) and (self.movePriority == other.movePriority) and \
               (self.moveAddedEffects == other.moveAddedEffects)

    def __repr__(self):
        return "%s" % self.moveName
    
    # get the name of the move
    def getMoveName(self):
        return self.moveName
    
    # get the type of the move (e.g. Fire, Water, Grass, etc.)
    def getMoveType(self):
        return self.moveType
    
    # get the category of the move (Physical, Special, Status)
    def getMoveCategory(self):
        return self.moveCategory
    
    # get the power of the move
    def getMovePower(self):
        return self.movePower
    
    # get the accuracy of the move
    def getMoveAccuracy(self):
        return self.moveAccuracy
    
    # get the PP of the move (number of times you can use the move)
    def getMovePP(self):
        return self.movePP
    
    # get the priority of the move (e.g. Quick Attack has a priority of +1, so
    # it will move before all other moves that do not have priority)
    def getMovePriority(self):
        return self.movePriority
    
    # get any status effects the move will inflict
    # ["", "", "", "", ""] / [burn, para, poison, sleep, freeze]
    def getMoveStatus(self):
        return self.moveAddedEffects[0]

    # get any stat changes the move will inflict
    # ["", "", "", "", ""] / [atk, def, spatk, spdef, spd, acc, eva]
    def getMoveDStat(self):
        return self.moveAddedEffects[1]

    # get other effects (flinch, multiple attacks, etc.) the move will inflict
    def getMoveAddedEffects(self):
        return self.moveAddedEffects[2]