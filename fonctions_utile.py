# Imports
import os
from random import shuffle


# Variables
dico_dir = {0: (-1, 0), 1: (0, 1), 2: (1, 0), 3: (0, -1)}
dico_ind = {(-1,0): (0,2), (0,1): (1,3), (1,0): (2,0), (0,-1): (3,1)}


def cree_dico(chemin):
    """
    Crée un dictionnaire des tuiles disponibles dans un dossier.
    
    :param chemin: (str) le chemin du dossier contenant les images des tuiles.
    
    :return dico: (dict) un dictionnaire dont les clefs sont les noms des tuiles,
    et les valeurs sont les chemins d’accès relatifs des images des tuiles correspondantes.
    
    """
    dico = {}
    for img in os.listdir(chemin):
        dico[img[:4]] = chemin + "/" + img
    return dico

def grille_remplie(grille):
    """
    Vérifie si la grille ne contient plus de case vide (None).
    
    :param grille: (list[list]) la carte actuelle.
    
    :return: (bool) True si la grille est remplie, False sinon.
    """
    for ligne in grille:
        for case in ligne:
            if case == None:
                return False
    return True


def emplacement_valide(grille, i, j, nom_tuile):
    """
    Vérifie si la tuile nom_tuile se place correctement à la position (i, j).
    
    :param grille: (list[list]) la carte actuelle.
    :param i, j: (int, int) position dans la grille.
    :param nom_tuile: (str) nom de la tuile à tester (4 caractères).
    
    :return: (bool) True si la tuile peut être placé, False sinon.
    
    """
    for direction, indices in dico_ind.items():
        if grille != [] and 0 <= i+direction[0] < len(grille) and 0 <=j+direction[1] < len(grille[0]):
            tuile_voisine = grille[i+direction[0]][j+direction[1]]
            if tuile_voisine != None:
                if tuile_voisine[indices[1]] != nom_tuile[indices[0]]:
                    return False
    return True


def tuiles_possibles(dico, grille, i, j):
    """
     Renvoie la liste de toutes les tuiles qui peuvent être positionnées à la case (i, j).
    
     :param dico: (dict) un dictionnaire dont les clefs sont les noms des tuiles,
      et les valeurs sont les chemins d’accès relatifs des images des tuiles correspondantes.
     :param grille: (list[list]) la carte actuelle.
     :param i, j: (int, int) position de la case à remplir.
     
     :return lst_pos: (list) liste des tuiles compatibles.
    
    """
    lst_pos = []
    for nom_tuile in dico:
        if emplacement_valide(grille, i, j, nom_tuile):
            lst_pos.append(nom_tuile)
    return lst_pos


def defilement(dico_tuiles, grille_s, grille_a, i , j,  direction):
    """
    Applique un défilement de la carte selon la direction donnée.
    
    :param dico_tuiles: (dict) dictionnaire des tuiles disponibles.
    :param grille_s: (list[list]) la grille complète sauvegardée.
    :param grille_a: (list[list]) la grille affichée actuellement.
    :param i, j: (int, int) position de départ de la carte sauvegardée.
    :param direction: (str) La direction du défilement ('gauche', 'droite', 'haut' ou 'bas').
    
    :return: (list[list]) Nouvelle grille décalée.
    :return grille_a, i, j: (tuple) nouvelle carte, nouvelles coordonnées.
    
    """
    if direction == "Right":
        j +=  1
    elif direction == "Left":
        j -= 1
    elif direction == "Down":
        i += 1        
    elif direction == "Up":
        i -= 1 
    grille_a = [[grille_s[a][b] if 0 <= a < len(grille_s) and 0 <= b < len(grille_s[0]) else None for b in range(j, j + 10)] for a in range(i, i + 10)]
    # Complétion automatique des cases vides
    grille_a = remplir_grille(dico_tuiles, grille_a)   
    return grille_a , i , j


def inserer_sous_grille(grille_s, i, j, grille_a):
    """
    Insère une sous-grille dans la grande grille à la position (i, j).
    
    :param grille_s: (list[list]) la grille complète.
    :param i, j: (int, int) position de départ de la sous-grille.
    :param grille_a: (list[list]) la sous-grille à insérer dans la grande carte.
    
    :return grille_s: (list[list]) la nouvelle carte avec la sous-grille insérée.
    
    """
    h = len(grille_a)
    w = len(grille_a[0]) if h > 0 else 0
    while len(grille_s) < i + h:
        grille_s.append([None] * len(grille_s[0]) if grille_s else [None] * (j + w))
    for a in range(len(grille_s)):
        if len(grille_s[a]) < j + w:
            grille_s[a].extend([None] * (j + w - len(grille_s[a])))
    for a in range(h):
        for b in range(w):
            grille_s[i + a][j + b] = grille_a[a][b]
    return grille_s


