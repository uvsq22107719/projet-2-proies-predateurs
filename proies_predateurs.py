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
HAUTEUR = 450 # Hauteur du canevas
LARGEUR = 450 # Largeur du canevas
LARGEUR_CASE = LARGEUR // N
HAUTEUR_CASE = HAUTEUR // N
Npro = 10 # Nombre de proies



### Définitions des variables globales
 


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
    global grille, config_cur
    grille = [[0 for i in range(N+2)] for j in range(N+2)]
    config_cur = [[0 for i in range(N+2)] for j in range(N+2)]
    for i in range(1, N+1):
        x = (i - 1) * LARGEUR_CASE
        for j in range(1, N+1):
            y = (j - 1) * HAUTEUR_CASE
            col = "white"
            carre = canvas.create_rectangle(x, y, x+LARGEUR_CASE,
                                            y+HAUTEUR_CASE, fill=col,
                                            outline="grey")
            grille[i][j] = carre


# Affichage de la grille
def affiche_grille(config):
    """Affiche la configuration donnée"""
    for i in range(1, N+1):
        for j in range(1, N+1):
            col = choix_couleur(config[i][j])
            canvas.itemconfigure(grille[i][j], fill=col)


# Ajout d'une proie
def ajout_proie(config):
    """Ajoute Npro proies à des coordonnées aléatoires"""
    for i in range(Npro):
        config[rd.randint(0, 31)][rd.randint(0, 31)] += 1
    affiche_grille(config)
    return config



### Programme principal

# Définition des widgets
racine = tk.Tk()
racine.title("Simulation proies-prédateurs")
canvas = tk.Canvas(racine, width = LARGEUR, height = HAUTEUR)
init_grille() # Création de la grille de départ
ajout_proie(config_cur) # Ajout de Npro proies à des coordonnées aléatoires
bouton1 = tk.Button(racine, text = "TEST")

# Placement des widgets
canvas.grid(column = 1, row = 1, rowspan = 3)
bouton1.grid(column = 0, row = 1)

# Boucle principale
racine.mainloop()