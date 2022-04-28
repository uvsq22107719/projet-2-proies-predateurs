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
LARGEUR = 700 # Largeur du canevas
LARGEUR_CASE = LARGEUR / 1.1 // N # Largeur des cases
HAUTEUR_CASE = HAUTEUR / 1.1 // N # Hauteur des cases

MIAM = 5 # Niveau d'énergie gagné lorsqu'un prédateur mange une proie
FLAIR = 5 # Distance maximale à laquelle un prédateur peut sentir un proie
Epre_repro = 15 # Niveau d'énergie nécessaire pour qu'un prédateur puisse se reproduire
Epro_repro = 2 # Niveau d'énergie nécessaire pour qu'une proie puisse se reproduire


### Définitions des variables globales

arret = True # Variable pour arrêter le passage des tours
id_after = 0 # Variable pour le compte à rebours entre chaque tours

tour = 0 # Numéro du tour

Npro = 50 # Nombre initial de proies (Npro proies apparaissent au début)
Apro = 5 # Espérance de vie des proies en nombre de tours
Epro = 2 # Énergie des proies (augmente de 1 par tour avec 3 en plafond. Baisse de 3 par reproduction)


Npre = 5 # Nombre initial de prédateurs (Npre prédateurs apparaissent au début)
Apre = 15 # Espérance de vie des prédateurs en nombre de tours
Epre = 12 # Énergie des prédateurs (baisse de 1 par tour, s'il elle atteint zéro, le prédateur meurt de faim)



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
            return "grey" # Couleur pour mettre les erreurs en évidence


# Création de la grille
def init_grille():
    """Retourne une grille carrée vide dimension N+2, les éléments de la configuration vont de 1 à N les indices 0 et N+1 sont les bords et permettent de ne pas gérer de cas particuliers"""
    global grille, config
    grille = [[0 for i in range(N + 2)] for j in range(N + 2)] # Création de la matrice de taille N + 2 pour les bords
    grille[0] = ["#" for i in range(N + 2)] # Ajout de "#" sur le bord gauche (invisible)
    grille[-1] = ["#" for i in range(N + 2)] # Ajout de "#" sur le bord droit (invisible)
    for i in range(1, N + 1): # Ajout de "#" en haut et en bas de chaque colonne
        grille[i][0] = "#"
        grille[i][-1] = "#"
    config = [[0 for i in range(N + 2)] for j in range(N + 2)] # Création de la matrice de taille N + 2 pour les bords
    config[0] = ["#" for i in range(N + 2)] # Ajout de "#" sur le bord gauche (invisible)
    config[-1] = ["#" for i in range(N + 2)] # Ajout de "#" sur le bord droit (invisible)
    for i in range(1, N + 1): # Ajout de "#" en haut et en bas de chaque colonne
        config[i][0] = "#"
        config[i][-1] = "#"
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
    for i in range(1, N + 1):
        for j in range(1, N + 1):
            col = choix_couleur(config[i][j])
            canvas.itemconfigure(grille[i][j], fill = col)


# Initialise les proies
def init_proies():
    """Ajoute Npro proies à des coordonnées aléatoires"""
    global config
    cpt = Npro
    while cpt > 0:
        i, j = rd.randint(1, N), rd.randint(1, N) # Génération des coordonnées aléatoires
        if config[i][j] == 0: # Si c'est une case vide
            config[i][j] = ["Proie", Apro, Epro] # Création d'une liste avec toutes les infos sur l'animal (ici c'est une proie avec Apro le nombre de tours d'espérance de vie)
            cpt -= 1
    affiche_grille(config)


# Initialise les prédateurs
def init_prédateurs():
    """Ajoute Npre prédateurs à des coordonnées aléatoires"""
    global config
    cpt = Npre
    while cpt > 0:
        i, j = rd.randint(1, N), rd.randint(1, N) # Génération des coordonnées aléatoires
        if config[i][j] == 0: # Si c'est une case vide
            config[i][j] = ["Prédateur", Apre, Epre] # Création d'une liste avec toutes les infos sur l'animal (ici c'est un prédateur avec Apre le nombre de tours d'espérance de vie puis Epre l'énergie du prédateur)
            cpt -= 1
    affiche_grille(config)


