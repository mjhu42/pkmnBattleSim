import pygame as pg

class hpBar:
	def __init__(self, lv, hp, cx, cy):
		self.lv = lv
		self.hp = hp
		self.cx = cx
		self.cy = cy

	def draw(self, screen):
		# background stuff
		bg = pg.image.load("classes/imgs/hp_bar_bg.png")
		barBG = pg.image.load("classes/imgs/hp_bar_gray.png")
		bgRect = bg.get_rect(center = (self.cx, self.cy))
		barBGRect = barBG.get_rect(center = (self.cx - 5, self.cy - 4))
		screen.blit(bg, bgRect)
		screen.blit(barBG, barBGRect)

		# actual hp rep
		hpBar = pg.Rect((self.cx - 48, self.cy - 7), (86, 6))
		pg.draw.rect(screen, (95, 255, 45), hpBar)

		# outline hp bar
		outline = pg.image.load("classes/imgs/hp_bar.png")
		outlineRect = outline.get_rect(center = (self.cx - 5, self.cy - 4))
		screen.blit(outline, outlineRect)

		# text
		pg.font.init()
		font = pg.font.SysFont("Gameplay Regular", 6)
		font2 = pg.font.SysFont("Gameplay Regular", 7)

		lvTxt = font2.render("Lv .  " + str(self.lv), True, (245, 245, 245))
		lvTxtShad = font2.render("Lv .  " + str(self.lv), True, (0, 0, 0))
		hpTxt = font.render(str(self.hp) + " / " + str(self.hp), True, (245, 245, 245))
		hpTxtShad = font.render(str(self.hp) + " / " + str(self.hp), True, (0, 0, 0))

		lvTxtRect = lvTxt.get_rect(topright = (self.cx + 54, self.cy - 24))
		lvShadRect1 = lvTxt.get_rect(topright = (self.cx + 54, self.cy - 23))
		lvShadRect2 = lvTxt.get_rect(topright = (self.cx + 55, self.cy - 24))
		lvShadRect3 = lvTxt.get_rect(topright = (self.cx + 53, self.cy - 24))
		lvShadRect4 = lvTxt.get_rect(topright = (self.cx + 54, self.cy - 25))
		lvShadList = [lvShadRect4, lvShadRect3, lvShadRect2, lvShadRect1]
		hpTxtRect = hpTxt.get_rect(topright = (self.cx + 40, self.cy + 2))
		hpShadRect = hpTxtShad.get_rect(topright = (self.cx + 41, self.cy + 3))

		for i in lvShadList:
			screen.blit(lvTxtShad, i)
		screen.blit(lvTxt, lvTxtRect)
		screen.blit(hpTxtShad, hpShadRect)
		screen.blit(hpTxt, hpTxtRect)

class BattleHPBar(hpBar):
	def __init__(self, lv, hp, cx, cy, maxHP):
		super().__init__(lv, hp, cx, cy)
		self.maxHP = maxHP

	def draw(self, screen):
		# background stuff
		bg = pg.image.load("classes/imgs/hp_bar_bg.png")
		barBG = pg.image.load("classes/imgs/hp_bar_gray.png")
		bgRect = bg.get_rect(center = (self.cx, self.cy))
		barBGRect = barBG.get_rect(center = (self.cx - 5, self.cy - 4))
		screen.blit(bg, bgRect)
		screen.blit(barBG, barBGRect)

		# actual hp rep
		pctHPLeft = self.hp / self.maxHP
		hpBar = pg.Rect((self.cx - 48, self.cy - 7), (86 * pctHPLeft, 6))
		if pctHPLeft <= 0.5 and pctHPLeft > 0.2:
			pg.draw.rect(screen, (249, 205, 32), hpBar)
		elif pctHPLeft <= 0.2:
			pg.draw.rect(screen, (250, 0, 0), hpBar)
		else:
			pg.draw.rect(screen, (95, 255, 45), hpBar)

		# outline hp bar
		outline = pg.image.load("classes/imgs/hp_bar.png")
		outlineRect = outline.get_rect(center = (self.cx - 5, self.cy - 4))
		screen.blit(outline, outlineRect)

		pg.font.init()
		font = pg.font.SysFont("Gameplay Regular", 6)

		hpTxt = font.render(str(self.hp) + " / " + str(self.maxHP), True, (245, 245, 245))
		hpTxtShad = font.render(str(self.hp) + " / " + str(self.maxHP), True, (0, 0, 0))

		hpTxtRect = hpTxt.get_rect(topright = (self.cx + 40, self.cy + 2))
		hpShadRect = hpTxtShad.get_rect(topright = (self.cx + 41, self.cy + 3))

		screen.blit(hpTxtShad, hpShadRect)
		screen.blit(hpTxt, hpTxtRect)