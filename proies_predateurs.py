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
    if n == 0: # Rien
        return "green"
    else:
        x = list(n) # Pour récupérer la première lettre (par exemple de L5)
        animal = x[0] # Si la première lettre est un L, c'est un lapin (proie)
        if animal == "L": # Lapin (Proie)
            return "white"
        elif animal == "R": # Renard (Prédateur)
            return "orange"
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
            col = "green"
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
        if config[i][j] == 0:
            nom = "L" + str(Apro) # L = lapin (proie) et Apro = espérance de vie
            config[i][j] = nom
            cpt -= 1
    affiche_grille(config)


# Passe un tour
def passer_tour():
    """Fait passer les tours (ajout de proies, modification de l'âge)"""
    global config
    global tour
    # Modification de l'espérance de vie (retirer 1 à chaque tour)
    for ligne in range(len(config)): # Pour chaque ligne (ex : [0, 0, L5, L2, R3, 0, 0, L1])
        for code in range(len(config[ligne])): # Pour chaque code (ex : L5)
            if config[ligne][code] != 0: # Seulement si c'est pas un 0
                l = list(str(config[ligne][code])) # Pour récupérer le nombre (par exemple de L5)
                lettre = str(l[0])
                del l[0] # Supprimer la lettre du début (si L15, devient 15)
                nombre = ""
                for i in l:
                    nombre = str(nombre) + str(i)
                nombre = int(nombre) - 1 # Si le chiffre est 5, l'animal a une espérance de vie de 5 tours. Soustrait 1.
                if nombre == 0: # Si c'est par exemple L0, remplacer par 0
                    config[ligne][code] = 0
                else: # Sinon, recréer le code à jour (par exemple L4)
                    config[ligne][code] = str(lettre + str(nombre))
    # Ajout de proies
    cpt = Fpro
    while cpt > 0:
        i, j = rd.randint(1, N), rd.randint(1, N)
        if config[i][j] == 0: # Si la case est vide
            config[i][j] = "L" + str(Apro) # L = lapin (proie) et Apro = espérance de vie
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