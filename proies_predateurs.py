##############################################################
# Groupe BI TD2                                              #
# Guillaume EMERDJIAN                                        #
# Victor DE BAETS                                            #
# Léa OSTER                                                  #
# Maxime BOUAMRA                                             #
# https://github.com/uvsq22107719/projet-2-proies-predateurs #
##############################################################

### Import des librairies

import tkinter as tk
import random as rd



### Définitions des constantes

N = 30 # Taille de la matrice
HAUTEUR = 700 # Hauteur du canevas
LARGEUR = 600 # Largeur du canevas
LARGEUR_CASE = 20 # Largeur des cases
HAUTEUR_CASE = LARGEUR_CASE # Hauteur des cases

CHRONO = 500 # Temps en millisecondes entre chaque tour

MIAM = 5 # Niveau d'énergie gagné lorsqu'un prédateur mange une proie
FLAIR_PRE = 5 # Nombre maximal de cases pour qu'un prédateur puisse sentir une proie et la pourchasser
FLAIR_PRO = 2 # Nombre maximal de cases pour qu'une proie puisse sentir un prédateur et fuir



### Définitions des variables globales

tour = 0 # Numéro du tour
arret = True # Variable pour arrêter le passage des tours
var_chrono = 0 # Variable pour le compte à rebours entre chaque tour

Npro = 50 # Nombre initial de proies (Npro proies apparaissent au début)
Apro = 10 # Espérance de vie des proies en nombre de tours
Epro = 2 # Énergie des proies (augmente de 1 par tour avec Epro en plafond. Une énergie maximale (égale à Epro) est nécessaire pour qu'une proie puisse se reproduire. Epro revient à 0 à chaque reproduction.)

Npre = 3 # Nombre initial de prédateurs (Npre prédateurs apparaissent au début)
Apre = 15 # Espérance de vie des prédateurs en nombre de tours
Epre = 10 # Énergie des prédateurs (baisse de 1 par tour, s'il elle atteint zéro, le prédateur meurt de faim)
Erepro = 15 # Niveau d'énergie nécessaire pour qu'un prédateur puisse se reproduire

sauv_validee = False # Variable pour afficher si la matrice actuelle est sauvegardée



### Définitions des fonctions

# Choix des couleurs
def choix_couleur(n):
    """Retourne une couleur à partir de l'entier n."""
    if n == 0: # S'il n'y a rien
        return "green" # Couleur du fond
    else:
        if n[0] == "Proie": # Si c'est une proie
            return "yellow" # Couleur des proies
        elif n[0] == "Predateur": # Si c'est un prédateur
            return "red" # Couleur des prédateurs
        else: # Si c'est autre chose
            return "grey"


# Création de la grille
def init_grille():
    """Retourne une grille carrée vide de dimension N+2, les éléments de la configuration vont de 1 à N. Les indices 0 et N+1 sont les bords."""
    global grille, config

    grille = [[0 for x in range(N + 2)] for y in range(N + 2)] # Création de la matrice de taille N + 2 pour les bords
    grille[0] = ["#" for x in range(N + 2)] # Ajout de "#" sur le bord gauche (invisible)
    grille[-1] = ["#" for x in range(N + 2)] # Ajout de "#" sur le bord droit (invisible)
    for x in range(1, N + 1): # Ajout de "#" en haut et en bas de chaque colonne
        grille[x][0] = "#"
        grille[x][-1] = "#"
    config = [[0 for x in range(N + 2)] for y in range(N + 2)] # Création de la matrice de taille N + 2 pour les bords
    config[0] = ["#" for x in range(N + 2)] # Ajout de "#" sur le bord gauche (invisible)
    config[-1] = ["#" for x in range(N + 2)] # Ajout de "#" sur le bord droit (invisible)
    for x in range(1, N + 1): # Ajout de "#" en haut et en bas de chaque colonne
        config[x][0] = "#"
        config[x][-1] = "#"

    for x in range(1, N + 1):
        i = (x - 1) * LARGEUR_CASE
        for y in range(1, N + 1):
            j = (y - 1) * HAUTEUR_CASE
            col = "green" # Couleur du fond
            carre = canvas.create_rectangle(i, j, i + LARGEUR_CASE, j + HAUTEUR_CASE, fill = col, outline = "green") # outline = couleur du contour des carrés
            grille[x][y] = carre


# Affichage de la grille
def affiche_grille(config):
    """Affiche la configuration donnée."""
    for x in range(1, N + 1): # Pour chaque abscisse
        for y in range(1, N + 1): # Pour chaque ordonnée
            col = choix_couleur(config[x][y]) # Choix de la couleur en fonction de l'élément
            canvas.itemconfigure(grille[x][y], fill = col) # Changement de la couleur de la case en fonction de la couleur retournée


