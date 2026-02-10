###########################################################################
# Projet MapMaker 2025                                                    #
# Équipe de projet: Mathusan SIVASUTHAN _ Ibrahim DULAC _ Mellina MAMMERI #
# TP-6  Groupe-7                                                          #
###########################################################################


# Imports
import fonction_affichage as fa
import fonctions_utile as fu
import fltk


# Constantes
TAILLE_GRILLE = 10
TAILLE_FENETRE = 80*TAILLE_GRILLE


# Main
dico_tuiles = (fu.cree_dico("fichiers fournis/tuiles"))
grille_a = [[None for _ in range(TAILLE_GRILLE)] for _ in range(TAILLE_GRILLE)]
grille_s = [[None for _ in range(TAILLE_GRILLE)] for _ in range(TAILLE_GRILLE)]

fltk.cree_fenetre(TAILLE_FENETRE,TAILLE_FENETRE)
i_grille , j_grille = 0 , 0
nom_sauv = ""
sauvegarde, partie_en_cours = fa.menu_principal()

if sauvegarde :
    grille_s, i_grille, j_grille, nom_sauv = fa.recup_sauvegarde()
    grille_a = [[grille_s[b][a] for a in range(i_grille, i_grille + 10)] for b in range(j_grille, j_grille + 10)]

while partie_en_cours:
    fa.map(grille_a , dico_tuiles, TAILLE_GRILLE)
    ev = fltk.attend_ev()
    type_ev = fltk.type_ev(ev)
    
    if type_ev == "ClicGauche":
        i,j =  fltk.ordonnee(ev), fltk.abscisse(ev)
        i = ((i-25)//75)
        j = ((j-25)//75)
        lst_prop = (fu.tuiles_possibles(dico_tuiles, grille_a, i, j))
        grille_a[i][j] = fa.proposition(dico_tuiles, lst_prop)
        if grille_a[i][j] != None:
            if 'R' in grille_a[i][j]:
                source_i, source_j = fu.trouver_source(grille_a, i, j)
                if not fu.riviere_naturelle(grille_a, source_i, source_j, tuiles_visitées=[], gestion_riviere_active=True):
                    grille_a[i][j] = None                    

    if type_ev == "Touche":
        touche_ev = fltk.touche(ev)
        if touche_ev == "c":
            grille_a = fu.remplir_grille(dico_tuiles, grille_a)
            grille_s = fu.inserer_sous_grille(grille_s, i_grille, j_grille, grille_a)
        elif touche_ev == "s":
            nom_sauv = fa.saisir_nom_sauvegarde(nom_sauv)
            fa.sauvegarde(grille_a, i_grille, j_grille, nom_sauv)
        elif touche_ev in ["Right", "Left", "Up", "Down"]:
            grille_a, i_grille, j_grille = fu.defilement(dico_tuiles, grille_s, grille_a, i_grille , j_grille ,  touche_ev)
            grille_s = fu.inserer_sous_grille(grille_s, i_grille, j_grille, grille_a)
    fltk.mise_a_jour()
    
    if type_ev == "Quitte":
        fa.menu_final(grille_s, i_grille, j_grille, nom_sauv)
        partie_en_cours = False
fltk.ferme_fenetre()