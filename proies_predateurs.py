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
LARGEUR = 550 # Largeur du canevas
LARGEUR_CASE = HAUTEUR // 1.23 // N # Largeur des cases
HAUTEUR_CASE = LARGEUR_CASE # Hauteur des cases

CHRONO = 500 # Temps en millisecondes entre chaque tour

MIAM = 5 # Niveau d'énergie gagné lorsqu'un prédateur mange une proie
FLAIR = 5 # Distance maximale à laquelle un prédateur peut sentir un proie
Erepro = 15 # Niveau d'énergie nécessaire pour qu'un prédateur puisse se reproduire



### Définitions des variables globales

arret = True # Variable pour arrêter le passage des tours
var_chrono = 0 # Variable pour le compte à rebours entre chaque tour

tour = 0 # Numéro du tour

Npro = 10 # Nombre initial de proies (Npro proies apparaissent au début)
Apro = 5 # Espérance de vie des proies en nombre de tours
Epro = 2 # Énergie des proies (augmente de 1 par tour avec Epro en plafond. Une énergie maximale (égale à Epro) est nécessaire pour qu'une proie puisse se reproduire. Epro revient à 0 à chaque reproduction.)

Npre = 2 # Nombre initial de prédateurs (Npre prédateurs apparaissent au début)
Apre = 15 # Espérance de vie des prédateurs en nombre de tours
Epre = 12 # Énergie des prédateurs (baisse de 1 par tour, s'il elle atteint zéro, le prédateur meurt de faim)

sauv_validee = False # Variable pour afficher si la matrice actuelle est sauvegardée



### Définitions des fonctions

# Choix des couleurs
def choix_couleur(n):
    """Retourne une couleur à partir de l'entier n"""
    if n == 0: # Si il n'y a rien
        return "green" # Couleur du fond
    else:
        if n[0] == "Proie": # Si c'est une proie
            return "yellow" # Couleur des proies
        elif n[0] == "Prédateur": # Si c'est un prédateur
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

    for i in range(1, N + 1):
        x = (i - 1) * LARGEUR_CASE
        for j in range(1, N + 1):
            y = (j - 1) * HAUTEUR_CASE
            col = "green" # Couleur du fond
            carre = canvas.create_rectangle(x, y, x + LARGEUR_CASE, y + HAUTEUR_CASE, fill = col, outline = "grey") # outline = couleur du contour des carrés
            grille[i][j] = carre


# Affichage de la grille
def affiche_grille(config):
    """Affiche la configuration donnée"""
    for x in range(1, N + 1):
        for y in range(1, N + 1):
            col = choix_couleur(config[x][y])
            canvas.itemconfigure(grille[x][y], fill = col)


# Initialise les proies
def init_proies():
    """Ajoute Npro proies à des coordonnées aléatoires"""
    global config
    cpt = Npro
    while cpt > 0:
        x, y = rd.randint(1, N + 1), rd.randint(1, N + 1) # Génération des coordonnées aléatoires
        if config[x][y] == 0: # Si c'est une case vide
            config[x][y] = ["Proie", Apro, Epro] # Création d'une liste avec toutes les infos sur l'animal (ici c'est une proie avec Apro le nombre de tours d'espérance de vie)
            cpt -= 1
    affiche_grille(config)


# Initialise les prédateurs
def init_prédateurs():
    """Ajoute Npre prédateurs à des coordonnées aléatoires"""
    global config
    cpt = Npre
    while cpt > 0:
        x, y = rd.randint(1, N + 1), rd.randint(1, N + 1) # Génération des coordonnées aléatoires
        if config[x][y] == 0: # Si c'est une case vide
            config[x][y] = ["Prédateur", Apre, Epre] # Création d'une liste avec toutes les infos sur l'animal (ici c'est un prédateur avec Apre le nombre de tours d'espérance de vie puis Epre l'énergie du prédateur)
            cpt -= 1
    affiche_grille(config)