# Initialise les proies
def init_proies():
    """Ajoute Npro proies à des coordonnées aléatoires."""
    global config
    cpt = Npro
    while cpt > 0:
        x, y = rd.randint(1, N + 1), rd.randint(1, N + 1) # Génération des coordonnées aléatoires
        if config[x][y] == 0: # Si c'est une case vide
            config[x][y] = ["Proie", Apro, Epro] # Création d'une liste avec toutes les infos sur l'animal (ici c'est une proie avec Apro le nombre de tours d'espérance de vie puis Epro l'énergie de la proie)
            cpt -= 1
    affiche_grille(config)


# Initialise les prédateurs
def init_prédateurs():
    """Ajoute Npre prédateurs à des coordonnées aléatoires."""
    global config
    cpt = Npre
    while cpt > 0:
        x, y = rd.randint(1, N + 1), rd.randint(1, N + 1) # Génération des coordonnées aléatoires
        if config[x][y] == 0: # Si c'est une case vide
            config[x][y] = ["Predateur", Apre, Epre] # Création d'une liste avec toutes les infos sur l'animal (ici c'est un prédateur avec Apre le nombre de tours d'espérance de vie puis Epre l'énergie du prédateur)
            cpt -= 1
    affiche_grille(config)


# Commencer/arrêter le passage des tours
def commencer():
    """Démarre ou arrête le passage des tours."""
    global arret
    compter_animaux() # Compter le nombre d'animaux
    if arret == True and nbre_animaux > 0: # Si la simulation est en pause et qu'il y a des animaux
        arret = False
        bouton_start.configure(text = "Arrêter") # Changer le texte du bouton en "Arrêter"
        passage_tours() # Faire passer les tours
    elif not arret: # Si arret == False (simulation en cours)
        arret = True
        bouton_start.configure(text = "Reprendre") # Changer le texte du bouton start en "Reprendre"
        canvas.after_cancel(var_chrono) # Arrêter le passage des tours


# Passage des tours
def passage_tours():
    """Lance la fonction de passage des tours toutes les [CHRONO] millisecondes."""
    global var_chrono
    var_chrono = canvas.after(CHRONO, tour_suivant) # La fonction tour_suivant est lancée toutes les [CHRONO] ms


# Tour suivant
def tour_suivant():
    """Fait passer les tours (modification de l'âge, de l'énergie et déplacement et reproduction)."""
    global tour, sauv_validee, arret

    vie_energie() # Modification de l'espérance de vie et de l'énergie des animaux
    reproduction_proies() # Reproduction des proies
    reproduction_predateurs() # Reproduction des prédateurs
    chasse() # Déplacement et chasse des prédateurs
    deplacement_proies() # Déplacement des proies

    # Boucle pour supprimer les termes "Reproduit" et "Déplacé" à la fin de chaque liste une fois que tous les déplacements/reproductions de ce tour ont été effectués
    for x in range(1, N + 1):
        for y in range(1, N + 1):
            if type(config[x][y]) == list and config[x][y].count("Reproduit") > 0: # Seulement si c'est une liste (donc un animal) et qu'elle contient le terme "Reproduit"
                config[x][y].remove("Reproduit") # Supprimer le terme "Reproduit" de la liste 
            if type(config[x][y]) == list and config[x][y].count("Déplacé") > 0: # Seulement si c'est une liste (donc un animal) et qu'elle contient le terme "Déplacé"
                config[x][y].remove("Déplacé") # Supprimer le terme "Déplacé" de la liste

    affiche_grille(config) # Actualise la grille
    tour += 1 # Ajout d'un tour au compteur
    label_tours.configure(text = ("Tour", tour)) # Actualise le texte du numéro de tour
    compter_animaux() # Compter le nombre d'animaux
    if nbre_animaux == 0: # S'il n'y a plus d'animaux
        arret = True # Arrêter la simulation
        bouton_start.configure(text = "Reprendre") # Changer le texte du bouton start en "Reprendre"
    if not arret: # Si la simulation n'est pas arrêtée
        passage_tours() # Continuer à passer les tours
    if sauv_validee: # Si le message de validation de la sauvegarde est affiché
        sauv_validee = False # Le supprimer (car la matrice affichée n'est plus celle qui a été sauvegardée dans le fichier)
        label_sauv_validee.configure(text = "") # Supprimer le texte "Sauvegarde effectuée"


