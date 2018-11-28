# class to draw small preview boxes

import csv
import pygame as pg
from classes.pokemonClass import Pokemon
from classes.hpBarClass import *

class Box(object): # SELECT SCREEN BOX
    def __init__(self, pkmn, pkmnType1, pkmnType2, topLeft, dimensions):
        # topLeft and dimensions are tuples
        # pkmn is a Pokémon object
        self.pkmn = pkmn
        self.pkmnType1 = pkmnType1
        self.pkmnType2 = pkmnType2
        self.topLeft = topLeft
        self.boxDim = pg.Rect(topLeft, dimensions)
        self.font = pg.font.SysFont("FuturaStd-Book", 16)
        self.movesFont = pg.font.SysFont("Bahnschrift", 12)
        self.pkbl = pg.image.load("classes/imgs/pokeball_small_grayscale.png")
        if self.pkmn != None:
        	self.pkmnName = pkmn.getName()
        	self.pkmnLevel = pkmn.getLevel()
        	self.pkmnBattleStats = pkmn.getBattleStats()
        	self.pkmnMoves = pkmn.getMoves()
    
    def draw(self, screen):
        pg.draw.rect(screen, (225, 225, 225), self.boxDim)
        screen.blit(self.pkbl, (self.topLeft[0] + 10, self.topLeft[1] + 10))
        pg.draw.line(screen, (190, 190, 190), (self.topLeft[0] + 160, self.topLeft[1] + 10),
                     (self.topLeft[0] + 160, self.topLeft[1] + 82))
        if self.pkmn != None:
        	pkmnIcon = pg.image.load("classes/imgs/tiny_icons/" + self.pkmnName.lower() + ".png")
        	screen.blit(pkmnIcon, (self.topLeft[0] + 10, self.topLeft[1] + 10))
        	pkmnNameDraw = self.font.render(self.pkmnName.upper(), True, (25, 25, 25))
        	screen.blit(pkmnNameDraw, (self.topLeft[0] + 50, self.topLeft[1] + 8))
        	hp = hpBar(self.pkmnLevel, self.pkmnBattleStats[0], self.topLeft[0] + 65, self.topLeft[1] + 70)
        	hp.draw(screen)
        	# types
        	if self.pkmnType1 != None:
        		screen.blit(self.pkmnType1, (self.topLeft[0] + 50, self.topLeft[1] + 26))
        	if self.pkmnType2 != None:
        		screen.blit(self.pkmnType2, (self.topLeft[0] + 85, self.topLeft[1] + 26))
        	# moves
        	if self.pkmnMoves[0] != None:
        		mvTxt = self.movesFont.render(self.pkmnMoves[0].getMoveName(), True, (65, 65, 65))
        		screen.blit(mvTxt, (self.topLeft[0] + 170, self.topLeft[1] + 11))
        	if self.pkmnMoves[1] != None:
        		mvTxt = self.movesFont.render(self.pkmnMoves[1].getMoveName(), True, (65, 65, 65))
        		screen.blit(mvTxt, (self.topLeft[0] + 170, self.topLeft[1] + 30.5))
        	if self.pkmnMoves[2] != None:
        		mvTxt = self.movesFont.render(self.pkmnMoves[2].getMoveName(), True, (65, 65, 65))
        		screen.blit(mvTxt, (self.topLeft[0] + 170, self.topLeft[1] + 49.5))
        	if self.pkmnMoves[3] != None:
        		mvTxt = self.movesFont.render(self.pkmnMoves[3].getMoveName(), True, (65, 65, 65))
        		screen.blit(mvTxt, (self.topLeft[0] + 170, self.topLeft[1] + 69))

