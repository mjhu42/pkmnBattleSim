"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"                                                                               "
"                                                                               "
"                                                                               "
"                           POKÉMON BATTLE SIMULATOR                            "
"                               15-112. fall '18.                               "
"                                  michelle hu                                  "
"                                                                               "
"                                                                               "
"                                                                               "
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import pygame, csv, copy
from pygamegame import PygameGame
from classes.rotatingButton import RotatingButton
from classes.pokemonClass import Pokemon
from classes.moveClass import Move
from classes.pkmnBoxClass import *
from classes.hpBarClass import *
from classes.characterClass import *
from classes.external_modules.textbox import TextBox
from classes.external_modules.gifImage import GifSprite

# (ノ◉益◉)ノ彡┻━━━━━┻
class BattleSimulator(PygameGame):
    POKEMON_DICT = {}
    MOVES_DICT = {}
    
    ###################
    ## INIT FUNCTION ##
    ###################
    def init(self):
        super().init()

        # POKÉMON DICTIONARY
        pkmnFile = "classes/spreadsheets/pokemon.csv"
        pkmnList = open(pkmnFile)
        csvReaderPkmn = csv.reader(pkmnList, delimiter = ",")
        for line in csvReaderPkmn:
            if line[0] == "Name":
                continue
            BattleSimulator.POKEMON_DICT[line[0]] = line[1:13]
        pkmnList.close()
        # print(BattleSimulator.POKEMON_DICT)

        # MOVES DICTIONARY
        movesFile = "classes/spreadsheets/moves.csv"
        movesList = open(movesFile)
        csvReaderMove = csv.reader(movesList, delimiter = ",")
        for line in csvReaderMove:
            if line[0] == "Move":
                continue
            BattleSimulator.MOVES_DICT[line[0]] = line[1:7] + [[line[7:12], line[12:19], line[19:]]]
        movesList.close()
        # print(BattleSimulator.MOVES_DICT)

        
        ## TITLE SCREEN
        self.titleCard = True

        self.centerX = self.width / 2
        self.screen = pygame.display.set_mode((900, 650))
        
        
        
        # IMAGES
        self.titleBG = pygame.image.load("images/game_bg.png")
        self.logo = pygame.image.load("images/pkmn_logo.png")
        self.playButton1 = pygame.image.load("images/playbutton1.png")
        self.logoRect = self.logo.get_rect()
        self.playButton1Rect = self.playButton1.get_rect(center = (300, 550))
        pkblButtonImage = pygame.image.load("images/pokeball_transparent.png").convert_alpha()
        
        
        
        # BUTTONS
        self.initButton = pygame.sprite.Group(RotatingButton(pkblButtonImage, (self.centerX, 487.5)))
        
        
        
        # TEXT
        pygame.font.init()
        
        self.logoFont = pygame.font.SysFont('Pokemon Solid Normal', 50)
        self.BSTextSurface = self.logoFont.render('Battle Simulator', True, (255, 204, 2))
        self.BSTextSurfaceShadow = self.logoFont.render('Battle Simulator', True, (53, 103, 176))
        self.BSTextSurfaceShadow2 = self.logoFont.render('Battle Simulator', True, (33, 56, 110))
        self.BSTextSurfaceRect = self.BSTextSurface.get_rect()
        
        self.enterFont = pygame.font.SysFont("SquareFont", 16)
        self.enterTextSurface = self.enterFont.render("CLICK POKéBALL TO ENTER", True, (159, 6, 6))
        self.enterTSRect = self.enterTextSurface.get_rect()
        
        self.events = pygame.event.get()
        
        
        
        ## SELECT SCREEN
        xSelectBoxCoord = 610
        padding = 14
        boxesDim = (280, 92)
        self.selectScreen = False
        


        # POKÉMON
        self.party = [None, None, None, None, None, None]
        self.partySize = 0

        self.pkmn1 = None
        self.pkmn1Name = None
        self.pkmn1Type1 = None
        self.pkmn1Type2 = None
        self.pkmn1ev = [0, 0, 0, 0, 0, 0]
        self.pkmn1Level = 50
        self.pkmn1Move1 = None
        self.pkmn1Move2 = None
        self.pkmn1Move3 = None
        self.pkmn1Move4 = None
        self.pkmn1Moves = [self.pkmn1Move1, self.pkmn1Move2, self.pkmn1Move3, self.pkmn1Move4]
        self.pkmn1BattleStats = [0, 0, 0, 0, 0, 0]
        self.pkmn1IsFainted = False
        self.pkmn1StatChanges = [0, 0, 0, 0, 0, 0]
        self.pkmn1Conditions = [False, False, False, False, False]

        self.pkmn2 = None
        self.pkmn2Name = None
        self.pkmn2Type1 = None
        self.pkmn2Type2 = None
        self.pkmn2ev = [0, 0, 0, 0, 0, 0]
        self.pkmn2Level = 50
        self.pkmn2Move1 = None
        self.pkmn2Move2 = None
        self.pkmn2Move3 = None
        self.pkmn2Move4 = None
        self.pkmn2Moves = [self.pkmn2Move1, self.pkmn2Move2, self.pkmn2Move3, self.pkmn2Move4]
        self.pkmn2BattleStats = [0, 0, 0, 0, 0, 0]
        self.pkmn2IsFainted = False
        self.pkmn2StatChanges = [0, 0, 0, 0, 0, 0]
        self.pkmn2Conditions = [False, False, False, False, False]

        self.pkmn3 = None
        self.pkmn3Name = None
        self.pkmn3Type1 = None
        self.pkmn3Type2 = None
        self.pkmn3ev = [0, 0, 0, 0, 0, 0]
        self.pkmn3Level = 50
        self.pkmn3Move1 = None
        self.pkmn3Move2 = None
        self.pkmn3Move3 = None
        self.pkmn3Move4 = None
        self.pkmn3Moves = [self.pkmn3Move1, self.pkmn3Move2, self.pkmn3Move3, self.pkmn3Move4]
        self.pkmn3BattleStats = [0, 0, 0, 0, 0, 0]
        self.pkmn3IsFainted = False
        self.pkmn3StatChanges = [0, 0, 0, 0, 0, 0]
        self.pkmn3Conditions = [False, False, False, False, False]

        self.pkmn4 = None
        self.pkmn4Name = None
        self.pkmn4Type1 = None
        self.pkmn4Type2 = None
        self.pkmn4ev = [0, 0, 0, 0, 0, 0]
        self.pkmn4Level = 50
        self.pkmn4Move1 = None
        self.pkmn4Move2 = None
        self.pkmn4Move3 = None
        self.pkmn4Move4 = None
        self.pkmn4Moves = [self.pkmn4Move1, self.pkmn4Move2, self.pkmn4Move3, self.pkmn4Move4]
        self.pkmn4BattleStats = [0, 0, 0, 0, 0, 0]
        self.pkmn4IsFainted = False
        self.pkmn4StatChanges = [0, 0, 0, 0, 0, 0]
        self.pkmn4Conditions = [False, False, False, False, False]

        self.pkmn5 = None
        self.pkmn5Name = None
        self.pkmn5Type1 = None
        self.pkmn5Type2 = None
        self.pkmn5ev = [0, 0, 0, 0, 0, 0]
        self.pkmn5Level = 50
        self.pkmn5Move1 = None
        self.pkmn5Move2 = None
        self.pkmn5Move3 = None
        self.pkmn5Move4 = None
        self.pkmn5Moves = [self.pkmn5Move1, self.pkmn5Move2, self.pkmn5Move3, self.pkmn5Move4]
        self.pkmn5BattleStats = [0, 0, 0, 0, 0, 0]
        self.pkmn5IsFainted = False
        self.pkmn5StatChanges = [0, 0, 0, 0, 0, 0]
        self.pkmn5Conditions = [False, False, False, False, False]

        self.pkmn6 = None
        self.pkmn6Name = None
        self.pkmn6Type1 = None
        self.pkmn6Type2 = None
        self.pkmn6ev = [0, 0, 0, 0, 0, 0]
        self.pkmn6Level = 50
        self.pkmn6Move1 = None
        self.pkmn6Move2 = None
        self.pkmn6Move3 = None
        self.pkmn6Move4 = None
        self.pkmn6Moves = [self.pkmn6Move1, self.pkmn6Move2, self.pkmn6Move3, self.pkmn6Move4]
        self.pkmn6BattleStats = [0, 0, 0, 0, 0, 0]
        self.pkmn6IsFainted = False
        self.pkmn6StatChanges = [0, 0, 0, 0, 0, 0]
        self.pkmn6Conditions = [False, False, False, False, False]

        self.pkmnTypes = [[self.pkmn1Type1, self.pkmn1Type2], [self.pkmn2Type1, self.pkmn2Type2],
                          [self.pkmn3Type1, self.pkmn3Type2], [self.pkmn4Type1, self.pkmn4Type2],
                          [self.pkmn5Type1, self.pkmn5Type2], [self.pkmn6Type1, self.pkmn6Type2]]

        self.cpuPkmn1 = Pokemon("Charizard", 100, [4, 0, 0, 252, 0, 252], [Move("Flamethrower", 'Fire', 'Special', '90', '100', '24', '', [['', '', '', '', ''], ['', '', '', '', '', '', ''], ['', '', '', '', '', '']]), Move("Wing Attack", 'Flying', 'Physical', '60', '100', '56', '', [['', '', '', '', ''], ['', '', '', '', '', '', ''], ['', '', '', '', '', '']]), Move("Slash", 'Normal', 'Physical', '70', '100', '32', '', [['', '', '', '', ''], ['', '', '', '', '', '', ''], ['1', '', '', '', '', '']]), None], False, [0, 0, 0, 0, 0, 0, 0, 0], [False, False, False, False, False], True)
        # self.cpuPkmn1 = None
        self.cpuPkmn1BattleStats = [0, 0, 0, 0, 0, 0]
        self.cpuPkmn1IsFainted = False
        self.cpuPkmn1StatChanges = [0, 0, 0, 0, 0, 0]
        self.cpuPkmn1Conditions = [False, False, False, False, False, False]

        self.cpuPkmn2 = Pokemon("Blastoise", 100, [4, 0, 0, 252, 0, 252], [Move("Surf", 'Water', 'Special', '65', '100', '32', '', [['', '', '', '', ''], ['', '', '', '', '', '', ''], ['', '', '', '', '', '']]), Move("Blizzard", 'Ice', 'Special', '110', '70', '8', '', [['', '', '', '', '10'], ['', '', '', '', '', '', ''], ['', '', '', '', '', '']]), Move("Ice Beam", 'Ice', 'Special', '90', '100', '16', '', [['', '', '', '', '10'], ['', '', '', '', '', '', ''], ['', '', '', '', '', '']]), None], False, [0, 0, 0, 0, 0, 0, 0, 0], [False, False, False, False, False])
        self.cpuPkmn2BattleStats = [0, 0, 0, 0, 0, 0]
        self.cpuPkmn2IsFainted = False
        self.cpuPkmn2StatChanges = [0, 0, 0, 0, 0, 0]
        self.cpuPkmn2Conditions = [False, False, False, False, False, False]

        self.cpuPkmn3 = Pokemon("Venusaur", 100, [0, 0, 4, 252, 252, 0], [Move("Petal Dance", 'Grass', 'Special', '120', '100', '16', '', [['', '', '', '', ''], ['', '', '', '', '', '', ''], ['', '', '10', '', '', '']]), Move("Double-Edge", 'Normal', 'Physical', '120', '100', '24', '', [['', '', '', '', ''], ['', '', '', '', '', '', ''], ['', '', '25', '', '', '']]), None, None], False, [0, 0, 0, 0, 0, 0, 0, 0], [False, False, False, False, False])
        self.cpuPkmn3BattleStats = [0, 0, 0, 0, 0, 0]
        self.cpuPkmn3IsFainted = False
        self.cpuPkmn3StatChanges = [0, 0, 0, 0, 0, 0]
        self.cpuPkmn3Conditions = [False, False, False, False, False, False]

        self.cpuPkmn4 = Pokemon("Zapdos", 100, [0, 0, 4, 252, 252, 0], [Move("Thunderbolt", 'Electric', 'Special', '90', '100', '24', '', [['', '', '10', '', ''], ['', '', '', '', '', '', ''], ['', '', '', '', '', '']]), Move("Wing Attack", 'Flying', 'Physical', '60', '100', '56', '', [['', '', '', '', ''], ['', '', '', '', '', '', ''], ['', '', '', '', '', '']]), None, None], False, [0, 0, 0, 0, 0, 0, 0, 0], [False, False, False, False, False])
        self.cpuPkmn4BattleStats = [0, 0, 0, 0, 0, 0]
        self.cpuPkmn4IsFainted = False
        self.cpuPkmn4StatChanges = [0, 0, 0, 0, 0, 0]
        self.cpuPkmn4Conditions = [False, False, False, False, False, False]

        self.cpuPkmn5 = None
        self.cpuPkmn5BattleStats = [0, 0, 0, 0, 0, 0]
        self.cpuPkmn5IsFainted = False
        self.cpuPkmn5StatChanges = [0, 0, 0, 0, 0, 0]
        self.cpuPkmn5Conditions = [False, False, False, False, False, False]

        self.cpuPkmn6 = None
        self.cpuPkmn6BattleStats = [0, 0, 0, 0, 0, 0]
        self.cpuPkmn6IsFainted = False
        self.cpuPkmn6StatChanges = [0, 0, 0, 0, 0, 0]
        self.cpuPkmn6Conditions = [False, False, False, False, False, False]

        self.cpuParty = [self.cpuPkmn1, self.cpuPkmn2, self.cpuPkmn3, self.cpuPkmn4, self.cpuPkmn5, self.cpuPkmn6]
        self.cpuActivePkmn = self.cpuPkmn2
        self.cpuActiveSprite = None
        self.cpuCrrActive = None


        self.playerActivePkmn = None
        self.plyrCrrActive = None
        self.playerActiveSprite = None
        self.activeMoves = None


        
        # IMAGES
        self.selectBG = pygame.image.load("images/selectscreen_bg.png")
        self.trprtSelectBG = pygame.image.load("images/selectscreen_transparent_bg.png").convert_alpha()
        self.selectedPkmnBG = pygame.image.load("images/pokeball_for_sprite.png")
        self.pkblSmallBW = pygame.image.load("images/pokeball_small_grayscale.png")
        self.pkblSmallBWCoords = [(xSelectBoxCoord + 10, padding + 10), (xSelectBoxCoord + 10, padding * 2 + 10 + 92),
                                  (xSelectBoxCoord + 10, padding * 3 + 10 + 92 * 2), (xSelectBoxCoord + 10, padding * 4 + 10 + 92 * 3),
                                  (xSelectBoxCoord + 10, padding * 5 + 10 + 92 * 4), (xSelectBoxCoord + 10, padding * 6 + 10 + 92 * 5)]

        saveIcon = pygame.image.load("images/pokeball_small.png").convert_alpha()

        # sprites
        self.inputSprite1 = None
        self.inputSprite2 = None
        self.inputSprite3 = None
        self.inputSprite4 = None
        self.inputSprite5 = None
        self.inputSprite6 = None

        # types
        self.bugTypeIcon = "images/types/bug.gif"
        self.darkTypeIcon = "images/types/dark.gif"
        self.dragonTypeIcon = "images/types/dragon.gif"
        self.electricTypeIcon = "images/types/electric.gif"
        self.fairyTypeIcon = "images/types/fairy.gif"
        self.fightingTypeIcon = "images/types/fighting.gif"
        self.fireTypeIcon = "images/types/fire.gif"
        self.flyingTypeIcon = "images/types/flying.gif"
        self.ghostTypeIcon = "images/types/ghost.gif"
        self.grassTypeIcon = "images/types/grass.gif"
        self.groundTypeIcon = "images/types/ground.gif"
        self.iceTypeIcon = "images/types/ice.gif"
        self.normalTypeIcon = "images/types/normal.gif"
        self.poisonTypeIcon = "images/types/poison.gif"
        self.psychicTypeIcon = "images/types/psychic.gif"
        self.rockTypeIcon = "images/types/rock.gif"
        self.steelTypeIcon = "images/types/steel.gif"
        self.waterTypeIcon = "images/types/water.gif"
        self.typeIconsList = {"Bug": self.bugTypeIcon, "Dark": self.darkTypeIcon, "Dragon": self.dragonTypeIcon,
                              "Electric": self.electricTypeIcon, "Fairy": self.fairyTypeIcon, "Fighting": self.fightingTypeIcon,
                              "Fire": self.fireTypeIcon, "Flying": self.flyingTypeIcon, "Ghost": self.ghostTypeIcon,
                              "Grass": self.grassTypeIcon, "Ground": self.groundTypeIcon, "Ice": self.iceTypeIcon,
                              "Normal": self.normalTypeIcon, "Poison": self.poisonTypeIcon,
                              "Psychic": self.psychicTypeIcon, "Rock": self.rockTypeIcon, "Steel": self.steelTypeIcon,
                              "Water": self.waterTypeIcon}

        # categories
        self.physicalIcon = "images/categories/physical.png"
        self.specialIcon = "images/categories/special.png"
        self.statusIcon = "images/categories/status.png"
        self.categoryIconsList = {"Physical": self.physicalIcon, "Special": self.specialIcon, "Status": self.statusIcon}


        # TEXT
        self.selectForBattleFont = pygame.font.SysFont("Bahnschrift", 14)
        self.selectForBattleName = self.selectForBattleFont.render("Name", True, (25, 25, 25))
        self.selectForBattleLvl = self.selectForBattleFont.render("Level", True, (25, 25, 25))
        self.selectForBattleMoves = self.selectForBattleFont.render("Moves", True, (25, 25, 25))
        self.selectForBattleEVs = self.selectForBattleFont.render("EVs", True, (25, 25, 25))
        self.selectForBattleStats = self.selectForBattleFont.render("Stats", True, (25, 25, 25))

        self.moveDetailsFont = pygame.font.SysFont("FuturaStd-Book", 12)
        self.moveTypeTxt = self.moveDetailsFont.render("TYPE", True, (25, 25, 25))
        self.moveCatTxt = self.moveDetailsFont.render("CATEGORY", True, (25, 25, 25))
        self.movePPTxt = self.moveDetailsFont.render("PP:", True, (25, 25, 25))
        self.movePowerTxt = self.moveDetailsFont.render("POWER:", True, (25, 25, 25))
        self.moveAccuracyTxt = self.moveDetailsFont.render("ACCURACY:", True, (25, 25, 25))

        self.statDetailsFont = pygame.font.SysFont("FuturaStd-Book", 13, bold = True)

        self.evDetailsFont = pygame.font.SysFont("FuturaStd-Book", 13)
        self.evHPTxt = self.evDetailsFont.render("HP", True, (25, 25, 25))
        self.evAtkTxt = self.evDetailsFont.render("ATTACK", True, (25, 25, 25))
        self.evDefTxt = self.evDetailsFont.render("DEFENSE", True, (25, 25, 25))
        self.evSpAtkTxt = self.evDetailsFont.render("SP. ATTACK", True, (25, 25, 25))
        self.evSpDefTxt = self.evDetailsFont.render("SP. DEFENSE", True, (25, 25, 25))
        self.evSpdTxt = self.evDetailsFont.render("SPEED", True, (25, 25, 25))
        self.evTxtList = [self.evHPTxt, self.evAtkTxt, self.evDefTxt,
                          self.evSpAtkTxt, self.evSpDefTxt, self.evSpdTxt]
        self.evTxtYCoordsList = [300, 355, 410, 465, 520, 575]
        self.statTxtYCoordsList = [114, 114 + 130/6, 114 + 260/6, 114 + 390/6, 114 + 520/6, 114 + 650/6]


        
        # TEXT INPUTS
        # name
        self.textInputPkmn1 = TextBox((220, 100, 120, 20), command = self.getPkmn, active = True)
        self.textInputPkmn2 = TextBox((220, 100, 120, 20), command = self.getPkmn)
        self.textInputPkmn3 = TextBox((220, 100, 120, 20), command = self.getPkmn)
        self.textInputPkmn4 = TextBox((220, 100, 120, 20), command = self.getPkmn)
        self.textInputPkmn5 = TextBox((220, 100, 120, 20), command = self.getPkmn)
        self.textInputPkmn6 = TextBox((220, 100, 120, 20), command = self.getPkmn)
        
        # level
        self.levelInputPkmn1 = TextBox((220, 170, 50, 20), command = self.getLevel)
        self.levelInputPkmn2 = TextBox((220, 170, 50, 20), command = self.getLevel)
        self.levelInputPkmn3 = TextBox((220, 170, 50, 20), command = self.getLevel)
        self.levelInputPkmn4 = TextBox((220, 170, 50, 20), command = self.getLevel)
        self.levelInputPkmn5 = TextBox((220, 170, 50, 20), command = self.getLevel)
        self.levelInputPkmn6 = TextBox((220, 170, 50, 20), command = self.getLevel)

        # moves
        self.inputPkmn1Move1 = TextBox((51, 311, 145, 20), command = self.getMove)
        self.inputPkmn1Move2 = TextBox((51, 391, 145, 20), command = self.getMove)
        self.inputPkmn1Move3 = TextBox((51, 471, 145, 20), command = self.getMove)
        self.inputPkmn1Move4 = TextBox((51, 551, 145, 20), command = self.getMove)

        self.inputPkmn2Move1 = TextBox((51, 311, 145, 20), command = self.getMove)
        self.inputPkmn2Move2 = TextBox((51, 391, 145, 20), command = self.getMove)
        self.inputPkmn2Move3 = TextBox((51, 471, 145, 20), command = self.getMove)
        self.inputPkmn2Move4 = TextBox((51, 551, 145, 20), command = self.getMove)

        self.inputPkmn3Move1 = TextBox((51, 311, 145, 20), command = self.getMove)
        self.inputPkmn3Move2 = TextBox((51, 391, 145, 20), command = self.getMove)
        self.inputPkmn3Move3 = TextBox((51, 471, 145, 20), command = self.getMove)
        self.inputPkmn3Move4 = TextBox((51, 551, 145, 20), command = self.getMove)

        self.inputPkmn4Move1 = TextBox((51, 311, 145, 20), command = self.getMove)
        self.inputPkmn4Move2 = TextBox((51, 391, 145, 20), command = self.getMove)
        self.inputPkmn4Move3 = TextBox((51, 471, 145, 20), command = self.getMove)
        self.inputPkmn4Move4 = TextBox((51, 551, 145, 20), command = self.getMove)

        self.inputPkmn5Move1 = TextBox((51, 311, 145, 20), command = self.getMove)
        self.inputPkmn5Move2 = TextBox((51, 391, 145, 20), command = self.getMove)
        self.inputPkmn5Move3 = TextBox((51, 471, 145, 20), command = self.getMove)
        self.inputPkmn5Move4 = TextBox((51, 551, 145, 20), command = self.getMove)

        self.inputPkmn6Move1 = TextBox((51, 311, 145, 20), command = self.getMove)
        self.inputPkmn6Move2 = TextBox((51, 391, 145, 20), command = self.getMove)
        self.inputPkmn6Move3 = TextBox((51, 471, 145, 20), command = self.getMove)
        self.inputPkmn6Move4 = TextBox((51, 551, 145, 20), command = self.getMove)

        self.input1List = [self.textInputPkmn1, self.levelInputPkmn1, self.inputPkmn1Move1,
                           self.inputPkmn1Move2, self.inputPkmn1Move3, self.inputPkmn1Move4]
        self.input2List = [self.textInputPkmn2, self.levelInputPkmn2, self.inputPkmn2Move1,
                           self.inputPkmn2Move2, self.inputPkmn2Move3, self.inputPkmn2Move4]
        self.input3List = [self.textInputPkmn3, self.levelInputPkmn3, self.inputPkmn3Move1,
                           self.inputPkmn3Move2, self.inputPkmn3Move3, self.inputPkmn3Move4]
        self.input4List = [self.textInputPkmn4, self.levelInputPkmn4, self.inputPkmn4Move1,
                           self.inputPkmn4Move2, self.inputPkmn4Move3, self.inputPkmn4Move4]
        self.input5List = [self.textInputPkmn5, self.levelInputPkmn5, self.inputPkmn5Move1,
                           self.inputPkmn5Move2, self.inputPkmn5Move3, self.inputPkmn5Move4]
        self.input6List = [self.textInputPkmn6, self.levelInputPkmn6, self.inputPkmn6Move1,
                           self.inputPkmn6Move2, self.inputPkmn6Move3, self.inputPkmn6Move4]

        # ev
        self.inputPkmn1HP = TextBox((410, 317, 50, 20), command = self.getEV)
        self.inputPkmn1Atk = TextBox((410, 372, 50, 20), command = self.getEV)
        self.inputPkmn1Def = TextBox((410, 427, 50, 20), command = self.getEV)
        self.inputPkmn1SpAtk = TextBox((410, 482, 50, 20), command = self.getEV)
        self.inputPkmn1SpDef = TextBox((410, 537, 50, 20), command = self.getEV)
        self.inputPkmn1Spd = TextBox((410, 592, 50, 20), command = self.getEV)
        self.inputEV1List = [self.inputPkmn1HP, self.inputPkmn1Atk, self.inputPkmn1Def,
                             self.inputPkmn1SpAtk, self.inputPkmn1SpDef, self.inputPkmn1Spd]

        self.inputPkmn2HP = TextBox((410, 317, 50, 20), command = self.getEV)
        self.inputPkmn2Atk = TextBox((410, 372, 50, 20), command = self.getEV)
        self.inputPkmn2Def = TextBox((410, 427, 50, 20), command = self.getEV)
        self.inputPkmn2SpAtk = TextBox((410, 482, 50, 20), command = self.getEV)
        self.inputPkmn2SpDef = TextBox((410, 537, 50, 20), command = self.getEV)
        self.inputPkmn2Spd = TextBox((410, 592, 50, 20), command = self.getEV)
        self.inputEV2List = [self.inputPkmn2HP, self.inputPkmn2Atk, self.inputPkmn2Def,
                             self.inputPkmn2SpAtk, self.inputPkmn2SpDef, self.inputPkmn2Spd]

        self.inputPkmn3HP = TextBox((410, 317, 50, 20), command = self.getEV)
        self.inputPkmn3Atk = TextBox((410, 372, 50, 20), command = self.getEV)
        self.inputPkmn3Def = TextBox((410, 427, 50, 20), command = self.getEV)
        self.inputPkmn3SpAtk = TextBox((410, 482, 50, 20), command = self.getEV)
        self.inputPkmn3SpDef = TextBox((410, 537, 50, 20), command = self.getEV)
        self.inputPkmn3Spd = TextBox((410, 592, 50, 20), command = self.getEV)
        self.inputEV3List = [self.inputPkmn3HP, self.inputPkmn3Atk, self.inputPkmn3Def,
                             self.inputPkmn3SpAtk, self.inputPkmn3SpDef, self.inputPkmn3Spd]

        self.inputPkmn4HP = TextBox((410, 317, 50, 20), command = self.getEV)
        self.inputPkmn4Atk = TextBox((410, 372, 50, 20), command = self.getEV)
        self.inputPkmn4Def = TextBox((410, 427, 50, 20), command = self.getEV)
        self.inputPkmn4SpAtk = TextBox((410, 482, 50, 20), command = self.getEV)
        self.inputPkmn4SpDef = TextBox((410, 537, 50, 20), command = self.getEV)
        self.inputPkmn4Spd = TextBox((410, 592, 50, 20), command = self.getEV)
        self.inputEV4List = [self.inputPkmn4HP, self.inputPkmn4Atk, self.inputPkmn4Def,
                             self.inputPkmn4SpAtk, self.inputPkmn4SpDef, self.inputPkmn4Spd]

        self.inputPkmn5HP = TextBox((410, 317, 50, 20), command = self.getEV)
        self.inputPkmn5Atk = TextBox((410, 372, 50, 20), command = self.getEV)
        self.inputPkmn5Def = TextBox((410, 427, 50, 20), command = self.getEV)
        self.inputPkmn5SpAtk = TextBox((410, 482, 50, 20), command = self.getEV)
        self.inputPkmn5SpDef = TextBox((410, 537, 50, 20), command = self.getEV)
        self.inputPkmn5Spd = TextBox((410, 592, 50, 20), command = self.getEV)
        self.inputEV5List = [self.inputPkmn5HP, self.inputPkmn5Atk, self.inputPkmn5Def,
                             self.inputPkmn5SpAtk, self.inputPkmn5SpDef, self.inputPkmn5Spd]

        self.inputPkmn6HP = TextBox((410, 317, 50, 20), command = self.getEV)
        self.inputPkmn6Atk = TextBox((410, 372, 50, 20), command = self.getEV)
        self.inputPkmn6Def = TextBox((410, 427, 50, 20), command = self.getEV)
        self.inputPkmn6SpAtk = TextBox((410, 482, 50, 20), command = self.getEV)
        self.inputPkmn6SpDef = TextBox((410, 537, 50, 20), command = self.getEV)
        self.inputPkmn6Spd = TextBox((410, 592, 50, 20), command = self.getEV)
        self.inputEV6List = [self.inputPkmn6HP, self.inputPkmn6Atk, self.inputPkmn6Def,
                             self.inputPkmn6SpAtk, self.inputPkmn6SpDef, self.inputPkmn6Spd]
        

        
        # BOXES & SHAPES
        self.selectBox1 = Box(self.pkmn1, self.pkmn1Type1, self.pkmn1Type2, (610, padding), boxesDim)
        self.selectBox2 = Box(self.pkmn2, self.pkmn2Type1, self.pkmn2Type2,
                              (xSelectBoxCoord, 2 * padding + 92), boxesDim)
        self.selectBox3 = Box(self.pkmn3, self.pkmn3Type1, self.pkmn3Type2,
                              (xSelectBoxCoord, 3 * padding + 2 * 92), boxesDim)
        self.selectBox4 = Box(self.pkmn4, self.pkmn4Type1, self.pkmn4Type2,
                              (xSelectBoxCoord, 4 * padding + 3 * 92), boxesDim)
        self.selectBox5 = Box(self.pkmn5, self.pkmn5Type1, self.pkmn5Type2,
                              (xSelectBoxCoord, 5 * padding + 4 * 92), boxesDim)
        self.selectBox6 = Box(self.pkmn6, self.pkmn6Type1, self.pkmn6Type2,
                              (xSelectBoxCoord, 6 * padding + 5 * 92), boxesDim)
        self.selectBoxList = [self.selectBox1, self.selectBox2, self.selectBox3, self.selectBox4, self.selectBox5,
                              self.selectBox6]

        self.pkmnIcon = pygame.Rect((20, 70), (170, 170))
        
        
        
        # BUTTONS
        self.boxButton1 = pygame.Rect((xSelectBoxCoord, padding), boxesDim)
        self.boxButton2 = pygame.Rect((xSelectBoxCoord, 2 * padding + 92), boxesDim)
        self.boxButton3 = pygame.Rect((xSelectBoxCoord, 3 * padding + 92 * 2), boxesDim)
        self.boxButton4 = pygame.Rect((xSelectBoxCoord, 4 * padding + 92 * 3), boxesDim)
        self.boxButton5 = pygame.Rect((xSelectBoxCoord, 5 * padding + 92 * 4), boxesDim)
        self.boxButton6 = pygame.Rect((xSelectBoxCoord, 6 * padding + 92 * 5), boxesDim)
        
        self.backButton = pygame.Rect((10, 10), (45, 45))
        self.clearButton = pygame.Rect((120, 10), (45, 45))
        self.saveIcon = pygame.sprite.Group(RotatingButton(saveIcon, (88, 32)))
        
        self.invalidBattleSel = pygame.Rect((600, 0), (300, 650))

        self.battleButton = pygame.Rect((98, 505), (404, 89))
        
        
        # IN-GAME STATES
        self.selectPokemon1 = False
        self.selectPokemon2 = False
        self.selectPokemon3 = False
        self.selectPokemon4 = False
        self.selectPokemon5 = False
        self.selectPokemon6 = False
        

        ## BATTLE SCREEN
        self.battleScreen = False

        self.chooseAction = False # battle, run, or team
        self.pickMoves = False
        self.viewParty = False
        self.mightRun = False

        self.inTurn = False

        self.playerSwitched = False
        self.cpuSwitched = False


        # IMAGES
        self.battleBG = pygame.image.load("images/battle_bg.png")
        self.viewPartyBG = pygame.image.load("images/viewParty.png")
        self.checkRunIMG = pygame.image.load("images/checkRun.png")

        # BUTTONS
        self.chooseActionB = pygame.image.load("images/chooseActionButtons.png")
        self.chooseActionBRect = self.chooseActionB.get_rect(center = (317.5, 522.5))
        self.chooseBattle = pygame.Rect((25, 420), (290, 205))
        self.chooseRun = pygame.Rect((375, 420), (235, 98))
        self.chooseViewParty = pygame.Rect((375, 518), (235, 98))

        self.yesRun = pygame.Rect((120, 326), (324, 123))
        self.noRun = pygame.Rect((456, 326), (324, 123))

        # MOVE BOXES
        self.moveBoxCoords = [(30, 425), (325, 425), (30, 530), (325, 530)]
        self.move1Button = pygame.Rect((30, 425), (280, 90))
        self.move2Button = pygame.Rect((325, 425), (280, 90))
        self.move3Button = pygame.Rect((30, 530), (280, 90))
        self.move4Button = pygame.Rect((325, 530), (280, 90))

        # PARTY BOXES
        self.partyBox1 = None
        self.partyBox2 = None
        self.partyBox3 = None
        self.partyBox4 = None
        self.partyBox5 = None
        self.partyBox6 = None
        self.partyBoxList = [self.partyBox1, self.partyBox2, self.partyBox3, self.partyBox4, self.partyBox5,
                             self.partyBox6]

        self.partyCoords = [(20, 75), (318, 75), (20, 262), (318, 262), (20, 449), (318, 449)]
        self.partyButton1 = pygame.Rect((20, 75), (292, 181))
        self.partyButton2 = pygame.Rect((318, 75), (292, 181))
        self.partyButton3 = pygame.Rect((20, 262), (292, 181))
        self.partyButton4 = pygame.Rect((318, 262), (292, 181))
        self.partyButton5 = pygame.Rect((20, 449), (292, 181))
        self.partyButton6 = pygame.Rect((318, 449), (292, 181))

        # TEXT
        self.hpFont = pygame.font.SysFont("Spantaran (demo)", 11)

        # IMAGES
        self.hpBarBGRed = pygame.image.load("images/HPBarBGRed.png")
        self.hpBarBGBlue = pygame.image.load("images/HPBarBGBlue.png")

        # FAINTED PKMN LISTS
        self.playerFainted = []
        self.cpuFainted = []

        # PLAYERS
        self.player = Player(self.playerActivePkmn, self.party, self.cpuActivePkmn, BattleSimulator.POKEMON_DICT, BattleSimulator.MOVES_DICT)
        self.cpuEasy = EasyOpponent(self.playerActivePkmn, self.party, self.cpuActivePkmn, self.cpuParty, BattleSimulator.POKEMON_DICT, BattleSimulator.MOVES_DICT)

        self.activeHPBar = None
        self.cpuHPBar = None

        self.plyrJustFainted = False
        self.cpuJustFainted = False

        self.plyrUsedMove = None
        self.cpuUsedMove = None

        self.plyrMsg = "What will %s do?" % (self.playerActivePkmn)
        self.cpuMsg = ""

        ## GAME OVER
        self.gameOver = False
        self.playerWon = False
        self.cpuWon = False

        # IMAGES
        self.playerWonBG = pygame.image.load("images/plyrwon.png")
        self.cpuWonBG = pygame.image.load("images/cpuwon.png")

        # BUTTONS
        self.replayButton = self.yesRun
        self.quitButton = self.noRun

    ############################
    ## INITIALIZE ACTIVE PKMN ##
    ############################
    def initializeActive(self):
        # FOR PLAYER PARTY: set first pkmn inputted as the active pkmn
        index = 0
        for i in range(0, 6):
            if self.party[i] != None:
                index = i + 1
                self.party[i].activeTrue()
                self.playerActivePkmn = self.party[i]
                self.plyrCrrActive = self.party[i]

                # FOLDERS AND FRAMES
                activeName = self.playerActivePkmn.getName()
                properName = str(activeName).title()
                if properName == "Farfetch'D":
                    properName = "Farfetch'd"
                folderPath = "images/pkmn_sprites_back/"
                pkmnLower = str(activeName).lower()
                if pkmnLower == "mr. mime":
                    pkmnLower = "mrmime"
                pkmnFolderPath = folderPath + pkmnLower + "/"
                frameNum = BattleSimulator.POKEMON_DICT[properName][10]

                # MAKE SPRITE OBJECTS
                spriteInit = GifSprite(pkmnFolderPath, frameNum, pkmnLower, (170, 275))
                self.playerActiveSprite = pygame.sprite.Group(spriteInit)

                self.player = Player(self.playerActivePkmn, self.party, self.cpuActivePkmn, BattleSimulator.POKEMON_DICT, BattleSimulator.MOVES_DICT)
                break
        if index != 6:
            for j in range(index, 6):
                if self.party[j] != None:
                    self.party[j].activeFalse()

        # FOLDERS AND FRAMES
        activeName = self.cpuActivePkmn.getName()
        properName = str(activeName).title()
        if properName == "Farfetch'D":
            properName = "Farfetch'd"
        folderPath = "images/pkmn_sprites_front/"
        pkmnLower = str(activeName).lower()
        if pkmnLower == "mr. mime":
            pkmnLower = "mrmime"
        pkmnFolderPath = folderPath + pkmnLower + "/"
        frameNum = BattleSimulator.POKEMON_DICT[properName][9]

        # MAKE SPRITE OBJECTS
        spriteInit = GifSprite(pkmnFolderPath, frameNum, pkmnLower, (460, 140))
        self.cpuActiveSprite = pygame.sprite.Group(spriteInit)

        self.cpuEasy = EasyOpponent(self.playerActivePkmn, self.party, self.cpuActivePkmn, BattleSimulator.POKEMON_DICT, BattleSimulator.MOVES_DICT, self.cpuParty)
        
    #################
    ## GET POKÉMON ##
    #################
    def getPkmn(self, id, pkmn):
        if str(pkmn) == "":
            print("Please enter a valid Pokémon.")
            return
        properName = str(pkmn).title()
        if properName == "Farfetch'D":
            properName = "Farfetch'd"
        validPkmn = properName in BattleSimulator.POKEMON_DICT
        folderPath = "images/pkmn_sprites_front/"
        centerPos = (115, 165)
        if self.selectPokemon1:
            if validPkmn:
                # INITIALIZE POKÉMON
                self.pkmn1 = Pokemon(properName, self.pkmn1Level, self.pkmn1ev, self.pkmn1Moves,
                                     self.pkmn1IsFainted, self.pkmn1StatChanges, self.pkmn1Conditions)
                self.party[0] = self.pkmn1
                self.pkmn1Name = str(self.pkmn1.getName())

                # FOLDERS AND FRAMES
                pkmn1Lower = str(pkmn).lower()
                if pkmn1Lower == "mr. mime":
                    pkmn1Lower = "mrmime"
                pkmnFolderPath = folderPath + pkmn1Lower + "/"
                frameNum = BattleSimulator.POKEMON_DICT[properName][9]

                # MAKE SPRITE OBJECTS
                sprite1 = GifSprite(pkmnFolderPath, frameNum, pkmn1Lower, centerPos)
                self.inputSprite1 = pygame.sprite.Group(sprite1)

                # TYPE IMAGES
                pkmn1Type = self.pkmn1.getType()
                pkmn1Type1Img = pygame.image.load(self.typeIconsList[pkmn1Type[0]])
                self.pkmn1Type1 = pkmn1Type1Img
                if len(pkmn1Type) == 2:
                    pkmn1Type2Img = pygame.image.load(self.typeIconsList[pkmn1Type[1]])
                    self.pkmn1Type2 = pkmn1Type2Img
                self.pkmnTypes[0] = [self.pkmn1Type1, self.pkmn1Type2]
                
                # STATS
                self.pkmn1BattleStats = self.pkmn1.getBattleStats()

            else:
                print("Please enter a valid Pokémon.")

        elif self.selectPokemon2:
            if validPkmn:
                # INITIALIZE POKÉMON
                self.pkmn2 = Pokemon(properName, self.pkmn2Level, self.pkmn2ev, self.pkmn2Moves,
                                     self.pkmn2IsFainted, self.pkmn2StatChanges, self.pkmn2Conditions)
                self.party[1] = self.pkmn2
                self.pkmn2Name = str(self.pkmn2.getName())

                # FOLDERS AND FRAMES
                pkmn2Lower = str(pkmn).lower()
                if pkmn2Lower == "mr. mime":
                    pkmn2Lower = "mrmime"
                pkmnFolderPath = folderPath + pkmn2Lower + "/"
                frameNum = BattleSimulator.POKEMON_DICT[properName][9]

                # MAKE SPRITE OBJECTS
                sprite2 = GifSprite(pkmnFolderPath, frameNum, pkmn2Lower, centerPos)
                self.inputSprite2 = pygame.sprite.Group(sprite2)

                # TYPE IMAGES
                pkmn2Type = self.pkmn2.getType()
                pkmn2Type1Img = pygame.image.load(self.typeIconsList[pkmn2Type[0]])
                self.pkmn2Type1 = pkmn2Type1Img
                if len(pkmn2Type) == 2:
                    pkmn2Type2Img = pygame.image.load(self.typeIconsList[pkmn2Type[1]])
                    self.pkmn2Type2 = pkmn2Type2Img
                self.pkmnTypes[1] = [self.pkmn2Type1, self.pkmn2Type2]
                
                # STATS
                self.pkmn2BattleStats = self.pkmn2.getBattleStats()

            else:
                print("Please enter a valid Pokémon.")

        elif self.selectPokemon3:
            if validPkmn:
                # INITIALIZE POKÉMON
                self.pkmn3 = Pokemon(properName, self.pkmn3Level, self.pkmn3ev, self.pkmn3Moves,
                                     self.pkmn3IsFainted, self.pkmn3StatChanges, self.pkmn3Conditions)
                self.party[2] = self.pkmn3
                self.pkmn3Name = str(self.pkmn3.getName())

                # FOLDERS AND FRAMES
                pkmn3Lower = str(pkmn).lower()
                if pkmn3Lower == "mr. mime":
                    pkmn3Lower = "mrmime"
                pkmnFolderPath = folderPath + pkmn3Lower + "/"
                frameNum = BattleSimulator.POKEMON_DICT[properName][9]

                # MAKE SPRITE OBJECTS
                sprite3 = GifSprite(pkmnFolderPath, frameNum, pkmn3Lower, centerPos)
                self.inputSprite3 = pygame.sprite.Group(sprite3)

                # TYPE IMAGES
                pkmn3Type = self.pkmn3.getType()
                pkmn3Type1Img = pygame.image.load(self.typeIconsList[pkmn3Type[0]])
                self.pkmn3Type1 = pkmn3Type1Img
                if len(pkmn3Type) == 2:
                    pkmn3Type2Img = pygame.image.load(self.typeIconsList[pkmn3Type[1]])
                    self.pkmn3Type2 = pkmn3Type2Img
                self.pkmnTypes[2] = [self.pkmn3Type1, self.pkmn3Type2]
                
                # STATS
                self.pkmn3BattleStats = self.pkmn3.getBattleStats()

            else:
                print("Please enter a valid Pokémon.")

        elif self.selectPokemon4:
            if validPkmn:
                # INITIALIZE POKÉMON
                self.pkmn4 = Pokemon(properName, self.pkmn4Level, self.pkmn4ev, self.pkmn4Moves,
                                     self.pkmn4IsFainted, self.pkmn4StatChanges, self.pkmn4Conditions)
                self.party[3] = self.pkmn4
                self.pkmn4Name = str(self.pkmn4.getName())

                # FOLDERS AND FRAMES
                pkmn4Lower = str(pkmn).lower()
                if pkmn4Lower == "mr. mime":
                    pkmn4Lower = "mrmime"
                pkmnFolderPath = folderPath + pkmn4Lower + "/"
                frameNum = BattleSimulator.POKEMON_DICT[properName][9]

                # MAKE SPRITE OBJECTS
                sprite4 = GifSprite(pkmnFolderPath, frameNum, pkmn4Lower, centerPos)
                self.inputSprite4 = pygame.sprite.Group(sprite4)

                # TYPE IMAGES
                pkmn4Type = self.pkmn4.getType()
                pkmn4Type1Img = pygame.image.load(self.typeIconsList[pkmn4Type[0]])
                self.pkmn4Type1 = pkmn4Type1Img
                if len(pkmn4Type) == 2:
                    pkmn4Type2Img = pygame.image.load(self.typeIconsList[pkmn4Type[1]])
                    self.pkmn4Type2 = pkmn4Type2Img
                self.pkmnTypes[3] = [self.pkmn4Type1, self.pkmn4Type2]
                
                # STATS
                self.pkmn4BattleStats = self.pkmn4.getBattleStats()

            else:
                print("Please enter a valid Pokémon.")

        elif self.selectPokemon5:
            if validPkmn:
                # INITIALIZE POKÉMON
                self.pkmn5 = Pokemon(properName, self.pkmn5Level, self.pkmn5ev, self.pkmn5Moves,
                                     self.pkmn5IsFainted, self.pkmn5StatChanges, self.pkmn5Conditions)
                self.party[4] = self.pkmn5
                self.pkmn5Name = str(self.pkmn5.getName())

                # FOLDERS AND FRAMES
                pkmn5Lower = str(pkmn).lower()
                if pkmn5Lower == "mr. mime":
                    pkmn5Lower = "mrmime"
                pkmnFolderPath = folderPath + pkmn5Lower + "/"
                frameNum = BattleSimulator.POKEMON_DICT[properName][9]

                # MAKE SPRITE OBJECTS
                sprite5 = GifSprite(pkmnFolderPath, frameNum, pkmn5Lower, centerPos)
                self.inputSprite5 = pygame.sprite.Group(sprite5)

                # TYPE IMAGES
                pkmn5Type = self.pkmn5.getType()
                pkmn5Type1Img = pygame.image.load(self.typeIconsList[pkmn5Type[0]])
                self.pkmn5Type1 = pkmn5Type1Img
                if len(pkmn5Type) == 2:
                    pkmn5Type2Img = pygame.image.load(self.typeIconsList[pkmn5Type[1]])
                    self.pkmn5Type2 = pkmn5Type2Img
                self.pkmnTypes[4] = [self.pkmn5Type1, self.pkmn5Type2]
                
                # STATS
                self.pkmn5BattleStats = self.pkmn5.getBattleStats()

            else:
                print("Please enter a valid Pokémon.")

        elif self.selectPokemon6:
            if validPkmn:
                # INITIALIZE POKÉMON
                self.pkmn6 = Pokemon(properName, self.pkmn6Level, self.pkmn6ev, self.pkmn6Moves,
                                     self.pkmn6IsFainted, self.pkmn6StatChanges, self.pkmn6Conditions)
                self.party[5] = self.pkmn6
                self.pkmn6Name = str(self.pkmn6.getName())

                # FOLDERS AND FRAMES
                pkmn6Lower = str(pkmn).lower()
                if pkmn6Lower == "mr. mime":
                    pkmn6Lower = "mrmime"
                pkmnFolderPath = folderPath + pkmn6Lower + "/"
                frameNum = BattleSimulator.POKEMON_DICT[properName][9]

                # MAKE SPRITE OBJECTS
                sprite6 = GifSprite(pkmnFolderPath, frameNum, pkmn6Lower, centerPos)
                self.inputSprite6 = pygame.sprite.Group(sprite6)

                # TYPE IMAGES
                pkmn6Type = self.pkmn6.getType()
                pkmn6Type1Img = pygame.image.load(self.typeIconsList[pkmn6Type[0]])
                self.pkmn6Type1 = pkmn6Type1Img
                if len(pkmn6Type) == 2:
                    pkmn6Type2Img = pygame.image.load(self.typeIconsList[pkmn6Type[1]])
                    self.pkmn6Type2 = pkmn6Type2Img
                self.pkmnTypes[5] = [self.pkmn6Type1, self.pkmn6Type2]

                # STATS
                self.pkmn6BattleStats = self.pkmn6.getBattleStats()

            else:
                print("Please enter a valid Pokémon.")
        
        # set first pkmn inputted as the active pkmn
        self.initializeActive()

        # count current party size
        self.partySize = 0
        for i in self.party:
            if i != None:
                self.partySize += 1
        print(self.partySize)

    ###############
    ## GET LEVEL ##
    ###############
    def getLevel(self, id, lvl):
        isValid = str(lvl) == "" or (not str(lvl).isdigit())
        if isValid:
            print("Please enter a valid level.")
            return
        elif int(lvl) > 100 or int(lvl) < 1:
            print("Please enter a valid level.")
        elif self.selectPokemon1:
            if self.pkmn1 == None:
                print("First, please enter a valid Pokémon.")
            else:
                self.pkmn1Level = int(lvl)
                self.pkmn1.changeLevel(self.pkmn1Level)
                self.pkmn1BattleStats = self.pkmn1.getBattleStats()

        elif self.selectPokemon2:
            if self.pkmn2 == None:
                print("First, please enter a valid Pokémon.")
            else:
                self.pkmn2Level = int(lvl)
                self.pkmn2.changeLevel(self.pkmn2Level)
                self.pkmn2BattleStats = self.pkmn2.getBattleStats()

        elif self.selectPokemon3:
            if self.pkmn3 == None:
                print("First, please enter a valid Pokémon.")
            else:
                self.pkmn3Level = int(lvl)
                self.pkmn3.changeLevel(self.pkmn3Level)
                self.pkmn3BattleStats = self.pkmn3.getBattleStats()

        elif self.selectPokemon4:
            if self.pkmn4 == None:
                print("First, please enter a valid Pokémon.")
            else:
                self.pkmn4Level = int(lvl)
                self.pkmn4.changeLevel(self.pkmn4Level)
                self.pkmn4BattleStats = self.pkmn4.getBattleStats()

        elif self.selectPokemon5:
            if self.pkmn5 == None:
                print("First, please enter a valid Pokémon.")
            else:
                self.pkmn5Level = int(lvl)
                self.pkmn5.changeLevel(self.pkmn5Level)
                self.pkmn5BattleStats = self.pkmn5.getBattleStats()

        elif self.selectPokemon6:
            if self.pkmn6 == None:
                print("First, please enter a valid Pokémon.")
            else:
                self.pkmn6Level = int(lvl)
                self.pkmn6.changeLevel(self.pkmn6Level)
                self.pkmn6BattleStats = self.pkmn6.getBattleStats()

    ###############
    ## GET MOVES ##
    ###############
    def getMove(self, id, move):
        properName = str(move).title()
        inMoves = properName in BattleSimulator.MOVES_DICT
        if str(move) == "" or (not inMoves):
            print("Please enter a valid move.")
            return
        elif self.selectPokemon1:
            if self.pkmn1 == None:
                print("First, please enter a valid Pokémon.")
            else:
                validMoves = BattleSimulator.POKEMON_DICT[self.pkmn1Name.title()][11]
                validMoves = [x.strip() for x in validMoves.split(",")]
                if properName in validMoves:
                    moveInfo = BattleSimulator.MOVES_DICT[properName]
                    currentMove = Move(properName, moveInfo[0], moveInfo[1], moveInfo[2], moveInfo[3], moveInfo[4],
                                       moveInfo[5], moveInfo[6])
                    if currentMove not in self.pkmn1Moves:
                        if self.inputPkmn1Move1.isActive(): # check if move 1 text box is the one you're typing into
                            self.pkmn1Move1 = currentMove
                            self.pkmn1Moves[0] = self.pkmn1Move1
                        elif self.inputPkmn1Move2.isActive():
                            self.pkmn1Move2 = currentMove
                            self.pkmn1Moves[1] = self.pkmn1Move2
                        elif self.inputPkmn1Move3.isActive():
                            self.pkmn1Move3 = currentMove
                            self.pkmn1Moves[2] = self.pkmn1Move3
                        elif self.inputPkmn1Move4.isActive():
                            self.pkmn1Move4 = currentMove
                            self.pkmn1Moves[3] = self.pkmn1Move4
                    else:
                        print("Please enter a move that you have not already inputted.")

        elif self.selectPokemon2:
            if self.pkmn2 == None:
                print("First, please enter a valid Pokémon.")
            else:
                validMoves = BattleSimulator.POKEMON_DICT[self.pkmn2Name.title()][11]
                validMoves = [x.strip() for x in validMoves.split(",")]
                if properName in validMoves:
                    moveInfo = BattleSimulator.MOVES_DICT[properName]
                    currentMove = Move(properName, moveInfo[0], moveInfo[1], moveInfo[2], moveInfo[3], moveInfo[4],
                                       moveInfo[5], moveInfo[6])
                    if currentMove not in self.pkmn2Moves:
                        if self.inputPkmn2Move1.isActive(): # check if move 1 text box is the one you're typing into
                            self.pkmn2Move1 = currentMove
                            self.pkmn2Moves[0] = self.pkmn2Move1
                        elif self.inputPkmn2Move2.isActive():
                            self.pkmn2Move2 = currentMove
                            self.pkmn2Moves[1] = self.pkmn2Move2
                        elif self.inputPkmn2Move3.isActive():
                            self.pkmn2Move3 = currentMove
                            self.pkmn2Moves[2] = self.pkmn2Move3
                        elif self.inputPkmn2Move4.isActive():
                            self.pkmn2Move4 = currentMove
                            self.pkmn2Moves[3] = self.pkmn2Move4
                    else:
                        print("Please enter a move that you have not already inputted.")

        elif self.selectPokemon3:
            if self.pkmn3 == None:
                print("First, please enter a valid Pokémon.")
            else:
                validMoves = BattleSimulator.POKEMON_DICT[self.pkmn3Name.title()][11]
                validMoves = [x.strip() for x in validMoves.split(",")]
                if properName in validMoves:
                    moveInfo = BattleSimulator.MOVES_DICT[properName]
                    currentMove = Move(properName, moveInfo[0], moveInfo[1], moveInfo[2], moveInfo[3], moveInfo[4],
                                       moveInfo[5], moveInfo[6])
                    if currentMove not in self.pkmn3Moves:
                        if self.inputPkmn3Move1.isActive(): # check if move 1 text box is the one you're typing into
                            self.pkmn3Move1 = currentMove
                            self.pkmn3Moves[0] = self.pkmn3Move1
                        elif self.inputPkmn3Move2.isActive():
                            self.pkmn3Move2 = currentMove
                            self.pkmn3Moves[1] = self.pkmn3Move2
                        elif self.inputPkmn3Move3.isActive():
                            self.pkmn3Move3 = currentMove
                            self.pkmn3Moves[2] = self.pkmn3Move3
                        elif self.inputPkmn3Move4.isActive():
                            self.pkmn3Move4 = currentMove
                            self.pkmn3Moves[3] = self.pkmn3Move4
                    else:
                        print("Please enter a move that you have not already inputted.")

        elif self.selectPokemon4:
            if self.pkmn4 == None:
                print("First, please enter a valid Pokémon.")
            else:
                validMoves = BattleSimulator.POKEMON_DICT[self.pkmn4Name.title()][11]
                validMoves = [x.strip() for x in validMoves.split(",")]
                if properName in validMoves:
                    moveInfo = BattleSimulator.MOVES_DICT[properName]
                    currentMove = Move(properName, moveInfo[0], moveInfo[1], moveInfo[2], moveInfo[3], moveInfo[4],
                                       moveInfo[5], moveInfo[6])
                    if currentMove not in self.pkmn4Moves:
                        if self.inputPkmn4Move1.isActive(): # check if move 1 text box is the one you're typing into
                            self.pkmn4Move1 = currentMove
                            self.pkmn4Moves[0] = self.pkmn4Move1
                        elif self.inputPkmn4Move2.isActive():
                            self.pkmn4Move2 = currentMove
                            self.pkmn4Moves[1] = self.pkmn4Move2
                        elif self.inputPkmn4Move3.isActive():
                            self.pkmn4Move3 = currentMove
                            self.pkmn4Moves[2] = self.pkmn4Move3
                        elif self.inputPkmn4Move4.isActive():
                            self.pkmn4Move4 = currentMove
                            self.pkmn4Moves[3] = self.pkmn4Move4
                    else:
                        print("Please enter a move that you have not already inputted.")

        elif self.selectPokemon5:
            if self.pkmn5 == None:
                print("First, please enter a valid Pokémon.")
            else:
                validMoves = BattleSimulator.POKEMON_DICT[self.pkmn5Name.title()][11]
                validMoves = [x.strip() for x in validMoves.split(",")]
                if properName in validMoves:
                    moveInfo = BattleSimulator.MOVES_DICT[properName]
                    currentMove = Move(properName, moveInfo[0], moveInfo[1], moveInfo[2], moveInfo[3], moveInfo[4],
                                       moveInfo[5], moveInfo[6])
                    if currentMove not in self.pkmn5Moves:
                        if self.inputPkmn5Move1.isActive(): # check if move 1 text box is the one you're typing into
                            self.pkmn5Move1 = currentMove
                            self.pkmn5Moves[0] = self.pkmn5Move1
                        elif self.inputPkmn5Move2.isActive():
                            self.pkmn5Move2 = currentMove
                            self.pkmn5Moves[1] = self.pkmn5Move2
                        elif self.inputPkmn5Move3.isActive():
                            self.pkmn5Move3 = currentMove
                            self.pkmn5Moves[2] = self.pkmn5Move3
                        elif self.inputPkmn5Move4.isActive():
                            self.pkmn5Move4 = currentMove
                            self.pkmn5Moves[3] = self.pkmn5Move4
                    else:
                        print("Please enter a move that you have not already inputted.")

        elif self.selectPokemon6:
            if self.pkmn6 == None:
                print("First, please enter a valid Pokémon.")
            else:
                validMoves = BattleSimulator.POKEMON_DICT[self.pkmn6Name.title()][11]
                validMoves = [x.strip() for x in validMoves.split(",")]
                if properName in validMoves:
                    moveInfo = BattleSimulator.MOVES_DICT[properName]
                    currentMove = Move(properName, moveInfo[0], moveInfo[1], moveInfo[2], moveInfo[3], moveInfo[4],
                                       moveInfo[5], moveInfo[6])
                    if currentMove not in self.pkmn6Moves:
                        if self.inputPkmn6Move1.isActive(): # check if move 1 text box is the one you're typing into
                            self.pkmn6Move1 = currentMove
                            self.pkmn6Moves[0] = self.pkmn6Move1
                        elif self.inputPkmn6Move2.isActive():
                            self.pkmn6Move2 = currentMove
                            self.pkmn6Moves[1] = self.pkmn6Move2
                        elif self.inputPkmn6Move3.isActive():
                            self.pkmn6Move3 = currentMove
                            self.pkmn6Moves[2] = self.pkmn6Move3
                        elif self.inputPkmn6Move4.isActive():
                            self.pkmn6Move4 = currentMove
                            self.pkmn6Moves[3] = self.pkmn6Move4
                    else:
                        print("Please enter a move that you have not already inputted.")

    #############
    ## GET EVs ##
    #############
    def getEV(self, id, ev):
        isValid = str(ev).isdigit() and (int(ev) < 253)
        if not isValid:
            print("Please enter a valid EV value.")
            return
        currentEV = int(ev)
        currTotalEV = 0
        if self.selectPokemon1:
            # validity checks
            if self.pkmn1 == None:
                print("First, please enter a valid Pokémon.")
                return
            for value in self.pkmn1ev:
                currTotalEV += value
            isOver = (currTotalEV + currentEV) > 508
            if isOver:
                print("You cannot have over 508 total EVs.")
                return
            # EV inputs
            for index in range(0, 6):
                if self.inputEV1List[index].isActive():
                    self.pkmn1ev[index] = currentEV
                    break
            self.pkmn1BattleStats = self.pkmn1.getBattleStats()
        elif self.selectPokemon2:
            # validity checks
            if self.pkmn2 == None:
                print("First, please enter a valid Pokémon.")
                return
            for value in self.pkmn2ev:
                currTotalEV += value
            isOver = (currTotalEV + currentEV) > 508
            if isOver:
                print("You cannot have over 508 total EVs.")
                return
            # EV inputs
            for index in range(0, 6):
                if self.inputEV2List[index].isActive():
                    self.pkmn2ev[index] = currentEV
                    break
            self.pkmn2BattleStats = self.pkmn2.getBattleStats()
        elif self.selectPokemon3:
            # validity checks
            if self.pkmn3 == None:
                print("First, please enter a valid Pokémon.")
                return
            for value in self.pkmn3ev:
                currTotalEV += value
            isOver = (currTotalEV + currentEV) > 508
            if isOver:
                print("You cannot have over 508 total EVs.")
                return
            # EV inputs
            for index in range(0, 6):
                if self.inputEV3List[index].isActive():
                    self.pkmn3ev[index] = currentEV
                    break
            self.pkmn3BattleStats = self.pkmn3.getBattleStats()
        elif self.selectPokemon4:
            # validity checks
            if self.pkmn4 == None:
                print("First, please enter a valid Pokémon.")
                return
            for value in self.pkmn4ev:
                currTotalEV += value
            isOver = (currTotalEV + currentEV) > 508
            if isOver:
                print("You cannot have over 508 total EVs.")
                return
            # EV inputs
            for index in range(0, 6):
                if self.inputEV4List[index].isActive():
                    self.pkmn4ev[index] = currentEV
                    break
            self.pkmn4BattleStats = self.pkmn4.getBattleStats()
        elif self.selectPokemon5:
            # validity checks
            if self.pkmn5 == None:
                print("First, please enter a valid Pokémon.")
                return
            for value in self.pkmn5ev:
                currTotalEV += value
            isOver = (currTotalEV + currentEV) > 508
            if isOver:
                print("You cannot have over 508 total EVs.")
                return
            # EV inputs
            for index in range(0, 6):
                if self.inputEV5List[index].isActive():
                    self.pkmn5ev[index] = currentEV
                    break
            self.pkmn5BattleStats = self.pkmn5.getBattleStats()
        elif self.selectPokemon6:
            # validity checks
            if self.pkmn6 == None:
                print("First, please enter a valid Pokémon.")
                return
            for value in self.pkmn6ev:
                currTotalEV += value
            isOver = (currTotalEV + currentEV) > 508
            if isOver:
                print("You cannot have over 508 total EVs.")
                return
            # EV inputs
            for index in range(0, 6):
                if self.inputEV6List[index].isActive():
                    self.pkmn6ev[index] = currentEV
                    break
            self.pkmn6BattleStats = self.pkmn6.getBattleStats()

    ########################
    ## UPDATE ACTIVE PKMN ##
    ########################
    def updateActivePkmn(self, formerActive, currentActive):
        currentActive.activeTrue()
        formerActive.activeFalse()
        self.playerActivePkmn = currentActive
        self.plyrCrrActive = currentActive
        # FOLDERS AND FRAMES
        activeName = self.playerActivePkmn.getName()
        properName = str(activeName).title()
        if properName == "Farfetch'D":
            properName = "Farfetch'd"
        folderPath = "images/pkmn_sprites_back/"
        pkmnLower = str(activeName).lower()
        if pkmnLower == "mr. mime":
            pkmnLower = "mrmime"
        pkmnFolderPath = folderPath + pkmnLower + "/"
        frameNum = BattleSimulator.POKEMON_DICT[properName][10]

        # MAKE SPRITE OBJECTS
        spriteInit = GifSprite(pkmnFolderPath, frameNum, pkmnLower, (170, 275))
        self.playerActiveSprite = pygame.sprite.Group(spriteInit)

        self.player = Player(self.playerActivePkmn, self.party, self.cpuActivePkmn, BattleSimulator.POKEMON_DICT, BattleSimulator.MOVES_DICT)

    ################
    ## CPU SWITCH ##
    ################
    def cpuSwitch(self):
        if self.cpuEasy.switchOut() != 0:
            return self.cpuEasy.switchOut()
        else:
            self.gameOver = True
            self.playerWon = True
            self.battleScreen = False
            return None

    #####################################
    ## STAT/COND. CHANGES DUE TO MOVES ##
    #####################################
    def getMoveStatChanges(self, effects):
        for plyrChange in range(1, len(effects[0])):
            if effects[0][plyrChange] != 0:
                self.playerActivePkmn.changeStats(plyrChange, effects[0][plyrChange])
        for cpuChange in range(1, len(effects[1])):
            if effects[1][cpuChange] != 0:
                print("here")
                self.cpuActivePkmn.changeStats(cpuChange, effects[1][cpuChange])
        for plyrChange in range(0, len(effects[2])):
            if effects[2][plyrChange] != False:
                self.playerActivePkmn.changeConditions(plyrChange)
        for cpuChange in range(0, len(effects[3])):
            if effects[3][cpuChange] != False:
                self.cpuActivePkmn.changeConditions(cpuChange)

    ##########
    ## TURN ##
    ##########
    def turn(self):
        self.cpuUsedMove = self.cpuEasy.useMove() # initialize cpu move
        plyrSpeed = self.playerActivePkmn.getBattleStats()[5] # player speed
        cpuSpeed = self.cpuActivePkmn.getBattleStats()[5] # cpu speed

        isPlayerBurned = self.playerActivePkmn.getConditions()[0]
        isCPUBurned = self.cpuActivePkmn.getConditions()[0]

        isPlayerPoisoned = self.playerActivePkmn.getConditions()[2]
        isCPUPoisoned = self.cpuActivePkmn.getConditions()[2]

        # if a pokemon are paralyzed, cut its speed in half.
        if self.playerActivePkmn.getConditions()[1]:
            plyrSpeed //= 2
        if self.cpuActivePkmn.getConditions()[1]:
            cpuSpeed //= 2
        
        if self.cpuActivePkmn != None and self.playerActivePkmn != None:
            if cpuSpeed > plyrSpeed: # if opposing pkmn is faster than plyr pkmn
                # check if move will faint the plyr pkmn
                hpLeft = self.playerActivePkmn.getBattleStats()[0] - self.playerActivePkmn.getStatChanges()[0]

                # if move from cpu WILL NOT KO:
                if self.cpuUsedMove[0] < hpLeft:
                    self.playerActivePkmn.changeHP(self.cpuUsedMove[0])
                    hpLeft = self.cpuActivePkmn.getBattleStats()[0] - self.cpuActivePkmn.getStatChanges()[0]
                    if self.plyrUsedMove[0] < hpLeft:
                        self.cpuActivePkmn.changeHP(self.plyrUsedMove[0])
                    else:
                        self.plyrUsedMove[0] = hpLeft
                        self.cpuActivePkmn.changeHP(self.plyrUsedMove[0])
                        self.cpuActivePkmn.changeToFainted()
                        self.cpuFainted.append(self.cpuActivePkmn)
                        self.cpuActivePkmn = self.cpuSwitch()
                        if self.cpuActivePkmn != None:
                            self.player.updateOppActive(self.cpuActivePkmn)
                            self.cpuActiveSprite = self.cpuEasy.updateCPUSprite(self.cpuActivePkmn, BattleSimulator.POKEMON_DICT)

                # if move from cpu WILL KO:
                else:
                    self.cpuUsedMove[0] = hpLeft
                    self.playerActivePkmn.changeHP(self.cpuUsedMove[0])
                    self.playerActivePkmn.changeToFainted()
                    self.playerFainted.append(self.playerActivePkmn)
                    self.plyrJustFainted = True
            elif plyrSpeed > cpuSpeed: # if plyr pkmn is faster than opposing pkmn
                hpLeft = self.cpuActivePkmn.getBattleStats()[0] - self.cpuActivePkmn.getStatChanges()[0]
                # if move from plyr WILL NOT KO
                if self.plyrUsedMove[0] < hpLeft:
                    self.cpuActivePkmn.changeHP(self.plyrUsedMove[0])
                    # self.getMoveStatChanges(effects)
                    hpLeft = self.playerActivePkmn.getBattleStats()[0] - self.playerActivePkmn.getStatChanges()[0]
                    if self.cpuUsedMove[0] < hpLeft:
                        self.playerActivePkmn.changeHP(self.cpuUsedMove[0])
                    else:
                        self.cpuUsedMove[0] = hpLeft
                        self.playerActivePkmn.changeHP(self.cpuUsedMove[0])
                        self.playerActivePkmn.changeToFainted()
                        self.playerFainted.append(self.playerActivePkmn)
                        self.plyrJustFainted = True
                # if move from plyr WILL KO
                else:
                    self.plyrUsedMove[0] = hpLeft
                    self.cpuActivePkmn.changeHP(self.plyrUsedMove[0])
                    self.cpuActivePkmn.changeToFainted()
                    self.cpuFainted.append(self.cpuActivePkmn)
                    self.cpuActivePkmn = self.cpuSwitch()
                    if self.cpuActivePkmn != None:
                        self.player.updateOppActive(self.cpuActivePkmn)
                        self.cpuActiveSprite = self.cpuEasy.updateCPUSprite(self.cpuActivePkmn, BattleSimulator.POKEMON_DICT)
            else: # if speed tie
                speedTie = random.randint(0, 1)
                if speedTie == 0:
                    hpLeft = self.playerActivePkmn.getBattleStats()[0] - self.playerActivePkmn.getStatChanges()[0]
                    if self.cpuUsedMove[0] < hpLeft:
                        self.playerActivePkmn.changeHP(self.cpuUsedMove[0])
                    else:
                        self.cpuUsedMove[0] = hpLeft
                        self.playerActivePkmn.changeHP(self.cpuUsedMove[0])
                        self.playerActivePkmn.changeToFainted()
                        self.playerFainted.append(self.playerActivePkmn)
                        self.plyrJustFainted = True
                else:
                    hpLeft = self.cpuActivePkmn.getBattleStats()[0] - self.cpuActivePkmn.getStatChanges()[0]
                    if self.plyrUsedMove[0] < hpLeft:
                        self.cpuActivePkmn.changeHP(self.plyrUsedMove[0])
                    else:
                        self.plyrUsedMove[0] = hpLeft
                        self.cpuActivePkmn.changeHP(self.plyrUsedMove[0])
                        self.cpuActivePkmn.changeToFainted()
                        self.cpuFainted.append(self.cpuActivePkmn)
                        self.cpuActivePkmn = self.cpuSwitch()
                        if self.cpuActivePkmn != None:
                            self.player.updateOppActive(self.cpuActivePkmn)
                            self.cpuActiveSprite = self.cpuEasy.updateCPUSprite(self.cpuActivePkmn, BattleSimulator.POKEMON_DICT)
        
        # BURN MECHANICS: LOSE 1/16 OF HP AT END OF TURN
        if isPlayerBurned:
            hpLeft = self.playerActivePkmn.getBattleStats()[0] - self.playerActivePkmn.getStatChanges()[0]
            damageDealt = self.playerActivePkmn.getBattleStats()[0] // 16
            if hpLeft < damageDealt:
                damageDealt = hpLeft
                self.playerActivePkmn.changeHP(damageDealt)
                self.playerActivePkmn.changeToFainted()
                self.playerFainted.append(self.playerActivePkmn)
                self.plyrJustFainted = True
            else:
                self.playerActivePkmn.changeHP(damageDealt)
                print("%s was hurt by its burn!") % (self.playerActivePkmn)
        if isCPUBurned:
            hpLeft = self.cpuActivePkmn.getBattleStats()[0] - self.cpuActivePkmn.getStatChanges()[0]
            damageDealt = self.cpuActivePkmn.getBattleStats()[0] // 16
            if hpLeft < damageDealt:
                damageDealt = hpLeft
                self.cpuActivePkmn.changeHP(damageDealt)
                self.cpuActivePkmn.changeToFainted()
                self.cpuFainted.append(self.cpuActivePkmn)
                self.cpuActivePkmn = self.cpuSwitch()
                if self.cpuActivePkmn != None:
                    self.player.updateOppActive(self.cpuActivePkmn)
                    self.cpuActiveSprite = self.cpuEasy.updateCPUSprite(self.cpuActivePkmn, BattleSimulator.POKEMON_DICT)
            else:
                self.cpuActivePkmn.changeHP(damageDealt)
                print("%s was hurt by its burn!") % (self.cpuActivePkmn)
        
        # POISON MECHANICS: LOSE 1/8 OF HP AT END OF TURN
        if isPlayerPoisoned:
            hpLeft = self.playerActivePkmn.getBattleStats()[0] - self.playerActivePkmn.getStatChanges()[0]
            damageDealt = self.playerActivePkmn.getBattleStats()[0] // 8
            if hpLeft < damageDealt:
                damageDealt = hpLeft
                self.playerActivePkmn.changeHP(damageDealt)
                self.playerActivePkmn.changeToFainted()
                self.playerFainted.append(self.playerActivePkmn)
                self.plyrJustFainted = True
            else:
                self.playerActivePkmn.changeHP(damageDealt)
                msg = ("%s was hurt by its burn!") % (self.playerActivePkmn)
                print(msg)
        if isCPUPoisoned:
            hpLeft = self.cpuActivePkmn.getBattleStats()[0] - self.cpuActivePkmn.getStatChanges()[0]
            damageDealt = self.cpuActivePkmn.getBattleStats()[0] // 8
            if hpLeft < damageDealt:
                damageDealt = hpLeft
                self.cpuActivePkmn.changeHP(damageDealt)
                self.cpuActivePkmn.changeToFainted()
                self.cpuFainted.append(self.cpuActivePkmn)
                self.cpuActivePkmn = self.cpuSwitch()
                if self.cpuActivePkmn != None:
                    self.player.updateOppActive(self.cpuActivePkmn)
                    self.cpuActiveSprite = self.cpuEasy.updateCPUSprite(self.cpuActivePkmn, BattleSimulator.POKEMON_DICT)
            else:
                self.cpuActivePkmn.changeHP(damageDealt)
                msg = ("%s was hurt by its burn!") % (self.cpuActivePkmn)
                print(msg)
        if len(self.playerFainted) == self.partySize:
            self.gameOver = True
            self.cpuWon = True
            self.battleScreen = False


    #####################
    ## SWITCH OUT TURN ##
    #####################
    def switchTurn(self):
        self.cpuUsedMove = self.cpuEasy.useMove() # initialize cpu move
        hpLeft = self.playerActivePkmn.getBattleStats()[0] - self.playerActivePkmn.getStatChanges()[0]
        if self.cpuUsedMove[0] < hpLeft:
            self.playerActivePkmn.getStatChanges()[0] += self.cpuUsedMove[0]
        else:
            self.cpuUsedMove[0] = hpLeft
            self.playerActivePkmn.getStatChanges()[0] += self.cpuUsedMove[0]
            self.playerActivePkmn.changeToFainted()
            self.playerFainted.append(self.playerActivePkmn)
            self.plyrJustFainted = True

    ###############
    ## RESET ALL ##
    ###############
    def clearAll(self):
        # 1
        self.pkmn1 = None
        self.pkmn1Type1 = None
        self.pkmn1Type2 = None
        self.party[0] = None
        self.pkmn1Move1 = None
        self.pkmn1Move2 = None
        self.pkmn1Move3 = None
        self.pkmn1Move4 = None
        self.pkmn1Moves = [None, None, None, None]
        self.pkmn1ev = [0, 0, 0, 0, 0, 0]

        # text input
        for txt in self.input1List:
            txt.change_ClearOnClear()
        for ev in self.inputEV1List:
            ev.change_ClearOnClear()

        # select screen box
        self.selectBox1 = Box(self.pkmn1, self.pkmn1Type1, self.pkmn1Type2, (610, 14), (280, 92))

        # 2
        self.pkmn2 = None
        self.pkmn2Type1 = None
        self.pkmn2Type2 = None
        self.party[1] = None
        self.pkmn2Move1 = None
        self.pkmn2Move2 = None
        self.pkmn2Move3 = None
        self.pkmn2Move4 = None
        self.pkmn2ev = [0, 0, 0, 0, 0, 0]

        # text input
        for txt in self.input2List:
            txt.change_ClearOnClear()
        for ev in self.inputEV2List:
            ev.change_ClearOnClear()

        # select screen box
        self.selectBox2 = Box(self.pkmn2, self.pkmn2Type1, self.pkmn2Type2, (610, 120), (280, 92))

        # 3
        self.pkmn3 = None
        self.pkmn3Type1 = None
        self.pkmn3Type2 = None
        self.party[2] = None
        self.pkmn3Move2 = None
        self.pkmn3Move3 = None
        self.pkmn3Move4 = None
        self.pkmn3Moves = [None, None, None, None]
        self.pkmn3ev = [0, 0, 0, 0, 0, 0]

        # text input
        for txt in self.input3List:
            txt.change_ClearOnClear()
        for ev in self.inputEV3List:
            ev.change_ClearOnClear()

        # select screen box
        self.selectBox3 = Box(self.pkmn3, self.pkmn3Type1, self.pkmn3Type2, (610, 226), (280, 92))

        # 4
        self.pkmn4 = None
        self.pkmn4Type1 = None
        self.pkmn4Type2 = None
        self.party[3] = None
        self.pkmn4Move2 = None
        self.pkmn4Move3 = None
        self.pkmn4Move4 = None
        self.pkmn4Moves = [None, None, None, None]
        self.pkmn4ev = [0, 0, 0, 0, 0, 0]

        # text input
        for txt in self.input4List:
            txt.change_ClearOnClear()
        for ev in self.inputEV4List:
            ev.change_ClearOnClear()

        # select screen box
        self.selectBox4 = Box(self.pkmn4, self.pkmn4Type1, self.pkmn4Type2, (610, 332), (280, 92))

        # 5
        self.pkmn5 = None
        self.pkmn5Type1 = None
        self.pkmn5Type2 = None
        self.party[4] = None
        self.pkmn5Move2 = None
        self.pkmn5Move3 = None
        self.pkmn5Move4 = None
        self.pkmn5Moves = [None, None, None, None]
        self.pkmn5ev = [0, 0, 0, 0, 0, 0]

        # text input
        for txt in self.input5List:
            txt.change_ClearOnClear()
        for ev in self.inputEV5List:
            ev.change_ClearOnClear()

        # select screen box
        self.selectBox5 = Box(self.pkmn5, self.pkmn5Type1, self.pkmn5Type2, (610, 438), (280, 92))

        # 6
        self.pkmn6 = None
        self.pkmn6Type1 = None
        self.pkmn6Type2 = None
        self.party[5] = None
        self.pkmn6Move2 = None
        self.pkmn6Move3 = None
        self.pkmn6Move4 = None
        self.pkmn6Moves = [None, None, None, None]
        self.pkmn6ev = [0, 0, 0, 0, 0, 0]

        # text input
        for txt in self.input6List:
            txt.change_ClearOnClear()
        for ev in self.inputEV6List:
            ev.change_ClearOnClear()

        # select screen box
        self.selectBox6 = Box(self.pkmn6, self.pkmn6Type1, self.pkmn6Type2, (610, 544), (280, 92))

    ###################
    ## MOUSE PRESSED ##
    ###################
    def mousePressed(self, x, y):
        ## TITLE SCREEN
        if self.titleCard == True:
            lowerXBound = pygame.mouse.get_pos()[0] > self.centerX - 125
            upperXBound = pygame.mouse.get_pos()[0] < self.centerX + 125
            lowerYBound = pygame.mouse.get_pos()[1] > 362.5
            upperYBound = pygame.mouse.get_pos()[1] < 612.5
            if lowerXBound and upperXBound and lowerYBound and upperYBound:
                self.titleCard = False
                self.selectScreen = True
        
        ## SELECT SCREEN
        elif self.selectScreen == True:
            clickedBack = self.backButton.collidepoint(pygame.mouse.get_pos())
            clearPkmn = self.clearButton.collidepoint(pygame.mouse.get_pos())
            invalidPosBattleSel = self.invalidBattleSel.collidepoint(pygame.mouse.get_pos())
            playGame = self.battleButton.collidepoint(pygame.mouse.get_pos())
            
            # PLAY GAME
            if playGame and not self.selectPokemon1 and not self.selectPokemon2 and not \
            self.selectPokemon3 and not self.selectPokemon4 and not self.selectPokemon5 and not \
            self.selectPokemon6:
                if self.party == [None, None, None, None, None, None]:
                    print("Please add at least one Pokémon to your party.")
                else:
                    self.selectScreen = False
                    self.battleScreen = True
                    self.chooseAction = True

            # BRING UP SELECT POKÉMON BOXES
            if self.boxButton1.collidepoint(pygame.mouse.get_pos()):
                self.selectPokemon1 = True
            elif self.boxButton2.collidepoint(pygame.mouse.get_pos()):
                self.selectPokemon2 = True
            elif self.boxButton3.collidepoint(pygame.mouse.get_pos()):
                self.selectPokemon3 = True
            elif self.boxButton4.collidepoint(pygame.mouse.get_pos()):
                self.selectPokemon4 = True
            elif self.boxButton5.collidepoint(pygame.mouse.get_pos()):
                self.selectPokemon5 = True
            elif self.boxButton6.collidepoint(pygame.mouse.get_pos()):
                self.selectPokemon6 = True
            
            # BACK / CLEAR BUTTONS
            if self.selectPokemon1:
                if invalidPosBattleSel:
                    self.selectPokemon2 = False
                    self.selectPokemon3 = False
                    self.selectPokemon4 = False
                    self.selectPokemon5 = False
                    self.selectPokemon6 = False
                elif clickedBack:
                    self.selectPokemon1 = False
                elif clearPkmn:
                    # self
                    self.pkmn1 = None
                    self.pkmn1Type1 = None
                    self.pkmn1Type2 = None
                    self.party[0] = None
                    self.pkmn1Move1 = None
                    self.pkmn1Move2 = None
                    self.pkmn1Move3 = None
                    self.pkmn1Move4 = None
                    self.pkmn1Moves = [None, None, None, None]
                    self.pkmn1ev = [0, 0, 0, 0, 0, 0]

                    # text input
                    for txt in self.input1List:
                        txt.change_ClearOnClear()
                    for ev in self.inputEV1List:
                        ev.change_ClearOnClear()

                    # select screen box
                    self.selectBox1 = Box(self.pkmn1, self.pkmn1Type1, self.pkmn1Type2, (610, 14), (280, 92))
            
            elif self.selectPokemon2:
                if invalidPosBattleSel:
                    self.selectPokemon1 = False
                    self.selectPokemon3 = False
                    self.selectPokemon4 = False
                    self.selectPokemon5 = False
                    self.selectPokemon6 = False
                elif clickedBack:
                    self.selectPokemon2 = False
                elif clearPkmn:
                    # self
                    self.pkmn2 = None
                    self.pkmn2Type1 = None
                    self.pkmn2Type2 = None
                    self.party[1] = None
                    self.pkmn2Move1 = None
                    self.pkmn2Move2 = None
                    self.pkmn2Move3 = None
                    self.pkmn2Move4 = None
                    self.pkmn2ev = [0, 0, 0, 0, 0, 0]

                    # text input
                    for txt in self.input2List:
                        txt.change_ClearOnClear()
                    for ev in self.inputEV2List:
                        ev.change_ClearOnClear()

                    # select screen box
                    self.selectBox2 = Box(self.pkmn2, self.pkmn2Type1, self.pkmn2Type2, (610, 120), (280, 92))
            
            elif self.selectPokemon3:
                if invalidPosBattleSel:
                    self.selectPokemon1 = False
                    self.selectPokemon2 = False
                    self.selectPokemon4 = False
                    self.selectPokemon5 = False
                    self.selectPokemon6 = False
                elif clickedBack:
                    self.selectPokemon3 = False
                elif clearPkmn:
                    # self
                    self.pkmn3 = None
                    self.pkmn3Type1 = None
                    self.pkmn3Type2 = None
                    self.party[2] = None
                    self.pkmn3Move2 = None
                    self.pkmn3Move3 = None
                    self.pkmn3Move4 = None
                    self.pkmn3Moves = [None, None, None, None]
                    self.pkmn3ev = [0, 0, 0, 0, 0, 0]

                    # text input
                    for txt in self.input3List:
                        txt.change_ClearOnClear()
                    for ev in self.inputEV3List:
                        ev.change_ClearOnClear()

                    # select screen box
                    self.selectBox3 = Box(self.pkmn3, self.pkmn3Type1, self.pkmn3Type2, (610, 226), (280, 92))
            
            elif self.selectPokemon4:
                if invalidPosBattleSel:
                    self.selectPokemon1 = False
                    self.selectPokemon2 = False
                    self.selectPokemon3 = False
                    self.selectPokemon5 = False
                    self.selectPokemon6 = False
                elif clickedBack:
                    self.selectPokemon4 = False
                elif clearPkmn:
                    # self
                    self.pkmn4 = None
                    self.pkmn4Type1 = None
                    self.pkmn4Type2 = None
                    self.party[3] = None
                    self.pkmn4Move2 = None
                    self.pkmn4Move3 = None
                    self.pkmn4Move4 = None
                    self.pkmn4Moves = [None, None, None, None]
                    self.pkmn4ev = [0, 0, 0, 0, 0, 0]

                    # text input
                    for txt in self.input4List:
                        txt.change_ClearOnClear()
                    for ev in self.inputEV4List:
                        ev.change_ClearOnClear()

                    # select screen box
                    self.selectBox4 = Box(self.pkmn4, self.pkmn4Type1, self.pkmn4Type2, (610, 332), (280, 92))
            
            elif self.selectPokemon5:
                if invalidPosBattleSel:
                    self.selectPokemon1 = False
                    self.selectPokemon2 = False
                    self.selectPokemon3 = False
                    self.selectPokemon4 = False
                    self.selectPokemon6 = False
                elif clickedBack:
                    self.selectPokemon5 = False
                elif clearPkmn:
                    # self
                    self.pkmn5 = None
                    self.pkmn5Type1 = None
                    self.pkmn5Type2 = None
                    self.party[4] = None
                    self.pkmn5Move2 = None
                    self.pkmn5Move3 = None
                    self.pkmn5Move4 = None
                    self.pkmn5Moves = [None, None, None, None]
                    self.pkmn5ev = [0, 0, 0, 0, 0, 0]

                    # text input
                    for txt in self.input5List:
                        txt.change_ClearOnClear()
                    for ev in self.inputEV5List:
                        ev.change_ClearOnClear()

                    # select screen box
                    self.selectBox5 = Box(self.pkmn5, self.pkmn5Type1, self.pkmn5Type2, (610, 438), (280, 92))

            elif self.selectPokemon6:
                if invalidPosBattleSel:
                    self.selectPokemon1 = False
                    self.selectPokemon2 = False
                    self.selectPokemon3 = False
                    self.selectPokemon4 = False
                    self.selectPokemon5 = False
                elif clickedBack:
                    self.selectPokemon6 = False
                elif clearPkmn:
                    # self
                    self.pkmn6 = None
                    self.pkmn6Type1 = None
                    self.pkmn6Type2 = None
                    self.party[5] = None
                    self.pkmn6Move2 = None
                    self.pkmn6Move3 = None
                    self.pkmn6Move4 = None
                    self.pkmn6Moves = [None, None, None, None]
                    self.pkmn6ev = [0, 0, 0, 0, 0, 0]

                    # text input
                    for txt in self.input6List:
                        txt.change_ClearOnClear()
                    for ev in self.inputEV6List:
                        ev.change_ClearOnClear()

                    # select screen box
                    self.selectBox6 = Box(self.pkmn6, self.pkmn6Type1, self.pkmn6Type2, (610, 544), (280, 92))
        
        ## BATTLE SCREEN
        elif self.battleScreen == True:
            chooseBattle = self.chooseBattle.collidepoint(pygame.mouse.get_pos())
            chooseRun = self.chooseRun.collidepoint(pygame.mouse.get_pos())
            chooseViewParty = self.chooseViewParty.collidepoint(pygame.mouse.get_pos())
            clickedBack = self.backButton.collidepoint(pygame.mouse.get_pos())
            
            # more party viewing
            if self.viewParty:
                currentActive = None
                for i in self.party:
                    if i != None:
                        if i.getIsActive():
                            currentActive = i
                if clickedBack:
                    self.viewParty = False
                    self.chooseAction = True
                elif self.partyButton1.collidepoint(pygame.mouse.get_pos()):
                    notFainted = self.pkmn1 not in self.playerFainted
                    if self.pkmn1 != self.playerActivePkmn and self.pkmn1 != None and notFainted:
                        self.updateActivePkmn(currentActive, self.pkmn1)
                        self.cpuEasy.updateOppActive(self.playerActivePkmn)
                        self.viewParty = False
                        if not self.plyrJustFainted:
                            self.switchTurn()
                        else:
                            self.plyrJustFainted = False
                    else:
                        print("Please choose a valid Pokémon.")
                elif self.partyButton2.collidepoint(pygame.mouse.get_pos()):
                    notFainted = self.pkmn2 not in self.playerFainted
                    if self.pkmn2 != self.playerActivePkmn and self.pkmn2 != None and notFainted:
                        self.updateActivePkmn(currentActive, self.pkmn2)
                        self.cpuEasy.updateOppActive(self.playerActivePkmn)
                        self.viewParty = False
                        if not self.plyrJustFainted:
                            self.switchTurn()
                        else:
                            self.plyrJustFainted = False
                    else:
                        print("Please choose a valid Pokémon.")
                elif self.partyButton3.collidepoint(pygame.mouse.get_pos()):
                    notFainted = self.pkmn3 not in self.playerFainted
                    if self.pkmn3 != self.playerActivePkmn and self.pkmn3 != None and notFainted:
                        self.updateActivePkmn(currentActive, self.pkmn3)
                        self.cpuEasy.updateOppActive(self.playerActivePkmn)
                        self.viewParty = False
                        if not self.plyrJustFainted:
                            self.switchTurn()
                        else:
                            self.plyrJustFainted = False
                    else:
                        print("Please choose a valid Pokémon.")
                elif self.partyButton4.collidepoint(pygame.mouse.get_pos()):
                    notFainted = self.pkmn4 not in self.playerFainted
                    if self.pkmn4 != self.playerActivePkmn and self.pkmn4 != None and notFainted:
                        self.updateActivePkmn(currentActive, self.pkmn4)
                        self.cpuEasy.updateOppActive(self.playerActivePkmn)
                        self.viewParty = False
                        if not self.plyrJustFainted:
                            self.switchTurn()
                        else:
                            self.plyrJustFainted = False
                    else:
                        print("Please choose a valid Pokémon.")
                elif self.partyButton5.collidepoint(pygame.mouse.get_pos()):
                    notFainted = self.pkmn5 not in self.playerFainted
                    if self.pkmn5 != self.playerActivePkmn and self.pkmn5 != None and notFainted:
                        self.updateActivePkmn(currentActive, self.pkmn5)
                        self.cpuEasy.updateOppActive(self.playerActivePkmn)
                        self.viewParty = False
                        if not self.plyrJustFainted:
                            self.switchTurn()
                        else:
                            self.plyrJustFainted = False
                    else:
                        print("Please choose a valid Pokémon.")
                elif self.partyButton6.collidepoint(pygame.mouse.get_pos()):
                    notFainted = self.pkmn6 not in self.playerFainted
                    if self.pkmn6 != self.playerActivePkmn and self.pkmn6 != None and notFainted:
                        self.updateActivePkmn(currentActive, self.pkmn6)
                        self.cpuEasy.updateOppActive(self.playerActivePkmn)
                        self.viewParty = False
                        if not self.plyrJustFainted:
                            self.switchTurn()
                        else:
                            self.plyrJustFainted = False
                    else:
                        print("Please choose a valid Pokémon.")

            # PICKING MOVES
            elif self.pickMoves:
                self.activeMoves = self.playerActivePkmn.getMoves()
                if self.move1Button.collidepoint(pygame.mouse.get_pos()) and self.activeMoves[0] != None:
                    self.plyrUsedMove = self.player.useMove(self.activeMoves[0])
                    plyrDmgDealt = self.plyrUsedMove[0]
                    plyrDStatus = copy.deepcopy(self.plyrUsedMove[1])
                    plyrMsg = self.plyrUsedMove[2]
                    self.pickMoves = False
                    self.chooseAction = True
                    print("Player dealt", plyrDmgDealt)
                elif self.move2Button.collidepoint(pygame.mouse.get_pos()) and self.activeMoves[1] != None:
                    self.plyrUsedMove = self.player.useMove(self.activeMoves[1])
                    plyrDmgDealt = self.plyrUsedMove[0]
                    plyrDStatus = copy.deepcopy(self.plyrUsedMove[1])
                    msg = self.plyrUsedMove[2]
                    self.pickMoves = False
                    self.chooseAction = True
                    print("Player dealt", plyrDmgDealt)
                elif self.move3Button.collidepoint(pygame.mouse.get_pos()) and self.activeMoves[2] != None:
                    self.plyrUsedMove = self.player.useMove(self.activeMoves[2])
                    plyrDmgDealt = self.plyrUsedMove[0]
                    plyrDStatus = copy.deepcopy(self.plyrUsedMove[1])
                    msg = self.plyrUsedMove[2]
                    self.pickMoves = False
                    self.chooseAction = True
                    print("Player dealt", plyrDmgDealt)
                elif self.move4Button.collidepoint(pygame.mouse.get_pos()) and self.activeMoves[3] != None:
                    self.plyrUsedMove = self.player.useMove(self.activeMoves[3])
                    plyrDmgDealt = self.plyrUsedMove[0]
                    plyrDStatus = copy.deepcopy(self.plyrUsedMove[1])
                    msg = self.plyrUsedMove[2]
                    self.pickMoves = False
                    self.chooseAction = True
                    print("Player dealt", plyrDmgDealt)
                
                # GO THROUGH TURN
                self.turn()

            # PICK MOVES TO BATTLE
            elif chooseBattle:
                self.chooseAction = False
                self.pickMoves = True
            
            # VIEW CURRENT PARTY
            elif chooseViewParty and not self.pickMoves and not self.mightRun:
                self.viewParty = True
            
            # RUN
            elif chooseRun and not self.viewParty and not self.pickMoves:
                self.mightRun = True
            # are u sure
            if self.mightRun:
                if self.yesRun.collidepoint(pygame.mouse.get_pos()):
                    # RESET PKMN
                    for pkmn in range(0, 6):
                        if self.party[pkmn] != None:
                            self.party[pkmn].resetStatConds()
                            self.party[pkmn].changeNotFainted()
                        if self.cpuParty[pkmn] != None:
                            self.cpuParty[pkmn].resetStatConds()
                            self.cpuParty[pkmn].changeNotFainted()
                    self.mightRun = False
                    self.battleScreen = False
                    self.chooseAction = False
                    self.selectScreen = True
                elif self.noRun.collidepoint(pygame.mouse.get_pos()):
                    self.mightRun = False

        elif self.gameOver == True:
            replay = self.replayButton.collidepoint(pygame.mouse.get_pos())
            quit = self.quitButton.collidepoint(pygame.mouse.get_pos())
            if replay:
            # RESET PKMN
                self.gameOver = False
                self.clearAll()
                for pkmn in range(0, 6):
                    self.party[pkmn] = None
                    self.cpuParty[pkmn] = None
                self.mightRun = False
                self.battleScreen = False
                self.chooseAction = False
                self.selectScreen = False
                self.titleCard = True
            elif quit:
                pygame.quit()

    #################
    ## TIMER FIRED ##
    #################
    def timerFired(self, dt):
        self.initButton.update()
        self.saveIcon.update()

    ####################
    ## GET TINY ICONS ##
    ####################
    def getTinyIcon(self, pkmnName):
        pkmnIcon = pg.image.load("classes/imgs/tiny_icons/" + pkmnName.lower() + ".png")
        return pkmnIcon

    ################
    ## REDRAW ALL ##
    ################
    def redrawAll(self, screen):
        # TITLE SCREEN
        if self.titleCard == True:
            screen.blit(self.titleBG, (0, 0))
            screen.blit(self.logo, (self.centerX - self.logoRect.width / 2, 15))
            screen.blit(self.BSTextSurfaceShadow2,
                        (self.centerX - self.BSTextSurfaceRect.width / 2 + 5, 215))
            screen.blit(self.BSTextSurfaceShadow,
                        (self.centerX - self.BSTextSurfaceRect.width / 2 - 5, 205))
            screen.blit(self.BSTextSurface,
                        (self.centerX - self.BSTextSurfaceRect.width / 2, 210))
            
            screen.blit(self.enterTextSurface, (self.centerX - self.enterTSRect.width / 2, 625))
            self.initButton.draw(screen)
        
        # SELECT SCREEN
        elif self.selectScreen == True:            
            screen.blit(self.selectBG, (0, 0))
            screen.blit(self.playButton1, self.playButton1Rect)

            # draw select boxes (sidebar) + ornaments
            if self.pkmn1 != None:
                self.selectBox1 = Box(self.pkmn1, self.pkmn1Type1, self.pkmn1Type2, (610, 14), (280, 92))
            self.selectBox1.draw(screen)
            if self.pkmn2 != None:
                self.selectBox2 = Box(self.pkmn2, self.pkmn2Type1, self.pkmn2Type2, (610, 120), (280, 92))
            self.selectBox2.draw(screen)
            if self.pkmn3 != None:
                self.selectBox3 = Box(self.pkmn3, self.pkmn3Type1, self.pkmn3Type2, (610, 226), (280, 92))
            self.selectBox3.draw(screen)
            if self.pkmn4 != None:
                self.selectBox4 = Box(self.pkmn4, self.pkmn4Type1, self.pkmn4Type2, (610, 332), (280, 92))
            self.selectBox4.draw(screen)
            if self.pkmn5 != None:
                self.selectBox5 = Box(self.pkmn5, self.pkmn5Type1, self.pkmn5Type2, (610, 438), (280, 92))
            self.selectBox5.draw(screen)
            if self.pkmn6 != None:
                self.selectBox6 = Box(self.pkmn6, self.pkmn6Type1, self.pkmn6Type2, (610, 544), (280, 92))
            self.selectBox6.draw(screen)

            # draw select pokemon boxes
            if self.selectPokemon1 == True:
                screen.blit(self.trprtSelectBG, (0, 0))
                self.saveIcon.draw(screen)
                screen.blit(self.selectedPkmnBG, (30, 80))

                # NAME FIELD
                screen.blit(self.selectForBattleName, (220, 80))

                # LEVEL
                screen.blit(self.selectForBattleLvl, (220, 150))

                # MOVES
                screen.blit(self.selectForBattleMoves, (30, 270))
                for yCoord in range(311, 552, 80):
                    screen.blit(self.movePPTxt, (220, yCoord))
                for yCoord in range(329, 570, 80):
                    screen.blit(self.movePowerTxt, (220, yCoord))
                for yCoord in range(347, 588, 80):
                    screen.blit(self.moveAccuracyTxt, (220, yCoord))
                for yCoord in range(337, 658, 80):
                    screen.blit(self.moveTypeTxt, (50, yCoord))
                for yCoord in range(351, 671, 80):
                    screen.blit(self.moveCatTxt, (50, yCoord))

                # text inputs
                for txt in self.input1List:
                    txt.draw(screen)

                # EVs
                screen.blit(self.selectForBattleEVs, (400, 270))
                for i in range(0, 6):
                    screen.blit(self.evTxtList[i], (410, self.evTxtYCoordsList[i]))
                for ev in self.inputEV1List:
                    ev.draw(screen)

                # STATS
                screen.blit(self.selectForBattleStats, (400, 80))
                for i in range(0, 6):
                    screen.blit(self.evTxtList[i], (470, self.statTxtYCoordsList[i]))

                # IMGS TO DRAW ONLY IF SELF.PKMN1 IS FILLED
                if self.pkmn1 != None:
                    # sprite
                    if self.inputSprite1 != None:
                        self.inputSprite1.draw(screen)

                    # typing
                    if self.pkmn1Type1 != None:
                        screen.blit(self.pkmn1Type1, (220, 125))
                    if self.pkmn1Type2 != None:
                        screen.blit(self.pkmn1Type2, (255, 125))

                    # EVs
                    statTxt = []
                    statTxtRects = []
                    for stat in self.pkmn1BattleStats:
                        statTxt.append(self.statDetailsFont.render(str(stat), True, (5, 35, 80)))
                    for i in range(0, 6):
                        statTxtRects.append(statTxt[i].get_rect(topright = (465, self.statTxtYCoordsList[i])))
                    for j in range(0, 6):
                        screen.blit(statTxt[j], statTxtRects[j])

                    # MOVE TYPING
                    if self.pkmn1Move1 != None:
                        mvType, mvCat = self.pkmn1Move1.getMoveType(), self.pkmn1Move1.getMoveCategory()
                        mvImgType, mvImgCat = pygame.image.load(self.typeIconsList[mvType]), pygame.image.load(self.categoryIconsList[mvCat])
                        screen.blit(mvImgType, (84, 335))
                        screen.blit(mvImgCat, (121, 350))
                        mvPP, mvPower, mvAcc = self.moveDetailsFont.render(str(self.pkmn1Move1.getMovePP()), 12, (25, 25, 25)), \
                                               self.moveDetailsFont.render(str(self.pkmn1Move1.getMovePower()), 12, (25, 25, 25)), \
                                               self.moveDetailsFont.render(str(self.pkmn1Move1.getMoveAccuracy()), 12, (25, 25, 25))
                        screen.blit(mvPP, (238, 311))
                        screen.blit(mvPower, (269, 329))
                        screen.blit(mvAcc, (291, 347))
                    if self.pkmn1Move2 != None:
                        mvType, mvCat = self.pkmn1Move2.getMoveType(), self.pkmn1Move2.getMoveCategory()
                        mvImgType, mvImgCat = pygame.image.load(self.typeIconsList[mvType]), pygame.image.load(self.categoryIconsList[mvCat])
                        screen.blit(mvImgType, (84, 415))
                        screen.blit(mvImgCat, (121, 430))
                        mvPP, mvPower, mvAcc = self.moveDetailsFont.render(str(self.pkmn1Move2.getMovePP()), 12, (25, 25, 25)), self.moveDetailsFont.render(str(self.pkmn1Move2.getMovePower()), 12, (25, 25, 25)), self.moveDetailsFont.render(str(self.pkmn1Move2.getMoveAccuracy()), 12, (25, 25, 25))
                        screen.blit(mvPP, (238, 391))
                        screen.blit(mvPower, (269, 409))
                        screen.blit(mvAcc, (291, 427))
                    if self.pkmn1Move3 != None:
                        mvType, mvCat = self.pkmn1Move3.getMoveType(), self.pkmn1Move3.getMoveCategory()
                        mvImgType, mvImgCat = pygame.image.load(self.typeIconsList[mvType]), pygame.image.load(self.categoryIconsList[mvCat])
                        screen.blit(mvImgType, (84, 495))
                        screen.blit(mvImgCat, (121, 510))
                        mvPP, mvPower, mvAcc = self.moveDetailsFont.render(str(self.pkmn1Move3.getMovePP()), 12, (25, 25, 25)), self.moveDetailsFont.render(str(self.pkmn1Move3.getMovePower()), 12, (25, 25, 25)), self.moveDetailsFont.render(str(self.pkmn1Move3.getMoveAccuracy()), 12, (25, 25, 25))
                        screen.blit(mvPP, (238, 471))
                        screen.blit(mvPower, (269, 489))
                        screen.blit(mvAcc, (291, 507))
                    if self.pkmn1Move4 != None:
                        mvType, mvCat = self.pkmn1Move4.getMoveType(), self.pkmn1Move4.getMoveCategory()
                        mvImgType = pygame.image.load(self.typeIconsList[mvType])
                        mvImgType, mvImgCat = pygame.image.load(self.typeIconsList[mvType]), pygame.image.load(self.categoryIconsList[mvCat])
                        screen.blit(mvImgType, (84, 575))
                        screen.blit(mvImgCat, (121, 590))
                        mvPP, mvPower, mvAcc = self.moveDetailsFont.render(str(self.pkmn1Move4.getMovePP()), 12, (25, 25, 25)), self.moveDetailsFont.render(str(self.pkmn1Move4.getMovePower()), 12, (25, 25, 25)), self.moveDetailsFont.render(str(self.pkmn1Move4.getMoveAccuracy()), 12, (25, 25, 25))
                        screen.blit(mvPP, (238, 551))
                        screen.blit(mvPower, (269, 569))
                        screen.blit(mvAcc, (291, 587))
                               
            elif self.selectPokemon2 == True:
                screen.blit(self.trprtSelectBG, (0, 0))
                self.saveIcon.draw(screen)
                screen.blit(self.selectedPkmnBG, (30, 80))

                # NAME FIELD
                screen.blit(self.selectForBattleName, (220, 80))

                # LEVEL
                screen.blit(self.selectForBattleLvl, (220, 150))

                # MOVES
                screen.blit(self.selectForBattleMoves, (30, 270))
                for yCoord in range(311, 552, 80):
                    screen.blit(self.movePPTxt, (220, yCoord))
                for yCoord in range(329, 570, 80):
                    screen.blit(self.movePowerTxt, (220, yCoord))
                for yCoord in range(347, 588, 80):
                    screen.blit(self.moveAccuracyTxt, (220, yCoord))
                for yCoord in range(337, 658, 80):
                    screen.blit(self.moveTypeTxt, (50, yCoord))
                for yCoord in range(351, 671, 80):
                    screen.blit(self.moveCatTxt, (50, yCoord))
                
                # text inputs
                for txt in self.input2List:
                    txt.draw(screen)

                # EVs
                screen.blit(self.selectForBattleEVs, (400, 270))
                for i in range(0, 6):
                    screen.blit(self.evTxtList[i], (410, self.evTxtYCoordsList[i]))
                for ev in self.inputEV2List:
                    ev.draw(screen)

                # STATS
                screen.blit(self.selectForBattleStats, (400, 80))
                for i in range(0, 6):
                    screen.blit(self.evTxtList[i], (470, self.statTxtYCoordsList[i]))

                # IMGS TO DRAW ONLY IF SELF.PKMN2 IS FILLED
                if self.pkmn2 != None:
                    # SPRITE
                    if self.inputSprite2 != None:
                        self.inputSprite2.draw(screen)

                    # TYPING
                    if self.pkmn2Type1 != None:
                        screen.blit(self.pkmn2Type1, (220, 125))
                    if self.pkmn2Type2 != None:
                        screen.blit(self.pkmn2Type2, (255, 125))

                    # EVs
                    statTxt = []
                    statTxtRects = []
                    for stat in self.pkmn2BattleStats:
                        statTxt.append(self.statDetailsFont.render(str(stat), True, (5, 35, 80)))
                    for i in range(0, 6):
                        statTxtRects.append(statTxt[i].get_rect(topright = (465, self.statTxtYCoordsList[i])))
                    for j in range(0, 6):
                        screen.blit(statTxt[j], statTxtRects[j])

                    # MOVE TYPING
                    if self.pkmn2Move1 != None:
                        mvType, mvCat = self.pkmn2Move1.getMoveType(), self.pkmn2Move1.getMoveCategory()
                        mvImgType, mvImgCat = pygame.image.load(self.typeIconsList[mvType]), pygame.image.load(self.categoryIconsList[mvCat])
                        screen.blit(mvImgType, (84, 335))
                        screen.blit(mvImgCat, (121, 350))
                        mvPP, mvPower, mvAcc = self.moveDetailsFont.render(str(self.pkmn2Move1.getMovePP()), 12, (25, 25, 25)), self.moveDetailsFont.render(str(self.pkmn2Move1.getMovePower()), 12, (25, 25, 25)), self.moveDetailsFont.render(str(self.pkmn2Move1.getMoveAccuracy()), 12, (25, 25, 25))
                        screen.blit(mvPP, (238, 311))
                        screen.blit(mvPower, (269, 329))
                        screen.blit(mvAcc, (291, 347))
                    if self.pkmn2Move2 != None:
                        mvType, mvCat = self.pkmn2Move2.getMoveType(), self.pkmn2Move2.getMoveCategory()
                        mvImgType, mvImgCat = pygame.image.load(self.typeIconsList[mvType]), pygame.image.load(self.categoryIconsList[mvCat])
                        screen.blit(mvImgType, (84, 415))
                        screen.blit(mvImgCat, (121, 430))
                        mvPP, mvPower, mvAcc = self.moveDetailsFont.render(str(self.pkmn2Move2.getMovePP()), 12, (25, 25, 25)), self.moveDetailsFont.render(str(self.pkmn2Move2.getMovePower()), 12, (25, 25, 25)), self.moveDetailsFont.render(str(self.pkmn2Move2.getMoveAccuracy()), 12, (25, 25, 25))
                        screen.blit(mvPP, (238, 391))
                        screen.blit(mvPower, (269, 409))
                        screen.blit(mvAcc, (291, 427))
                    if self.pkmn2Move3 != None:
                        mvType, mvCat = self.pkmn2Move3.getMoveType(), self.pkmn2Move3.getMoveCategory()
                        mvImgType, mvImgCat = pygame.image.load(self.typeIconsList[mvType]), pygame.image.load(self.categoryIconsList[mvCat])
                        screen.blit(mvImgType, (84, 495))
                        screen.blit(mvImgCat, (121, 510))
                        mvPP, mvPower, mvAcc = self.moveDetailsFont.render(str(self.pkmn2Move3.getMovePP()), 12, (25, 25, 25)), self.moveDetailsFont.render(str(self.pkmn2Move3.getMovePower()), 12, (25, 25, 25)), self.moveDetailsFont.render(str(self.pkmn2Move3.getMoveAccuracy()), 12, (25, 25, 25))
                        screen.blit(mvPP, (238, 471))
                        screen.blit(mvPower, (269, 489))
                        screen.blit(mvAcc, (291, 507))
                    if self.pkmn2Move4 != None:
                        mvType, mvCat = self.pkmn2Move4.getMoveType(), self.pkmn2Move4.getMoveCategory()
                        mvImgType = pygame.image.load(self.typeIconsList[mvType])
                        mvImgType, mvImgCat = pygame.image.load(self.typeIconsList[mvType]), pygame.image.load(self.categoryIconsList[mvCat])
                        screen.blit(mvImgType, (84, 575))
                        screen.blit(mvImgCat, (121, 590))
                        mvPP, mvPower, mvAcc = self.moveDetailsFont.render(str(self.pkmn2Move4.getMovePP()), 12, (25, 25, 25)), self.moveDetailsFont.render(str(self.pkmn2Move4.getMovePower()), 12, (25, 25, 25)), self.moveDetailsFont.render(str(self.pkmn2Move4.getMoveAccuracy()), 12, (25, 25, 25))
                        screen.blit(mvPP, (238, 551))
                        screen.blit(mvPower, (269, 569))
                        screen.blit(mvAcc, (291, 587))
            
            elif self.selectPokemon3 == True:
                screen.blit(self.trprtSelectBG, (0, 0))
                self.saveIcon.draw(screen)
                screen.blit(self.selectedPkmnBG, (30, 80))

                # NAME FIELD
                screen.blit(self.selectForBattleName, (220, 80))

                # LEVEL
                screen.blit(self.selectForBattleLvl, (220, 150))

                # MOVES
                screen.blit(self.selectForBattleMoves, (30, 270))
                for yCoord in range(311, 552, 80):
                    screen.blit(self.movePPTxt, (220, yCoord))
                for yCoord in range(329, 570, 80):
                    screen.blit(self.movePowerTxt, (220, yCoord))
                for yCoord in range(347, 588, 80):
                    screen.blit(self.moveAccuracyTxt, (220, yCoord))
                for yCoord in range(337, 658, 80):
                    screen.blit(self.moveTypeTxt, (50, yCoord))
                for yCoord in range(351, 671, 80):
                    screen.blit(self.moveCatTxt, (50, yCoord))
                
                # text inputs
                for txt in self.input3List:
                    txt.draw(screen)

                # EVs
                screen.blit(self.selectForBattleEVs, (400, 270))
                for i in range(0, 6):
                    screen.blit(self.evTxtList[i], (410, self.evTxtYCoordsList[i]))
                for ev in self.inputEV3List:
                    ev.draw(screen)

                # STATS
                screen.blit(self.selectForBattleStats, (400, 80))
                for i in range(0, 6):
                    screen.blit(self.evTxtList[i], (470, self.statTxtYCoordsList[i]))

                # IMGS TO DRAW ONLY IF SELF.PKMN3 IS FILLED
                if self.pkmn3 != None:
                    # SPRITE
                    if self.inputSprite3 != None:
                        self.inputSprite3.draw(screen)

                    # TYPING
                    if self.pkmn3Type1 != None:
                        screen.blit(self.pkmn3Type1, (220, 125))
                    if self.pkmn3Type2 != None:
                        screen.blit(self.pkmn3Type2, (255, 125))

                    # EVs
                    statTxt = []
                    statTxtRects = []
                    for stat in self.pkmn3BattleStats:
                        statTxt.append(self.statDetailsFont.render(str(stat), True, (5, 35, 80)))
                    for i in range(0, 6):
                        statTxtRects.append(statTxt[i].get_rect(topright = (465, self.statTxtYCoordsList[i])))
                    for j in range(0, 6):
                        screen.blit(statTxt[j], statTxtRects[j])

                    # MOVE TYPING
                    if self.pkmn3Move1 != None:
                        mvType, mvCat = self.pkmn3Move1.getMoveType(), self.pkmn3Move1.getMoveCategory()
                        mvImgType, mvImgCat = pygame.image.load(self.typeIconsList[mvType]), pygame.image.load(self.categoryIconsList[mvCat])
                        screen.blit(mvImgType, (84, 335))
                        screen.blit(mvImgCat, (121, 350))
                        mvPP, mvPower, mvAcc = self.moveDetailsFont.render(str(self.pkmn3Move1.getMovePP()), 12, (25, 25, 25)), self.moveDetailsFont.render(str(self.pkmn3Move1.getMovePower()), 12, (25, 25, 25)), self.moveDetailsFont.render(str(self.pkmn3Move1.getMoveAccuracy()), 12, (25, 25, 25))
                        screen.blit(mvPP, (238, 311))
                        screen.blit(mvPower, (269, 329))
                        screen.blit(mvAcc, (291, 347))
                    if self.pkmn3Move2 != None:
                        mvType, mvCat = self.pkmn3Move2.getMoveType(), self.pkmn3Move2.getMoveCategory()
                        mvImgType, mvImgCat = pygame.image.load(self.typeIconsList[mvType]), pygame.image.load(self.categoryIconsList[mvCat])
                        screen.blit(mvImgType, (84, 415))
                        screen.blit(mvImgCat, (121, 430))
                        mvPP, mvPower, mvAcc = self.moveDetailsFont.render(str(self.pkmn3Move2.getMovePP()), 12, (25, 25, 25)), self.moveDetailsFont.render(str(self.pkmn3Move2.getMovePower()), 12, (25, 25, 25)), self.moveDetailsFont.render(str(self.pkmn3Move2.getMoveAccuracy()), 12, (25, 25, 25))
                        screen.blit(mvPP, (238, 391))
                        screen.blit(mvPower, (269, 409))
                        screen.blit(mvAcc, (291, 427))
                    if self.pkmn3Move3 != None:
                        mvType, mvCat = self.pkmn3Move3.getMoveType(), self.pkmn3Move3.getMoveCategory()
                        mvImgType, mvImgCat = pygame.image.load(self.typeIconsList[mvType]), pygame.image.load(self.categoryIconsList[mvCat])
                        screen.blit(mvImgType, (84, 495))
                        screen.blit(mvImgCat, (121, 510))
                        mvPP, mvPower, mvAcc = self.moveDetailsFont.render(str(self.pkmn3Move3.getMovePP()), 12, (25, 25, 25)), self.moveDetailsFont.render(str(self.pkmn3Move3.getMovePower()), 12, (25, 25, 25)), self.moveDetailsFont.render(str(self.pkmn3Move3.getMoveAccuracy()), 12, (25, 25, 25))
                        screen.blit(mvPP, (238, 471))
                        screen.blit(mvPower, (269, 489))
                        screen.blit(mvAcc, (291, 507))
                    if self.pkmn3Move4 != None:
                        mvType, mvCat = self.pkmn3Move4.getMoveType(), self.pkmn3Move4.getMoveCategory()
                        mvImgType = pygame.image.load(self.typeIconsList[mvType])
                        mvImgType, mvImgCat = pygame.image.load(self.typeIconsList[mvType]), pygame.image.load(self.categoryIconsList[mvCat])
                        screen.blit(mvImgType, (84, 575))
                        screen.blit(mvImgCat, (121, 590))
                        mvPP, mvPower, mvAcc = self.moveDetailsFont.render(str(self.pkmn3Move4.getMovePP()), 12, (25, 25, 25)), self.moveDetailsFont.render(str(self.pkmn3Move4.getMovePower()), 12, (25, 25, 25)), self.moveDetailsFont.render(str(self.pkmn3Move4.getMoveAccuracy()), 12, (25, 25, 25))
                        screen.blit(mvPP, (238, 551))
                        screen.blit(mvPower, (269, 569))
                        screen.blit(mvAcc, (291, 587))
                
            elif self.selectPokemon4 == True:
                screen.blit(self.trprtSelectBG, (0, 0))
                self.saveIcon.draw(screen)
                screen.blit(self.selectedPkmnBG, (30, 80))

                # NAME FIELD
                screen.blit(self.selectForBattleName, (220, 80))

                # LEVEL
                screen.blit(self.selectForBattleLvl, (220, 150))

                # MOVES
                screen.blit(self.selectForBattleMoves, (30, 270))
                for yCoord in range(311, 552, 80):
                    screen.blit(self.movePPTxt, (220, yCoord))
                for yCoord in range(329, 570, 80):
                    screen.blit(self.movePowerTxt, (220, yCoord))
                for yCoord in range(347, 588, 80):
                    screen.blit(self.moveAccuracyTxt, (220, yCoord))
                for yCoord in range(337, 658, 80):
                    screen.blit(self.moveTypeTxt, (50, yCoord))
                for yCoord in range(351, 671, 80):
                    screen.blit(self.moveCatTxt, (50, yCoord))
                
                # text inputs
                for txt in self.input4List:
                    txt.draw(screen)

                # EVs
                screen.blit(self.selectForBattleEVs, (400, 270))
                for i in range(0, 6):
                    screen.blit(self.evTxtList[i], (410, self.evTxtYCoordsList[i]))
                for ev in self.inputEV4List:
                    ev.draw(screen)

                # STATS
                screen.blit(self.selectForBattleStats, (400, 80))
                for i in range(0, 6):
                    screen.blit(self.evTxtList[i], (470, self.statTxtYCoordsList[i]))

                # IMGS TO DRAW ONLY IF SELF.PKMN4 IS FILLED
                if self.pkmn4 != None:
                    # SPRITE
                    if self.inputSprite4 != None:
                        self.inputSprite4.draw(screen)

                    # TYPING
                    if self.pkmn4Type1 != None:
                        screen.blit(self.pkmn4Type1, (220, 125))
                    if self.pkmn4Type2 != None:
                        screen.blit(self.pkmn4Type2, (255, 125))

                    # EVs
                    statTxt = []
                    statTxtRects = []
                    for stat in self.pkmn4BattleStats:
                        statTxt.append(self.statDetailsFont.render(str(stat), True, (5, 35, 80)))
                    for i in range(0, 6):
                        statTxtRects.append(statTxt[i].get_rect(topright = (465, self.statTxtYCoordsList[i])))
                    for j in range(0, 6):
                        screen.blit(statTxt[j], statTxtRects[j])

                    # MOVE TYPING
                    if self.pkmn4Move1 != None:
                        mvType, mvCat = self.pkmn4Move1.getMoveType(), self.pkmn4Move1.getMoveCategory()
                        mvImgType, mvImgCat = pygame.image.load(self.typeIconsList[mvType]), pygame.image.load(self.categoryIconsList[mvCat])
                        screen.blit(mvImgType, (84, 335))
                        screen.blit(mvImgCat, (121, 350))
                        mvPP, mvPower, mvAcc = self.moveDetailsFont.render(str(self.pkmn4Move1.getMovePP()), 12, (25, 25, 25)), self.moveDetailsFont.render(str(self.pkmn4Move1.getMovePower()), 12, (25, 25, 25)), self.moveDetailsFont.render(str(self.pkmn4Move1.getMoveAccuracy()), 12, (25, 25, 25))
                        screen.blit(mvPP, (238, 311))
                        screen.blit(mvPower, (269, 329))
                        screen.blit(mvAcc, (291, 347))
                    if self.pkmn4Move2 != None:
                        mvType, mvCat = self.pkmn4Move2.getMoveType(), self.pkmn4Move2.getMoveCategory()
                        mvImgType, mvImgCat = pygame.image.load(self.typeIconsList[mvType]), pygame.image.load(self.categoryIconsList[mvCat])
                        screen.blit(mvImgType, (84, 415))
                        screen.blit(mvImgCat, (121, 430))
                        mvPP, mvPower, mvAcc = self.moveDetailsFont.render(str(self.pkmn4Move2.getMovePP()), 12, (25, 25, 25)), self.moveDetailsFont.render(str(self.pkmn4Move2.getMovePower()), 12, (25, 25, 25)), self.moveDetailsFont.render(str(self.pkmn4Move2.getMoveAccuracy()), 12, (25, 25, 25))
                        screen.blit(mvPP, (238, 391))
                        screen.blit(mvPower, (269, 409))
                        screen.blit(mvAcc, (291, 427))
                    if self.pkmn4Move3 != None:
                        mvType, mvCat = self.pkmn4Move3.getMoveType(), self.pkmn4Move3.getMoveCategory()
                        mvImgType, mvImgCat = pygame.image.load(self.typeIconsList[mvType]), pygame.image.load(self.categoryIconsList[mvCat])
                        screen.blit(mvImgType, (84, 495))
                        screen.blit(mvImgCat, (121, 510))
                        mvPP, mvPower, mvAcc = self.moveDetailsFont.render(str(self.pkmn4Move3.getMovePP()), 12, (25, 25, 25)), self.moveDetailsFont.render(str(self.pkmn4Move3.getMovePower()), 12, (25, 25, 25)), self.moveDetailsFont.render(str(self.pkmn4Move3.getMoveAccuracy()), 12, (25, 25, 25))
                        screen.blit(mvPP, (238, 471))
                        screen.blit(mvPower, (269, 489))
                        screen.blit(mvAcc, (291, 507))
                    if self.pkmn4Move4 != None:
                        mvType, mvCat = self.pkmn4Move4.getMoveType(), self.pkmn4Move4.getMoveCategory()
                        mvImgType = pygame.image.load(self.typeIconsList[mvType])
                        mvImgType, mvImgCat = pygame.image.load(self.typeIconsList[mvType]), pygame.image.load(self.categoryIconsList[mvCat])
                        screen.blit(mvImgType, (84, 575))
                        screen.blit(mvImgCat, (121, 590))
                        mvPP, mvPower, mvAcc = self.moveDetailsFont.render(str(self.pkmn4Move4.getMovePP()), 12, (25, 25, 25)), self.moveDetailsFont.render(str(self.pkmn4Move4.getMovePower()), 12, (25, 25, 25)), self.moveDetailsFont.render(str(self.pkmn4Move4.getMoveAccuracy()), 12, (25, 25, 25))
                        screen.blit(mvPP, (238, 551))
                        screen.blit(mvPower, (269, 569))
                        screen.blit(mvAcc, (291, 587))
                
            elif self.selectPokemon5 == True:
                screen.blit(self.trprtSelectBG, (0, 0))
                self.saveIcon.draw(screen)
                screen.blit(self.selectedPkmnBG, (30, 80))

                # NAME FIELD
                screen.blit(self.selectForBattleName, (220, 80))

                # LEVEL
                screen.blit(self.selectForBattleLvl, (220, 150))

                # MOVES
                screen.blit(self.selectForBattleMoves, (30, 270))
                for yCoord in range(311, 552, 80):
                    screen.blit(self.movePPTxt, (220, yCoord))
                for yCoord in range(329, 570, 80):
                    screen.blit(self.movePowerTxt, (220, yCoord))
                for yCoord in range(347, 588, 80):
                    screen.blit(self.moveAccuracyTxt, (220, yCoord))
                for yCoord in range(337, 658, 80):
                    screen.blit(self.moveTypeTxt, (50, yCoord))
                for yCoord in range(351, 671, 80):
                    screen.blit(self.moveCatTxt, (50, yCoord))
                
                # text inputs
                for txt in self.input5List:
                    txt.draw(screen)

                # EVs
                screen.blit(self.selectForBattleEVs, (400, 270))
                for i in range(0, 6):
                    screen.blit(self.evTxtList[i], (410, self.evTxtYCoordsList[i]))
                for ev in self.inputEV5List:
                    ev.draw(screen)

                # STATS
                screen.blit(self.selectForBattleStats, (400, 80))
                for i in range(0, 6):
                    screen.blit(self.evTxtList[i], (470, self.statTxtYCoordsList[i]))

                # IMGS TO DRAW ONLY IF SELF.PKMN5 IS FILLED
                if self.pkmn5 != None:
                    # SPRITE
                    if self.inputSprite5 != None:
                        self.inputSprite5.draw(screen)

                    # TYPING
                    if self.pkmn5Type1 != None:
                        screen.blit(self.pkmn5Type1, (220, 125))
                    if self.pkmn5Type2 != None:
                        screen.blit(self.pkmn5Type2, (255, 125))

                    # EVs
                    statTxt = []
                    statTxtRects = []
                    for stat in self.pkmn5BattleStats:
                        statTxt.append(self.statDetailsFont.render(str(stat), True, (5, 35, 80)))
                    for i in range(0, 6):
                        statTxtRects.append(statTxt[i].get_rect(topright = (465, self.statTxtYCoordsList[i])))
                    for j in range(0, 6):
                        screen.blit(statTxt[j], statTxtRects[j])

                    # MOVE TYPING
                    if self.pkmn5Move1 != None:
                        mvType, mvCat = self.pkmn5Move1.getMoveType(), self.pkmn5Move1.getMoveCategory()
                        mvImgType, mvImgCat = pygame.image.load(self.typeIconsList[mvType]), pygame.image.load(self.categoryIconsList[mvCat])
                        screen.blit(mvImgType, (84, 335))
                        screen.blit(mvImgCat, (121, 350))
                        mvPP, mvPower, mvAcc = self.moveDetailsFont.render(str(self.pkmn5Move1.getMovePP()), 12, (25, 25, 25)), self.moveDetailsFont.render(str(self.pkmn5Move1.getMovePower()), 12, (25, 25, 25)), self.moveDetailsFont.render(str(self.pkmn5Move1.getMoveAccuracy()), 12, (25, 25, 25))
                        screen.blit(mvPP, (238, 311))
                        screen.blit(mvPower, (269, 329))
                        screen.blit(mvAcc, (291, 347))
                    if self.pkmn5Move2 != None:
                        mvType, mvCat = self.pkmn5Move2.getMoveType(), self.pkmn5Move2.getMoveCategory()
                        mvImgType, mvImgCat = pygame.image.load(self.typeIconsList[mvType]), pygame.image.load(self.categoryIconsList[mvCat])
                        screen.blit(mvImgType, (84, 415))
                        screen.blit(mvImgCat, (121, 430))
                        mvPP, mvPower, mvAcc = self.moveDetailsFont.render(str(self.pkmn5Move2.getMovePP()), 12, (25, 25, 25)), self.moveDetailsFont.render(str(self.pkmn5Move2.getMovePower()), 12, (25, 25, 25)), self.moveDetailsFont.render(str(self.pkmn5Move2.getMoveAccuracy()), 12, (25, 25, 25))
                        screen.blit(mvPP, (238, 391))
                        screen.blit(mvPower, (269, 409))
                        screen.blit(mvAcc, (291, 427))
                    if self.pkmn5Move3 != None:
                        mvType, mvCat = self.pkmn5Move3.getMoveType(), self.pkmn5Move3.getMoveCategory()
                        mvImgType, mvImgCat = pygame.image.load(self.typeIconsList[mvType]), pygame.image.load(self.categoryIconsList[mvCat])
                        screen.blit(mvImgType, (84, 495))
                        screen.blit(mvImgCat, (121, 510))
                        mvPP, mvPower, mvAcc = self.moveDetailsFont.render(str(self.pkmn5Move3.getMovePP()), 12, (25, 25, 25)), self.moveDetailsFont.render(str(self.pkmn5Move3.getMovePower()), 12, (25, 25, 25)), self.moveDetailsFont.render(str(self.pkmn5Move3.getMoveAccuracy()), 12, (25, 25, 25))
                        screen.blit(mvPP, (238, 471))
                        screen.blit(mvPower, (269, 489))
                        screen.blit(mvAcc, (291, 507))
                    if self.pkmn5Move4 != None:
                        mvType, mvCat = self.pkmn5Move4.getMoveType(), self.pkmn5Move4.getMoveCategory()
                        mvImgType = pygame.image.load(self.typeIconsList[mvType])
                        mvImgType, mvImgCat = pygame.image.load(self.typeIconsList[mvType]), pygame.image.load(self.categoryIconsList[mvCat])
                        screen.blit(mvImgType, (84, 575))
                        screen.blit(mvImgCat, (121, 590))
                        mvPP, mvPower, mvAcc = self.moveDetailsFont.render(str(self.pkmn5Move4.getMovePP()), 12, (25, 25, 25)), self.moveDetailsFont.render(str(self.pkmn5Move4.getMovePower()), 12, (25, 25, 25)), self.moveDetailsFont.render(str(self.pkmn5Move4.getMoveAccuracy()), 12, (25, 25, 25))
                        screen.blit(mvPP, (238, 551))
                        screen.blit(mvPower, (269, 569))
                        screen.blit(mvAcc, (291, 587))
                
            elif self.selectPokemon6 == True:
                screen.blit(self.trprtSelectBG, (0, 0))
                self.saveIcon.draw(screen)
                screen.blit(self.selectedPkmnBG, (30, 80))

                # NAME FIELD
                screen.blit(self.selectForBattleName, (220, 80))

                # LEVEL
                screen.blit(self.selectForBattleLvl, (220, 150))

                # MOVES
                screen.blit(self.selectForBattleMoves, (30, 270))
                for yCoord in range(311, 552, 80):
                    screen.blit(self.movePPTxt, (220, yCoord))
                for yCoord in range(329, 570, 80):
                    screen.blit(self.movePowerTxt, (220, yCoord))
                for yCoord in range(347, 588, 80):
                    screen.blit(self.moveAccuracyTxt, (220, yCoord))
                for yCoord in range(337, 658, 80):
                    screen.blit(self.moveTypeTxt, (50, yCoord))
                for yCoord in range(351, 671, 80):
                    screen.blit(self.moveCatTxt, (50, yCoord))
                
                # text inputs
                for txt in self.input6List:
                    txt.draw(screen)

                # EVs
                screen.blit(self.selectForBattleEVs, (400, 270))
                for i in range(0, 6):
                    screen.blit(self.evTxtList[i], (410, self.evTxtYCoordsList[i]))
                for ev in self.inputEV6List:
                    ev.draw(screen)

                # STATS
                screen.blit(self.selectForBattleStats, (400, 80))
                for i in range(0, 6):
                    screen.blit(self.evTxtList[i], (470, self.statTxtYCoordsList[i]))

                # IMGS TO DRAW ONLY IF SELF.PKMN6 IS FILLED
                if self.pkmn6 != None:
                    # SPRITE
                    if self.inputSprite6 != None:
                        self.inputSprite6.draw(screen)

                    # TYPING
                    if self.pkmn6Type1 != None:
                        screen.blit(self.pkmn6Type1, (220, 125))
                    if self.pkmn6Type2 != None:
                        screen.blit(self.pkmn6Type2, (255, 125))

                    # EVs
                    statTxt = []
                    statTxtRects = []
                    for stat in self.pkmn6BattleStats:
                        statTxt.append(self.statDetailsFont.render(str(stat), True, (5, 35, 80)))
                    for i in range(0, 6):
                        statTxtRects.append(statTxt[i].get_rect(topright = (465, self.statTxtYCoordsList[i])))
                    for j in range(0, 6):
                        screen.blit(statTxt[j], statTxtRects[j])

                    # MOVE TYPING
                    if self.pkmn6Move1 != None:
                        mvType, mvCat = self.pkmn6Move1.getMoveType(), self.pkmn6Move1.getMoveCategory()
                        mvImgType, mvImgCat = pygame.image.load(self.typeIconsList[mvType]), pygame.image.load(self.categoryIconsList[mvCat])
                        screen.blit(mvImgType, (84, 335))
                        screen.blit(mvImgCat, (121, 350))
                        mvPP, mvPower, mvAcc = self.moveDetailsFont.render(str(self.pkmn6Move1.getMovePP()), 12, (25, 25, 25)), self.moveDetailsFont.render(str(self.pkmn6Move1.getMovePower()), 12, (25, 25, 25)), self.moveDetailsFont.render(str(self.pkmn6Move1.getMoveAccuracy()), 12, (25, 25, 25))
                        screen.blit(mvPP, (238, 311))
                        screen.blit(mvPower, (269, 329))
                        screen.blit(mvAcc, (291, 347))
                    if self.pkmn6Move2 != None:
                        mvType, mvCat = self.pkmn6Move2.getMoveType(), self.pkmn6Move2.getMoveCategory()
                        mvImgType, mvImgCat = pygame.image.load(self.typeIconsList[mvType]), pygame.image.load(self.categoryIconsList[mvCat])
                        screen.blit(mvImgType, (84, 415))
                        screen.blit(mvImgCat, (121, 430))
                        mvPP, mvPower, mvAcc = self.moveDetailsFont.render(str(self.pkmn6Move2.getMovePP()), 12, (25, 25, 25)), self.moveDetailsFont.render(str(self.pkmn6Move2.getMovePower()), 12, (25, 25, 25)), self.moveDetailsFont.render(str(self.pkmn6Move2.getMoveAccuracy()), 12, (25, 25, 25))
                        screen.blit(mvPP, (238, 391))
                        screen.blit(mvPower, (269, 409))
                        screen.blit(mvAcc, (291, 427))
                    if self.pkmn6Move3 != None:
                        mvType, mvCat = self.pkmn6Move3.getMoveType(), self.pkmn6Move3.getMoveCategory()
                        mvImgType, mvImgCat = pygame.image.load(self.typeIconsList[mvType]), pygame.image.load(self.categoryIconsList[mvCat])
                        screen.blit(mvImgType, (84, 495))
                        screen.blit(mvImgCat, (121, 510))
                        mvPP, mvPower, mvAcc = self.moveDetailsFont.render(str(self.pkmn6Move3.getMovePP()), 12, (25, 25, 25)), self.moveDetailsFont.render(str(self.pkmn6Move3.getMovePower()), 12, (25, 25, 25)), self.moveDetailsFont.render(str(self.pkmn6Move3.getMoveAccuracy()), 12, (25, 25, 25))
                        screen.blit(mvPP, (238, 471))
                        screen.blit(mvPower, (269, 489))
                        screen.blit(mvAcc, (291, 507))
                    if self.pkmn6Move4 != None:
                        mvType, mvCat = self.pkmn6Move4.getMoveType(), self.pkmn6Move4.getMoveCategory()
                        mvImgType = pygame.image.load(self.typeIconsList[mvType])
                        mvImgType, mvImgCat = pygame.image.load(self.typeIconsList[mvType]), pygame.image.load(self.categoryIconsList[mvCat])
                        screen.blit(mvImgType, (84, 575))
                        screen.blit(mvImgCat, (121, 590))
                        mvPP, mvPower, mvAcc = self.moveDetailsFont.render(str(self.pkmn6Move4.getMovePP()), 12, (25, 25, 25)), self.moveDetailsFont.render(str(self.pkmn6Move4.getMovePower()), 12, (25, 25, 25)), self.moveDetailsFont.render(str(self.pkmn6Move4.getMoveAccuracy()), 12, (25, 25, 25))
                        screen.blit(mvPP, (238, 551))
                        screen.blit(mvPower, (269, 569))
                        screen.blit(mvAcc, (291, 587))
            
        # BATTLE SCREEN
        elif self.battleScreen == True:
            screen.blit(self.battleBG, (0, 0))

            # SPRITES
            if self.playerActivePkmn != None and not self.playerActivePkmn.getIsFainted():
                self.playerActiveSprite.draw(screen)
            if self.cpuActivePkmn != None and not self.cpuActivePkmn.getIsFainted():
                self.cpuActiveSprite.draw(screen)

            # BG
            screen.blit(self.hpBarBGRed, (290, 262))
            screen.blit(self.hpBarBGBlue, (101, 62))

            # NAME/LEVEL
            activeName = self.playerActivePkmn.getName().upper()
            cpuName = self.cpuActivePkmn.getName().upper()

            activeNameTxt = self.hpFont.render(activeName, True, (245, 245, 245))
            activeNameTxtS = self.hpFont.render(activeName, True, (0, 0, 0))
            cpuNameTxt = self.hpFont.render(cpuName, True, (245, 245, 245))
            cpuNameTxtS = self.hpFont.render(cpuName, True, (0, 0, 0))

            # active pkmn
            screen.blit(activeNameTxtS, (305, 272))
            screen.blit(activeNameTxtS, (305, 274))
            screen.blit(activeNameTxtS, (304, 273))
            screen.blit(activeNameTxtS, (306, 273))
            screen.blit(activeNameTxt, (305, 273))

            # cpu pkmn
            screen.blit(cpuNameTxtS, (246, 72))
            screen.blit(cpuNameTxtS, (246, 74))
            screen.blit(cpuNameTxtS, (245, 73))
            screen.blit(cpuNameTxtS, (247, 73))
            screen.blit(cpuNameTxt, (246, 73))

            # HP BARS
            self.activeHPBar = BattleHPBar(self.playerActivePkmn.getLevel(), self.playerActivePkmn.getBattleStats()[0] - self.playerActivePkmn.getStatChanges()[0], 360, 300, self.playerActivePkmn.getBattleStats()[0])
            self.activeHPBar.draw(screen)
            self.cpuHPBar = BattleHPBar(self.cpuActivePkmn.getLevel(), self.cpuActivePkmn.getBattleStats()[0] - self.cpuActivePkmn.getStatChanges()[0], 300, 100, self.cpuActivePkmn.getBattleStats()[0])
            self.cpuHPBar.draw(screen)

            # ACITVE PKMN INFO
            # tiny icons
            plyrIcon = self.getTinyIcon(activeName)
            screen.blit(plyrIcon, (640, 25))
            cpuIcon = self.getTinyIcon(cpuName)
            screen.blit(cpuIcon, (640, 295))

            # print(self.cpuActivePkmn)
            otherDetails = ActiveBox(self.playerActivePkmn, self.cpuActivePkmn, (630, 15))
            otherDetails.draw(screen)

            # OTHER
            if self.chooseAction:
                screen.blit(self.chooseActionB, self.chooseActionBRect)

            elif self.pickMoves:
                for i in range(0, 4):
                    self.activeMoves = self.playerActivePkmn.getMoves()
                    mv = MoveBox(self.activeMoves[i], self.moveBoxCoords[i], (280, 90), self.typeIconsList, self.categoryIconsList)
                    mv.draw(screen)
            
            if self.viewParty:
                # GRID
                screen.blit(self.viewPartyBG, (0, 0))
                for i in range(0, 6):
                    if self.party[i] != None:
                        self.partyBoxList[i] = PartyBox(self.party[i], self.pkmnTypes[i][0],
                                                        self.pkmnTypes[i][1], self.partyCoords[i],
                                                        (292, 181), self.party[i].getIsActive(), self.party[i].getIsFainted())
                    else:
                        self.partyBoxList[i] = PartyBox(self.party[i], self.pkmnTypes[i][0],
                                                        self.pkmnTypes[i][1], self.partyCoords[i],
                                                        (292, 181), False, False)
                for box in self.partyBoxList:
                    box.draw(screen)

            if self.mightRun:
                screen.blit(self.checkRunIMG, (0, 0))

        # GAME OVER
        elif self.gameOver:
            if self.playerWon:
                screen.blit(self.playerWonBG, (0, 0))
            elif self.cpuWon:
                screen.blit(self.cpuWonBG, (0, 0))

    #########
    ## RUN ##
    #########
    def run(self):
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        # set the title of the window
        pygame.display.set_caption(self.title)

        # stores all the keys currently being held down
        self._keys = dict()
        
        # call game-specific initialization
        self.init()
        playing = True
        while playing:
            time = clock.tick(self.fps)
            self.timerFired(time)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.mousePressed(*(event.pos))
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.mouseReleased(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons == (0, 0, 0)):
                    self.mouseMotion(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons[0] == 1):
                    self.mouseDrag(*(event.pos))
                elif event.type == pygame.KEYDOWN:
                    self._keys[event.key] = True
                    self.keyPressed(event.key, event.mod)
                elif event.type == pygame.KEYUP:
                    self._keys[event.key] = False
                    self.keyReleased(event.key, event.mod)
                elif event.type == pygame.QUIT:
                    playing = False
                
                # TEXT INPUTS
                if self.selectPokemon1:
                    # name, level, moves
                    for txt in self.input1List:
                        txt.get_event(event)
                    # ev
                    for ev in self.inputEV1List:
                        ev.get_event(event)

                elif self.selectPokemon2:
                    # name, level, moves
                    for txt in self.input2List:
                        txt.get_event(event)
                    # ev
                    for ev in self.inputEV2List:
                        ev.get_event(event)

                elif self.selectPokemon3:
                    # name, level, moves
                    for txt in self.input3List:
                        txt.get_event(event)
                    # ev
                    for ev in self.inputEV3List:
                        ev.get_event(event)

                elif self.selectPokemon4:
                    # name, level, moves
                    for txt in self.input4List:
                        txt.get_event(event)
                    # ev
                    for ev in self.inputEV4List:
                        ev.get_event(event)

                elif self.selectPokemon5:
                    # name, level, moves
                    for txt in self.input5List:
                        txt.get_event(event)
                    # EVs
                    for ev in self.inputEV5List:
                        ev.get_event(event)

                elif self.selectPokemon6:
                    # name, level, moves
                    for txt in self.input6List:
                        txt.get_event(event)
                    # EVs
                    for ev in self.inputEV6List:
                        ev.get_event(event)
            
            # UPDATE SELECT PKMN BOXES
            if self.selectPokemon1:
                if self.inputSprite1 != None:
                    self.inputSprite1.update()
                # name, level, moves
                for txt in self.input1List:
                    txt.update()
                # ev
                for ev in self.inputEV1List:
                    ev.update()
            
            elif self.selectPokemon2:
                if self.inputSprite2 != None:
                    self.inputSprite2.update()
                # name, level, moves
                for txt in self.input2List:
                    txt.update()
                # ev
                for ev in self.inputEV2List:
                    ev.update()
            
            elif self.selectPokemon3:
                if self.inputSprite3 != None:
                    self.inputSprite3.update()
                # name, level, moves
                for txt in self.input3List:
                    txt.update()
                # ev
                for ev in self.inputEV3List:
                    ev.update()
            
            elif self.selectPokemon4:
                if self.inputSprite4 != None:
                    self.inputSprite4.update()
                # name, level, moves
                for txt in self.input4List:
                    txt.update()
                # ev
                for ev in self.inputEV4List:
                    ev.update()
            
            elif self.selectPokemon5:
                if self.inputSprite5 != None:
                    self.inputSprite5.update()
                # name, level, moves
                for txt in self.input5List:
                    txt.update()
                # EVs
                for ev in self.inputEV5List:
                    ev.update()
            
            elif self.selectPokemon6:
                if self.inputSprite6 != None:
                    self.inputSprite6.update()
                # name, level, moves
                for txt in self.input6List:
                    txt.update()
                # ev
                for ev in self.inputEV6List:
                    ev.update()

            if self.battleScreen == True:
                if self.playerActiveSprite != None:
                    self.playerActiveSprite.update()
                if self.cpuActiveSprite != None:
                    self.cpuActiveSprite.update()
            
            screen.fill(self.bgColor)
            self.redrawAll(screen)
            pygame.display.update()
            pygame.display.flip()
        pygame.quit()

game = BattleSimulator()
game.run()