# Modification de l'espérance de vie et de l'énergie des animaux
def vie_energie():
    """Retire 1 tour d'espérance de vie à tous les animaux, retire 1 d'énergie à tous les prédateurs et ajoute 1 d'énergie à toutes les proies."""
    global config
    for x in range(1, N + 1): # Pour chaque abscisse (ex : [0, 0, ["Proie", 5, 3], ["Proie", 2, 3], 0, ["Predateur", 15, 12], 0])
        for y in range(1, N + 1): # Pour chaque ordonnée (ex : ["Proie", 5, 3])
            # Espérance de vie des animaux
            if type(config[x][y]) == list: # Seulement si c'est une liste (donc un animal)
                config[x][y][1] -= 1 # Retirer 1 à l'espérance de vie (ex : ["Proie", 5, 3] devient ["Proie", 4, 3])
                if config[x][y][1] <= 0: # Si c'est par exemple ["Proie", 0, 3]
                    config[x][y] = 0 # Remplacer par 0 (mort de l'animal)

            # Énergie des proies
            if type(config[x][y]) == list and config[x][y][0] == "Proie" and config[x][y][2] < Epro: # Si c'est une proie et que celle-ci a une énergie inférieure à Epro
                config[x][y][2] += 1 # Ajouter 1 d'énergie

            # Énergie des prédateurs
            if type(config[x][y]) == list and config[x][y][0] == "Predateur": # Seulement si c'est un prédateur
                config[x][y][2] -= 1 # Retirer 1 à l'énergie (ex : ["Predateur", 14, 12] devient ["Predateur", 14, 11])
                if config[x][y][2] <= 0: # Si c'est par exemple ["Predateur", 14, 0]
                    config[x][y] = 0 # Remplacer par 0 (mort de l'animal)


# Reproduction des proies
def reproduction_proies():
    """Reproduit toutes les proies qui sont côte à côte si elles ont une énergie égale à Epro."""
    global config
    for x in range(1, N + 1):
        for y in range(1, N + 1):
            if type(config[x][y]) == list and config[x][y][0] == "Proie" and config[x][y][2] >= Epro: # Seulement si c'est une proie et que son niveau d'énergie est maximal (égal à Epro)
                case = direction(x, y, "Proie", "Reproduction") # Obtenir une case aléatoire ou se trouve une proie pour une reproduction
                if case == 0: # Si aucune case disponible
                    break # Annuler la boucle
                else:
                    coordonnees_case(x, y, case) # Récupérer les coordonnées i et j de la case selon son numéro
                    config[x][y][2] = 0 # Réinitialisation de l'énergie
                    config[i][j][2] = 0 # Réinitialisation de l'énergie
                    case = direction(x, y, 0, "Déplacement")
                    if case == 0: # Si aucune case disponible
                        break # Annuler la boucle
                    else: # Si la case 2 est disponible
                        coordonnees_case(x, y, case) # Récupérer les coordonnées i et j de la case selon son numéro
                        config[i][j] = ["Proie", Apro, (Epro - 1)]


# Reproduction des prédateurs
def reproduction_predateurs():
    """Pour chaque prédateur, s'il possède une énergie supérieure ou égale à Erepro, un nouveau prédateur apparaît à un endroit aléatoire sur la grille."""
    global config
    for x in range(1, N + 1):
        for y in range(1, N + 1):
            if type(config[x][y]) == list and config[x][y][0] == "Predateur" and config[x][y][2] >= Erepro and config[x][y].count("Reproduit") == 0: # Seulement si c'est un prédateur, qu'il ne s'est pas déjà reproduit pendant ce tour et que son niveau d'énergie est supérieur ou égal au niveau d'énergie Erepro nécessaire pour pouvoir se reproduire
                config[x][y].append("Reproduit") # Ajouter le terme "Reproduit" à la fin de la liste pour éviter qu'il se reproduise deux fois dans le même tour
                r = True # Variable pour arrêter la boucle
                while r: # Tant que r == True
                    x, y = rd.randint(1, N + 1), rd.randint(1, N + 1) # Génération de coordonnées aléatoires
                    if config[x][y] == 0: # Si la case à ces coordonnées est vide
                        config[x][y] = ["Predateur", Apre, Epre] # Ajouter un prédateur (Apre le nombre de tours d'espérance de vie et Epre l'énergie du prédateur)
                        r = False # Variable pour arrêter la boucle


