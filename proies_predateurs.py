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

N = 10 # Taille de la matrice
HAUTEUR = 700 # Hauteur du canevas
LARGEUR = 700 # Largeur du canevas
LARGEUR_CASE = LARGEUR / 1.1 // N # Largeur des cases
HAUTEUR_CASE = HAUTEUR / 1.1 // N # Hauteur des cases

MIAM = 5 # Niveau d'énergie gagné lorsqu'un prédateur mange une proie
Erepro = 15 # Niveau d'énergie nécessaire pour qu'un prédateur puisse se reproduire
FLAIR = 5 # Distance maximale à laquelle un prédateur peut sentir un proie


### Définitions des variables globales

tour = 0 # Numéro du tour

Npro = 1 # Nombre initial de proies (Npro proies apparaissent au début)
Fpro = 3 # Fréquence de naissance des proies (Fpro proies naissent à chaque tour)
Apro = 5 # Espérance de vie des proies en nombre de tours
Npre = 2 # Nombre initial de prédateurs (Npre prédateurs apparaissent au début)
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
            config[i][j] = ["Proie", Apro] # Création d'une liste avec toutes les infos sur l'animal (ici c'est une proie avec Apro le nombre de tours d'espérance de vie)
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
            config[i][j] = ["Prédateur", Apre] # Création d'une liste avec toutes les infos sur l'animal (ici c'est une Prédateur avec Apre le nombre de tours d'espérance de vie)
            cpt -= 1
    affiche_grille(config)


def direction(i, j, n):
    case_1 = False
    case_2 = False
    case_3 = False
    case_4 = False
    case_5 = False
    case_6 = False
    case_7 = False
    case_8 = False
    if not type(config[i-1][j-1]) == list and config[i-1][j-1] == n:
        case_1 = True
    if not type(config[i-1][j-1]) == list and config[i-1][j] == n:
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

    if type(config[i-1][j-1]) == list and config[i-1][j-1][0] == n:
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
    t = True
    while t == True:
        x = rd.randint(1, 8) # Génération d'un chiffre aléatoire entre 1 et 8 pour choisir la direction aléatoirement
        if case_1 == True and x == 1:
            case = 1
            t = False
        elif case_2 == True and x == 2:
            case = 2
            t = False
        elif case_3 == True and x == 3:
            case = 3
            t = False
        elif case_4 == True and x == 4:
            case = 4
            t = False
        elif case_5 == True and x == 5:
            case = 5
            t = False
        elif case_6 == True and x == 6:
            case = 6
            t = False
        elif case_7 == True and x == 7:
            case = 7
            t = False
        elif case_8 == True and x == 8:
            case = 8
            t = False
    return case



                        

