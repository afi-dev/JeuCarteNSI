from pile import Pile


# _____ classe _____ #
class Joueur():

	def __init__(self):
		""" le joueur possede une pile de cartes qui sera utilisée pour jouer et une autre pile qui sera utilisee pour stocket les cartes gagnees """
		self.cartes = Pile()
		self.cartes_gagnee = Pile()
		self.score = 0

	def ajoute(self, element):
		""" ajoute une carte au paquet de jeu """
		self.cartes.empiler(element)

	def ajoute_gagnee(self, element):
		"""  ajoute une carte au paquet des cartes gagnées """
		self.cartes_gagnee.empiler(element)

	def retire(self):
		""" retire une carte du paquet de jeu """
		return self.cartes.depiler()

	def retire_gagnee(self):
		""" retire une carte du paquet des cartes gagnées  """
		return self.cartes_gagnee.depiler()

	def taille_gagnee(self):
		""" renvoie la taille du paquet des cartes gagnées """
		return self.cartes_gagnee.longueur()

	def reset_gagnee(self):
		""" vide le paquet des cartes gagnées """
		while not self.cartes_gagnee.est_vide():
			self.cartes_gagnee.depiler()

	def est_vide(self):
		""" renvoie True si le paquet de jeu est vide, False sinon """
		return len(self.cartes.pile) == 0

	def ajouter_score(self):
		""" incremente le score """
		self.score += 1

	def recuperer_score(self):
		""" renvoie le score  """
		return self.score