class PartyBox(Box):
    def __init__(self, pkmn, pkmnType1, pkmnType2, topLeft, dimensions, isActive, isFainted):
        # isActive is a boolean (referring to whether the pokemon is out or not)
        super().__init__(pkmn, pkmnType1, pkmnType2, topLeft, dimensions)
        self.isActive = isActive
        self.isFainted = isFainted
        self.lvFont = pg.font.SysFont("FuturaStd-Book", 12)

    def draw(self, screen):
        if self.isActive:
            pg.draw.rect(screen, (83, 191, 96), self.boxDim)
        elif self.isFainted:
            pg.draw.rect(screen, (173, 46, 46), self.boxDim)
        else:
            pg.draw.rect(screen, (63, 102, 165), self.boxDim)
        screen.blit(self.pkbl, (self.topLeft[0] + 10, self.topLeft[1] + 10))
        if self.pkmn != None:
            pkmnIcon = pg.image.load("classes/imgs/tiny_icons/" + self.pkmnName.lower() + ".png")
            screen.blit(pkmnIcon, (self.topLeft[0] + 10, self.topLeft[1] + 10))
            pkmnNameDraw = self.font.render(self.pkmnName.upper(), True, (25, 25, 25))
            screen.blit(pkmnNameDraw, (self.topLeft[0] + 50, self.topLeft[1] + 10))
            statChanges = self.pkmn.getStatChanges()
            lv = self.pkmn.getLevel()
            lvTxt = self.lvFont.render("LV. " + str(lv), True, (50, 50, 50))
            lvTxtRect = lvTxt.get_rect(topright = (self.topLeft[0] + 282, self.topLeft[1] + 10))
            screen.blit(lvTxt, lvTxtRect)
            hp = BattleHPBar(self.pkmnLevel, self.pkmnBattleStats[0] - statChanges[0], self.topLeft[0] + 103, self.topLeft[1] + 62, self.pkmnBattleStats[0])
            hp.draw(screen)
            # types
            if self.pkmnType1 != None:
                screen.blit(self.pkmnType1, (self.topLeft[0] + 50, self.topLeft[1] + 28))
            if self.pkmnType2 != None:
                screen.blit(self.pkmnType2, (self.topLeft[0] + 85, self.topLeft[1] + 28))

class MoveBox:
    def __init__(self, move, topLeft, dimensions, typeIcons, catIcons):
        self.move = move
        if self.move != None:
            self.name = move.getMoveName()
            self.type = move.getMoveType()
            self.cat = move.getMoveCategory()
            self.pp = move.getMovePP()
        self.typeIcons = typeIcons
        self.catIcons = catIcons
        self.topLeft = topLeft
        self.boxDim = pg.Rect(topLeft, dimensions)
        self.font = pg.font.SysFont("FuturaStd-Book", 18)
        self.fontDetails = pg.font.SysFont("FuturaStd-Book", 14)

    def draw(self, screen):
        pg.draw.rect(screen, (40, 40, 40), self.boxDim)
        if self.move != None:
            mvName = self.font.render(self.name.upper(), True, (220, 220, 220))
            screen.blit(mvName, (self.topLeft[0] + 10, self.topLeft[1] + 10))
            mvImgType, mvImgCat = pg.image.load(self.typeIcons[self.type]), pg.image.load(self.catIcons[self.cat])
            mvImgTypeRect = mvImgType.get_rect(topright = (self.topLeft[0] + 270, self.topLeft[1] + 10))
            mvImgCatRect = mvImgCat.get_rect(topright = (self.topLeft[0] + 270, self.topLeft[1] + 30))
            screen.blit(mvImgType, mvImgTypeRect)
            screen.blit(mvImgCat, mvImgCatRect)

            mvPP = self.fontDetails.render("PP: " + str(self.pp), True, (140, 140, 140))
            screen.blit(mvPP, (self.topLeft[0] + 25, self.topLeft[1] + 35))