# Passe un tour
def passer_tour():
    """Fait passer les tours (ajout de proies, modification de l'âge, déplacement des proies, ...)"""
    global config
    global tour

    # Modification de l'espérance de vie (retirer 1 à chaque tour)
    for i in range(1, N + 1): # Pour chaque ligne (ex : [0, 0, ["Proie", 5], ["Proie", 2], 0, ["Prédateur", 5], 0])
        for j in range(1, N + 1): # Pour chaque élément (ex : ["Proie", 5])
            if type(config[i][j]) == list : # Seulement si c'est une liste (pas un 0 ou un #)
                config[i][j][1] -= 1 # Retirer 1 à l'espérance de vie (ex : ["Proie", 5] devient ["Proie", 4])
                if config[i][j][1] == 0: # Si c'est par exemple [Proie, 0]
                    config[i][j] = 0 # Remplacer par 0 (mort de l'animal)

    # Ajout de proies
    cpt = Fpro # Compteur égal à Fpro, la fréquence de naissance des proies
    while cpt > 0:
        i, j = rd.randint(1, N), rd.randint(1, N) # Génération des coordonnées aléatoires
        if config[i][j] == 0: # Si la case est vide
            config[i][j] = ["Proie", Apro] # Création d'une liste avec toutes les infos sur l'animal (ici c'est une proie avec Apro le nombre de tours d'espérance de vie)
            cpt -= 1
        else: # Si la case n'est pas vide
            continue # Recommencer la boucle

    # Déplacement des proies
    for i in range(1, N + 1):
        for j in range(1, N + 1):
            if type(config[i][j]) == list and config[i][j][0] == "Proie" and config[i][j][-1] != "Déplacé" : # Seulement si c'est une proie et qu'elle n'a pas déjà effectué un déplacement pendant ce tour
                deplacement = False # Variable pour arrêter la boucle quand le déplacement est effectué
                while deplacement == False:
                    n = rd.randint(1,8) # Génération d'un chiffre aléatoire entre 1 et 8 pour choisir la direction aléatoirement
                    if n == 1 and config[i-1][j-1] == 0: # Si le chiffre aléatoire est 1, on choisit la 1ère direction (en haut à gauche de la proie) si la case est vide
                        config[i-1][j-1] = config[i][j][:] # Copie de la liste sur la nouvelle position
                        config[i][j] = 0 # Suppression de la liste sur l'ancienne position
                        config[i-1][j-1].append("Déplacé") # Ajout du terme "Déplacé" à la fin de la liste pour éviter de déplacer la même proie 2 fois de suite
                        deplacement = True # Variable pour arrêter la boucle
                    elif n == 2 and config[i-1][j] == 0:
                        config[i-1][j] = config[i][j][:]
                        config[i][j] = 0
                        config[i-1][j].append("Déplacé")
                        deplacement = True
                    elif n == 3 and config[i-1][j+1] == 0:
                        config[i-1][j+1] = config[i][j][:]
                        config[i][j] = 0
                        config[i-1][j+1].append("Déplacé")
                        deplacement = True
                    elif n == 4 and config[i][j-1] == 0:
                        config[i][j-1] = config[i][j][:]
                        config[i][j] = 0
                        config[i][j-1].append("Déplacé")
                        deplacement = True
                    elif n == 5 and config[i][j+1] == 0:
                        config[i][j+1] = config[i][j][:]
                        config[i][j] = 0
                        config[i][j+1].append("Déplacé")
                        deplacement = True
                    elif n == 6 and config[i+1][j-1] == 0:
                        config[i+1][j-1] = config[i][j][:]
                        config[i][j] = 0
                        config[i+1][j-1].append("Déplacé")
                        deplacement = True
                    elif n == 7 and config[i+1][j] == 0:
                        config[i+1][j] = config[i][j][:]
                        config[i][j] = 0
                        config[i+1][j].append("Déplacé")
                        deplacement = True
                    elif n == 8 and config[i+1][j+1] == 0:
                        config[i+1][j+1] = config[i][j][:]
                        config[i][j] = 0
                        config[i+1][j+1].append("Déplacé")
                        deplacement = True
    for i in range(1, N + 1): # Boucle pour supprimer le terme "Déplacé" à la fin de chaque liste une fois que tous les déplacement de ce tour on été effectués
        for j in range(1, N + 1):
            if type(config[i][j]) == list and config[i][j][-1] == "Déplacé": # Seulement si c'est une liste (donc un animal) et qu'elle a le terme "Déplacé" à la fin
                del config[i][j][-1]

    # Reproduction des proies
    for i in range(1, N + 1):
        for j in range(1, N + 1):
            if type(config[i][j]) == list and config[i][j][0] == "Proie" and config[i][j][-1] != "Reproduit" : # Seulement si c'est une proie et qu'elle ne s'est pas déjà reproduite pendant ce tour
                case = direction(i, j, "Proie")
                if case == 1:
                    config[i][j].append("Reproduit")
                    config[i-1][j-1].append("Reproduit")
                    case = direction(i, j, 0)
                    if case == 2:
                        config[i-1][j] = ["Proie", Apro]
                    if case == 3:
                        config[i-1][j+1] = ["Proie", Apro]
                    if case == 4:
                        config[i][j-1] = ["Proie", Apro]
                    if case == 5:
                        config[i][j+1] = ["Proie", Apro]
                    if case == 6:
                        config[i+1][j-1] = ["Proie", Apro]
                    if case == 7:
                        config[i+1][j] = ["Proie", Apro]
                    if case == 8:
                        config[i+1][j+1] = ["Proie", Apro]
                elif case == 2:
                    config[i][j].append("Reproduit")
                    config[i-1][j].append("Reproduit")
                    case = direction(i, j, 0)
                    if case == 1:
                        config[i-1][j-1] = ["Proie", Apro]
                    if case == 3:
                        config[i-1][j+1] = ["Proie", Apro]
                    if case == 4:
                        config[i][j-1] = ["Proie", Apro]
                    if case == 5:
                        config[i][j+1] = ["Proie", Apro]
                    if case == 6:
                        config[i+1][j-1] = ["Proie", Apro]
                    if case == 7:
                        config[i+1][j] = ["Proie", Apro]
                    if case == 8:
                        config[i+1][j+1] = ["Proie", Apro]
                elif case == 3:
                    config[i][j].append("Reproduit")
                    config[i-1][j+1].append("Reproduit")
                    case = direction(i, j, 0)
                    if case == 1:
                        config[i-1][j-1] = ["Proie", Apro]
                    if case == 2:
                        config[i-1][j] = ["Proie", Apro]
                    if case == 4:
                        config[i][j-1] = ["Proie", Apro]
                    if case == 5:
                        config[i][j+1] = ["Proie", Apro]
                    if case == 6:
                        config[i+1][j-1] = ["Proie", Apro]
                    if case == 7:
                        config[i+1][j] = ["Proie", Apro]
                    if case == 8:
                        config[i+1][j+1] = ["Proie", Apro]
                elif case == 4:
                    config[i][j].append("Reproduit")
                    config[i][j-1].append("Reproduit")
                    case = direction(i, j, 0)
                    if case == 1:
                        config[i-1][j-1] = ["Proie", Apro]
                    if case == 2:
                        config[i-1][j] = ["Proie", Apro]
                    if case == 3:
                        config[i-1][j+1] = ["Proie", Apro]
                    if case == 5:
                        config[i][j+1] = ["Proie", Apro]
                    if case == 6:
                        config[i+1][j-1] = ["Proie", Apro]
                    if case == 7:
                        config[i+1][j] = ["Proie", Apro]
                    if case == 8:
                        config[i+1][j+1] = ["Proie", Apro]
                elif case == 5:
                    config[i][j].append("Reproduit")
                    config[i][j+1].append("Reproduit")
                    case = direction(i, j, 0)
                    if case == 1:
                        config[i-1][j-1] = ["Proie", Apro]
                    if case == 2:
                        config[i-1][j] = ["Proie", Apro]
                    if case == 3:
                        config[i-1][j+1] = ["Proie", Apro]
                    if case == 4:
                        config[i][j-1] = ["Proie", Apro]
                    if case == 6:
                        config[i+1][j-1] = ["Proie", Apro]
                    if case == 7:
                        config[i+1][j] = ["Proie", Apro]
                    if case == 8:
                        config[i+1][j+1] = ["Proie", Apro]
                elif case == 6:
                    config[i][j].append("Reproduit")
                    config[i+1][j-1].append("Reproduit")
                    case = direction(i, j, 0)
                    if case == 1:
                        config[i-1][j-1] = ["Proie", Apro]
                    if case == 2:
                        config[i-1][j] = ["Proie", Apro]
                    if case == 3:
                        config[i-1][j+1] = ["Proie", Apro]
                    if case == 4:
                        config[i][j-1] = ["Proie", Apro]
                    if case == 5:
                        config[i][j+1] = ["Proie", Apro]
                    if case == 7:
                        config[i+1][j] = ["Proie", Apro]
                    if case == 8:
                        config[i+1][j+1] = ["Proie", Apro]
                elif case == 7:
                    config[i][j].append("Reproduit")
                    config[i+1][j].append("Reproduit")
                    case = direction(i, j, 0)
                    if case == 1:
                        config[i-1][j-1] = ["Proie", Apro]
                    if case == 2:
                        config[i-1][j] = ["Proie", Apro]
                    if case == 3:
                        config[i-1][j+1] = ["Proie", Apro]
                    if case == 4:
                        config[i][j-1] = ["Proie", Apro]
                    if case == 5:
                        config[i][j+1] = ["Proie", Apro]
                    if case == 6:
                        config[i+1][j-1] = ["Proie", Apro]
                    if case == 8:
                        config[i+1][j+1] = ["Proie", Apro]
                elif case == 8:
                    config[i][j].append("Reproduit")
                    config[i+1][j+1].append("Reproduit")
                    case = direction(i, j, 0)
                    if case == 1:
                        config[i-1][j-1] = ["Proie", Apro]
                    if case == 2:
                        config[i-1][j] = ["Proie", Apro]
                    if case == 3:
                        config[i-1][j+1] = ["Proie", Apro]
                    if case == 4:
                        config[i][j-1] = ["Proie", Apro]
                    if case == 5:
                        config[i][j+1] = ["Proie", Apro]
                    if case == 6:
                        config[i+1][j-1] = ["Proie", Apro]
                    if case == 7:
                        config[i+1][j] = ["Proie", Apro]
    for i in range(1, N + 1): # Boucle pour supprimer le terme "Reproduit" à la fin de chaque liste une fois que tous les déplacement de ce tour on été effectués
        for j in range(1, N + 1):
            if type(config[i][j]) == list and config[i][j][-1] == "Reproduit": # Seulement si c'est une liste (donc un animal) et qu'elle a le terme "Reproduit" à la fin
                del config[i][j][-1]

    affiche_grille(config) # Actualisation de la grille
    tour += 1 # Ajout d'un tour au compteur
    label_tours.configure(text = ("Tour", tour)) # Actualise le texte du numéro de tour



### Programme principal

# Définition des widgets
racine = tk.Tk()
racine.title("Simulation proies-prédateurs")
canvas = tk.Canvas(racine, width = LARGEUR, height = HAUTEUR)
init_grille() # Création de la grille de départ
init_proies() # Ajout de Npro proies à des coordonnées aléatoires
init_prédateurs() # Ajout de Npre Prédateur à des coordonnées aléatoires
bouton_tours = tk.Button(racine, text = "Tour suivant", command = passer_tour) # Bouton pour passer le tour (à remplacer pour ne pas avoir à cliquer sur le bouton pour passer les tours, peut-être avec la commande after())
label_tours = tk.Label(racine, text = ("Tour", tour)) # Texte pour affiche le numéro du tour actuel

# Placement des widgets
canvas.grid(column = 1, row = 0, rowspan = 4)
bouton_tours.grid(column = 0, row = 1)
label_tours.grid(column = 0, row = 0)

# Boucle principale
racine.mainloop()