# Retourne une case adjacente aléatoire selon la condition demandée
def direction(x, y, n):
    """Retourne une case adjacente aléatoire ayant pour condition n (par exemple 0 ou Proie)"""
    case_1 = case_2 = case_3 = case_4 = case_5 = case_6 = case_7 = case_8 = False # Création des variables pour chaque case (False = indisponible, True = disponible)

    # Vérifier pour chaque case (8 directions) que ce n'est pas une liste et que c'est égal à n
    if not type(config[x-1][y-1]) == list and config[x-1][y-1] == n:
        case_1 = True # Case 1 : en haut à gauche
    if not type(config[x-1][y-1]) == list and config[x-1][y] == n:
        case_2 = True # Case 2 : à gauche
    if not type(config[x-1][y+1]) == list and config[x-1][y+1] == n:
        case_3 = True # Case 3 : en bas à gauche
    if not type(config[x][y-1]) == list and config[x][y-1] == n:
        case_4 = True # Case 4 : en haut
    if not type(config[x][y+1]) == list and config[x][y+1] == n:
        case_5 = True # Case 5 : en bas
    if not type(config[x+1][y-1]) == list and config[x+1][y-1] == n:
        case_6 = True # Case 6 : en haut à droite
    if not type(config[x+1][y]) == list and config[x+1][y] == n:
        case_7 = True # Case 7 : à droite
    if not type(config[x+1][y+1]) == list and config[x+1][y+1] == n:
        case_8 = True # Case 8 : en bas à droite

    # Vérifier pour chaque case (8 directions) que c'est une liste et que son premier terme est égal à n
    if type(config[x-1][y-1]) == list and config[x-1][y-1][0] == n:
        case_1 = True
    if type(config[x-1][y]) == list and config[x-1][y][0] == n:
        case_2 = True
    if type(config[x-1][y+1]) == list and config[x-1][y+1][0] == n:
        case_3 = True
    if type(config[x][y-1]) == list and config[x][y-1][0] == n:
        case_4 = True
    if type(config[x][y+1]) == list and config[x][y+1][0] == n:
        case_5 = True
    if type(config[x+1][y-1]) == list and config[x+1][y-1][0] == n:
        case_6 = True
    if type(config[x+1][y]) == list and config[x+1][y][0] == n:
        case_7 = True
    if type(config[x+1][y+1]) == list and config[x+1][y+1][0] == n:
        case_8 = True

    if case_1 == False and case_2 == False and case_3 == False and case_4 == False and case_5 == False and case_6 == False and case_7 == False and case_8 == False:
        case = 0 # Si aucune case n'est disponible, retourner case = 0
    else:
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


# Modification de l'espérance de vie et de l'énergie des animaux
def vie_energie():
    """Retire 1 tour d'espérance de vie à tous les animaux, 1 d'énergie à tous les prédateurs et ajout 1 d'énergie à toutes les proies"""
    global config
    for x in range(1, N + 1): # Pour chaque liste (ex : [0, 0, ["Proie", 5, 3], ["Proie", 2, 3], 0, ["Prédateur", 15, 12], 0])
        for y in range(1, N + 1): # Pour chaque élément dans la liste (ex : ["Proie", 5, 3])
            # Espérance de vie des animaux
            if type(config[x][y]) == list: # Seulement si c'est une liste (pas un 0 ou un #)
                config[x][y][1] -= 1 # Retirer 1 à l'espérance de vie (ex : ["Proie", 5, 3] devient ["Proie", 4, 3])
                if config[x][y][1] <= 0: # Si c'est par exemple [Proie, 0]
                    config[x][y] = 0 # Remplacer par 0 (mort de l'animal)

            # Énergie des proies
            if type(config[x][y]) == list and config[x][y][0] == "Proie" and config[x][y][2] < Epro: # Si c'est une proie et que celle-ci a une énergie inférieure à Epro
                config[x][y][2] += 1 # Ajouter 1 d'énergie

            # Énergie des prédateurs
            if type(config[x][y]) == list and config[x][y][0] == "Prédateur": # Seulement si c'est un prédateur
                config[x][y][2] -= 1 # Retirer 1 à l'énergie (ex : ["Prédateur", 14, 12] devient ["Prédateur", 14, 11])
                if config[x][y][2] <= 0: # Si c'est par exemple ["Prédateur", 14, 0]
                    config[x][y] = 0 # Remplacer par 0 (mort de l'animal)


