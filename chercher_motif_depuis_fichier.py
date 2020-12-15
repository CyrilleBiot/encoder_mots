#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def selection_du_motif_de_recherche(fichier, theme, motif):
    """
    Fonction de recherche sur les digrammes ou les trigrammes
    :param fichier:
    :param motif:
    :return: list of results
    """
    liste_de_mots_a_exporter = []
    # Stockage dans une variable de la totalité des mots
    with open(fichier) as f:
        liste_mots_a_trouver = [line.rstrip() for line in f]
    #print(liste_mots_a_trouver)
    # split de la liste (spéaration MOT / GRAPHEMES
    for i in range(len(liste_mots_a_trouver)):
        liste_mots_a_trouver[i] = liste_mots_a_trouver[i].split(';',3)
        #print(liste_mots_a_trouver[i][1])
        liste_mots_a_trouver[i][1] = liste_mots_a_trouver[i][1].split(',')
        # DEBUG
        #print(liste_mots_a_trouver[i][0], ' --- ', liste_mots_a_trouver[i][1], ' - ', liste_mots_a_trouver[i][2])



    if motif == "in" or motif == "ain" or motif == "ein" or motif == "un":
        motif = ["un", "ain", "ein"]
    elif motif == "é" or motif == "ai" or motif == "et" or motif == "ez" or motif == "er":
        motif = ["é","et","ai","et","ez","er"]
    elif motif == "an" or motif == "en" or motif == "em" or  motif == "am" or motif == "oan":
        motif = ["an","am","en","em","aon"]
    elif motif == "f" or motif == "ph" or motif == "ff":
        motif = ["ff","ph","f"]
    elif motif == "i" or motif == "y" or motif == "il" or motif =="ille":
        motif = ["i","y","il","ille"]
    elif motif == "on" or motif == "om":
        motif = ["om","on"]
    elif motif == "o" or motif == "au" or motif == "eau":
        motif = ["o","eau","au"]
    elif motif == "c" or motif == "cc" or motif == "q" or motif == "qu" or motif == "ck" or motif == "k":
        motif = ["c","q","qu","ck","k"]

    else:
        motif = [motif]
    print(motif)


    for i in range(len(liste_mots_a_trouver)):
         if theme in liste_mots_a_trouver[i][2]:
            for j in motif:
                if j in liste_mots_a_trouver[i][1]:
                    print(liste_mots_a_trouver[i][0])
                    liste_de_mots_a_exporter.append(liste_mots_a_trouver[i][0])

    return liste_de_mots_a_exporter


fichier = "mots_test.txt"
while True:
    theme = input("Theme de recherche : ")
    motif = input("Motif de recherche : ")
    if motif == 'quit':
        break
    l = selection_du_motif_de_recherche(fichier, theme, motif)
    print(l)

