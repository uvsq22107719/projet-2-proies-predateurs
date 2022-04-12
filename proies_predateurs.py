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
import random

### Définitions des constantes

HAUTEUR = 1000 # Hauteur du canevas
LARGEUR = 1000 # Largeur du canevas

### Définitions des variables globales

taille = 30 # Taille de la matrice
print("Taille de la matrice :", taille)

### Définitions des fonctions

# Configuration courante
def config_courante():
    """Crée la matrice de départ, sans sable"""
    mat = []
    for i in range(taille):
        l = [0 for i in range(taille)]
        mat.append(l)
    creer_grille(mat)
    return(mat)

# Création de la grille
def creer_grille(mat):
    """Crée des rectangles à partir de la matrice générée"""
    for ligne in range(len(mat)): # Chaque ligne de la matrice
        for chiffre in range(len(mat[ligne])): # Chaque chiffre des lignes de la matrice
            # Taille des rectangles = LARGEUR/taille
            # activeoutline = "red" : bordure rouge si le rectangle est visé avec la souris
            canvas.create_rectangle((chiffre * (LARGEUR/taille), ligne * (LARGEUR/taille)),((chiffre + 1) * (LARGEUR/taille), (ligne + 1) * (LARGEUR/taille)), activeoutline = "red", fill = "#FFFFFF") # blanc



### Programme principal

# Définition des widgets
racine = tk.Tk()
racine.title("Simulation proies-prédateurs")
canvas = tk.Canvas(racine, width = LARGEUR, height = HAUTEUR)
config_courante() # Création de la grille de départ
#bouton1 = tk.Button(racine, text = "", command = )

# Placement des widgets
canvas.grid(column = 1, row = 0, rowspan = 3)
#bouton1.grid(column = 0, row = 0)

# Boucle principale
racine.mainloop()