# Déplacement des proies
def deplacement_proies():
    """Déplace toutes les proies aléatoirement si une case adjacente est vide"""
    global config
    for x in range(1, N + 1):
        for y in range(1, N + 1):
            if type(config[x][y]) == list and config[x][y][0] == "Proie" and config[x][y][-1] != "Déplacé" : # Seulement si c'est une proie et qu'elle n'a pas déjà effectué un déplacement pendant ce tour
                case = direction(x, y, 0)
                if case == 0: # Si aucune case adjacente n'est vide
                    break # Arrêter la boucle
                elif case == 1: # Si la case 1 est libre
                    config[x-1][y-1] = config[x][y][:] # Copie de la liste sur la nouvelle position
                    config[x][y] = 0 # Suppression de la liste sur l'ancienne position
                    config[x-1][y-1].append("Déplacé") # Ajout du terme "Déplacé" à la fin de la liste pour éviter de déplacer la même proie 2 fois de suite
                elif case == 2:
                    config[x-1][y] = config[x][y][:]
                    config[x][y] = 0
                    config[x-1][y].append("Déplacé")
                elif case == 3:
                    config[x-1][y+1] = config[x][y][:]
                    config[x][y] = 0
                    config[x-1][y+1].append("Déplacé")
                elif case == 4:
                    config[x][y-1] = config[x][y][:]
                    config[x][y] = 0
                    config[x][y-1].append("Déplacé")
                elif case == 5:
                    config[x][y+1] = config[x][y][:]
                    config[x][y] = 0
                    config[x][y+1].append("Déplacé")
                elif case == 6:
                    config[x+1][y-1] = config[x][y][:]
                    config[x][y] = 0
                    config[x+1][y-1].append("Déplacé")
                elif case == 7:
                    config[x+1][y] = config[x][y][:]
                    config[x][y] = 0
                    config[x+1][y].append("Déplacé")
                elif case == 8:
                    config[x+1][y+1] = config[x][y][:]
                    config[x][y] = 0
                    config[x+1][y+1].append("Déplacé")


