import pygame as pg
import tkinter as tk
from classes.external_modules.textbox import *

class DictBox:
	def __init__(self, topLeft, dim, content, compareText = []):
		self.topLeft = topLeft
		self.boxDim = pg.Rect(topLeft, dim)
		self.content = content # content is a set
		self.compareText = compareText # taken from whatever's being typed in TextBox object

		self.font = pg.font.SysFont("FuturaStd-Book", 12)

		self.dictScreen = pg.Surface((950, 600), pg.SRCALPHA, 32)
		self.dictScreen = self.dictScreen.convert_alpha()

	def draw(self, screen):
		pg.draw.rect(screen, (230, 230, 230), self.boxDim)
		yTxt = self.topLeft[1]
		# if self.compareText != []:
		for name in self.content:
			nameList = list(name.lower())
			count = 0
			cmprTxt = []
			for i in self.compareText:
				if i != "":
					cmprTxt.append(i)
			for letter in cmprTxt:
				letter = letter.lower()
				if count > len(nameList) - 1:
					break
				elif nameList[count] == letter:
					count += 1
				else:
					break
				if count == len(cmprTxt):
					screen.blit(self.font.render(name, True, (0, 0, 0)),
									(self.topLeft[0] + 10, yTxt + 10))
					yTxt += 15

class MoveDictBox(DictBox):
	def __init__(self, topLeft, dim, content, compareText = [], moves = []):
		super().__init__(topLeft, dim, content, compareText)
		self.moves = moves

	def draw(self, screen):
		pg.draw.rect(screen, (230, 230, 230), self.boxDim)
		yTxt = self.topLeft[1]
		# if self.compareText != []:
		for name in self.content:
			nameList = list(name.lower())
			count = 0
			cmprTxt = []
			for i in self.compareText:
				if i != "":
					cmprTxt.append(i)
			for letter in cmprTxt:
				letter = letter.lower()
				if count > len(nameList) - 1:
					break
				elif nameList[count] == letter:
					count += 1
				else:
					break
				if count == len(cmprTxt):
					if name not in self.moves:
						screen.blit(self.font.render(name, True, (0, 0, 0)),
									(self.topLeft[0] + 10, yTxt + 10))
					else:
						screen.blit(self.font.render(name, True, (153, 0, 0)),
									(self.topLeft[0] + 10, yTxt + 10))
					yTxt += 15