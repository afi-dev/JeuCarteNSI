"""					_                              
				   | |                             
   ___ __ _ _ __ __| |   __ _  __ _ _ __ ___   ___ 
  / __/ _` | '__/ _` |  / _` |/ _` | '_ ` _ \ / _ \
 | (_| (_| | | | (_| | | (_| | (_| | | | | | |  __/
  \___\__,_|_|  \__,_|  \__, |\__,_|_| |_| |_|\___|
						 __/ |                     
						|___/             

rêgles du jeu :
 - on divise le paquet en trois tas égaux
 - on prends le premier tas et on distribue aux deux joueurs
 - une par une, on retourne les cartes en même temps, le joueur qui a la carte la plus élevée gagne les cartes
 - le joueur qui à le plus de nombre de carte à la fin de la manche remporte un point
 - on recommence avec la deuxième manche
 - en cas d'égualité à la fin des deux manches on recommence avec la troisième manche
 le gagnant est celui qui a remporté le plus de manches
"""
# _____ bibliotheques _____ #
import pygame
import pygame.font
from packet import Packets_cartes
from pile import Pile
from joueur import Joueur
import time


# _____ Classes _____ #
class App:

	def __init__(self):
		"""
  		Initialisation de la classe App
		"""
		# pygame setup
		pygame.init()
		self.screen = pygame.display.set_mode((1280, 720))
		self.clock = pygame.time.Clock()
		self.running = True
		self.statut_partie = 0
		self.window_name = "Jeu de Carte Pygame"
		self.player_pos = pygame.Vector2(self.screen.get_width() / 2,
		                                 self.screen.get_height() / 2)
		self.dt = 0

		# on cree les joueurs
		self.player = Joueur()
		self.ordi = Joueur()

		# on créé les manches de jeu
		self.manches = [Pile(), Pile(), Pile()]
		self.manche_en_cours = 0
		self.manche_finie = True
  
		# on créé le paqquer puis les paquets de manches
		self.packet = Packets_cartes()
		self.packet.creation_packet()

		while not self.packet.est_vide():
			# on distribue les cartes
			for manche in self.manches:
				manche.empiler(self.packet.prendre_carte())

	def comparaison_cartes(self, carte1, carte2) -> int:
		""" compare deux objets carte  d'abord par leurs valeur et, en cas d'egalite, par leur couleurs
	    ordre des couleurs de la plus nulle a la plus forte : coeur, carreau, trefle, pique 
	    elle return le numero de la carte gagnante (1 ou 2)
	    """
		if carte1.get_valeur() > carte2.get_valeur():
			return 1
		elif carte1.get_valeur() < carte2.get_valeur():
			return 2
		elif carte1.couleur_numerique() > carte2.couleur_numerique():
			return 1
		elif carte1.couleur_numerique() < carte2.couleur_numerique():
			return 2

	def debut_manche(self):
		""" initialise la manche à jouer si la manche précédente est finit ou est la première """
		if self.manche_finie == True and self.statut_partie == 0:
			# on distribue les cartes
			for manche in self.manches:
				while not manche.est_vide():
					self.player.ajoute(manche.depiler())
					self.ordi.ajoute(manche.depiler())
			# on indique dans quelle manche on entre et que celle ci n'est donc pas finie
			self.manche_en_cours += 1
			self.manche_finie = False


	def gestion_manche(self):
		""" Gestion de la manche """

		# on effectue les comparaisons
		while not self.player.est_vide() and not self.ordi.est_vide():
			self.temp_carte_joueur = self.player.retire()
			self.temp_carte_ordi = self.ordi.retire()

			self.screen.fill((255, 255, 255))
			#dessine le texte joueur:
			self.screen.blit(
				pygame.font.Font(None, 26).render("Joueur :", True, (0, 0, 0)),
				(100, 75))
			self.screen.blit(
			#dessine le texte de l'ordinateur:
				pygame.font.Font(None, 26).render("Ordinateur :", True, (0, 0, 0)),
				(300, 75))
			# on affiche les cartes a partir de l'arribut de l'objet carte
			self.screen.blit(self.temp_carte_joueur.image, (100, 100))
			self.screen.blit(self.temp_carte_ordi.image, (300, 100))
			time.sleep(2.5)  # pas propre mais sera remplacer par un vrai couldown
			# on compare les cartes
			self.gagnant = self.comparaison_cartes(self.temp_carte_joueur, self.temp_carte_ordi)

			if self.gagnant == 2:
				print("Ordi gagne contre joueur car : ", self.temp_carte_ordi, " > ",
						self.temp_carte_joueur)
				self.ordi.ajoute_gagnee(self.temp_carte_joueur)
				self.ordi.ajoute_gagnee(self.temp_carte_ordi)
				self.screen.blit(
					pygame.font.Font(None,
									26).render("Joueur : Perdu | Ordinateur : Gagner",
												True, (0, 0, 0)), (100, 315))

			elif self.gagnant == 1:
				print("Joueur gagne contre ordi car : ", self.temp_carte_joueur, " > ",
						self.temp_carte_ordi)
				self.player.ajoute_gagnee(self.temp_carte_joueur)
				self.player.ajoute_gagnee(self.temp_carte_ordi)
				self.screen.blit(
					pygame.font.Font(None,
									26).render("Joueur : Gagner | Ordinateur : Perdu",
												True, (0, 0, 0)), (100, 315))

	def fin_manche(self):
		""" regarde si la manche est finit et on effectue les verifications et modifications necessaires """
		if self.player.est_vide() or self.ordi.est_vide():
			if self.player.taille_gagnee() > self.ordi.taille_gagnee():
				print("😱 Joueur gagne cette manche")
				self.player.ajouter_score()
				self.player.reset_gagnee()
				self.screen.blit(
					pygame.font.Font(None, 26).render("Joueur à gagner la manche", True,
													(0, 0, 0)), (100, 375))
			else:
				print("😱 Ordi gagne cette manche")
				self.ordi.ajouter_score()
				self.ordi.reset_gagnee()
				self.screen.blit(
					pygame.font.Font(None, 26).render("Ordinateur à gagner la manche", True,
													(0, 0, 0)), (100, 375))

			self.manche_finie = True

	def fin_partie(self):
		""" fin de la partie apres les deux ou trois manches """
		if self.statut_partie == 0:
			if self.player.recuperer_score() > self.ordi.recuperer_score():
				print("🏆 Le joueur gagne la partie")
				self.screen.fill((255, 255, 255))
				self.screen.blit(
					pygame.font.Font(None, 26).render("Joueur à gagner les 3 manches !!!!",
													True, (0, 0, 0)), (100, 75))
				pygame.display.flip()
				self.statut_partie = 1

			else:
				print("🏆 L'ordinateur gagne la partie")
				self.screen.fill((255, 255, 255))
				self.screen.blit(
					pygame.font.Font(None,
									26).render("Ordinateur à gagner les 3 manches !!!!",
												True, (0, 0, 0)), (100, 75))
				pygame.display.flip()
				self.statut_partie = 1
    
    def affichage(self):
 
	def run(self):
		"""
		Fonction principale du jeu
		"""
		pygame.display.set_caption(self.window_name)
		while self.running:
			# poll for events
			# pygame.QUIT event means the user clicked X to close your window
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False

			# fill the screen with a color to wipe away anything from last frame
			self.screen.fill("white")

			# gestion des manches
			self.debut_manche()
			self.gestion_manche()
			self.fin_manche()
			self.fin_partie()

			# flip() the display to put your work on screen

			self.dt = self.clock.tick(60) / 1000

			pygame.display.flip()


# _____ programme principal _____ #
Game = App()
Game.run()