# Reproduction des proies
def reproduction_proies():
    """Reproduit toutes les proies qui sont côte à côte si elles ont une énergie égale à Epro"""
    global config
    for x in range(1, N + 1):
        for y in range(1, N + 1):
            if type(config[x][y]) == list and config[x][y][0] == "Proie" and config[x][y][-1] != "Reproduit" and config[x][y][2] >= Epro: # Seulement si c'est une proie, qu'elle ne s'est pas déjà reproduite pendant ce tour et que son niveau d'énergie est maximal (égal à Epro)
                case = direction(x, y, "Proie")
                if case == 0: # Si aucune case adjacente n'a de proie
                    break # Annuler la boucle
                elif case == 1: # Si la case 1 est une proie
                    config[x][y].append("Reproduit") # Ajout du terme "Reproduit" à la fin de la liste pour éviter que les proies se reproduisent plusieurs fois par tour
                    config[x][y][2] -= 3
                    config[x-1][y-1].append("Reproduit")
                    config[x-1][y-1][2] -= 3
                    case = direction(x, y, 0)
                    if case == 0: # Si aucune case n'est vide (pas de place pour une nouvelle proie)
                        break # Annuler la boucle
                    elif case == 2: # Si la case 2 est disponible
                        config[x-1][y] = ["Proie", Apro, Epro] # Ajouter une proies avec une espérance de vie de Apro tours
                    elif case == 3:
                        config[x-1][y+1] = ["Proie", Apro, Epro]
                    elif case == 4:
                        config[x][y-1] = ["Proie", Apro, Epro]
                    elif case == 5:
                        config[x][y+1] = ["Proie", Apro, Epro]
                    elif case == 6:
                        config[x+1][y-1] = ["Proie", Apro, Epro]
                    elif case == 7:
                        config[x+1][y] = ["Proie", Apro, Epro]
                    elif case == 8:
                        config[x+1][y+1] = ["Proie", Apro, Epro]
                elif case == 2:
                    config[x][y].append("Reproduit")
                    config[x][y][2] -= 3
                    config[x-1][y].append("Reproduit")
                    config[x-1][y][2] -= 3
                    case = direction(x, y, 0)
                    if case == 0:
                        pass
                    elif case == 1:
                        config[x-1][y-1] = ["Proie", Apro, Epro]
                    elif case == 3:
                        config[x-1][y+1] = ["Proie", Apro, Epro]
                    elif case == 4:
                        config[x][y-1] = ["Proie", Apro, Epro]
                    elif case == 5:
                        config[x][y+1] = ["Proie", Apro, Epro]
                    elif case == 6:
                        config[x+1][y-1] = ["Proie", Apro, Epro]
                    elif case == 7:
                        config[x+1][y] = ["Proie", Apro, Epro]
                    elif case == 8:
                        config[x+1][y+1] = ["Proie", Apro, Epro]
                elif case == 3:
                    config[x][y].append("Reproduit")
                    config[x][y][2] -= 3
                    config[x-1][y+1].append("Reproduit")
                    config[x-1][y+1][2] -= 3
                    case = direction(x, y, 0)
                    if case == 0:
                        pass
                    elif case == 1:
                        config[x-1][y-1] = ["Proie", Apro, Epro]
                    elif case == 2:
                        config[x-1][y] = ["Proie", Apro, Epro]
                    elif case == 4:
                        config[x][y-1] = ["Proie", Apro, Epro]
                    elif case == 5:
                        config[x][y+1] = ["Proie", Apro, Epro]
                    elif case == 6:
                        config[x+1][y-1] = ["Proie", Apro, Epro]
                    elif case == 7:
                        config[x+1][y] = ["Proie", Apro, Epro]
                    elif case == 8:
                        config[x+1][y+1] = ["Proie", Apro, Epro]
                elif case == 4:
                    config[x][y].append("Reproduit")
                    config[x][y][2] -= 3
                    config[x][y-1].append("Reproduit")
                    config[x][y-1][2] -= 3
                    case = direction(x, y, 0)
                    if case == 0:
                        pass
                    elif case == 1:
                        config[x-1][y-1] = ["Proie", Apro, Epro]
                    elif case == 2:
                        config[x-1][y] = ["Proie", Apro, Epro]
                    elif case == 3:
                        config[x-1][y+1] = ["Proie", Apro, Epro]
                    elif case == 5:
                        config[x][y+1] = ["Proie", Apro, Epro]
                    elif case == 6:
                        config[x+1][y-1] = ["Proie", Apro, Epro]
                    elif case == 7:
                        config[x+1][y] = ["Proie", Apro, Epro]
                    elif case == 8:
                        config[x+1][y+1] = ["Proie", Apro, Epro]
                elif case == 5:
                    config[x][y].append("Reproduit")
                    config[x][y][2] -= 3
                    config[x][y+1].append("Reproduit")
                    config[x][y+1][2] -= 3
                    case = direction(x, y, 0)
                    if case == 0:
                        pass
                    elif case == 1:
                        config[x-1][y-1] = ["Proie", Apro, Epro]
                    elif case == 2:
                        config[x-1][y] = ["Proie", Apro, Epro]
                    elif case == 3:
                        config[x-1][y+1] = ["Proie", Apro, Epro]
                    elif case == 4:
                        config[x][y-1] = ["Proie", Apro, Epro]
                    elif case == 6:
                        config[x+1][y-1] = ["Proie", Apro, Epro]
                    elif case == 7:
                        config[x+1][y] = ["Proie", Apro, Epro]
                    elif case == 8:
                        config[x+1][y+1] = ["Proie", Apro, Epro]
                elif case == 6:
                    config[x][y].append("Reproduit")
                    config[x][y][2] -= 3
                    config[x+1][y-1].append("Reproduit")
                    config[x+1][y-1][2] -= 3
                    case = direction(x, y, 0)
                    if case == 0:
                        pass
                    elif case == 1:
                        config[x-1][y-1] = ["Proie", Apro, Epro]
                    elif case == 2:
                        config[x-1][y] = ["Proie", Apro, Epro]
                    elif case == 3:
                        config[x-1][y+1] = ["Proie", Apro, Epro]
                    elif case == 4:
                        config[x][y-1] = ["Proie", Apro, Epro]
                    elif case == 5:
                        config[x][y+1] = ["Proie", Apro, Epro]
                    elif case == 7:
                        config[x+1][y] = ["Proie", Apro, Epro]
                    elif case == 8:
                        config[x+1][y+1] = ["Proie", Apro, Epro]
                elif case == 7:
                    config[x][y].append("Reproduit")
                    config[x][y][2] -= 3
                    config[x+1][y].append("Reproduit")
                    config[x+1][y][2] -= 3
                    case = direction(x, y, 0)
                    if case == 0:
                        pass
                    elif case == 1:
                        config[x-1][y-1] = ["Proie", Apro, Epro]
                    elif case == 2:
                        config[x-1][y] = ["Proie", Apro, Epro]
                    elif case == 3:
                        config[x-1][y+1] = ["Proie", Apro, Epro]
                    elif case == 4:
                        config[x][y-1] = ["Proie", Apro, Epro]
                    elif case == 5:
                        config[x][y+1] = ["Proie", Apro, Epro]
                    elif case == 6:
                        config[x+1][y-1] = ["Proie", Apro, Epro]
                    elif case == 8:
                        config[x+1][y+1] = ["Proie", Apro, Epro]
                elif case == 8:
                    config[x][y].append("Reproduit")
                    config[x][y][2] -= 3
                    config[x+1][y+1].append("Reproduit")
                    config[x+1][y+1][2] -= 3
                    case = direction(x, y, 0)
                    if case == 0:
                        pass
                    elif case == 1:
                        config[x-1][y-1] = ["Proie", Apro, Epro]
                    elif case == 2:
                        config[x-1][y] = ["Proie", Apro, Epro]
                    elif case == 3:
                        config[x-1][y+1] = ["Proie", Apro, Epro]
                    elif case == 4:
                        config[x][y-1] = ["Proie", Apro, Epro]
                    elif case == 5:
                        config[x][y+1] = ["Proie", Apro, Epro]
                    elif case == 6:
                        config[x+1][y-1] = ["Proie", Apro, Epro]
                    elif case == 7:
                        config[x+1][y] = ["Proie", Apro, Epro]