# Déplacement et chasse des prédateurs
def chasse():
    """Déplace les prédateurs sur une case adjacente, en priorité une case où se trouve une proie."""
    global config
    for x in range(1, N + 1):
        for y in range(1, N + 1):
            if type(config[x][y]) == list and config[x][y][0] == "Predateur" and config[x][y].count("Déplacé") == 0: # Seulement si c'est un prédateur et qu'il n'a pas déjà effectué de déplacement pendant ce tour
                case = direction(x, y, "Proie", "Déplacement") # Retourner une case adjacente aléatoire où se situe une proie
                if case == 0: # S'il n'y a pas de proie à côté
                    case = direction(x, y, 0, "Déplacement") # Cherche une case vide adjacente aléatoire
                    if case == 0: # S'il n'y a pas de case vide non plus
                        break # Annuler la boucle
                    else:
                        coordonnees_case(x, y, case) # Récupérer les coordonnées i et j de la case selon son numéro
                        config[i][j] = config[x][y][:] # Copie de la liste sur la nouvelle position
                        config[x][y] = 0 # Suppression de la liste sur l'ancienne position
                        config[i][j].append("Déplacé") # Ajout du terme "Déplacé" à la fin de la liste pour éviter de déplacer le même animal 2 fois dans le même tour
                else: # Si la case 1 a une proie
                    coordonnees_case(x, y, case) # Récupérer les coordonnées i et j de la case selon son numéro
                    config[i][j] = config[x][y][:] # Copie de la liste sur la nouvelle position
                    config[x][y] = 0 # Suppression de la liste sur l'ancienne position
                    config[i][j].append("Déplacé") # Ajout du terme "Déplacé" à la fin de la liste pour éviter de déplacer le même animal 2 fois de suite
                    if not pas_de_proie: # Si le prédateur se déplace sur la case d'une proie
                        config[i][j][2] += MIAM # Ajout de MIAM énergie à l'énergie du prédateur


# Déplacement des proies
def deplacement_proies():
    """Déplace toutes les proies aléatoirement si une case adjacente est vide."""
    global config
    for x in range(1, N + 1):
        for y in range(1, N + 1):
            if type(config[x][y]) == list and config[x][y][0] == "Proie" and config[x][y].count("Déplacé") == 0: # Seulement si c'est une proie et qu'elle n'a pas déjà effectué un déplacement pendant ce tour
                case = direction(x, y, 0, "Déplacement") # Obtenir une case aléatoire pour un déplacement
                if case == 0: # Si aucune case disponible
                    break # Annuler la boucle
                else:
                    coordonnees_case(x, y, case) # Récupérer les coordonnées i et j de la case selon son numéro
                    config[i][j] = config[x][y][:] # Copie de la liste sur la nouvelle position
                    config[x][y] = 0 # Suppression de la liste sur l'ancienne position
                    config[i][j].append("Déplacé") # Ajout du terme "Déplacé" à la fin de la liste pour éviter de déplacer la même proie plusieurs fois dans le même tour


# Récupérer les coordonnées de la case
def coordonnees_case(x, y, case):
    """Récupère les nouvelles coordonnées i et j de la case à partir du numéro de cette case et des coordonnées x et y de la case de départ."""
    global i, j
    if case == 1: # En haut à gauche
        i, j = x - 1, y - 1
    elif case == 2: # À gauche
        i, j = x - 1, y
    elif case == 3: # En bas à gauche
        i, j = x - 1, y + 1
    elif case == 4: # En haut
        i, j = x, y - 1
    elif case == 5: # En bas
        i, j = x, y + 1
    elif case == 6: # En haut à droite
        i, j = x + 1, y - 1
    elif case == 7: # À droite
        i, j = x + 1, y
    elif case == 8: # En bas à droite
        i, j = x + 1, y + 1


