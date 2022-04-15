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
LARGEUR_CASE = LARGEUR / 1.1 // N
HAUTEUR_CASE = HAUTEUR / 1.1 // N



### Définitions des variables globales

Npro = 6 # Nombre initial de proies (10 proies apparaissent au début)
Fpro = 2 # Fréquence de naissance des proies (Fpro proies naissent à chaque tour)


### Définitions des fonctions

# Choix des couleurs
def choix_couleur(n):
    """Retourne une couleur à partir de l'entier n"""
    liste_col = ["white", "yellow", "red", "blue"]
    if n < 4:
        return liste_col[n]
    else:
        return "grey" + str(min(n + 20, 100))


# Création de la grille
def init_grille():
    """Retourne une grille carrée vide dimension N+2, les éléments de la configuration vont de 1 à N les indices 0 et N+1 sont les bords et permettent de ne pas gérer de cas particuliers"""
    global grille, config
    grille = [[0 for i in range(N+2)] for j in range(N+2)]
    config = [[0 for i in range(N+2)] for j in range(N+2)]
    for i in range(1, N+1):
        x = (i - 1) * LARGEUR_CASE
        for j in range(1, N+1):
            y = (j - 1) * HAUTEUR_CASE
            carre = canvas.create_rectangle(x, y, x + LARGEUR_CASE, y + HAUTEUR_CASE, fill = "white")
            grille[i][j] = carre


# Affichage de la grille
def affiche_grille(config):
    """Affiche la configuration donnée"""
    for i in range(1, N+1):
        for j in range(1, N+1):
            col = choix_couleur(config[i][j])
            canvas.itemconfigure(grille[i][j], fill=col)


# Initialise les proies
def init_proies():
    """Ajoute Npro proies à des coordonnées aléatoires"""
    global config
    cpt = Npro
    while cpt > 0:
        i, j = rd.randint(1, N), rd.randint(1, N)
        if config[i][j] == 0:
            config[i][j] = 1
            cpt -= 1
    affiche_grille(config)


# Ajoute des proies
def ajout_proies():
    """Ajoute Fpro proies à des coordonnées aléatoires"""
    global config
    cpt = Fpro
    while cpt > 0:
        print("test")
        i, j = rd.randint(1, N), rd.randint(1, N)
        if config[i][j] == 0:
            config[i][j] = 1
            cpt -= 1
    affiche_grille(config)



### Programme principal

# Définition des widgets
racine = tk.Tk()
racine.title("Simulation proies-prédateurs")
canvas = tk.Canvas(racine, width = LARGEUR, height = HAUTEUR)
init_grille() # Création de la grille de départ
init_proies() # Ajout de Npro proies à des coordonnées aléatoires
bouton1 = tk.Button(racine, text = "Tours", command = ajout_proies())

# Placement des widgets
canvas.grid(column = 1, row = 1, rowspan = 3)
bouton1.grid(column = 0, row = 1)

# Boucle principale
racine.mainloop()