# Reproduction des prédateurs
def reproduction_predateurs():
    """Pour chaque prédateur, s'il possède une énergie supérieure ou égale à Erepro, un prédateur apparaît à un endroit aléatoire sur la grille"""
    global config
    for x in range(1, N + 1):
        for y in range(1, N + 1):
            if type(config[x][y]) == list and config[x][y][0] == "Prédateur" and config[x][y][-1] != "Reproduit" and config[x][y][2] >= Erepro: # Seulement si c'est un prédateur, qu'il ne s'est pas déjà reproduit pendant ce tour et que son niveau d'énergie est supérieur ou égal au niveau d'énergie Erepro nécessaire pour pouvoir se reproduire
                config[x][y].append("Reproduit") # Ajouter le terme "Reproduit" à la fin de la liste pour éviter qu'il se reproduise deux fois dans le même tour
                r = True # Variable pour arrêter la boucle
                while r: # Tant que r == True
                    x, y = rd.randint(1, N + 1), rd.randint(1, N + 1) # Génération de coordonnées aléatoires
                    if config[x][y] == 0: # Si la case à ces coordonnées est vide
                        config[x][y] = ["Prédateur", Apro, Epre] # Ajouter un prédateur
                        r = False # Variable pour arrêter la boucle


# Déplacement et chasse des prédateurs
def chasse():
    """Déplace les prédateurs sur une case adjacente, en priorité une case où se trouve une proie"""
    global config
    for x in range(1, N + 1):
        for y in range(1, N + 1):
            if type(config[x][y]) == list and config[x][y][0] == "Prédateur" and config[x][y][-1] != "Déplacé" : # Seulement si c'est un prédateur et qu'il n'a pas déjà effectué un déplacement pendant ce tour
                case = direction(x, y, "Proie") # Retourner une case adjacente aléatoire où se situe une proie
                if case == 0: # S'il n'y a pas de proie à côté
                    case = direction(x, y, 0) # Cherche une case vide adjacente aléatoire
                    if case == 0: # S'il n'y en a pas non plus
                        break # Annuler la boucle
                    elif case == 1: # Si la case 1 est vide
                        config[x-1][y-1] = config[x][y][:] # Copie de la liste sur la nouvelle position
                        config[x][y] = 0 # Suppression de la liste sur l'ancienne position
                        config[x-1][y-1].append("Déplacé") # Ajout du terme "Déplacé" à la fin de la liste pour éviter de déplacer le même animal 2 fois dans le même tour
                    elif case == 2:
                        config[x-1][y] = config[x][y][:]
                        config[x][y] = 0
                        config[x-1][y].append("Déplacé")
                    elif case == 3:
                        config[x-1][y+1] = config[x][y][:]
                        config[x][y] = 0
                        config[x-1][y+1].append("Déplacé")
                    elif case == 4:
                        config[x][y-1] = config[x][y][:]
                        config[x][y] = 0
                        config[x][y-1].append("Déplacé")
                    elif case == 5:
                        config[x][y+1] = config[x][y][:]
                        config[x][y] = 0
                        config[x][y+1].append("Déplacé")
                    elif case == 6:
                        config[x+1][y-1] = config[x][y][:]
                        config[x][y] = 0
                        config[x+1][y-1].append("Déplacé")
                    elif case == 7:
                        config[x+1][y] = config[x][y][:]
                        config[x][y] = 0
                        config[x+1][y].append("Déplacé")
                    elif case == 8:
                        config[x+1][y+1] = config[x][y][:]
                        config[x][y] = 0
                        config[x+1][y+1].append("Déplacé")
                elif case == 1: # Si la case 1 a une proie
                    config[x-1][y-1] = config[x][y][:] # Copie de la liste sur la nouvelle position
                    config[x][y] = 0 # Suppression de la liste sur l'ancienne position
                    config[x-1][y-1].append("Déplacé") # Ajout du terme "Déplacé" à la fin de la liste pour éviter de déplacer le même animal 2 fois de suite
                    config[x-1][y-1][2] += MIAM # Ajout de MIAM énergie à l'énergie du prédateur
                elif case == 2:
                    config[x-1][y] = config[x][y][:]
                    config[x][y] = 0
                    config[x-1][y].append("Déplacé")
                    config[x-1][y][2] += MIAM
                elif case == 3:
                    config[x-1][y+1] = config[x][y][:]
                    config[x][y] = 0
                    config[x-1][y+1].append("Déplacé")
                    config[x-1][y+1][2] += MIAM
                elif case == 4:
                    config[x][y-1] = config[x][y][:]
                    config[x][y] = 0
                    config[x][y-1].append("Déplacé")
                    config[x][y-1][2] += MIAM
                elif case == 5:
                    config[x][y+1] = config[x][y][:]
                    config[x][y] = 0
                    config[x][y+1].append("Déplacé")
                    config[x][y+1][2] += MIAM
                elif case == 6:
                    config[x+1][y-1] = config[x][y][:]
                    config[x][y] = 0
                    config[x+1][y-1].append("Déplacé")
                    config[x+1][y-1][2] += MIAM
                elif case == 7:
                    config[x+1][y] = config[x][y][:]
                    config[x][y] = 0
                    config[x+1][y].append("Déplacé")
                    config[x+1][y][2] += MIAM
                elif case == 8:
                    config[x+1][y+1] = config[x][y][:]
                    config[x][y] = 0
                    config[x+1][y+1].append("Déplacé")
                    config[x+1][y+1][2] += MIAM