# Retourne une case adjacente aléatoire selon la condition demandée
def direction(i, j, n):
    """Retourne une case adjacente aléatoire ayant pour condition n (par exemple 0 ou Proie)"""
    case_1, case_2, case_3, case_4, case_5, case_6, case_7, case_8 = False, False, False, False, False, False, False, False # Création des variables pour chaque case (False = indisponible, True = disponible)
    if not type(config[i-1][j-1]) == list and config[i-1][j-1] == n: # Si ce n'est pas une liste et que c'est égal à n
        case_1 = True # La case est disponible
    if not type(config[i-1][j-1]) == list and config[i-1][j] == n: # Idem pour les 8 directions possibles
        case_2 = True
    if not type(config[i-1][j+1]) == list and config[i-1][j+1] == n:
        case_3 = True
    if not type(config[i][j-1]) == list and config[i][j-1] == n:
        case_4 = True
    if not type(config[i][j+1]) == list and config[i][j+1] == n:
        case_5 = True
    if not type(config[i+1][j-1]) == list and config[i+1][j-1] == n:
        case_6 = True
    if not type(config[i+1][j]) == list and config[i+1][j] == n:
        case_7 = True
    if not type(config[i+1][j+1]) == list and config[i+1][j+1] == n:
        case_8 = True

    if type(config[i-1][j-1]) == list and config[i-1][j-1][0] == n: # Si c'est une liste et que le premier terme est n (par exemple "Proie")
        case_1 = True
    if type(config[i-1][j]) == list and config[i-1][j][0] == n:
        case_2 = True
    if type(config[i-1][j+1]) == list and config[i-1][j+1][0] == n:
        case_3 = True
    if type(config[i][j-1]) == list and config[i][j-1][0] == n:
        case_4 = True
    if type(config[i][j+1]) == list and config[i][j+1][0] == n:
        case_5 = True
    if type(config[i+1][j-1]) == list and config[i+1][j-1][0] == n:
        case_6 = True
    if type(config[i+1][j]) == list and config[i+1][j][0] == n:
        case_7 = True
    if type(config[i+1][j+1]) == list and config[i+1][j+1][0] == n:
        case_8 = True
    if case_1 == False and case_2 == False and case_3 == False and case_4 == False and case_5 == False and case_6 == False and case_7 == False and case_8 == False:
        case = 0
    else:
        t = True
        while t:
            x = rd.randint(1, 8) # Génération d'un chiffre aléatoire entre 1 et 8 pour choisir la direction aléatoirement
            if case_1 and x == 1: # Si la case 1 est disponible et que le chiffre aléatoire est 1
                case = 1 # On retourne une valeur de 1
                t = False # Variable pour arrêter la boucle
            elif case_2 and x == 2: # Idem pour les 8 cases possibles
                case = 2
                t = False
            elif case_3 and x == 3:
                case = 3
                t = False
            elif case_4 and x == 4:
                case = 4
                t = False
            elif case_5 and x == 5:
                case = 5
                t = False
            elif case_6 and x == 6:
                case = 6
                t = False
            elif case_7 and x == 7:
                case = 7
                t = False
            elif case_8 and x == 8:
                case = 8
                t = False
    return case # Retourner la valeur de case (comprise entre 0 et 8 inclus)


