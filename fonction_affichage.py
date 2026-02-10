# Imports
import fltk
import os 
import json
import time


# Constantes
TAILLE_GRILLE  = 10
liste_touche = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
                "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
                "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]


# Fonctions
def menu_principal():
    """
    Affiche le menu principal avec 3 boutons: Start, Load, Quit.

    :return: (bool, bool) True si nouvelle partie, False sinon. True si une partie démarre, False si quitter
    """
    fltk.image(400,400, "fichiers fournis/images/menu.png", 800,800)
    while True:
        ev = fltk.attend_ev()
        x, y = fltk.abscisse(ev), fltk.ordonnee(ev)
        if 45 <= x <= 270 and 605 <= y <= 690:
            return True, True
        elif 300 <= x <= 500 and 605 <= y <= 690:
            return False, True
        elif 550 <= x <= 800 and 605 <= y <= 690:
            return False, False


def map(grille , dico_tuiles, TAILLE_GRILLE):
    """
    Affiche la carte actuelle.
    
    :param grille: (list[list]) la carte actuelle.
    :param dico_tuiles: (dict) un dictionnaire dont les clefs sont les noms des tuiles.
     et les valeurs sont les chemins d’accès relatifs des images des tuiles correspondantes.
    :param TAILLE_GRILLE: (int) taille de la grille.
    
    """
    fltk.rectangle(0, 0, 800, 800, remplissage ="#ebd195")
    for i in range(TAILLE_GRILLE):
        for j in range(TAILLE_GRILLE):
            if grille[i][j] == None:
                fltk.rectangle(25 + j * 75, 25 + i * 75, 100 + j * 75 , 100 + i * 75, remplissage = "#825d61", epaisseur = 0)
            if grille[i][j] in dico_tuiles.keys():
                fltk.image(62 + j*75, 62+i*75, dico_tuiles[grille[i][j]], 75 , 75)

        
def afficher_proposition(dico_tuiles, lst, vide, page=0):
    """
    Affiche une page de tuiles proposées.
    
    :param dico_tuiles: (dict) un dictionnaire dont les clefs sont les noms des tuiles.
     et les valeurs sont les chemins d’accès relatifs des images des tuiles correspondantes.
    :param lst: (list) liste des noms des tuiles.
    :param page: (int) numéro de page.

    """
    fltk.rectangle(100, 100, 700, 700, remplissage = "grey")
    absc, ordn = 150,150
    if vide:
        fltk.rectangle(150,350,650,450, remplissage = "#901d1d")
        fltk.texte(175, 375, "Il n'y a pas de tuiles possibles.", police = "Dai-Atlas", taille = 27)
    else:
        boutton_page(page)
        couleurs =  ["#85bdf5","#a2b9eb", "#b4a2eb", "#c9a2eb"]
        i=0
        for elem in lst :
            if i == 3:
                couleur = couleurs[i]
                i = 0
            else :
                couleur = couleurs[i]
                i += 1 
            fltk.rectangle((absc - 50 ), (ordn - 50), (absc + 50), (ordn + 50), remplissage = couleur)
            fltk.image(absc, ordn, dico_tuiles[elem], 75, 75)
            absc += 100
            if absc > 675:
                absc = 150
                ordn += 100
            if ordn > 620:
                break


def boutton_page(page):
    """
    Affiche les boutons pour naviguer entre les pages.
    
    :param page: (int) numéro de page.

    """
    if page == 0:
        fltk.rectangle(350,625,450,675, remplissage="#d95656")
        fltk.texte(365,640,"Annuler", taille = 15)
        fltk.rectangle(515,625,690,675, remplissage="#1399B6")
        fltk.texte(535,640,"Page Suivante", taille = 15)
    else:
        fltk.rectangle(350,625,450,675, remplissage="#d95656")
        fltk.texte(365,640,"Annuler", taille = 15)
        fltk.rectangle(515,625,690,675, remplissage="#1399B6")
        fltk.texte(535,640,"Page Suivante", taille = 15)
        fltk.rectangle(110,625,285,675, remplissage="#B85DEA")
        fltk.texte(120,640,"Page Précédente", taille = 15)
    
    
