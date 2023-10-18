# ____ bibliotheques ____ #
from random import shuffle


# _____ classe _____ #
class Pile:

	def __init__(self):
		self.pile = []

	def est_vide(self):
		return len(self.pile) == 0

	def empiler(self, element):
		self.pile.append(element)

	def depiler(self):
		return self.pile.pop()

	def melanger(self):
		shuffle(self.pile)

	def affiche(self):
		for element in self.pile:
			print(str(element))

	def vider(self):
		self.pile = []