# Tour suivant
def tour_suivant():
    """Fait passer les tours (ajout de proies, modification de l'âge, déplacement des proies, ...)"""
    global config
    global tour

    # Modification de l'espérance de vie (retirer 1 à chaque tour)
    for i in range(1, N + 1): # Pour chaque liste (ex : [0, 0, ["Proie", 5, 3], ["Proie", 2, 3], 0, ["Prédateur", 15, 12], 0])
        for j in range(1, N + 1): # Pour chaque élément dans la liste (ex : ["Proie", 5, 3])
            if type(config[i][j]) == list and config[i][j][0] == "Proie" and config[i][j][2] < Epro_repro: # Si c'est une proie et que celle-ci a une énergie inférieure à Erepro
                config[i][j][2] += 1 # Ajouter 1 d'énergie
            if type(config[i][j]) == list: # Seulement si c'est une liste (pas un 0 ou un #)
                config[i][j][1] -= 1 # Retirer 1 à l'espérance de vie (ex : ["Proie", 5, 3] devient ["Proie", 4, 3])
                if config[i][j][1] == 0: # Si c'est par exemple [Proie, 0]
                    config[i][j] = 0 # Remplacer par 0 (mort de l'animal)

    # Modification de l'énergie des prédateurs (retirer 1 à chaque tour)
    for i in range(1, N + 1): # Pour chaque liste (ex : [0, 0, ["Proie", 5, 3], ["Proie", 2, 3], 0, ["Prédateur", 15, 12], 0])
        for j in range(1, N + 1): # Pour chaque élément dans la liste (ex : ["Proie", 5, 3])
            if type(config[i][j]) == list and config[i][j][0] == "Prédateur": # Seulement si c'est un prédateur
                config[i][j][2] -= 1 # Retirer 1 à l'espérance de vie (ex : ["Prédateur", 14, 12] devient ["Prédateur", 14, 11])
                if config[i][j][2] == 0: # Si c'est par exemple ["Prédateur", 14, 0]
                    config[i][j] = 0 # Remplacer par 0 (mort de l'animal)

    # Déplacement des proies
    for i in range(1, N + 1):
        for j in range(1, N + 1):
            if type(config[i][j]) == list and config[i][j][0] == "Proie" and config[i][j][-1] != "Déplacé" : # Seulement si c'est une proie et qu'elle n'a pas déjà effectué un déplacement pendant ce tour
                case = direction(i, j, 0)
                if case == 0: # Si aucune case adjacente n'est vide
                    break # Arrêter la boucle
                elif case == 1: # Si la case 1 est libre
                    config[i-1][j-1] = config[i][j][:] # Copie de la liste sur la nouvelle position
                    config[i][j] = 0 # Suppression de la liste sur l'ancienne position
                    config[i-1][j-1].append("Déplacé") # Ajout du terme "Déplacé" à la fin de la liste pour éviter de déplacer la même proie 2 fois de suite
                elif case == 2:
                    config[i-1][j] = config[i][j][:]
                    config[i][j] = 0
                    config[i-1][j].append("Déplacé")
                elif case == 3:
                    config[i-1][j+1] = config[i][j][:]
                    config[i][j] = 0
                    config[i-1][j+1].append("Déplacé")
                elif case == 4:
                    config[i][j-1] = config[i][j][:]
                    config[i][j] = 0
                    config[i][j-1].append("Déplacé")
                elif case == 5:
                    config[i][j+1] = config[i][j][:]
                    config[i][j] = 0
                    config[i][j+1].append("Déplacé")
                elif case == 6:
                    config[i+1][j-1] = config[i][j][:]
                    config[i][j] = 0
                    config[i+1][j-1].append("Déplacé")
                elif case == 7:
                    config[i+1][j] = config[i][j][:]
                    config[i][j] = 0
                    config[i+1][j].append("Déplacé")
                elif case == 8:
                    config[i+1][j+1] = config[i][j][:]
                    config[i][j] = 0
                    config[i+1][j+1].append("Déplacé")

    for i in range(1, N + 1): # Boucle pour supprimer le terme "Déplacé" à la fin de chaque liste une fois que tous les déplacement de ce tour on été effectués
        for j in range(1, N + 1):
            if type(config[i][j]) == list and config[i][j][-1] == "Déplacé": # Seulement si c'est une liste (donc un animal) et qu'elle a le terme "Déplacé" à la fin
                del config[i][j][-1] # Supprimer le dernier terme de la liste ("Déplacé")

    # Reproduction des proies
    for i in range(1, N + 1):
        for j in range(1, N + 1):
            if type(config[i][j]) == list and config[i][j][0] == "Proie" and config[i][j][-1] != "Reproduit" and config[i][j][2] >= Epro_repro: # Seulement si c'est une proie et qu'elle ne s'est pas déjà reproduite pendant ce tour
                case = direction(i, j, "Proie")
                if case == 0: # Si aucune case adjacente n'a de proie
                    break # Annuler la boucle
                elif case == 1: # Si la case 1 est une proie
                    config[i][j].append("Reproduit") # Ajout du terme "Reproduit" à la fin de la liste pour éviter que les proies se reproduisent plusieurs fois par tour
                    config[i][j][2] -= 3
                    config[i-1][j-1].append("Reproduit")
                    config[i-1][j-1][2] -= 3
                    case = direction(i, j, 0)
                    if case == 0: # Si aucune case n'est vide (pas de place pour une nouvelle proie)
                        break # Annuler la boucle
                    elif case == 2: # Si la case 2 est disponible
                        config[i-1][j] = ["Proie", Apro, Epro] # Ajouter une proies avec une espérance de vie de Apro tours
                    elif case == 3:
                        config[i-1][j+1] = ["Proie", Apro, Epro]
                    elif case == 4:
                        config[i][j-1] = ["Proie", Apro, Epro]
                    elif case == 5:
                        config[i][j+1] = ["Proie", Apro, Epro]
                    elif case == 6:
                        config[i+1][j-1] = ["Proie", Apro, Epro]
                    elif case == 7:
                        config[i+1][j] = ["Proie", Apro, Epro]
                    elif case == 8:
                        config[i+1][j+1] = ["Proie", Apro, Epro]
                elif case == 2:
                    config[i][j].append("Reproduit")
                    config[i][j][2] -= 3
                    config[i-1][j].append("Reproduit")
                    config[i-1][j][2] -= 3
                    case = direction(i, j, 0)
                    if case == 0:
                        pass
                    elif case == 1:
                        config[i-1][j-1] = ["Proie", Apro, Epro]
                    elif case == 3:
                        config[i-1][j+1] = ["Proie", Apro, Epro]
                    elif case == 4:
                        config[i][j-1] = ["Proie", Apro, Epro]
                    elif case == 5:
                        config[i][j+1] = ["Proie", Apro, Epro]
                    elif case == 6:
                        config[i+1][j-1] = ["Proie", Apro, Epro]
                    elif case == 7:
                        config[i+1][j] = ["Proie", Apro, Epro]
                    elif case == 8:
                        config[i+1][j+1] = ["Proie", Apro, Epro]
                elif case == 3:
                    config[i][j].append("Reproduit")
                    config[i][j][2] -= 3
                    config[i-1][j+1].append("Reproduit")
                    config[i-1][j+1][2] -= 3
                    case = direction(i, j, 0)
                    if case == 0:
                        pass
                    elif case == 1:
                        config[i-1][j-1] = ["Proie", Apro, Epro]
                    elif case == 2:
                        config[i-1][j] = ["Proie", Apro, Epro]
                    elif case == 4:
                        config[i][j-1] = ["Proie", Apro, Epro]
                    elif case == 5:
                        config[i][j+1] = ["Proie", Apro, Epro]
                    elif case == 6:
                        config[i+1][j-1] = ["Proie", Apro, Epro]
                    elif case == 7:
                        config[i+1][j] = ["Proie", Apro, Epro]
                    elif case == 8:
                        config[i+1][j+1] = ["Proie", Apro, Epro]
                elif case == 4:
                    config[i][j].append("Reproduit")
                    config[i][j][2] -= 3
                    config[i][j-1].append("Reproduit")
                    config[i][j-1][2] -= 3
                    case = direction(i, j, 0)
                    if case == 0:
                        pass
                    elif case == 1:
                        config[i-1][j-1] = ["Proie", Apro, Epro]
                    elif case == 2:
                        config[i-1][j] = ["Proie", Apro, Epro]
                    elif case == 3:
                        config[i-1][j+1] = ["Proie", Apro, Epro]
                    elif case == 5:
                        config[i][j+1] = ["Proie", Apro, Epro]
                    elif case == 6:
                        config[i+1][j-1] = ["Proie", Apro, Epro]
                    elif case == 7:
                        config[i+1][j] = ["Proie", Apro, Epro]
                    elif case == 8:
                        config[i+1][j+1] = ["Proie", Apro, Epro]
                elif case == 5:
                    config[i][j].append("Reproduit")
                    config[i][j][2] -= 3
                    config[i][j+1].append("Reproduit")
                    config[i][j+1][2] -= 3
                    case = direction(i, j, 0)
                    if case == 0:
                        pass
                    elif case == 1:
                        config[i-1][j-1] = ["Proie", Apro, Epro]
                    elif case == 2:
                        config[i-1][j] = ["Proie", Apro, Epro]
                    elif case == 3:
                        config[i-1][j+1] = ["Proie", Apro, Epro]
                    elif case == 4:
                        config[i][j-1] = ["Proie", Apro, Epro]
                    elif case == 6:
                        config[i+1][j-1] = ["Proie", Apro, Epro]
                    elif case == 7:
                        config[i+1][j] = ["Proie", Apro, Epro]
                    elif case == 8:
                        config[i+1][j+1] = ["Proie", Apro, Epro]
                elif case == 6:
                    config[i][j].append("Reproduit")
                    config[i][j][2] -= 3
                    config[i+1][j-1].append("Reproduit")
                    config[i+1][j-1][2] -= 3
                    case = direction(i, j, 0)
                    if case == 0:
                        pass
                    elif case == 1:
                        config[i-1][j-1] = ["Proie", Apro, Epro]
                    elif case == 2:
                        config[i-1][j] = ["Proie", Apro, Epro]
                    elif case == 3:
                        config[i-1][j+1] = ["Proie", Apro, Epro]
                    elif case == 4:
                        config[i][j-1] = ["Proie", Apro, Epro]
                    elif case == 5:
                        config[i][j+1] = ["Proie", Apro, Epro]
                    elif case == 7:
                        config[i+1][j] = ["Proie", Apro, Epro]
                    elif case == 8:
                        config[i+1][j+1] = ["Proie", Apro, Epro]
                elif case == 7:
                    config[i][j].append("Reproduit")
                    config[i][j][2] -= 3
                    config[i+1][j].append("Reproduit")
                    config[i+1][j][2] -= 3
                    case = direction(i, j, 0)
                    if case == 0:
                        pass
                    elif case == 1:
                        config[i-1][j-1] = ["Proie", Apro, Epro]
                    elif case == 2:
                        config[i-1][j] = ["Proie", Apro, Epro]
                    elif case == 3:
                        config[i-1][j+1] = ["Proie", Apro, Epro]
                    elif case == 4:
                        config[i][j-1] = ["Proie", Apro, Epro]
                    elif case == 5:
                        config[i][j+1] = ["Proie", Apro, Epro]
                    elif case == 6:
                        config[i+1][j-1] = ["Proie", Apro, Epro]
                    elif case == 8:
                        config[i+1][j+1] = ["Proie", Apro, Epro]
                elif case == 8:
                    config[i][j].append("Reproduit")
                    config[i][j][2] -= 3
                    config[i+1][j+1].append("Reproduit")
                    config[i+1][j+1][2] -= 3
                    case = direction(i, j, 0)
                    if case == 0:
                        pass
                    elif case == 1:
                        config[i-1][j-1] = ["Proie", Apro, Epro]
                    elif case == 2:
                        config[i-1][j] = ["Proie", Apro, Epro]
                    elif case == 3:
                        config[i-1][j+1] = ["Proie", Apro, Epro]
                    elif case == 4:
                        config[i][j-1] = ["Proie", Apro, Epro]
                    elif case == 5:
                        config[i][j+1] = ["Proie", Apro, Epro]
                    elif case == 6:
                        config[i+1][j-1] = ["Proie", Apro, Epro]
                    elif case == 7:
                        config[i+1][j] = ["Proie", Apro, Epro]

    # Reproduction des prédateurs
    for i in range(1, N + 1):
        for j in range(1, N + 1):
            if type(config[i][j]) == list and config[i][j][0] == "Prédateur" and config[i][j][-1] != "Reproduit" and config[i][j][2] >= Epre_repro: # Seulement si c'est un prédateur, qu'il ne s'est pas déjà reproduit pendant ce tour et que son niveau d'énergie est supérieur ou égal au niveau d'énergie Epre_repro nécessaire pour pouvoir se reproduire
                config[i][j].append("Reproduit")
                cpt_repro = 1
                r = True
                while r == True and cpt_repro != 0:
                    i = rd.randint(1, N + 1)
                    j = rd.randint(1, N + 1)
                    if config[i][j] == 0:
                        config[i][j] = ["Prédateur", Apro, Epre]
                        cpt_repro -= 1
                        r = False

    for i in range(1, N + 1): # Boucle pour supprimer le terme "Reproduit" à la fin de chaque liste une fois que toutes les proies qui le peuvent se sont reproduites pendant ce tour
        for j in range(1, N + 1):
            if type(config[i][j]) == list and config[i][j][-1] == "Reproduit": # Seulement si c'est une liste (donc un animal) et qu'elle a le terme "Reproduit" à la fin
                del config[i][j][-1] # Supprimer le dernier terme de la liste ("Reproduit")

    # Déplacement et chasse des prédateurs
    for i in range(1, N + 1):
        for j in range(1, N + 1):
            if type(config[i][j]) == list and config[i][j][0] == "Prédateur" and config[i][j][-1] != "Déplacé" : # Seulement si c'est un prédateur et qu'il n'a pas déjà effectué un déplacement pendant ce tour
                case = direction(i, j, "Proie")
                if case == 0:
                    case = direction(i, j, 0)
                    if case == 0:
                        break
                    elif case == 1: # Si la case 1 a une proie
                        config[i-1][j-1] = config[i][j][:] # Copie de la liste sur la nouvelle position
                        config[i][j] = 0 # Suppression de la liste sur l'ancienne position
                        config[i-1][j-1].append("Déplacé") # Ajout du terme "Déplacé" à la fin de la liste pour éviter de déplacer la même proie 2 fois de suite
                    elif case == 2:
                        config[i-1][j] = config[i][j][:]
                        config[i][j] = 0
                        config[i-1][j].append("Déplacé")
                    elif case == 3:
                        config[i-1][j+1] = config[i][j][:]
                        config[i][j] = 0
                        config[i-1][j+1].append("Déplacé")
                    elif case == 4:
                        config[i][j-1] = config[i][j][:]
                        config[i][j] = 0
                        config[i][j-1].append("Déplacé")
                    elif case == 5:
                        config[i][j+1] = config[i][j][:]
                        config[i][j] = 0
                        config[i][j+1].append("Déplacé")
                    elif case == 6:
                        config[i+1][j-1] = config[i][j][:]
                        config[i][j] = 0
                        config[i+1][j-1].append("Déplacé")
                    elif case == 7:
                        config[i+1][j] = config[i][j][:]
                        config[i][j] = 0
                        config[i+1][j].append("Déplacé")
                    elif case == 8:
                        config[i+1][j+1] = config[i][j][:]
                        config[i][j] = 0
                        config[i+1][j+1].append("Déplacé")
                elif case == 1: # Si la case 1 a une proie
                    config[i-1][j-1] = config[i][j][:] # Copie de la liste sur la nouvelle position
                    config[i][j] = 0 # Suppression de la liste sur l'ancienne position
                    config[i-1][j-1].append("Déplacé") # Ajout du terme "Déplacé" à la fin de la liste pour éviter de déplacer la même proie 2 fois de suite
                    config[i-1][j-1][2] += MIAM # Ajout de MIAM énergie à l'énergie du prédateur
                elif case == 2:
                    config[i-1][j] = config[i][j][:]
                    config[i][j] = 0
                    config[i-1][j].append("Déplacé")
                    config[i-1][j][2] += MIAM
                elif case == 3:
                    config[i-1][j+1] = config[i][j][:]
                    config[i][j] = 0
                    config[i-1][j+1].append("Déplacé")
                    config[i-1][j+1][2] += MIAM
                elif case == 4:
                    config[i][j-1] = config[i][j][:]
                    config[i][j] = 0
                    config[i][j-1].append("Déplacé")
                    config[i][j-1][2] += MIAM
                elif case == 5:
                    config[i][j+1] = config[i][j][:]
                    config[i][j] = 0
                    config[i][j+1].append("Déplacé")
                    config[i][j+1][2] += MIAM
                elif case == 6:
                    config[i+1][j-1] = config[i][j][:]
                    config[i][j] = 0
                    config[i+1][j-1].append("Déplacé")
                    config[i+1][j-1][2] += MIAM
                elif case == 7:
                    config[i+1][j] = config[i][j][:]
                    config[i][j] = 0
                    config[i+1][j].append("Déplacé")
                    config[i+1][j][2] += MIAM
                elif case == 8:
                    config[i+1][j+1] = config[i][j][:]
                    config[i][j] = 0
                    config[i+1][j+1].append("Déplacé")
                    config[i+1][j+1][2] += MIAM

    for i in range(1, N + 1): # Boucle pour supprimer le terme "Déplacé" à la fin de chaque liste une fois que tous les déplacement de ce tour on été effectués
        for j in range(1, N + 1):
            if type(config[i][j]) == list and config[i][j][-1] == "Déplacé": # Seulement si c'est une liste (donc un animal) et qu'elle a le terme "Déplacé" à la fin
                del config[i][j][-1] # Supprimer le dernier terme de la liste ("Déplacé")

    affiche_grille(config) # Actualisation de la grille
    tour += 1 # Ajout d'un tour au compteur
    label_tours.configure(text = ("Tour", tour)) # Actualise le texte du numéro de tour
    if not arret: # Si la simulation n'est pas arrêtée
        passage_tours() # Continuer à passer les tours

