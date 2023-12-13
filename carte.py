import pygame

# ____ classes ____ #
class Carte:

	def __init__(self, valeur: int, couleur: str):
		""" initie la classe carte :
        valeur est un int compris entre 2 et 13 
        de 2 a 10 : la valeur est le numero de la carte
        11 : valet
        12 : dame
        13 : roi
        14 : as

        couleur est un string soit coeur, pique, trefle ou carreau
        """
		self.valeur = valeur
		self.couleur = couleur
		# cree l'objet pygame image correspondant a la carte
		if self.valeur != 0:
			self.image = pygame.image.load("./images/{}-{}.png".format(self.valeur_naturelle(), self.couleur))

	def __str__(self) -> str:
		"""return la représentation de la carte sous forme de string"""
		return "{} de {}".format(self.valeur_naturelle(), self.couleur)

	def get_valeur(self) -> int:
		"""return la valeur de la carte"""
		return self.valeur
		
	def get_couleur(self) -> str:
		"""return la couleur de la carte"""
		return self.couleur
		
	def valeur_naturelle(self) -> str:
		"""return la valeur naturelle de la carte sous forme de string""" ""
		if self.valeur <= 10:
			return str(self.valeur)
		elif self.valeur == 11:
			return "valet"
		elif self.valeur == 12:
			return "reine"
		elif self.valeur == 13:
			return "roi"
		elif self.valeur == 14:
			return "as"
		return "joker"

	def couleur_numerique(self):
		""" return un nombre correspondant a la valeur de la couleur de la carte correspondante """
		if self.couleur == "coeur":
			return 1
		elif self.couleur == "carreau":
			return 2
		elif self.couleur == "trefle":
			return 3
		elif self.couleur == "pique":
			return 4