def choisir_tuile(lst_prop, x, y):
    """
    Retourne la tuile choisie.
    
    :param lst_prop: (list) liste des propositons.
    :param x, y: (int, int) coordonnées du clic dans la carte.
    
    return: (str) La tuile choisie ou None.

    """
    x = (x-100)//100
    y = (y-100)//100
    if 0 <= x <= 6 and 0 <= y <= 6:
        indice = x * 6 + y 
        if 0 <= indice < len(lst_prop):
            return lst_prop[indice]
    return None


def proposition(dico_tuiles, lst_prop):
    """
    Affiche les tuiles pour en choisir une.
    
    :param dico_tuiles: (dict) un dictionnaire dont les clefs sont les noms des tuiles.
     et les valeurs sont les chemins d’accès relatifs des images des tuiles correspondantes.
    :param lst_prop: (list) liste des propositons.
    
    return: (str) tuile choisie, ou None.
    
    """
    prop = None
    page = 0
    while prop == None:
        vide = True if lst_prop == [] else False
        lst = lst_prop[(30*page):] if (30*(page + 1)) >= len(lst_prop) else lst_prop[(30*page): (30*(page + 1))]
        afficher_proposition(dico_tuiles, lst, vide, page)
        ev = fltk.attend_ev()
        tev = fltk.type_ev(ev)
        if vide :
            break
        else:
            if tev == "ClicGauche":
                x,y = fltk.ordonnee(ev), fltk.abscisse(ev)
                if 110 <= y <= 285 and 625 <= x <= 675:
                    if page != 0 :
                        page -= 1
                if 515 <= y <= 690 and 625 <= x <= 675 and lst != []:
                    page += 1
                elif 350 <= y <= 450 and 625 <= x <= 675:
                    break
                else: 
                    prop = choisir_tuile(lst, x, y)
    return prop


def choisir_sauvegarde(lst, x, y):
    """
    Détermine la sauvegarde choisie par clic.

    :param lst: (list) liste des fichiers sauvegardés.
    :param x, y: (int, int) abscisse et ordonnée du clic

    :return: nom du fichier sélectionné ou None.
    
    """
    x = (x-100)//100
    y = (y-100)//200
    if 0 <= x <= 3 and 0 <= y <= 3:
        indice = x * 3 + y 
        if 0 <= indice < len(lst):
            return lst[indice]
    else:
        return None


def lire_sauv(sauv):
    """
    Lit le contenu d'un fichier sauvegardé.

    :param sauv: (str) nom du fichier json.
    
    :return grille, i, j: (list[list], int, int).
    
    """
    with open (f'sauvegarde/{sauv}', 'r') as f:
        dico = json.load(f)
    return dico["grille_sauvegarde"], dico["i_grille"], dico["j_grille"], sauv[:-5]


def recup_sauvegarde():
    """
    Affiche le menu de sauvegardes et récupère la sélection.

    :return: (grille_a, i_grille, j_grille, sauv) ou None si aucune sélection.
    """
    lst_sauv = os.listdir("sauvegarde")
    grille_s, i_grille, j_grille, sauv = [[None for _ in range(TAILLE_GRILLE)] for _ in range(TAILLE_GRILLE)], 0, 0, ""
    page = 0
    while grille_s == None:
        vide = True if lst_sauv == [] else False
        lst = lst_sauv[(15*page):] if (15*(page + 1)) >= len(lst_sauv) else lst_sauv[(15*page): (15*(page + 1))]
        afficher_sauvegarde(lst, page)
        ev = fltk.attend_ev()
        tev = fltk.type_ev(ev)
        if vide :
            break
        else:
            if tev == "ClicGauche":
                x,y = fltk.ordonnee(ev), fltk.abscisse(ev)
                if 110 <= y <= 285 and 625 <= x <= 675:
                    if page != 0 :
                        page -= 1
                if 515 <= y <= 690 and 625 <= x <= 675 and lst != []:
                    page += 1
                elif 350 <= y <= 450 and 625 <= x <= 675:
                    break
                else: 
                    sauv = choisir_sauvegarde(lst, x, y)
                    grille_s, i_grille, j_grille, sauv = lire_sauv(sauv)
        fltk.mise_a_jour()
    return grille_s, i_grille, j_grille, sauv  


