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
		# Initialisation de Pygame
		pygame.init()
		self.screen = pygame.display.set_mode((550, 550))
		self.clock = pygame.time.Clock()
		self.running = True
		self.window_name = "Jeu de Carte Pygame"
		self.player_pos = pygame.Vector2(self.screen.get_width() / 2,
		                                 self.screen.get_height() / 2)
		self.dt = 0

		# creation du statut de la partie
		self.statut_partie = 2  # 0 : menu ; 1 : manche en cours ; 2 : fin de manche ; 3 : fin de partie
		# pour le moment initialisé à 2 car aucune manche n'est lancée

		# On cree les joueurs
		self.player = Joueur()
		self.ordi = Joueur()

		# On créé les manches de jeu
		self.manches = [Pile(), Pile(), Pile()]
		self.manche_en_cours = 0
		self.manche_finie = True

		# On créé le paqquer puis les paquets de manches
		self.packet = Packets_cartes()
		self.packet.creation_packet()

		while not self.packet.est_vide():
			# On distribue les cartes
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
		# on retire les cartes gagnées pour redémarer
		self.player.reset_gagnee()
		self.ordi.reset_gagnee()
  
		# on distribue les cartes
		""" un for ne corresponsait pas car revenait à distribuer toutes les cartes du jeu """
		while not self.manches[self.manche_en_cours].est_vide():
			self.player.ajoute(self.manches[self.manche_en_cours].depiler())
			self.ordi.ajoute(self.manches[self.manche_en_cours].depiler())
		# on indique dans quelle manche on entre et que celle ci n'est donc pas finie
		self.manche_en_cours += 1
		self.statut_partie = 1 # statut_partie = manche en cours

	def gestion_manche(self):
		""" Gestion de la manche """
		# on effectue les comparaisons
		if not self.player.est_vide() and not self.ordi.est_vide():
			self.temp_carte_joueur = self.player.retire()
			self.temp_carte_ordi = self.ordi.retire()

			# on compare les cartes
			self.gagnant = self.comparaison_cartes(self.temp_carte_joueur,
			                                       self.temp_carte_ordi)

			if self.gagnant == 2:
				print("Ordi gagne contre joueur car : ", self.temp_carte_ordi, " > ",
				      self.temp_carte_joueur)
				self.ordi.ajoute_gagnee(self.temp_carte_joueur)
				self.ordi.ajoute_gagnee(self.temp_carte_ordi)

			elif self.gagnant == 1:
				print("Joueur gagne contre ordi car : ", self.temp_carte_joueur, " > ",
				      self.temp_carte_ordi)
				self.player.ajoute_gagnee(self.temp_carte_joueur)
				self.player.ajoute_gagnee(self.temp_carte_ordi)

	def fin_manche(self):
		""" regarde si la manche est finit et on effectue les verifications et modifications necessaires """
		if self.player.est_vide() or self.ordi.est_vide():
			if self.player.taille_gagnee() > self.ordi.taille_gagnee():
				print("😱 Joueur gagne cette manche")
				self.player.ajouter_score()

			else:
				print("😱 Ordi gagne cette manche")
				self.ordi.ajouter_score()

			if self.player.score > 1 or self.ordi.score > 1:
				self.statut_partie = 3 # statut_partie = jeu fini
			else:
				self.statut_partie = 2 # statut_partie = manche finie

	def fin_partie(self):
		""" fin de la partie apres les deux ou trois manches """
		if self.statut_partie == 0:
			if self.player.recuperer_score() > self.ordi.recuperer_score():
				print("🏆 Le joueur gagne la partie")

			else:
				print("🏆 L'ordinateur gagne la partie")

			self.statut_partie = 1


	def interaction(self):
		""" attends une interraction du joueur avant de finir """ 
		for event in pygame.event.get():
			return event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE

	def actualiser(self):
		""" met a jour les variables """
		if self.statut_partie == 2:
			# création de la manche
			self.debut_manche()
  
		if self.statut_partie == 1:
			# actualisation des manches
			self.gestion_manche()
			self.fin_manche()
   
		if self.statut_partie == 3:
			# actualisation de la fin de la partie
			self.fin_partie()

	def affichage(self):
		""" affichage du jeu pour pygame """
		if self.statut_partie == 0:
			pass

		elif self.statut_partie == 1:
			# on affiche les cartes a partir de l'arribut de l'objet carte
			self.screen.blit(self.temp_carte_joueur.image, (100, 100))
			self.screen.blit(self.temp_carte_ordi.image, (300, 100))

			# on affiche le texte selon le gagnant
			if self.gagnant == 2:
				self.screen.blit(
				 pygame.font.Font(None, 26).render("Joueur : Perd | Ordinateur : Gagne",
				                                   True, (0, 0, 0)), (100, 315))

			elif self.gagnant == 1:
				self.screen.blit(
				 pygame.font.Font(None, 26).render("Joueur : Gagne | Ordinateur : Perd",
				                                   True, (0, 0, 0)), (100, 315))

		elif self.statut_partie == 2:
			if self.player.taille_gagnee() > self.ordi.taille_gagnee():
				self.screen.blit(
					 pygame.font.Font(None, 26).render("Joueur a gagné la manche", True,
				                 	                  (0, 0, 0)), (100, 375))
    
			else:
				self.screen.blit(
					 pygame.font.Font(None, 26).render("Ordinateur a gagné la manche", True,
					                                   (0, 0, 0)), (100, 375))

		elif self.statut_partie == 3:
			# on affiche les cartes a partir de l'arribut de l'objet carte
			if self.player.recuperer_score() > self.ordi.recuperer_score():
				self.screen.blit(
				 pygame.font.Font(None, 26).render("Le joueur gagne la partie", True,
				                                   (0, 0, 0)), (100, 75))

			else:
				self.screen.blit(
				 pygame.font.Font(None, 26).render("L'ordinateur gagne la partie",
				                                   True, (0, 0, 0)), (100, 75))

		pygame.display.flip()

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

			# actualisation des variables
			self.actualiser()

			# affichage dans pygame
			self.affichage()

			# on attend l'interraction de l'utilisateur
			# pas propre mais sera remplacer par un vrai couldown
			action = False
			while not action:
				action = self.interaction()

			self.dt = self.clock.tick(60) / 1000


# _____ programme principal _____ #
Game = App()
Game.run()