# Compter le nombre d'animaux
def compter_animaux():
    """Compte le nombre total d'animaux, le nombre de proies et le nombre de prédateurs"""
    global nbre_animaux, nbre_proies, nbre_predateurs
    nbre_animaux, nbre_proies, nbre_predateurs = 0, 0, 0
    for x in range(1, N + 1):
        for y in range(1, N + 1):
            if type(config[x][y]) == list: # Si c'est une liste (donc un animal)
                nbre_animaux += 1 # On ajoute 1 au compteur d'animaux
                if config[x][y][0] == "Proie": # Si c'est une proie
                    nbre_proies += 1 # On ajoute 1 au compteur de proies
                if config[x][y][0] == "Prédateur": # Si c'est un prédateur
                    nbre_predateurs += 1 # On ajoute 1 au compteur de prédateurs
    label_animaux.configure(text = ("Nombre d'animaux :", nbre_animaux)) # Actualise le texte du nombre d'animaux
    label_proies.configure(text = ("Nombre de proies :", nbre_proies)) # Actualise le texte du nombre de proies
    label_predateurs.configure(text = ("Nombre de prédateurs :", nbre_predateurs)) # Actualise le texte du nombre de prédateurs


# Tour suivant
def tour_suivant():
    """Fait passer les tours (modification de l'âge, de l'énergie, déplacement et reproduction des animaux)"""
    global config, tour, sauv_validee, nbre_animaux, arret

    vie_energie() # Modification de l'espérance de vie et de l'énergie des animaux
    reproduction_proies() # Reproduction des proies
    reproduction_predateurs() # Reproduction des prédateurs
    deplacement_proies() # Déplacement des proies
    chasse() # Déplacement et chasse des prédateurs

    # Boucle pour supprimer les termes "Reproduit" et "Déplacé" à la fin de chaque liste une fois que tous les déplacements/reproductions de ce tour on été effectués
    for x in range(1, N + 1):
        for y in range(1, N + 1):
            if type(config[x][y]) == list and config[x][y].count("Reproduit") > 0: # Seulement si c'est une liste (donc un animal) et qu'elle contient le terme "Reproduit"
                config[x][y].remove("Reproduit") # Supprimer le terme "Reproduit" de la liste 
            if type(config[x][y]) == list and config[x][y].count("Déplacé") > 0: # Seulement si c'est une liste (donc un animal) et qu'elle contient le terme "Déplacé"
                config[x][y].remove("Déplacé") # Supprimer le terme "Déplacé" de la liste

    affiche_grille(config) # Actualisation de la grille
    tour += 1 # Ajout d'un tour au compteur
    label_tours.configure(text = ("Tour", tour)) # Actualise le texte du numéro de tour
    compter_animaux() # Compter le nombre d'animaux
    if nbre_animaux == 0: # S'il n'y a plus d'animaux
        arret = True # Arrêter la simulation
        bouton_start.configure(text = "Commencer") # Changer le texte du bouton en "Arrêter"
    if not arret: # Si la simulation n'est pas arrêtée
        passage_tours() # Continuer à passer les tours
    if sauv_validee: # Si le message de validation de la sauvegarde est affiché
        sauv_validee = False # Le supprimer (car la matrice affichée n'est plus celle qui a été sauvegardée dans le fichier)
        label_sauv_validee.configure(text = "") # Supprimer le texte "Sauvegarde effectuée"


