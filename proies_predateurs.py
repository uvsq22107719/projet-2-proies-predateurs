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

N = 50 # Taille de la matrice
HAUTEUR = 700 # Hauteur du canevas
LARGEUR = 700 # Largeur du canevas
LARGEUR_CASE = LARGEUR / 1.1 // N
HAUTEUR_CASE = HAUTEUR / 1.1 // N



### Définitions des variables globales

Npro = 10 # Nombre initial de proies (Npro proies apparaissent au début)
Fpro = 3 # Fréquence de naissance des proies (Fpro proies naissent à chaque tour)
Apro = 5 # Espérance de vie en nombre de tours
tour = 0 # Numéro du tour


### Définitions des fonctions

# Choix des couleurs
def choix_couleur(n):
    """Retourne une couleur à partir de l'entier n"""
    if n == 0: # Si il n'y a rien
        return "green" # Couleur du fond
    else:
        if n[0] == "Proie": # Si c'est une proie
            return "white" # Couleur des proies
        elif n[0] == "Prédateur": # Si c'est un prédateur
            return "red" # Couleur des prédateurs
        else: # Si c'est autre chose
            return "grey" # Pour mettre les erreurs en évidence on met du gris


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
            col = "green" # Couleur du fond
            carre = canvas.create_rectangle(x, y, x + LARGEUR_CASE, y + HAUTEUR_CASE, fill = col, outline = "grey")
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
        if config[i][j] == 0: # Si c'est une case vide
            config[i][j] = ["Proie", Apro] # Création d'une liste avec toutes les infos sur l'animal (ici c'est une proie avec Apro le nombre de tours d'espérance de vie)
            cpt -= 1
    affiche_grille(config)


# Passe un tour
def passer_tour():
    """Fait passer les tours (ajout de proies, modification de l'âge)"""
    global config
    global tour
    # Modification de l'espérance de vie (retirer 1 à chaque tour)
    for ligne in range(len(config)): # Pour chaque ligne (ex : [0, 0, ["Proie", 5], ["Proie", 2], 0, ["Prédateur", 5], 0])
        for element in range(len(config[ligne])): # Pour chaque élément (ex : ["Proie", 5])
            if config[ligne][element] != 0: # Seulement si c'est pas un 0
                config[ligne][element][1] -= 1 # Retirer 1 à l'espérance de vie (ex : ["Proie", 5] devient ["Proie", 4])
                if config[ligne][element][1] == 0: # Si c'est par exemple [Proie, 0], remplacer par 0 
                    config[ligne][element] = 0
    # Ajout de proies
    cpt = Fpro
    while cpt > 0:
        i, j = rd.randint(1, N), rd.randint(1, N)
        if config[i][j] == 0: # Si la case est vide
            config[i][j] = ["Proie", Apro] # Création d'une liste avec toutes les infos sur l'animal (ici c'est une proie avec Apro le nombre de tours d'espérance de vie)
            cpt -= 1
        else: # Si la case n'est pas vide, recommencer la boucle
            continue
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
canvas.grid(column = 1, row = 0, rowspan = 4)
bouton_tours.grid(column = 0, row = 1)
label_tours.grid(column = 0, row = 0)

# Boucle principale
racine.mainloop()