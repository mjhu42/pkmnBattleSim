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
        # 1: [datk, ddef, dspatk, dspdef, dspd]
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
    
    def getMoveName(self):
        return self.moveName
    
    def getMoveType(self):
        return self.moveType
    
    def getMoveCategory(self):
        return self.moveCategory
    
    def getMovePower(self):
        return self.movePower
    
    def getMoveAccuracy(self):
        return self.moveAccuracy
    
    def getMovePP(self):
        return self.movePP
    
    def getMovePriority(self):
        return self.movePriority
    
    def getMoveStatus(self):
        return self.moveAddedEffects[0]

    def getMoveDStat(self):
        return self.moveAddedEffects[1]

    def getMoveAddedEffects(self):
        return self.moveAddedEffects[2]