# Retourne une case adjacente aléatoire selon la condition demandée
def direction(x, y, recherche, action):
    """Retourne une case adjacente aléatoire. recherche = 0 ou "Proie" ou "Predateur" et action = "Déplacement" (= chasse pour les prédateurs) ou "Reproduction"."""
    global pas_de_proie
    case_1 = case_2 = case_3 = case_4 = case_5 = case_6 = case_7 = case_8 = False # Création des variables pour chaque case (False = case indisponible, True = case disponible)
    pas_de_proie = False # Réinitialisation de la variable pour la chasse des prédateurs

    # Pour le déplacement (ou chasse)
    if action == "Déplacement":
        # Si on cherche une case vide
        if recherche == 0:
            # Vérifier pour chaque case (8 directions) si elle est vide
            if not type(config[x-1][y-1]) == list and config[x-1][y-1] == 0:
                case_1 = True # Case 1 : en haut à gauche
            if not type(config[x-1][y-1]) == list and config[x-1][y] == 0:
                case_2 = True # Case 2 : à gauche
            if not type(config[x-1][y+1]) == list and config[x-1][y+1] == 0:
                case_3 = True # Case 3 : en bas à gauche
            if not type(config[x][y-1]) == list and config[x][y-1] == 0:
                case_4 = True # Case 4 : en haut
            if not type(config[x][y+1]) == list and config[x][y+1] == 0:
                case_5 = True # Case 5 : en bas
            if not type(config[x+1][y-1]) == list and config[x+1][y-1] == 0:
                case_6 = True # Case 6 : en haut à droite
            if not type(config[x+1][y]) == list and config[x+1][y] == 0:
                case_7 = True # Case 7 : à droite
            if not type(config[x+1][y+1]) == list and config[x+1][y+1] == 0:
                case_8 = True # Case 8 : en bas à droite
            # Flair des proies
            if config[x][y][0] == "Proie":
                for i in range(1, (FLAIR_PRO + 1)):
                    for j in range(1, (FLAIR_PRO + 1)):
                        if x - i > 0 and y - j > 0: # Pour éviter que ça cherche des listes qui n'existent pas (et donc que ça fasse une erreur)
                            if type(config[x-i][y-j]) == list and config[x-i][y-j][0] == "Predateur": # S'il y a un prédateur pas loin
                                case_1 = case_2 = case_4 = False # Les cases 1, 2 et 4 sont indisponibles car un prédateur est dans cette direction
                        if x - i > 0:
                            if type(config[x-i][y]) == list and config[x-i][y][0] == "Predateur":
                                case_1 = case_2 = case_3 = False
                        if x - i > 0 and y + j < N:
                            if type(config[x-i][y+j]) == list and config[x-i][y+j][0] == "Predateur":
                                case_2 = case_3 = case_5 = False
                        if y - j > 0:
                            if type(config[x][y-j]) == list and config[x][y-j][0] == "Predateur":
                                case_1 = case_4 = case_6 = False
                        if y + j < N:
                            if type(config[x][y+j]) == list and config[x][y+j][0] == "Predateur":
                                case_3 = case_5 = case_7 = False
                        if x + i < N and y - j > 0:
                            if type(config[x+i][y-j]) == list and config[x+i][y-j][0] == "Predateur":
                                case_4 = case_6 = case_7 = False
                        if x + i < N:
                            if type(config[x+i][y]) == list and config[x+i][y][0] == "Predateur":
                                case_6 = case_7 = case_8 = False
                        if x + i < N and y + j < N:
                            if type(config[x+i][y+j]) == list and config[x+i][y+j][0] == "Predateur":
                                case_5 = case_7 = case_8 = False

        # Chasse des prédateurs
        elif recherche == "Proie": # Si on cherche une proie
            if type(config[x-1][y-1]) == list and config[x-1][y-1][0] == "Proie": # Vérifier dans chaque direction s'il y a une proie
                case_1 = True # La case 1 est disponible
            if type(config[x-1][y]) == list and config[x-1][y][0] == "Proie":
                case_2 = True
            if type(config[x-1][y+1]) == list and config[x-1][y+1][0] == "Proie":
                case_3 = True
            if type(config[x][y-1]) == list and config[x][y-1][0] == "Proie":
                case_4 = True
            if type(config[x][y+1]) == list and config[x][y+1][0] == "Proie":
                case_5 = True
            if type(config[x+1][y-1]) == list and config[x+1][y-1][0] == "Proie":
                case_6 = True
            if type(config[x+1][y]) == list and config[x+1][y][0] == "Proie":
                case_7 = True
            if type(config[x+1][y+1]) == list and config[x+1][y+1][0] == "Proie":
                case_8 = True
            # S'il n'y a aucune proie à côté du prédateur
            # Flair des prédateurs
            if case_1 == case_2 == case_3 == case_4 == case_5 == case_6 == case_7 == case_8 == False:
                pas_de_proie = True # Variable pour indiquer que l'on ne va pas se déplacer sur la case d'une proie
                for i in range(1, (FLAIR_PRE + 1)):
                    for j in range(1, (FLAIR_PRE + 1)):
                        if x - i > 0 and y - j > 0: # Pour éviter que ça cherche des listes qui n'existent pas (et donc que ça fasse une erreur)
                            if type(config[x-i][y-j]) == list and config[x-i][y-j][0] == "Proie": # S'il y a une proie pas loin
                                if not type(config[x-1][y-1]) == list and config[x-1][y-1] == 0: # Et qu'il y a une case de libre dans cette direction
                                    case_1 = True # La case est disponible
                        if x - i > 0:
                            if type(config[x-i][y]) == list and config[x-i][y][0] == "Proie":
                                if not type(config[x-1][y]) == list and config[x-1][y] == 0:
                                    case_2 = True
                        if x - i > 0 and y + j < N:
                            if type(config[x-i][y+j]) == list and config[x-i][y+j][0] == "Proie":
                                if not type(config[x-1][y+1]) == list and config[x-1][y+1] == 0:
                                    case_3 = True
                        if y - j > 0:
                            if type(config[x][y-j]) == list and config[x][y-j][0] == "Proie":
                                if not type(config[x][y-1]) == list and config[x][y-1] == 0:
                                    case_4 = True
                        if y + j < N:
                            if type(config[x][y+j]) == list and config[x][y+j][0] == "Proie":
                                if not type(config[x][y+1]) == list and config[x][y+1] == 0:
                                    case_5 = True
                        if x + i < N and y - j > 0:
                            if type(config[x+i][y-j]) == list and config[x+i][y-j][0] == "Proie":
                                if not type(config[x+1][y-1]) == list and config[x+1][y-1] == 0:
                                    case_6 = True
                        if x + i < N:
                            if type(config[x+i][y]) == list and config[x+i][y][0] == "Proie":
                                if not type(config[x+1][y]) == list and config[x+1][y] == 0:
                                    case_7 = True
                        if x + i < N and y + j < N:
                            if type(config[x+i][y+j]) == list and config[x+i][y+j][0] == "Proie":
                                if not type(config[x+1][y+1]) == list and config[x+1][y+1] == 0:
                                    case_8 = True

    # Pour la reproduction des proies
    if action == "Reproduction":
        # Vérifier pour chaque case (8 directions) que c'est une proie, que celle-ci a une énergie supérieure où égale à l'énergie maximale et qu'elle ne s'est pas déjà reproduite pendant ce tour
        if type(config[x-1][y-1]) == list and config[x-1][y-1][0] == "Proie" and config[x-1][y-1][2] >= Epro and config[x-1][y-1].count("Reproduit") == 0:
            case_1 = True
        if type(config[x-1][y]) == list and config[x-1][y][0] == "Proie" and config[x-1][y][2] >= Epro and config[x-1][y].count("Reproduit") == 0:
            case_2 = True
        if type(config[x-1][y+1]) == list and config[x-1][y+1][0] == "Proie" and config[x-1][y+1][2] >= Epro and config[x-1][y+1].count("Reproduit") == 0:
            case_3 = True
        if type(config[x][y-1]) == list and config[x][y-1][0] == "Proie" and config[x][y-1][2] >= Epro and config[x][y-1].count("Reproduit") == 0:
            case_4 = True
        if type(config[x][y+1]) == list and config[x][y+1][0] == "Proie" and config[x][y+1][2] >= Epro and config[x][y+1].count("Reproduit") == 0:
            case_5 = True
        if type(config[x+1][y-1]) == list and config[x+1][y-1][0] == "Proie" and config[x+1][y-1][2] >= Epro and config[x+1][y-1].count("Reproduit") == 0:
            case_6 = True
        if type(config[x+1][y]) == list and config[x+1][y][0] == "Proie" and config[x+1][y][2] >= Epro and config[x+1][y].count("Reproduit") == 0:
            case_7 = True
        if type(config[x+1][y+1]) == list and config[x+1][y+1][0] == "Proie" and config[x+1][y+1][2] >= Epro and config[x+1][y+1].count("Reproduit") == 0:
            case_8 = True



    if case_1 == case_2 == case_3 == case_4 == case_5 == case_6 == case_7 == case_8 == False:
        case = 0 # Si aucune case n'est disponible, retourner case = 0
    else: # Sinon, on choisit une des cases disponibles aléatoirement
        d = True # Variable pour arrêter la boucle
        while d: # Tant que d == True
            x = rd.randint(1, 8) # Génération d'un chiffre aléatoire entre 1 et 8 pour choisir la direction aléatoirement
            if case_1 and x == 1: # Si la case 1 est disponible et que le chiffre aléatoire est 1
                case = 1 # On retourne une valeur de 1
                d = False # Variable pour arrêter la boucle
            elif case_2 and x == 2: # Idem pour les 8 cases possibles
                case = 2
                d = False
            elif case_3 and x == 3:
                case = 3
                d = False
            elif case_4 and x == 4:
                case = 4
                d = False
            elif case_5 and x == 5:
                case = 5
                d = False
            elif case_6 and x == 6:
                case = 6
                d = False
            elif case_7 and x == 7:
                case = 7
                d = False
            elif case_8 and x == 8:
                case = 8
                d = False
    return case # Retourner la valeur de case (comprise entre 0 et 8 inclus)