class ActiveBox:
    def __init__(self, plyrPkmn, cpuPkmn, topLeft):
        self.plyrPkmn = plyrPkmn
        self.cpuPkmn = cpuPkmn
        self.topLeft = topLeft
        self.titleFont = pg.font.SysFont("FuturaStd-Book", 18)
        self.levelFont = pg.font.SysFont("FuturaStd-Book", 13)
        self.statsFont = pg.font.SysFont("FuturaStd-Book", 10)
        self.burn = pg.image.load("classes/imgs/status_cond/burn.png")
        self.burnPlyrRect = self.burn.get_rect(center = (863, 38))
        self.burnCPURect = self.burn.get_rect(center = (863, 308))
        self.para = pg.image.load("classes/imgs/status_cond/para.png")
        self.paraPlyrRect = self.para.get_rect(center = (863, 73))
        self.paraCPURect = self.para.get_rect(center = (863, 343))
        self.poison = pg.image.load("classes/imgs/status_cond/poison.png")
        self.poisonPlyrRect = self.poison.get_rect(center = (863, 108))
        self.poisonCPURect = self.poison.get_rect(center = (863, 378))
        self.sleep = pg.image.load("classes/imgs/status_cond/sleep.png")
        self.sleepPlyrRect = self.sleep.get_rect(center = (863, 143))
        self.sleepCPURect = self.sleep.get_rect(center = (863, 413))
        self.frozen = pg.image.load("classes/imgs/status_cond/frozen.png")
        self.frozenPlyrRect = self.frozen.get_rect(center = (863, 178))
        self.frozenCPURect = self.frozen.get_rect(center = (863, 448))

    def draw(self, screen): # 675, 25
        plyrName = self.titleFont.render(self.plyrPkmn.getName().upper(), True, (220, 220, 220))
        cpuName = self.titleFont.render(self.cpuPkmn.getName().upper(), True, (220, 220, 220))
        plyrLevel = self.levelFont.render("LV. " + str(self.plyrPkmn.getLevel()), True, (150, 150, 150))
        cpuLevel = self.levelFont.render("LV. " + str(self.cpuPkmn.getLevel()), True, (150, 150, 150))
        screen.blit(plyrName, (self.topLeft[0] + 55, self.topLeft[1] + 10))
        screen.blit(cpuName, (self.topLeft[0] + 55, self.topLeft[1] + 280))
        screen.blit(plyrLevel, (self.topLeft[0] + 55, self.topLeft[1] + 29))
        screen.blit(cpuLevel, (self.topLeft[0] + 55, self.topLeft[1] + 299))

        statColor = (186, 168, 95)

        # PLYR STAT CHANGES
        plyrAtk = self.statsFont.render(str(self.plyrPkmn.getStatChanges()[1]), True, statColor)
        plyrDef = self.statsFont.render(str(self.plyrPkmn.getStatChanges()[2]), True, statColor)
        plyrSpAtk = self.statsFont.render(str(self.plyrPkmn.getStatChanges()[3]), True, statColor)
        plyrSpDef = self.statsFont.render(str(self.plyrPkmn.getStatChanges()[4]), True, statColor)
        plyrSpd = self.statsFont.render(str(self.plyrPkmn.getStatChanges()[5]), True, statColor)
        screen.blit(plyrAtk, (self.topLeft[0] + 95, self.topLeft[1] + 81))
        screen.blit(plyrDef, (self.topLeft[0] + 95, self.topLeft[1] + 112.5))
        screen.blit(plyrSpAtk, (self.topLeft[0] + 95, self.topLeft[1] + 144))
        screen.blit(plyrSpDef, (self.topLeft[0] + 119, self.topLeft[1] + 97))
        screen.blit(plyrSpd, (self.topLeft[0] + 119, self.topLeft[1] + 128.5))

        # CPU STAT CHANGES
        cpuAtk = self.statsFont.render(str(self.cpuPkmn.getStatChanges()[1]), True, statColor)
        cpuDef = self.statsFont.render(str(self.cpuPkmn.getStatChanges()[2]), True, statColor)
        cpuSpAtk = self.statsFont.render(str(self.cpuPkmn.getStatChanges()[3]), True, statColor)
        cpuSpDef = self.statsFont.render(str(self.cpuPkmn.getStatChanges()[4]), True, statColor)
        cpuSpd = self.statsFont.render(str(self.cpuPkmn.getStatChanges()[5]), True, statColor)
        screen.blit(cpuAtk, (self.topLeft[0] + 95, self.topLeft[1] + 351))
        screen.blit(cpuDef, (self.topLeft[0] + 95, self.topLeft[1] + 382.5))
        screen.blit(cpuSpAtk, (self.topLeft[0] + 95, self.topLeft[1] + 414))
        screen.blit(cpuSpDef, (self.topLeft[0] + 119, self.topLeft[1] + 367))
        screen.blit(cpuSpd, (self.topLeft[0] + 119, self.topLeft[1] + 398.5))

        # PLYR STATUS CONDITIONS
        if self.plyrPkmn.getConditions()[0] == True:
            screen.blit(self.burn, self.burnPlyrRect)
        elif self.plyrPkmn.getConditions()[1] == True:
            screen.blit(self.para, self.paraPlyrRect)
        elif self.plyrPkmn.getConditions()[2] == True:
            screen.blit(self.poison, self.poisonPlyrRect)
        elif self.plyrPkmn.getConditions()[3] == True:
            screen.blit(self.sleep, self.sleepPlyrRect)
        elif self.plyrPkmn.getConditions()[4] == True:
            screen.blit(self.frozen, self.frozenPlyrRect)

        # CPU STATUS CONDITIONS
        if self.cpuPkmn.getConditions()[0] == True:
            screen.blit(self.burn, self.burnCPURect)
        elif self.cpuPkmn.getConditions()[1] == True:
            screen.blit(self.para, self.paraCPURect)
        elif self.cpuPkmn.getConditions()[2] == True:
            screen.blit(self.poison, self.poisonCPURect)
        elif self.cpuPkmn.getConditions()[3] == True:
            screen.blit(self.sleep, self.sleepCPURect)
        elif self.cpuPkmn.getConditions()[4] == True:
            screen.blit(self.frozen, self.frozenCPURect)