# Commencer/arrêter le passage des tours
def commencer():
    """Démarre ou arrête le passage des tours"""
    global arret, nbre_animaux
    compter_animaux() # Compter le nombre d'animaux
    if arret == True and nbre_animaux > 0: # Si la simulation est en pause et qu'il y a des animaux
        arret = False
        bouton_start.configure(text = "Arrêter") # Changer le texte du bouton en "Arrêter"
        passage_tours() # Faire passer les tours
    elif not arret: # Si arret == False (simulation en cours)
        arret = True
        bouton_start.configure(text = "Commencer") # Changer le texte du bouton en "Arrêter"
        canvas.after_cancel(var_chrono) # Arrêter le passage des tours


# Passage des tours
def passage_tours():
    """Fait passer les tours"""
    global var_chrono
    var_chrono = canvas.after(CHRONO, tour_suivant) # La fonction tour_suivant est lancée toutes les [CHRONO] ms


# Réinitialiser la matrice
def reinitialiser():
    """Réinitialise la matrice"""
    global arret, tour, sauv_validee
    init_grille() # Création de la grille de départ
    init_proies() # Ajout de Npro proies à des coordonnées aléatoires
    init_prédateurs() # Ajout de Npre prédateurs à des coordonnées aléatoires
    if not arret: # Si la simulation est en cours
        arret = True # Arrêter la simulation
        bouton_start.configure(text = "Commencer") # Changer le texte du bouton "start" en "Arrêter"
    tour = 0 # Réinitialise le numéro du tour
    if sauv_validee: # Si le message de validation de la sauvegarde est affiché
        sauv_validee = False # Le supprimer (car la matrice affichée n'est plus celle qui a été sauvegardée dans le fichier)
        label_sauv_validee.configure(text = "") # Supprimer le texte "Sauvegarde effectuée"


# Sauvegarder la matrice
def sauvegarder():
    """Sauvegarde la matrice actuelle dans un fichier"""
    global sauv_validee
    fic = open("sauvegarde", "w")
    for x in range(1, N + 1):
        for y in range(1, N + 1):
            if config[x][y] == 0: # Si l'élément de la matrice est égal à 0
                fic.write(str(config[x][y])) # L'écrire sur cette ligne
                fic.write("\n") # Ajouter un retour à la ligne pour que le prochain élément soit sur la ligne suivante
            else: # Si c'est la liste d'un animal
                fic.write("ANIMAL\n") # Écrire "ANIMAL" sur cette ligne (avec le retour à la ligne)
                for i in range(0, len(config[x][y])): # Pour chaque élément de la liste de l'animal
                    fic.write(str(config[x][y][i])) # L'ajouter sur la ligne suivante
                    fic.write("\n")
                fic.write("FIN\n") # Puis écrire "FIN" sur la ligne suivante
    sauv_validee = True
    label_sauv_validee.configure(text = "Sauvegarde effectuée") # Afficher le texte "Sauvegarde effectuée" en dessous du bouton
    fic.close()