# Compter le nombre d'animaux
def compter_animaux():
    """Compte le nombre total d'animaux, le nombre de proies et le nombre de prédateurs."""
    global nbre_animaux, nbre_proies, nbre_predateurs
    nbre_animaux = nbre_proies = nbre_predateurs = 0
    for x in range(1, N + 1):
        for y in range(1, N + 1):
            if type(config[x][y]) == list: # Si c'est une liste (donc un animal)
                nbre_animaux += 1 # On ajoute 1 au compteur d'animaux
                if config[x][y][0] == "Proie": # Si c'est une proie
                    nbre_proies += 1 # On ajoute 1 au compteur de proies
                if config[x][y][0] == "Predateur": # Si c'est un prédateur
                    nbre_predateurs += 1 # On ajoute 1 au compteur de prédateurs
    label_animaux.configure(text = ("Nombre d'animaux : " + str(nbre_animaux))) # Actualise le texte du nombre d'animaux
    label_proies.configure(text = ("Nombre de proies : " + str(nbre_proies))) # Actualise le texte du nombre de proies
    label_predateurs.configure(text = ("Nombre de prédateurs : " + str(nbre_predateurs))) # Actualise le texte du nombre de prédateurs


# Réinitialiser la matrice
def reinitialiser():
    """Réinitialise la matrice."""
    global arret, tour, sauv_validee
    init_grille() # Création de la grille de départ
    init_proies() # Ajout de Npro proies à des coordonnées aléatoires
    init_prédateurs() # Ajout de Npre prédateurs à des coordonnées aléatoires
    bouton_start.configure(text = "Commencer") # Changer le texte du bouton start en "Commencer"
    if not arret: # Si la simulation est en cours
        arret = True # Arrêter la simulation
        canvas.after_cancel(var_chrono) # Arrêter le passage des tours
    tour = 0 # Réinitialise le numéro du tour
    label_tours.configure(text = ("Tour", tour)) # Actualise le texte du numéro de tour
    compter_animaux() # Actualiser le nombre d'animaux
    if sauv_validee: # Si le message de validation de la sauvegarde est affiché
        sauv_validee = False # Le supprimer (car la matrice affichée n'est plus celle qui a été sauvegardée dans le fichier)
        label_sauv_validee.configure(text = "") # Supprimer le texte "Sauvegarde effectuée"


