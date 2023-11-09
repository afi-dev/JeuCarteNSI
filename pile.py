# ____ bibliotheques ____ #
from random import shuffle


# _____ classe _____ #
class Pile:
	
	def __init__(self):
		""" cree une pile vide """
		self.pile = []

	def est_vide(self):
		""" renvoie True si la pile est vide, False sinon """
		return len(self.pile) == 0

	def longueur(self):
		""" renvoie la longueur de la pile """
		return len(self.pile)

	def empiler(self, element):
		""" empile l'element """
		self.pile.append(element)

	def depiler(self):
		""" depile l'element et le renvoi """
		return self.pile.pop()

	def melanger(self):
		""" melange l'ordre de la pile aleatoirement"""
		shuffle(self.pile)

	def affiche(self):
		""" affiche la pile (facilite la correction de bug)"""
		for element in self.pile:
			print(str(element))

	def vider(self):
		""" retire tout les elements de la pile """
		self.pile = []
