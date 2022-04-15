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

Npro = 6 # Nombre initial de proies (Npro proies apparaissent au début)
Fpro = 3 # Fréquence de naissance des proies (Fpro proies naissent à chaque tour)
tour = 0 # Numéro du tour


### Définitions des fonctions

# Choix des couleurs
def choix_couleur(n):
    """Retourne une couleur à partir de l'entier n"""
    if n == 0: # Rien
        return "white"
    if n > 0 and n < 1: # Proie
        return "yellow"
    if n > 1 and n < 2: # Prédateur
        return "yellow"
    else: # Autre
        return "grey"


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
            col = "white"
            carre = canvas.create_rectangle(x, y, x + LARGEUR_CASE, y + HAUTEUR_CASE, fill = col)
            grille[i][j] = carre


# Affichage de la grille
def affiche_grille(config):
    """Affiche la configuration donnée"""
    for i in range(1, N+1):
        for j in range(1, N+1):
            col = choix_couleur(config[i][j])
            canvas.itemconfigure(grille[i][j], fill = col)


# Initialise les proies
def init_proies():
    """Ajoute Npro proies à des coordonnées aléatoires"""
    global config
    cpt = Npro
    while cpt > 0:
        i, j = rd.randint(1, N), rd.randint(1, N)
        if config[i][j] == 0:
            config[i][j] = 0.05
            cpt -= 1
    affiche_grille(config)


# Passe un tour
def passer_tour():
    """Fait passer les tours (ajout de proies, modification de l'âge)"""
    global config
    global tour
    for ligne in range(len(config)):
        for chiffre in range(len(config[ligne])):
            #if config[ligne][chiffre] > 0:
            #    config[ligne][chiffre] -= 0.01 # cette commande crée des chiffres pas ronds jsp pourquoi, par ex. 0.0199999999997

            # Donc on utilise ça pour le moment :
            if config[ligne][chiffre] == 0.05:
                config[ligne][chiffre] = 0.04
            elif config[ligne][chiffre] == 0.04:
                config[ligne][chiffre] = 0.03
            elif config[ligne][chiffre] == 0.03:
                config[ligne][chiffre] = 0.02
            elif config[ligne][chiffre] == 0.02:
                config[ligne][chiffre] = 0.01
            elif config[ligne][chiffre] == 0.01:
                config[ligne][chiffre] = 0
    cpt = Fpro
    while cpt > 0:
        i, j = rd.randint(1, N), rd.randint(1, N)
        if config[i][j] == 0:
            config[i][j] = 0.05
            cpt -= 1
    affiche_grille(config)
    tour += 1
    label_tours.configure(text = ("Tour", tour)) # Actualise le texte du numéro de tour en haut



### Programme principal

# Définition des widgets
racine = tk.Tk()
racine.title("Simulation proies-prédateurs")
canvas = tk.Canvas(racine, width = LARGEUR, height = HAUTEUR)
init_grille() # Création de la grille de départ
init_proies() # Ajout de Npro proies à des coordonnées aléatoires
bouton_tours = tk.Button(racine, text = "Tour suivant", command = passer_tour)
label_tours = tk.Label(racine, text = ("Tour", tour))

# Placement des widgets
canvas.grid(column = 2, row = 0, rowspan = 4)
bouton_tours.grid(column = 0, row = 1)
label_tours.grid(column = 0, row = 0)

# Boucle principale
racine.mainloop()