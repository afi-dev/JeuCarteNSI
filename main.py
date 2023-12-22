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

pour passez a l'ecrant suivant, appuyez sur la barre espace
"""
# interraction utilisateur avec le choix de jouer la carte ou non avant de voir la carte adverse en bonus

# _____ bibliotheques _____ #
import pygame
import pygame.font
from packet import Packets_cartes
from carte import Carte
from pile import Pile
from joueur import Joueur

# _____ Classes _____ #


class App:

    def __init__(self):
        """
Initialisation de la classe App
"""
        # Initialisation de Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((896, 560))
        self.clock = pygame.time.Clock()
        self.running = True
        self.window_name = "CardClash"
        self.dt = 0

        # creation du statut de la partie
        # 0 : menu ; 1 : manche en cours ; 2 : fin de manche ; 3 : fin de partie
        self.statut_partie = 0

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
        self.statut_partie = 1  # statut_partie = manche en cours

    def gestion_manche(self):
        """ Gestion de la manche """
        # on effectue les comparaisons
        if not self.player.est_vide() and not self.ordi.est_vide():
            self.temp_carte_joueur = self.player.retire()
            self.temp_carte_ordi = self.ordi.retire()

            # on compare les cartes
            self.gagnant = self.comparaison_cartes(self.temp_carte_joueur,
                                                   self.temp_carte_ordi)

            # si l'ordi gagne :
            if self.gagnant == 2:
                print("DEBUG: Ordi gagne contre joueur car : ", self.temp_carte_ordi, " > ",
                      self.temp_carte_joueur)
                self.ordi.ajoute_gagnee(self.temp_carte_joueur)
                self.ordi.ajoute_gagnee(self.temp_carte_ordi)

            # si le joueur gagne :
            elif self.gagnant == 1:
                print("DEBUG: Joueur gagne contre ordi car : ", self.temp_carte_joueur, " > ",
                      self.temp_carte_ordi)
                self.player.ajoute_gagnee(self.temp_carte_joueur)
                self.player.ajoute_gagnee(self.temp_carte_ordi)

    def fin_manche(self):
        """ regarde si la manche est finit et on effectue les verifications et modifications necessaires """
        if self.player.est_vide() or self.ordi.est_vide():
            if self.player.taille_gagnee() > self.ordi.taille_gagnee():
                print("DEBUG: Joueur gagne cette manche")
                self.player.ajouter_score()

            else:
                print("DEBUG: Ordi gagne cette manche")
                self.ordi.ajouter_score()

            if self.player.score > 1 or self.ordi.score > 1:
                self.statut_partie = 3  # statut_partie = jeu fini
            else:
                self.statut_partie = 2  # statut_partie = manche finie

    def fin_jeu(self):
        """ si la partie est finit on remet les scores a 0 et on recommence """
        self.manche_en_cours = 0
        self.player.score = 0
        self.ordi.score = 0
        # on créé un nouveau packet
        self.packet.creation_packet()
        # on créé les manches
        self.manches = [Pile(), Pile(), Pile()]
        # on distribue les cartes
        while not self.packet.est_vide():
            for manche in self.manches:
                manche.empiler(self.packet.prendre_carte())

    def actualiser(self):
        """ met a jour les variables si le joueur appuie sur espace """
        if self.statut_partie == 0:
            self.statut_partie = 2

        if self.statut_partie == 2:
            # création de la manche
            self.debut_manche()

        if self.statut_partie == 1:
            # actualisation des manches
            self.fin_manche()
            self.gestion_manche()

        elif self.statut_partie == 3:
            # si la partie est finie on revient au menu et on rénitilise
            self.fin_jeu()
            self.statut_partie = 0  # statut_partie = debut partie

    def affichage(self):
        """ affichage du jeu pour pygame """
        # on vide la fenetre
        self.screen.fill("#E4EDF8")
        if self.statut_partie == -1:

            self.screen.blit(pygame.font.Font('fonts/parchment.ttf', 80).render(
                "Régles du jeux", True, "#000000"), (self.screen.get_width() / 2 - 420,
                                                     self.screen.get_height() / 2 - 250))

            self.screen.blit(pygame.font.Font('fonts/pridi-semibold.ttf', 12).render(
                "CardClash est un jeu qui s'inspire du jeu de carte traditionnel de la bataille, il est cependant plus simple et plus rapide que le jeu de carte", True, "#000000"), (self.screen.get_width() / 2 - 420,
                                                                                                                                                                                      self.screen.get_height() / 2 - 140))

            self.screen.blit(pygame.font.Font('fonts/pridi-semibold.ttf', 12).render(
                "traditionnel car on divise le paquet en trois tas égaux, chaque tas correspond à une manche, on distribue alors aux deux joueurs un nombre", True, "#000000"), (self.screen.get_width() / 2 - 420, self.screen.get_height() / 2 - 120))
            self.screen.blit(pygame.font.Font('fonts/pridi-semibold.ttf', 12).render(
                "de cartes égal au nombre de manche, une par une, on retourne les cartes en même temps, le joueur qui a la carte la plus élevée gagne un", True, "#000000"), (self.screen.get_width() / 2 - 420, self.screen.get_height() / 2 - 100))
            self.screen.blit(pygame.font.Font('fonts/pridi-semibold.ttf', 12).render("point, le joueur qui à le plus de points à la fin de la manche remporte la manche. Si les deux joueurs ont le même nombre de points à la fin",
                             True, "#000000"), (self.screen.get_width() / 2 - 420, self.screen.get_height() / 2 - 80))
            self. screen.blit(pygame.font.Font('fonts/pridi-semibold.ttf', 12).render("des deux manches, on determine le gagnant avec la troisième manche. Le gagnant est celui qui a remporté le plus de manches.",
                              True, "#000000"), (self.screen.get_width() / 2 - 420, self.screen.get_height() / 2 - 60))
            self.screen.blit(pygame.font.Font('fonts/pridi-semibold.ttf', 12).render("L'ordre des cartes sont : l'as, le roi, la dame, le valet, le 10, le 9, le 8, le 7, le 6, le 5, le 4, le 3, le 2. Il y a également un niveau de couleur, du",
                                                                                     True, "#000000"), (self.screen.get_width() / 2 - 420, self.screen.get_height() / 2 - 20))
            self.screen.blit(pygame.font.Font('fonts/pridi-semibold.ttf', 12).render("plus faible au plus fort : coeur, carreau, trefle, pique afin de déterminer le gagnant en cas d'égalité de valeur de carte.",
                                                                                     True, "#000000"), (self.screen.get_width() / 2 - 420, self.screen.get_height() / 2 - 0))
            self.screen.blit(pygame.font.Font('fonts/pridi-semibold.ttf', 12).render("Entre chaque manche, vous pouvez appuyer sur la barre espace pour passer à la manche suivante.",
                                                                                     True, "#000000"), (self.screen.get_width() / 2 - 420, self.screen.get_height() / 2 + 40))
            pygame.draw.rect(self.screen, (255, 255, 255), (self.screen.get_height(
            ) / 2 + 45, self.screen.get_height() / 2 + 125, 250, 30))
            self.screen.blit(pygame.font.Font('fonts/pridi-semibold.ttf', 20).render("Retour au menu principal",
                             True, "#000000"), (self.screen.get_width() / 2 - 115, self.screen.get_height() / 2 + 125))

        elif self.statut_partie == 0:
            picture = pygame.image.load("images/main.png")
            picture = pygame.transform.scale(picture, (896, 560))
            self.screen.blit(picture, (0, 0, 100, 100))

            # Titre du jeu

            pygame.draw.rect(self.screen, (255, 255, 255), (self.screen.get_height(
            ) / 2 + 140, self.screen.get_height() / 2 + 75, 70, 30))
            self.screen.blit(pygame.font.Font('fonts/pridi-semibold.ttf', 22).render(
                "Jouer", True, "#000000"), (self.screen.get_width() / 2 - 22,
                                            self.screen.get_height() / 2 + 72))

            pygame.draw.rect(self.screen, (255, 255, 255), (self.screen.get_height(
            ) / 2 + 135, self.screen.get_height() / 2 + 125, 80, 30))
            self.screen.blit(pygame.font.Font('fonts/pridi-semibold.ttf', 22).render(
                "Régles", True, "#000000"), (self.screen.get_width() / 2 - 26,
                                             self.screen.get_height() / 2 + 122))

            pygame.draw.rect(self.screen, (255, 255, 255), (self.screen.get_height(
            ) / 2 + 98, self.screen.get_height() / 2 + 175, 156, 30))
            self.screen.blit(pygame.font.Font('fonts/pridi-semibold.ttf', 22).render(
                "Quitter le jeu", True, "#000000"), (self.screen.get_width() / 2 - 63,
                                                     self.screen.get_height() / 2 + 172))

            self.screen.blit(pygame.font.Font('fonts/parchment.ttf', 175).render(
                "CardClash", True, "#000000"), (self.screen.get_width() / 2 - 250,
                                                self.screen.get_height() / 2 - 210))

            # Texte avant le nom des créateurs
            self.screen.blit(pygame.font.Font('fonts/pridi-semibold.ttf', 13).render(
                "Un jeu réalisé par", True, "#000000"), (self.screen.get_width() / 2 - 45,
                                                         self.screen.get_height() / 2 - 25))

            # Texte des créateurs
            self.screen.blit(pygame.font.Font('fonts/pridi-bold.ttf', 16).render(
                "Simon Cohet et Kaelian Baudelet", True, "#000000"), (self.screen.get_width() / 2 - 115,
                                                                      self.screen.get_height() / 2 + 5))

        elif self.statut_partie == 1:
            # affichage des cartes de la manche en cours
            self.screen.blit(self.temp_carte_joueur.image, (100, 100))
            self.screen.blit(self.temp_carte_ordi.image, (590, 100))

            # affichage des scores de la manche en cours
            self.screen.blit(
                pygame.font.Font('fonts/pridi-semibold.ttf', 26).render("joueur : {}".format(self.player.taille_gagnee()),
                                                                        True, (0, 0, 0)), (150, 450))

            self.screen.blit(
                pygame.font.Font('fonts/pridi-semibold.ttf', 26).render("ordi : {}".format(self.ordi.taille_gagnee()),
                                                                        True, (0, 0, 0)), (650, 450))

            # on affiche le texte selon le gagnant
            if self.gagnant == 2:
                self.screen.blit(
                    pygame.font.Font('fonts/pridi-semibold.ttf', 26).render("Joueur : Perd | Ordinateur : Gagne",
                                                                            True, (0, 0, 0)), (250, 400))

            elif self.gagnant == 1:
                self.screen.blit(
                    pygame.font.Font('fonts/pridi-semibold.ttf', 26).render("Joueur : Gagne | Ordinateur : Perd",
                                                                            True, (0, 0, 0)), (250, 400))

        elif self.statut_partie == 2:
            # affichage du gagnant de la manche

            # affichage des scores de la partie en cours
            self.screen.blit(
                pygame.font.Font('fonts/pridi-semibold.ttf', 26).render("joueur : {}".format(self.player.score),
                                                                        True, (0, 0, 0)), (100, 450))

            self.screen.blit(
                pygame.font.Font('fonts/pridi-semibold.ttf', 26).render("ordi : {}".format(self.ordi.score),
                                                                        True, (0, 0, 0)), (700, 450))

            # on cree une coupe a afficher
            cup = pygame.image.load("images/2nd-place.png")
            cup = pygame.transform.scale(cup, (200, 200))

            if self.player.taille_gagnee() > self.ordi.taille_gagnee():
                # si le joueur gagne
                # on affiche la "main" du joueur
                hand = pygame.image.load("images/human_hand.png")
                hand = pygame.transform.scale(hand, (256, 127.5))
                self.screen.blit(hand, (0, 300, 100, 100))
                # puis la coupe
                self.screen.blit(cup, (50, 100, 100, 100))
                # et enfin le texte
                self.screen.blit(
                    pygame.font.Font('fonts/pridi-semibold.ttf', 26).render("Joueur a gagné la manche", True,
                                                                            (0, 0, 0)), (285, 250))

            else:
                # si l'ordi gagne
                # on affiche la "main" de l'ordi
                hand = pygame.image.load("images/robot_hand.png")
                hand = pygame.transform.scale(hand, (256, 127.5))
                self.screen.blit(hand, (640, 300, 100, 100))
                # puis la coupe
                self.screen.blit(cup, (620, 100, 100, 100))
                # et enfin le texte
                self.screen.blit(
                    pygame.font.Font('fonts/pridi-semibold.ttf', 26).render("Ordinateur a gagné la manche", True,
                                                                            (0, 0, 0)), (285, 250))

        elif self.statut_partie == 3:
            # affichage de la fin de la partie

            # affichage des scores de la partie finie
            self.screen.blit(
                pygame.font.Font('fonts/pridi-semibold.ttf', 26).render("joueur : {}".format(self.player.score),
                                                                        True, (0, 0, 0)), (100, 450))

            self.screen.blit(
                pygame.font.Font('fonts/pridi-semibold.ttf', 26).render("ordi : {}".format(self.ordi.score),
                                                                        True, (0, 0, 0)), (700, 450))

            # on cree une coupe a afficher
            cup = pygame.image.load("images/1st-prize.png")
            cup = pygame.transform.scale(cup, (200, 200))

            if self.player.recuperer_score() > self.ordi.recuperer_score():
                # si le joueur gagne
                # on affiche la "main" du joueur
                hand = pygame.image.load("images/human_hand.png")
                hand = pygame.transform.scale(hand, (256, 127.5))
                self.screen.blit(hand, (0, 300, 100, 100))
                # puis la coupe
                self.screen.blit(cup, (50, 100, 100, 100))
                # et enfin le texte
                self.screen.blit(
                    pygame.font.Font('fonts/pridi-semibold.ttf', 26).render("Le joueur gagne la partie", True,
                                                                            (0, 0, 0)), (285, 250))

            else:
                # si l'ordi gagne
                # on affiche la "main" de l'ordi
                hand = pygame.image.load("images/robot_hand.png")
                hand = pygame.transform.scale(hand, (256, 127.5))
                self.screen.blit(hand, (640, 300, 100, 100))
                # puis la coupe
                self.screen.blit(cup, (620, 100, 100, 100))
                # et enfin le texte
                self.screen.blit(
                    pygame.font.Font('fonts/pridi-semibold.ttf', 26).render("L'ordinateur gagne la partie", True,
                                                                            (0, 0, 0)), (285, 250))

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
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and self.statut_partie == -1:
                    self.statut_partie = 0
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.actualiser()
                elif self.statut_partie == 0 and pygame.mouse.get_pos()[0] > 418 and pygame.mouse.get_pos()[0] < 490 and pygame.mouse.get_pos()[1] > 355 and pygame.mouse.get_pos()[1] < 388 and pygame.mouse.get_pressed()[0]:
                    # debut de la partie
                    self.actualiser()
                elif self.statut_partie == 0 and pygame.mouse.get_pos()[0] > 413 and pygame.mouse.get_pos()[0] < 496 and pygame.mouse.get_pos()[1] > 405 and pygame.mouse.get_pos()[1] < 438 and pygame.mouse.get_pressed()[0]:
                    self.statut_partie = -1
                elif self.statut_partie == 0 and pygame.mouse.get_pos()[0] > 377 and pygame.mouse.get_pos()[0] < 536 and pygame.mouse.get_pos()[1] > 440 and pygame.mouse.get_pos()[1] < 487 and pygame.mouse.get_pressed()[0]:
                    self.running = False
                elif self.statut_partie == -1 and pygame.mouse.get_pos()[0] > 325 and pygame.mouse.get_pos()[0] < 575 and pygame.mouse.get_pos()[1] > 405 and pygame.mouse.get_pos()[1] < 438 and pygame.mouse.get_pressed()[0]:
                    self.statut_partie = 0

            # affichage dans pygame
            self.affichage()

            self.dt = self.clock.tick(60) / 1000


pygame_icon = pygame.image.load("images/icon.png")
pygame.display.set_icon(pygame_icon)

# _____ programme principal _____ #
Game = App()
Game.run()