# Charger la matrice sauvegardée
def charger():
    """Charge la configuration sauvegardée et la retourne si elle a même valeur N que la config courante, sinon retourne config vide"""
    global arret
    fic = open("sauvegarde", "r")
    config = [[0 for x in range(N + 2)] for y in range(N + 2)] # Création de la matrice de taille N + 2 pour les bords
    config[0] = ["#" for x in range(N + 2)] # Ajout de "#" sur le bord gauche (invisible)
    config[-1] = ["#" for x in range(N + 2)] # Ajout de "#" sur le bord droit (invisible)
    for x in range(1, N + 1): # Ajout de "#" en haut et en bas de chaque colonne
        config[x][0] = "#"
        config[x][-1] = "#"
    x = y = 1 # On démarre avec abscisses et ordonnées égales à 1 pour ne pas compter les bords
    cpt = 0
    for ligne in fic: # Pour chaque ligne dans le fichier de sauvegarde
        if ligne == "0\n": # Si la ligne est un 0 (avec \n à la fin pour le saut de ligne présent)
            config[x][y] = 0 # La case correspondante dans la matrice sera un 0
            y += 1 # On ajoute 1 à l'ordonnée pour la prochaine ligne du fichier
            if y == N + 1: # Si l'ordonnée est supérieur à la taille de la matrice
                y = 1 # On la réinitialise à 1 (on revient à la première ligne)
                x += 1 # Et on ajout 1 à l'abscisse (on passe à la colonne à droite)
        if ligne == "ANIMAL\n": # (cf l'organisation du fichier sauvegarde) Si la ligne est "ANIMAL" (avec le saut de ligne à la fin) 
            cpt += 1 # On ajout 1 au compteur (on entre dans la liste d'un animal)
            config[x][y] = [] # Création de la liste de l'animal
        elif ligne == "FIN\n": # (cf l'organisation du fichier sauvegarde) Si la ligne n'est pas "FIN" (avec le saut de ligne à la fin) 
            cpt = 0 # On remet le compteur à 0 (fin de la liste de l'animal)
            y += 1 # On ajoute 1 à l'ordonnée pour la prochaine ligne du fichier
            if y == N + 1: # Si l'ordonnée est supérieur à la taille de la matrice
                y = 1 # On la réinitialise à 1 (on revient à la première ligne)
                x += 1 # Et on ajout 1 à l'abscisse (on passe à la colonne à droite)
        elif cpt == 1: # Si le compteur est égal à 1 (c'est la liste d'un animal)
            if ligne == "Proie\n": # Si la ligne est "Proie"
                config[x][y].append("Proie") # On ajoute "Proie" dans la liste de l'animal
            elif ligne == "Prédateur\n": # Idem
                config[x][y].append("Prédateur")
            elif ligne == "Reproduit\n":
                config[x][y].append("Reproduit")
            elif ligne == "Déplacé\n":
                config[x][y].append("Déplacé")
            else: # Si c'est aucun des 4 termes possibles (donc c'est un nombre)
                config[x][y].append(int(ligne)) # On ajoute le nombre dans la liste
    fic.close()
    affiche_grille(config)
    compter_animaux() # Compter le nombre d'animaux
    if not arret: # Si la simulation est en cours
        arret = True # Arrêter la simulation
        bouton_start.configure(text = "Commencer") # Changer le texte du bouton "start" en "Arrêter"



### Programme principal

# Définition des widgets
racine = tk.Tk()
racine.title("Simulation proies-prédateurs")
canvas = tk.Canvas(racine, width = LARGEUR, height = HAUTEUR)
bouton_start = tk.Button(racine, text = "Commencer", command = commencer, width = 10, font = ("bold", 12)) # Bouton pour commencer ou arrêter le passage des tours
bouton_reinit = tk.Button(racine, text = "Réinitialiser", command = reinitialiser, font = ("bold", 10)) # Bouton pour commencer ou arrêter le passage des tours
bouton_sauver = tk.Button(racine, text = "Sauvegarder", command = sauvegarder, width = 10, font = ("bold", 10)) # Bouton pour commencer ou arrêter le passage des tours
bouton_charger = tk.Button(racine, text = "Charger", command = charger, font = ("bold", 10)) # Bouton pour commencer ou arrêter le passage des tours
label_tours = tk.Label(racine, text = ("Tour", tour), font = ("bold", 15)) # Texte pour afficher le numéro du tour actuel
label_sauv_validee = tk.Label(racine, width = 30, font = ("bold", 8)) # Texte pour indiquer que la matrice actuellement affichée est sauvegardée dans le fichier
label_animaux = tk.Label(racine, text = ("Nombre d'animaux :", (Npro + Npre)), font = ("bold", 8)) # Texte pour indiquer le nombre d'animaux en vie
label_proies = tk.Label(racine, text = ("Nombre de proies :", Npro), font = ("bold", 8)) # Texte pour indiquer le nombre de proies en vie
label_predateurs = tk.Label(racine, text = ("Nombre de prédateurs :", Npre), font = ("bold", 8))  # Texte pour indiquer le nombre de prédateurs en vie

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