def est_source_riviere(grille, i, j, tuiles_visitées):
    """
    Vérifie si une rivière démarre d'une montagne ou hors de la carte.
    
    :param grille: (list[list]) la carte actuelle.
    :param i, j: (int, int) position actuelle dans la grille.
    :param tuiles_visitées: (list[tuple]) liste des positions des tuiles déja visitées.
    
    :return: (bool) True si la source est valide, False sinon.
    
    """
    nom_tuile = grille[i][j]

    # On ne vérifie la source que si c'est la première tuile.
    if len(tuiles_visitées) != 0:
        return True
    
    if 'M' in nom_tuile:
        return True
   
    if ((i == 0 and nom_tuile[0] == 'R') or
        (j == len(grille[0]) - 1 and nom_tuile[1] == 'R') or
        (i == len(grille) - 1 and nom_tuile[2] == 'R') or
        (j == 0 and nom_tuile[3] == 'R')):
        return True
    
    return False


def tuile_valide(nom_tuile):
    return nom_tuile is not None and len(nom_tuile) == 4


def trouver_source(grille, i, j):
    """
    Remonte la rivière jusqu'à trouver sa source.
    
    :param grille: (list[list]) la carte actuelle.
    :param i, j: (int, int) position de départ dans la grille.
    
    :return (i, j): (tuple) position de la source.

    """
    tuiles_visitées = []
    a_visiter = [(i, j)]
    while a_visiter:
        ni, nj = a_visiter.pop()
        # Passe, si la tuile a déja été visiter.
        if (ni, nj) in tuiles_visitées :
            continue
        
        tuiles_visitées.append((ni, nj))
        nom_tuile = grille[ni][nj]
        if not tuile_valide(nom_tuile):
            continue
        
        # Si la tuile est une source valide
        if est_source_riviere(grille, ni, nj, []):
            return ni, nj

        for index in range(4):
            if nom_tuile[index] == 'R':
                di, dj = dico_dir[index]
                vi, vj = ni + di, nj + dj
                if 0 <= vi < len(grille) and 0 <= vj < len(grille[0]):
                    tuile_voisine = grille[vi][vj]
                    if tuile_valide(tuile_voisine):
                        d_in = dico_ind[(di, dj)][1] # d'ou elle reçoit la rivière.
                        d_out = dico_ind[(di, dj)][0] # d'ou elle sort dans la tuile actuelle.
                        if tuile_voisine[d_in] == 'R' and tuile_voisine != nom_tuile:
                            a_visiter.append((vi, vj))
    # Si aucune source valide trouvée.
    return i, j


def est_sortie_riviere(grille, i, j, direction):
    """
    Vérifie si une rivière se termine dans la mer ou hors de la carte.
    
    :param grille: (list[list]) la carte actuelle.
    :param i, j: (int, int) position actuelle dans la grille.
    :param direction: (tuple) direction de la rivière.
    
    :return: (bool) True si la sortie est valide, False sinon.
    
    """
    ni, nj = i + direction[0], j + direction[1]
    
    # Sortie hors carte
    if not (0 <= ni< len(grille) and 0 <= nj< len(grille[0])):
        return True
    
    tuile_voisine = grille[ni][nj]
    if not tuile_valide(tuile_voisine):
        return False
    
    ind2 = dico_ind[direction][1]
    return tuile_voisine[ind2] == 'S'


def source_sortie(grille, tuiles_visitées):
    """
    Vérifie si le début et la fin de la rivière sont du même type (montagne ou rivière).
    
    :param grille: (list[list]) la carte actuelle.
    :param tuiles_visitées: (list[tuple]) liste des positions des tuiles déja visitées.
    
    :return: (bool) True si il n'y a pas de source ou de sortie, False sinon.

    """
    if len(tuiles_visitées) < 2:
        return False

    # Récupère la première et dernière tuile.
    i_source, j_source = tuiles_visitées[0]
    i_sortie, j_sortie = tuiles_visitées[-1]

    tuile_source = grille[i_source][j_source]
    tuile_sortie = grille[i_sortie][j_sortie]
    
    return ('S' in tuile_source and 'S' in tuile_sortie) or ('M' in tuile_source and 'M' in tuile_sortie)
    
    
