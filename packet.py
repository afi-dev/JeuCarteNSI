from carte import Carte
from pile import Pile


class Packets_cartes:

    def __init__(self):
        self.liste_cartes = Pile()
        self.taille = 52

    def creation_packet(self):
        couleurs = ["pique", "coeur", "carreau", "trefle"]
        for couleur in couleurs:
            for valeur in range(2, 15):  # Les valeurs vont de 2 à 14 (As)
                carte = Carte(valeur, couleur)
                self.liste_cartes.empiler(carte)
        self.liste_cartes.empiler(Carte(15,"pique"))
        self.liste_cartes.empiler(Carte(15,"coeur"))
        self.liste_cartes.melanger()
        # self.liste_cartes.affiche()  # debug

    def est_vide(self):
		# Retourne True si le nombre de cartes dans le paquet est nul
        return self.liste_cartes.est_vide()
	
    def prendre_carte(self):
        return self.liste_cartes.depiler()