def afficher_sauvegarde(lst_sauv, page):
    """
    Affiche la liste des sauvegardes.

    :param lst_sauv: (list) liste des noms de fichiers.
    :param page: (str) numéro de la page affichée.
    
    """
    fltk.rectangle(100, 100, 700, 700, remplissage = "grey")
    absc, ordn = 150,150
    if lst_sauv == []:
        fltk.rectangle(150,350,650,450, remplissage = "#901d1d")
        fltk.texte(175, 375, "Il n'y a pas de sauvegarde.", police = "Dai-Atlas", taille = 27)
    else:
        couleurs =  ["#85bdf5","#a2b9eb", "#b4a2eb", "#c9a2eb"]
        boutton_page(page)
        i=0
        for elem in lst_sauv :
            if i == 3:
                couleur = couleurs[i]
                i = 0
            else :
                couleur = couleurs[i]
                i += 1 
            fltk.rectangle((absc - 50 ), (ordn - 50), (absc + 150), (ordn + 50), remplissage = couleur)
            fltk.texte(absc - 25, ordn -15, elem[:-5])
            absc += 200
            if absc > 675:
                absc = 150
                ordn += 100
            if ordn > 620:
                break    
    

def sauvegarde(grille_s, i_grille, j_grille, nom_sauv):
    """
    Sauvegarde l'état actuel dans un fichier JSON.

    :param grille_s: (list[list]) la carte complète.
    :param i_grille, j_grille: (int, int) position de la sous-grille.
    :param nom_sauv: nom du fichier à sauvegarder.
    
    """
    with open(f'sauvegarde/{nom_sauv}.json','w', encoding = 'utf-8') as f:
        json.dump({"grille_sauvegarde": grille_s, "i_grille": i_grille, "j_grille": j_grille},f)


def saisir_nom_sauvegarde(nom_sauv):
    """
    Interface pour saisir le nom de sauvegarde.
    
    :param nom_sauv: nom du fichier à sauvegarder.
    
    """
    fltk.rectangle(200,320, 600, 420, remplissage = "#95a9eb")
    lst_sauv = os.listdir("sauvegarde")
    while True:
        fltk.efface("nom")
        fltk.texte(220, 340, f"Nom de la sauvegarde :\n{nom_sauv}", tag = "nom")
        ev = fltk.attend_ev()
        te = fltk.type_ev(ev) 
        if te == 'Touche':
            touche = fltk.touche(ev)
            if len(nom_sauv) < 10:
                if touche == 'Return' and len(nom_sauv) != 0:
                    if nom_sauv+".json" not in lst_sauv:
                        return nom_sauv
                    fltk.rectangle(250,520, 550, 600, remplissage = "#e25757", tag = 'existe')
                    fltk.texte(300, 540 , 'Ce nom est déjà pris.', remplissage = "white", police = "Dai-Atlas", taille = 15, tag = 'existe')
                    fltk.texte(260, 560 , 'Cliquer pour valider quand même', remplissage = "white", police = "Dai-Atlas", taille = 15, tag = 'existe')
                    valis_ev = fltk.attend_ev()
                    if 250 <= fltk.abscisse(valis_ev) <= 550 and 520 <= fltk.ordonnee(valis_ev) <= 600:
                        return nom_sauv
                    fltk.efface('existe')
                if touche == 'space':
                    nom_sauv += ' '
                if touche in liste_touche:
                    nom_sauv += touche
            if touche == 'BackSpace' and len(nom_sauv) > 0:
                nom_sauv = nom_sauv[:-1]


def menu_final(grille_s, i_grille, j_grille, nom_sauv):
    """
    Affiche le menu de fin de partie avec deux boutons: Load et Quit.
    
    :param grille_s: (list[list]) la carte complète.
    :param i_grille, j_grille: (int, int) position de la sous-grille.
    :param nom_sauv: nom du fichier à sauvegarder.
    
    """
    quitter = False
    fltk.image(400,400, 'fichiers fournis/images/menu_f.png', 800, 800 )
    while quitter == False:
        ev = fltk.attend_ev()
        te = fltk.type_ev(ev)
        if te == 'ClicGauche':
            if 100 <= fltk.abscisse(ev) <= 350 and 420 <= fltk.ordonnee(ev) <= 550:
                nom_sauv = saisir_nom_sauvegarde(nom_sauv)
                sauvegarde(grille_s, i_grille, j_grille, nom_sauv)
                quitter = True
            elif 430 <= fltk.abscisse(ev) <= 680 and 420 <= fltk.ordonnee(ev) <= 550:
                quitter = True
        elif te == 'Quitter':
            quitter = True