# Sauvegarder la matrice
def sauvegarder():
    """Sauvegarde la matrice actuelle dans le fichier "sauvegarde"."""
    global sauv_validee
    fic = open("sauvegarde", "w") # Ouvrir le fichier "sauvegarde" en écriture
    fic.write(str(tour)) # Écrire le numéro du tour au début du fichier
    fic.write("\n\n") # Laisser la deuxième ligne vide
    for x in range(1, N + 1): # Pour chaque abscisse
        for y in range(1, N + 1): # Pour chaque ordonnée
            if config[x][y] == 0: # Si l'élément de la matrice est égal à 0
                fic.write(str(config[x][y])) # L'écrire sur cette ligne
                fic.write("\n") # Ajouter un retour à la ligne pour que le prochain élément soit sur la ligne suivante
            else: # Si c'est la liste d'un animal
                fic.write("ANIMAL\n") # Écrire "ANIMAL" sur cette ligne (avec le retour à la ligne) pour signaler le début de la liste d'un animal
                for i in range(0, len(config[x][y])): # Pour chaque élément de la liste de l'animal
                    fic.write(str(config[x][y][i])) # L'ajouter sur la ligne suivante
                    fic.write("\n")
                fic.write("FIN\n") # Puis écrire "FIN" sur la ligne suivante pour signaler la fin de la liste d'un animal
    sauv_validee = True # Variable pour indiquer que la matrice actuelle est sauvegardée
    label_sauv_validee.configure(text = "Sauvegarde effectuée") # Afficher le texte "Sauvegarde effectuée" en dessous du bouton
    fic.close() # Fermer le fichier


