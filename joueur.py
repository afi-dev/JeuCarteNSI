from pile import Pile


# _____ classe _____ #
class Joueur():

	def __init__(self):
		""" le joueur possede une pile de cartes qui sera utilisée pour jouer et une autre pile qui sera utilisee pour stocket les cartes gagnees """
		
		self.cartes = Pile()
		self.cartes_gagnee = Pile()
		self.score = 0

	def ajoute(self, element):
		self.cartes.empiler(element)

	def ajoute_gagnee(self, element):
		self.cartes_gagnee.empiler(element)

	def retire(self):
		return self.cartes.depiler()

	def retire_gagnee(self):
		return self.cartes_gagnee.depiler()

	def taille_gagnee(self):
		# depile puis rempile pour calculer la taille de la pile
		return self.cartes_gagnee.longueur()

	def reset_gagnee(self):
		while not self.cartes_gagnee.est_vide():
			self.cartes_gagnee.depiler()

	def vider_gagnee(self):
		self.cartes_gagnee.vider()

	def est_vide(self):
		if len(self.cartes.pile) == 0:
			return True
		return False

	def ajouter_score(self):
		self.score += 1
	
	def recuperer_score(self):
		return self.score