# Commencer/arrêter le passage des tours
def commencer():
    """Démarre ou arrête le passage des tours"""
    global arret
    if arret:
        arret = False
        bouton_start.configure(text = "Arrêter")
        passage_tours()
    else:
        arret = True
        bouton_start.configure(text = "Commencer")
        canvas.after_cancel(id_after)

# Passage des tours
def passage_tours():
    """Fait passer les tours"""
    global id_after
    id_after = canvas.after(500, tour_suivant)


### Programme principal

# Définition des widgets
racine = tk.Tk()
racine.title("Simulation proies-prédateurs")
canvas = tk.Canvas(racine, width = LARGEUR, height = HAUTEUR)
init_grille() # Création de la grille de départ
init_proies() # Ajout de Npro proies à des coordonnées aléatoires
init_prédateurs() # Ajout de Npre prédateurs à des coordonnées aléatoires
bouton_start = tk.Button(racine, text = "Commencer", command = commencer) # Bouton pour commencer ou arrêter le passage des tours
label_tours = tk.Label(racine, text = ("Tour", tour)) # Texte pour affiche le numéro du tour actuel

# Placement des widgets
canvas.grid(column = 1, row = 0, rowspan = 4)
bouton_start.grid(column = 0, row = 1)
label_tours.grid(column = 0, row = 0)

# Boucle principale
racine.mainloop()