# Charger la matrice sauvegardée
def charger():
    """Charge la configuration sauvegardée dans le fichier "sauvegarde"."""
    global arret, tour, config
    # Réinitialisation de la matrice
    config = [[0 for x in range(N + 2)] for y in range(N + 2)] # Création de la matrice de taille N + 2 pour les bords
    config[0] = ["#" for x in range(N + 2)] # Ajout de "#" sur le bord gauche (invisible)
    config[-1] = ["#" for x in range(N + 2)] # Ajout de "#" sur le bord droit (invisible)
    for x in range(1, N + 1): # Ajout de "#" en haut et en bas de chaque colonne
        config[x][0] = "#"
        config[x][-1] = "#"

    fic = open("sauvegarde", "r") # Ouvrir le fichier "sauvegarde" en lecture
    x = y = 1 # On démarre avec une abscisse et une ordonnée égales à 1 pour ne pas compter les bords
    animal = False # Variable pour indiquer si la ligne fait partie de la liste d'un animal
    recup_tour = True # Variable pour récupérer le numéro de tour
    for ligne in fic: # Pour chaque ligne dans le fichier de sauvegarde
        if recup_tour:
            tour = int(ligne) # Récupère le numéro de tour
            recup_tour = False
        elif ligne == "0\n" and not animal: # Si la ligne est un 0 (avec \n à la fin pour le saut de ligne présent) et que le 0 n'est pas dans une liste d'animal
            config[x][y] = 0 # La case correspondante dans la matrice sera un 0
            y += 1 # On ajoute 1 à l'ordonnée pour la prochaine ligne du fichier
            if y == N + 1: # Si l'ordonnée est supérieure à la taille de la matrice
                y = 1 # On la réinitialise à 1 (on revient à la première ligne)
                x += 1 # Et on ajoute 1 à l'abscisse (on passe à la colonne à droite)
        if ligne == "ANIMAL\n": # Si la ligne est "ANIMAL" (avec le saut de ligne à la fin)
            animal = True # On entre dans la liste d'un animal
            config[x][y] = [] # Création de la liste de l'animal
        elif ligne == "FIN\n": # Si la ligne est "FIN" (avec le saut de ligne à la fin) 
            animal = False # Fin de la liste de l'animal
            y += 1 # On ajoute 1 à l'ordonnée pour la prochaine ligne du fichier
            if y == N + 1: # Si l'ordonnée est supérieure à la taille de la matrice
                y = 1 # On la réinitialise à 1 (on revient à la première ligne)
                x += 1 # Et on ajoute 1 à l'abscisse (on passe à la colonne à droite)
        elif animal: # Si la ligne est dans la liste d'un animal
            if ligne == "Proie\n": # Si la ligne est "Proie"
                config[x][y].append("Proie") # On ajoute "Proie" dans la liste de l'animal
            elif ligne == "Predateur\n":
                config[x][y].append("Predateur")
            elif ligne == "Reproduit\n":
                config[x][y].append("Reproduit")
            elif ligne == "Déplacé\n":
                config[x][y].append("Déplacé")
            else: # Si c'est aucun des 4 termes possibles (donc c'est un nombre)
                config[x][y].append(int(ligne)) # On ajoute le nombre dans la liste
    fic.close() # Fermer le fichier
    affiche_grille(config) # Actualise la grille
    label_tours.configure(text = ("Tour", tour)) # Actualise le texte du numéro de tour récupéré dans le fichier
    compter_animaux() # Compter le nombre d'animaux
    bouton_start.configure(text = "Commencer") # Changer le texte du bouton start en "Commencer"
    if not arret: # Si la simulation est en cours
        arret = True # Arrêter la simulation
        canvas.after_cancel(var_chrono) # Arrêter le passage des tours



### Programme principal

# Définition des widgets
racine = tk.Tk()
racine.title("Simulation proies-prédateurs")
canvas = tk.Canvas(racine, width = LARGEUR, height = HAUTEUR)
bouton_start = tk.Button(racine, text = "Commencer", command = commencer, width = 10, font = ("bold", 12)) # Bouton pour commencer ou arrêter le passage des tours
bouton_reinit = tk.Button(racine, text = "Réinitialiser", command = reinitialiser, font = ("bold", 10)) # Bouton pour réinitialiser la matrice
bouton_sauver = tk.Button(racine, text = "Sauvegarder", command = sauvegarder, width = 10, font = ("bold", 10)) # Bouton pour sauvegarder la matrice actuelle
bouton_charger = tk.Button(racine, text = "Charger", command = charger, font = ("bold", 10)) # Bouton pour charger la matrice sauvegardée
label_tours = tk.Label(racine, text = ("Tour", tour), font = ("bold", 15)) # Texte pour afficher le numéro du tour actuel
label_sauv_validee = tk.Label(racine, width = 30, font = ("bold", 8)) # Texte pour indiquer que la matrice actuellement affichée est sauvegardée dans le fichier "sauvegarde"
label_animaux = tk.Label(racine, text = ("Nombre d'animaux : " + str((Npro + Npre))), font = ("bold", 8)) # Texte pour indiquer le nombre d'animaux en vie
label_proies = tk.Label(racine, text = ("Nombre de proies : " + str(Npro)), font = ("bold", 8)) # Texte pour indiquer le nombre de proies en vie
label_predateurs = tk.Label(racine, text = ("Nombre de prédateurs : " + str(Npre)), font = ("bold", 8))  # Texte pour indiquer le nombre de prédateurs en vie

# Fonctions
init_grille() # Création de la grille de départ
init_proies() # Ajout de Npro proies à des coordonnées aléatoires
init_prédateurs() # Ajout de Npre prédateurs à des coordonnées aléatoires

# Placement des widgets
canvas.grid(column = 1, row = 1, rowspan = 50)
label_tours.grid(column = 1, row = 0)
bouton_start.grid(column = 0, row = 5)
bouton_reinit.grid(column = 0, row = 10)
label_animaux.grid(column = 0, row = 19)
label_proies.grid(column = 0, row = 20)
label_predateurs.grid(column = 0, row = 21)
bouton_sauver.grid(column = 0, row = 30)
label_sauv_validee.grid(column = 0, row = 31)
bouton_charger.grid(column = 0, row = 33)

# Boucle principale
racine.mainloop()