def est_boucle(i, j, tuiles_visitées):
    """
    Détecte si la position actuelle a déjà été visitée.
    
    :param i, j: (int, int) position actuelle dans la grille.
    :param tuiles_visitées: (list[tuple]) liste des positions des tuiles déja visitées.
    
    :return: (bool) True si c'est une boucle, False sinon.
    
    """
    return len(tuiles_visitées) >= 4 and (i, j) in tuiles_visitées


def riviere_naturelle(grille, i, j, tuiles_visitées, gestion_riviere_active = True):
    """
    Vérifie si une rivière respecte les contraintes naturelles.
    
    :param grille: (list[list]) la carte actuelle.
    :param i, j: (int, int) position actuelle dans la grille.
    :param tuiles_visitées: (list[tuple]) liste des positions des tuiles déja visitées.
    :param gestion_riviere_active: (bool) active ou désactive la gestion des rivières.
    
    :return: (bool) True si la rivière est valide, False sinon.
    
    """
    if not gestion_riviere_active:
        # Si la gestion est désactivée on considère que tout est valide.
        return True
    
    if est_boucle(i, j, tuiles_visitées):
        return False
    
    if len(tuiles_visitées) == 0:
        if not est_source_riviere(grille, i, j, tuiles_visitées):
            return False
    
    tuiles_visitées.append((i, j))
    nom_tuile = grille[i][j]
    if not tuile_valide(nom_tuile):
        return False
    
    # On ajoute les directions ou il y'a une rivière ou une sortie vers la mer.
    direction_possible = [(index, dico_dir[index]) for index in range(4) if nom_tuile[index] in ('R', 'S')]
            
    # Compteur pour les séparations de rivière        
    nb_separations = 0        
    for index, direction in direction_possible:
        ni, nj = i+direction[0], j+direction[1]
        
        if nom_tuile[index] == 'S':
            if not (0 <= ni < len(grille) and 0 <= nj < len(grille[0])) or grille[ni][nj] is None:
                nb_separations += 1
                continue
        
        if est_sortie_riviere(grille, i, j, direction):
            nb_separations += 1
            continue

        tuile_voisine = grille[ni][nj]
        if not tuile_valide(tuile_voisine):
            continue  # On passe à la direction suivante.

        ind2 = dico_ind[direction][1]

        # Rivière connecté.
        if tuile_voisine[ind2] == 'R':
            if (ni, nj) in tuiles_visitées:
                continue
            nb_separations += 1
            if not riviere_naturelle(grille, ni, nj, tuiles_visitées):
                return False

    if nb_separations > 2:
        # Une rivière naturelle ne peut pas avoir plus de 2 sorties.
         return False
 
    if nb_separations == 0:
        return True
    
    if source_sortie(grille, tuiles_visitées):
        return False
    
    return True


def recup_case_vide(grille):
    """
    Parcourt la grille jusqu'à trouver une case vide.
    
    :param grille: (list[list]) la carte actuelle.
    
    :return lst_vide: (list) liste des coordonnées des cases vides.
    
    """
    lst_vide = []
    for i, ligne in enumerate (grille):
        for j, case in enumerate (ligne):
            if case == None:
                lst_vide.append((i,j))
    return lst_vide


def remplir_grille(dico_tuiles, grille):
    """
    S'occupe de la complétion automatique de la carte.
    
    :param dico_tuiles: (dict) un dictionnaire dont les clefs sont les noms des tuiles,
     et les valeurs sont les chemins d’accès relatifs des images des tuiles correspondantes.
    :param grille: (list[list]) la carte actuelle.
    
    :return grille: (list[list]) la carte completé
    
    """
    lst_vide = recup_case_vide(grille)
    if lst_vide == []:
        return grille
    min_tuiles = None
    for case in lst_vide:
        i, j = case[0], case[1]
        nb_tuiles_pos = len(tuiles_possibles(dico_tuiles, grille, i, j ))
        if min_tuiles == None or nb_tuiles_pos < min_tuiles:
            i_min , j_min = i, j
            min_tuiles = nb_tuiles_pos
    tuile_possible = tuiles_possibles(dico_tuiles, grille, i_min, j_min)
    shuffle(tuile_possible)
    for case in tuile_possible:
        grille[i_min][j_min] = case
        # Vérifie si la rivière est naturelle
        if 'R' in case:
            source_i, source_j = trouver_source(grille, i_min, j_min)
            if not riviere_naturelle(grille, source_i, source_j, tuiles_visitées=[]):
                grille[source_i][source_j] = None
                continue
        
        if remplir_grille(dico_tuiles, grille):
            return grille
        grille[i_min][j_min] = None