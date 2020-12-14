#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def select_pattern_to_play(fichier, motif):
    liste_de_mots_a_exporter = []
    # Stockage dans une variable de la totalité des mots
    with open(fichier) as f:
        liste_mots_a_trouver = [line.rstrip() for line in f]
    # split de la liste (spéaration MOT / GRAPHEMES
    for i in range(len(liste_mots_a_trouver)):
        liste_mots_a_trouver[i] = liste_mots_a_trouver[i].split(';',1)
        #print(liste_mots_a_trouver[i][1])
        liste_mots_a_trouver[i][1] = liste_mots_a_trouver[i][1].split(',')
    #print(liste_mots_a_trouver , " -- -- ", type(liste_mots_a_trouver))

    if motif == "in" or motif == "ain" or motif == "ein" or motif == "un":
        motif = ("un", "ain", "ein")
    if motif == "é" or motif == "ai" or motif == "et" or motif == "ez" or motif == "er":
        motif = ("é","et","ai","et","ez","er")
    if motif == "an" or motif == "en" or motif == "em" or  motif == "am" or motif == "oan":
        motif = ("an","am","en","em","aon")
    if motif == "f" or motif == "ph" or motif == "ff":
        motif = ("ff","ph","f")
    if motif == "i" or motif == "y" or motif == "il" or motif =="ille":
        motif = ("i","y","il","ille")
    if motif == "on" or motif == "om":
        motif = ("om","on")
    print(motif)

    for i in range(len(liste_mots_a_trouver)):
        for j in motif:
            if j in liste_mots_a_trouver[i][1]:
                print(liste_mots_a_trouver[i][0])
                liste_de_mots_a_exporter.append(liste_mots_a_trouver[i][0])

    return liste_de_mots_a_exporter


fichier = "mots_test.txt"
while True:
    motif = input("Motif de recherche : ")
    if motif == 'quit':
        break
    l = select_pattern_to_play(fichier, motif)
    print(l)

