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
            if mat[ligne][chiffre] == 0: # Si le chiffre est 0, couleur blanche
                # Taille des rectangles = LARGEUR/taille
                canvas.create_rectangle((chiffre * (LARGEUR/taille), ligne * (LARGEUR/taille)),((chiffre + 1) * (LARGEUR/taille), (ligne + 1) * (LARGEUR/taille)), fill = "#FFFFFF") # blanc
            elif mat[ligne][chiffre] == 1: # Si le chiffre est 1, autre couleur
                canvas.create_rectangle((chiffre * (LARGEUR/taille), ligne * (LARGEUR/taille)),((chiffre + 1) * (LARGEUR/taille), (ligne + 1) * (LARGEUR/taille)), fill = "#FFFBC8") # Couleurs : code hexadécimal

def ajout_lapin():
    """"""
    global mat
    for ligne in range(len(mat)): # Chaque ligne de la matrice
        for chiffre in range(len(mat[ligne])): # Chaque chiffre des lignes de la matrice
            if mat[ligne][chiffre] == 0:
                mat[ligne][chiffre] =+ 1
    creer_grille(mat)
    print(mat)
    return(mat)

### Programme principal

# Définition des widgets
racine = tk.Tk()
racine.title("Simulation proies-prédateurs")
canvas = tk.Canvas(racine, width = LARGEUR, height = HAUTEUR)
config_courante() # Création de la grille de départ
ajout_lapin()
#bouton1 = tk.Button(racine, text = "", command = )

# Placement des widgets
canvas.grid(column = 1, row = 0, rowspan = 3)
#bouton1.grid(column = 0, row = 0)

# Boucle principale
racine.mainloop()