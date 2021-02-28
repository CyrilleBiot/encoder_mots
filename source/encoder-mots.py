#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
encoder-mots.py
Logiciel pour l'apprentissage de l'encodade
Niveaux Cycle 2, élèves à BEP.
__author__ = "Cyrille BIOT <cyrille@cbiot.fr>"
__copyright__ = "Copyleft"
__credits__ = "Cyrille BIOT <cyrille@cbiot.fr>"
__license__ = "GPL"
__version__ = "1.1"
__date__ = "2020/02/27"
__maintainer__ = "Cyrille BIOT <cyrille@cbiot.fr>"
__email__ = "cyrille@cbiot.fr"
__status__ = "Devel"
"""
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf, Gdk
from random import choice
import string
import vlc
import os.path


# ==============================================
#      Si utilisation hors package, nécessite
#      les paquets :  python3-vlc, python3-gi
# ==============================================

class EcrireMot(Gtk.Window):

    def __init__(self):
        # Quelques variables pour l'environnement
        if os.path.exists('.git'):
            # On est dans le git
            self.dirBase = './source/'
        else:
            if os.path.isdir('/usr/share/encoder-mots/') == True:
                # Sur install paquet
                self.dirBase = '/usr/share/encoder-mots/'
            else:
                # en dev
                self.dirBase = './'


        Gtk.Window.__init__(self, title="Mes premiers mots")
        self.set_border_width(3)
        self.set_resizable(False)
        self.set_icon_from_file(self.dirBase+"apropos.png")
        self.set_border_width(10)

        self.init_the_game()


        # SCORE
        self.score_total = len(self.liste_mots_a_trouver)

        self.message_score = "Score : " + str(self.score) + " sur " + str(self.score_total)
        # Label du score
        self.label_du_score = Gtk.Label(label=self.message_score)

        # Ajout d'un notebook
        self.notebook = Gtk.Notebook()
        self.add(self.notebook)
        self.connect

        #
        # # ONGLET 1 DU NOTEBOOK
        #
        # Creation de la grille
        grid = Gtk.Grid()
        grid.set_column_homogeneous(False)
        grid.set_column_spacing(6)
        grid.set_row_spacing(6)
        grid.set_row_homogeneous(False)

        # Zone de saisie
        self.mot_cache = "-" * len(self.mot_a_trouver)
        self.label_mot_cache = Gtk.Label(label=self.mot_cache)
        self.label_mot_cache.set_name('label_mot_cache')

        # Bouton EFFACER, CORRIGER et VALIDER
        bouton_effacer = Gtk.Button(label="Effacer")
        bouton_effacer.connect("clicked", self.on_delete_word, self.label_mot_cache)

        self.bouton_corriger = Gtk.Button(label="<")
        self.bouton_corriger.connect("clicked", self.on_correct_word, self.bouton_corriger, self.label_mot_cache)
        self.bouton_corriger.set_sensitive(False)

        bouton_valider = Gtk.Button(label="Valider")
        bouton_valider.connect("clicked", self.on_validate_word, self.label_mot_cache, self.label_du_score)

        # Création du clavier virtuel
        self.voyelles = "aàeéèêiîïoôöuy"
        self.consommes = "bcçdfghjklmnpqrstvwxz"
        self.g = ["au", "eau", "ar", "ai", "ei", "er","et", "ez", "eu", "an", "am", "en", "em", "ou", "oi", "or", "on", "om", "ar",
                  "ch", "ph", "ain", "ein", "in", "im",  "un", "um" , "ion", "oin","ss"]
        self.alphabet = self.voyelles + self.consommes
        nombre_de_boutons = len(self.voyelles) + len(self.consommes) + len(self.g)
        self.bouton_lettres = [0] * nombre_de_boutons

        # Creation d'une eventbox pour gestion clic droit de la souris
        eventbox = [0] * nombre_de_boutons

        # Fixe la position des graphemes et des consommes
        position_bouton_grapheme = 0
        position_bouton_consomme = 0

        # Les voyelles
        for i in range(len(self.voyelles)):
            # self.boutonLettres[i] = Gtk.Button(label=chr(i + 65))
            self.bouton_lettres[i] = Gtk.Button(label=str(self.voyelles[i]))
            self.bouton_lettres[i].set_name('bouton_voyelles')
            self.bouton_lettres[i].set_property("tooltip-text", "Clic droit pour écouter le nom de la voyelle.")
            self.bouton_lettres[i].connect("clicked", self.on_letter_add, self.bouton_lettres[i], self.label_mot_cache,
                                           self.bouton_corriger)
            eventbox[i] = Gtk.EventBox()
            eventbox[i].connect("button-press-event", self.on_button_press_event_letters, self.bouton_lettres[i])
            eventbox[i].add(self.bouton_lettres[i])
            grid.attach(eventbox[i], i, 0, 1, 1)

        # Les graphèmes
        for i in range(len(self.voyelles), len(self.voyelles) + len(self.g)):
            if position_bouton_grapheme > (len(self.g) -2) / 2:
                nouvelle_ligne = 2
                pg = position_bouton_grapheme - round((len(self.g) / 2))
            else:
                nouvelle_ligne = 1
                pg = position_bouton_grapheme

            self.bouton_lettres[i] = Gtk.Button(label=str(self.g[position_bouton_grapheme]))
            self.bouton_lettres[i].set_name('bouton_graphemes')
            self.bouton_lettres[i].set_property("tooltip-text", "Clic droit pour écouter le son du graphème.")
            self.bouton_lettres[i].connect("clicked", self.on_letter_add, self.bouton_lettres[i], self.label_mot_cache,
                                           self.bouton_corriger)
            eventbox[i] = Gtk.EventBox()
            eventbox[i].connect("button-press-event", self.on_button_press_event_letters, self.bouton_lettres[i])
            eventbox[i].add(self.bouton_lettres[i])
            grid.attach(eventbox[i], pg, nouvelle_ligne, 1, 1)
            position_bouton_grapheme += 1

        # Les consommes
        for i in range(len(self.voyelles) + len(self.g), len(self.voyelles) + len(self.g) + len(self.consommes)):
            if position_bouton_consomme > len(self.consommes) / 2 + 1:
                nouvelle_ligne = 4
                pc = position_bouton_consomme - round((len(self.consommes) / 2))
            else:
                nouvelle_ligne = 3
                pc = position_bouton_consomme

            self.bouton_lettres[i] = Gtk.Button(label=str(self.consommes[position_bouton_consomme]))
            self.bouton_lettres[i].set_name('bouton_consommes')
            self.bouton_lettres[i].set_property("tooltip-text", "Clic droit pour écouter le nom de la consomme.")
            self.bouton_lettres[i].connect("clicked", self.on_letter_add, self.bouton_lettres[i], self.label_mot_cache,
                                           self.bouton_corriger)
            eventbox[i] = Gtk.EventBox()
            eventbox[i].connect("button-press-event", self.on_button_press_event_letters, self.bouton_lettres[i])
            eventbox[i].add(self.bouton_lettres[i])
            grid.attach(eventbox[i], pc, nouvelle_ligne, 1, 1)
            position_bouton_consomme += 1

        # On récup les events sur les touches
        self.connect("key-press-event", self.on_key_press_event, self.label_mot_cache, self.bouton_corriger)

        # Affichage de l'image
        image = self.dirBase + '/images/' + self.mot_a_trouver + '.png'
        image = self.check_if_image_exist(image)

        # Redimensionnement
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(filename=image, width=200, height=200,
                                                         preserve_aspect_ratio=False)
        self.image = Gtk.Image.new_from_pixbuf(pixbuf)

        # Bouton lecture du son
        self.bouton_lire_son = Gtk.Button(label="ECOUTER SON")

        # Fichier son Test de son existence
        file = self.dirBase + '/images-mp3/' + self.mot_a_trouver + '.mp3'
        file = self.check_if_sound_exist(file)
        self.bouton_lire_son.connect("clicked", self.on_sound_play)
        self.bouton_lire_son.set_hexpand(False)

        # bouton A propos
        bouton_a_propos = Gtk.Button(label="About")
        bouton_a_propos.connect("clicked", self.on_about)

        # Label choix du theme
        self.label_choix_du_theme = Gtk.Label(label="Animaux domestiques")

        # Positionnement des widgets sur le grid
        grid.attach(self.image, 0, 11, 3, 8)
        grid.attach(self.label_mot_cache, 3, 11, 9, 8)
        grid.attach(self.bouton_lire_son, 13, 11, 2, 1)
        grid.attach(bouton_effacer, 14, 12, 1, 1)
        grid.attach(self.bouton_corriger, 13, 12, 1, 1)
        grid.attach(bouton_valider, 13, 13, 2, 1)
        grid.attach(self.label_du_score, 13, 15, 2, 3)
        grid.attach(bouton_a_propos, 13, 18, 2, 1)
        grid.attach(self.label_choix_du_theme, 6, 19, 5, 1)
        #self.add(grid)

        # Ajout au notebook
        self.notebook.append_page(grid, Gtk.Label(label='Jeu'))

        #
        # # ONGLET 2 DU NOTEBOOK
        #
        # a new radiobutton with a label

        # a grid to place the buttons
        # Initialyze first button on a new grid and attach it
        grid2 = Gtk.Grid.new()
        grid2.set_column_homogeneous(False)
        grid2.set_column_spacing(6)
        grid2.set_row_spacing(6)
        grid2.set_row_homogeneous(False)

        #
        # PATTERN OF RESEARCH : THEMES
        #
        # other buttons.
        # a new radiobutton with a label
        label_config_theme = Gtk.Label(label='Thèmes :')
        grid2.attach(label_config_theme,1,1,3,1)

        buttonTheme0 = Gtk.RadioButton(label="'Animaux domestiques'")
        buttonTheme0.connect("toggled", self.toggled_cb_theme)
        grid2.attach(buttonTheme0, 1, 2, 1, 1)

        possibilities = ['Animaux de la forêt','Animaux sauvages']
        buttonTheme = [0] * len(possibilities)
        nb_lignes_grid2 = len(possibilities)+3

        for i in range(len(possibilities)):
            # another radiobutton, in the same group as button1
            buttonTheme[i] = Gtk.RadioButton.new_from_widget(buttonTheme0)
            buttonTheme[i].set_label(possibilities[i])
            buttonTheme[i].connect("toggled", self.toggled_cb_theme)
            buttonTheme[i].set_active(False)
            # attach the button
            grid2.attach(buttonTheme[i], 1, i+3, 1, 1)

        buttonOK = Gtk.Button(label="Valider le choix")
        buttonOK.connect('clicked', self.on_valid_config_theme)

        # Pack at bottom of the button OK theme
        if nb_lignes_grid2 < len(possibilities)+2:
            nb_lignes_grid2 = len(possibilities)+2

        grid2.attach(buttonOK,1,nb_lignes_grid2,1,1)

        #
        # PATTERN OF RESEARCH : PHONEMES
        #
        # other buttons.
        # a new radiobutton with a label
        label_config_phoneme = Gtk.Label(label='Phonèmes : ')
        grid2.attach(label_config_phoneme,4,1,3,1)

        buttonPhoneme0 = Gtk.RadioButton(label="ou")
        buttonPhoneme0.connect("toggled", self.toggled_cb_theme)
        grid2.attach(buttonPhoneme0, 4, 2, 1, 1)

        possibilities = ['on-om','on', 'o-au-eau','k-q-qu-c','ch','an-en','an-en-em-am','in-ain-im-aim-ein']
        buttonPhoneme = [0] * len(possibilities)
        nb_lignes_grid2 = len(possibilities)+3

        for i in range(len(possibilities)):
            # another radiobutton, in the same group as button1
            buttonPhoneme[i] = Gtk.RadioButton.new_from_widget(buttonTheme0)
            buttonPhoneme[i].set_label(possibilities[i])
            buttonPhoneme[i].connect("toggled", self.toggled_cb_theme)
            buttonPhoneme[i].set_active(False)
            # attach the button
            grid2.attach(buttonPhoneme[i], 4, i+3, 1, 1)

        buttonOK = Gtk.Button(label="Valider le choix")
        buttonOK.connect('clicked', self.on_valid_config_theme)

        # Pack at bottom of the button OK theme
        if nb_lignes_grid2 < len(possibilities)+2:
            nb_lignes_grid2 = len(possibilities)+2

        grid2.attach(buttonOK,4,nb_lignes_grid2,1,1)

        # Ajout au notebook
        self.notebook.append_page(grid2, Gtk.Label(label='Configuration'))

    def init_the_game(self):
        # Fichier par défaut
        self.file = self.dirBase  + 'listes-de-mots/animaux-domestiques.txt'

        # Initialisation des variables
        self.positionInWord = 0
        self.motif_tri = ""
        self.theme_tri = ""
        self.score = 0

        # Lecture du fichier de mots
        self.liste_mots_a_trouver = self.creer_liste_mot(self.file)
        print(self.liste_mots_a_trouver)
        self.mot_a_trouver = choice(self.liste_mots_a_trouver)
        self.mots_deja_sortis = []
        self.mots_deja_sortis.append(self.mot_a_trouver)
        self.nombreDeMots = 1
        print(self.mot_a_trouver)

        # SCORE
        self.score_total = len(self.liste_mots_a_trouver)

    def creer_liste_mot(self, filePath):
        """
        Fichier fichier contenant les noms
        :param file:
        :return:
        """
        try:
            filePath
            # Do something with the file
        except IOError:
            print("Fichier demandé non accessible")

        # Création d'un tableau pour récupérer les noms contenus dans le fichier
        tableau_de_mots = []

        with open(filePath) as fp:
            line = fp.readline()
            while line:
                tableau_de_mots.append(line.strip())
                line = fp.readline()
        return tableau_de_mots

    def check_if_sound_exist(self, file_sound):
        if not os.path.isfile(file_sound):
            self.bouton_lire_son.set_sensitive(False)
        else:
            self.bouton_lire_son.set_sensitive(True)

    def check_if_image_exist(self, image):
        if os.path.isfile(image):
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(filename=image, width=200, height=200, \
                                                             preserve_aspect_ratio=False)
        else:
            image = self.dirBase + '/images/' +  'croix-rouge.jpg'
        return image

    def on_next_word(self):
        """
        Fonction relancement la partie
        :return:
        """

        self.positionInWord = 0
        # Mise à jour du mot
        print("replay : ", self.theme_tri, self.motif_tri)
        if len(self.mots_deja_sortis) < len(self.liste_mots_a_trouver):
            while True:
                self.mot_a_trouver = choice(self.liste_mots_a_trouver).rstrip()
                print("nouveau mot")
                print(self.liste_mots_a_trouver)
                if self.mot_a_trouver not in self.mots_deja_sortis:
                    break
        else:
            if len(self.mots_deja_sortis) == len(self.liste_mots_a_trouver):
             #exit()
             print("normaelement exit")
             pass

        # Incrémente la liste de mots deja vu
        self.nombreDeMots += 1
        self.mots_deja_sortis.append(self.mot_a_trouver)

        # Mise à jour de la zone de saisie
        self.mot_cache = "-" * len(self.mot_a_trouver)
        self.label_mot_cache.set_text(self.mot_cache)

        # Mise à jour de l'image
        image = self.dirBase + '/images/' + self.mot_a_trouver + '.png'
        image = self.check_if_image_exist(image)

        # Mise à jour du mp3
        file = self.dirBase + '/images-mp3/' + self.mot_a_trouver + '.mp3'
        file = self.check_if_sound_exist(file)


        # Redimensionnement
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(filename=image, width=200, height=200,
                                                         preserve_aspect_ratio=False)
        self.image.set_from_pixbuf(pixbuf)
        print(self.mot_a_trouver)

    def on_button_press_event_letters(self, widget, event, param):
        """
        https://developer.gnome.org/pygtk/stable/gdk-constants.html
        https://developer.gnome.org/pygtk/stable/class-gtkeventbox.html
        :param widget:
        :param event:
        :param param:
        :return:
        """
        # Si le bouton droit de la souris est pressé
        if event.type == Gdk.EventType.BUTTON_PRESS and event.button == 3:
            file = "phonemes/" + param.get_label() + '.mp3'
            print(file)
            piste = vlc.MediaPlayer(file)
            piste.play()
            return True  # event has been handled
        pass

    def on_sound_play(self, wigdet):
        """
        Lit un fichier ogg ou mp3
        :param wigdet:
        :param ogg: le fichier son
        """
        file = self.dirBase + "/images-mp3/" + self.mot_a_trouver + '.mp3'
        piste = vlc.MediaPlayer(file)
        piste.play()

    def on_valid_config_theme(self, widget):
        """
        Configuration de jeu enregistrée. Retour onglet 1.
        :param widget:
        :return:
        """
        if self.theme_tri == "Animaux domestiques":
            self.file = "listes-de-mots/animaux-domestiques.txt"
        if self.theme_tri == "Animaux sauvages":
            self.file = "listes-de-mots/animaux-sauvages.txt"
        if self.theme_tri == "Animaux de la forêt":
            self.file = "listes-de-mots/animaux-foret.txt"

        print("ON VALID CONF", self.theme_tri, self.file)

        # Initialisation des variables
        self.positionInWord = 0
        self.score = 0

        # Lecture du fichier de mots
        self.liste_mots_a_trouver = self.creer_liste_mot(self.file)
        print(self.liste_mots_a_trouver)
        self.mot_a_trouver = choice(self.liste_mots_a_trouver)
        self.mots_deja_sortis = []
        self.mots_deja_sortis.append(self.mot_a_trouver)
        self.nombreDeMots = 1
        print(self.mot_a_trouver)

        # SCORE :Réinitialisation
        self.score_total = len(self.liste_mots_a_trouver)

        # Actualisation du mot caché
        self.mot_cache = "-" * len(self.mot_a_trouver)
        self.label_mot_cache.set_text(self.mot_cache)

        # Actulisation de la zone de CHoix du thème
        self.label_choix_du_theme.set_text(self.theme_tri)

        # Mise à jour de l'image
        image = self.dirBase + '/images/' + self.mot_a_trouver + '.png'
        print(image)
        image = self.check_if_image_exist(image)

        # Mise à jour du mp3
        file = self.dirBase + '/images-mp3/' + self.mot_a_trouver + '.mp3'
        file = self.check_if_sound_exist(file)

        # Redimensionnement
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(filename=image, width=200, height=200,
                                                         preserve_aspect_ratio=False)
        self.image.set_from_pixbuf(pixbuf)

        # Retourne vers l'onglet actif
        self.notebook.set_current_page(0)
        print(self.mot_a_trouver)
        print(self.motif_tri, " - - ", self.theme_tri)


    def on_valid_config_phoneme(self, widget):
        """
        Configuration de jeu enregistrée. Retour onglet 1.
        :param widget:
        :return:
        """
        if self.theme_tri == "Animaux domestiques":
            self.file = "listes-de-mots/animaux-domestiques.txt"
        if self.theme_tri == "Animaux sauvages":
            self.file = "listes-de-mots/animaux-sauvages.txt"
        if self.theme_tri == "Animaux de la forêt":
            self.file = "listes-de-mots/animaux-foret.txt"

        print("ON VALID CONF", self.theme_tri, self.file)

        # Initialisation des variables
        self.positionInWord = 0
        self.score = 0

        # Lecture du fichier de mots
        self.liste_mots_a_trouver = self.creer_liste_mot(self.file)
        print(self.liste_mots_a_trouver)
        self.mot_a_trouver = choice(self.liste_mots_a_trouver)
        self.mots_deja_sortis = []
        self.mots_deja_sortis.append(self.mot_a_trouver)
        self.nombreDeMots = 1
        print(self.mot_a_trouver)

        # SCORE :Réinitialisation
        self.score_total = len(self.liste_mots_a_trouver)

        # Actualisation du mot caché
        self.mot_cache = "-" * len(self.mot_a_trouver)
        self.label_mot_cache.set_text(self.mot_cache)

        # Actulisation de la zone de CHoix du thème
        self.label_choix_du_theme.set_text(self.theme_tri)

        # Mise à jour de l'image
        image = self.dirBase + '/images/' + self.mot_a_trouver + '.png'
        print(image)
        image = self.check_if_image_exist(image)

        # Mise à jour du mp3
        file = self.dirBase + '/images-mp3/' + self.mot_a_trouver + '.mp3'
        file = self.check_if_sound_exist(file)

        # Redimensionnement
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(filename=image, width=200, height=200,
                                                         preserve_aspect_ratio=False)
        self.image.set_from_pixbuf(pixbuf)

        # Retourne vers l'onglet actif
        self.notebook.set_current_page(0)
        print(self.mot_a_trouver)
        print(self.motif_tri, " - - ", self.theme_tri)


    def on_key_press_event(self, widget, event, label, buttonSensitive):
        """
        Recupérer l'entrée standard du clavier;
        Sélectionne que les touches affichées par l'application
        Met à jour le label en fonction de la touche appuyée
        :param widget:
        :param event: touche du clavier --> chr(event.keyval)
        """
        print(event.keyval)
        if event.keyval == 65293:
            self.on_validate_word(self, self.label_mot_cache, self.label_du_score)

        if event.keyval == 65288:
            self.on_correct_word(self, self.bouton_corriger, self.label_mot_cache)

        if chr(event.keyval) in self.alphabet:
            editable = list(self.mot_cache)
            editable[self.positionInWord] = chr(event.keyval)
            self.mot_cache = ''.join(editable)
            self.positionInWord += 1
            label.set_text(self.mot_cache)
            if self.positionInWord < len(self.mot_a_trouver):
                buttonSensitive.set_sensitive(True)
        else:
            print("TOUCHE NON DANS LA LISTE")
        print(chr(event.keyval))

    def on_letter_add(self, widget, button, label, buttonSensitive):
        """
        Récuperer la touche du clavier virtuel sélectionnée
        Met à jour le label en fonction de la touche "virtuelle appuyée"
        :param widget:
        :param button: bouton généré pour la clavier virtuel
        :param label: label à mettre à jour
        :param buttonSensitive: le bouton à activer / desactiver
        """
        print(len(button.get_label()))
        # Message warning si plus de lettres que dans le mot
        if self.positionInWord + len(button.get_label()) < len(self.mot_a_trouver) + 1:
            editable = list(self.mot_cache)

            # lettre ou graphme / traitement
            for i in range(len(button.get_label())):
                print(type(i))
                editable[self.positionInWord + i] = button.get_label()[i]
            self.mot_cache = ''.join(editable)
            self.positionInWord += len(button.get_label())
            label.set_text(self.mot_cache)
            buttonSensitive.set_sensitive(True)
            print(self.positionInWord, " - - ", len(self.mot_a_trouver))
        else:
            msg1 = "Trop de lettres"
            msg2 = "Le mot ne contient pas autant de lettres !"
            self.ok_alert(self, msg1, msg2)
            return

    def on_correct_word(self, widget, button, label):
        """
        Corrige le mot proposé
        :param widget:
        :param button: le bouton de correction <
        :param label: le label à corriger
        :return:
        """
        if self.positionInWord > 0:
            editable = list(self.mot_cache)
            editable[self.positionInWord - 1] = '-'
            self.mot_cache = ''.join(editable)
            self.positionInWord = self.positionInWord - 1
            label.set_text(self.mot_cache)
        # Si recul max, desactive le button
        if self.positionInWord == 0:
            button.set_sensitive(False)

    def on_delete_word(self, widget, label):
        """
        Réinitialise le label
        :param widget:
        :param label: widget à réinitialiser
        """
        self.mot_cache = "-" * len(self.mot_a_trouver)
        label.set_text(self.mot_cache)
        self.positionInWord = 0

    def on_validate_word(self, widget, label, label2):
        """
        Valide le mot proposé
        :param widget:
        :param label: widget où afficher le message de correction
        :return:
        """
        if self.mot_cache.capitalize() == self.mot_a_trouver.capitalize():
            message = 'très bien'
            self.score += 1
            label2.set_text("Score : " + str(self.score) + " / " + str(self.nombreDeMots) + " sur " + str(self.score_total))

        else:
            # Ouvre une boite dee dialogue gérant l'erreur
            label2.set_text("Score : " + str(self.score) + " / " + str(self.nombreDeMots) + " sur " + str(self.score_total))
            message = 'Le bon mot était : ' + self.mot_a_trouver
            messageTitre = "ERREUR !"
            label.set_text(messageTitre)
            self.ok_alert(self, messageTitre, message)

        # On poussa à l'autre mot
        self.on_next_word()

    def ok_alert(self, widget, message1, message2):
        """
        FOnction ouvrant une dialog box d'alerte
        :param widget:
        :param message1: Le titre du message
        :param message2: Le contenu du message
        :return:
        """
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK,
            text=message1,
        )
        dialog.format_secondary_text(message2)
        dialog.run()
        dialog.destroy()

    def gtk_style(self):
        """
        Fonction definition de CSS de l'application
        Le fichier css : pendu-peda-gtk.css
        :return:
        """
        style_provider = Gtk.CssProvider()
        style_provider.load_from_path(self.dirBase + 'style.css')

        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def on_about(self, widget):
        """
        Fonction de la Boite de Dialogue About
        :param widget:
        :return:
        """
        # Recuperation n° de version
        print(__doc__)
        lignes = __doc__.split("\n")
        for l in lignes:
            if '__version__' in l:
                version = l[15:-1]
            if '__date__' in l:
                dateGtKBox = l[12:-1]

        authors = ["Cyrille BIOT"]
        documenters = ["Cyrille BIOT"]
        self.dialog = Gtk.AboutDialog()
        logo = GdkPixbuf.Pixbuf.new_from_file(self.dirBase+"apropos.png")
        if logo != None:
            self.dialog.set_logo(logo)
        else:
            print("A GdkPixbuf Error has occurred.")
        self.dialog.set_name("Gtk.AboutDialog")
        self.dialog.set_version(version)
        self.dialog.set_copyright("(C) 2020 Cyrille BIOT")
        self.dialog.set_comments("encoder-mots.py.\n\n" \
                                 "[" + dateGtKBox + "]")
        self.dialog.set_license("GNU General Public License (GPL), version 3.\n"
                                "This program is free software: you can redistribute it and/or modify\n"
                                "it under the terms of the GNU General Public License as published by\n"
                                "the Free Software Foundation, either version 3 of the License, or\n"
                                "(at your option) any later version.\n"
                                "\n"
                                "This program is distributed in the hope that it will be useful,\n"
                                "but WITHOUT ANY WARRANTY; without even the implied warranty of\n"
                                "MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n"
                                "GNU General Public License for more details.\n"
                                "You should have received a copy of the GNU General Public License\n"
                                "along with this program.  If not, see <https://www.gnu.org/licenses/>\n")
        self.dialog.set_website("https://cbiot.fr")
        self.dialog.set_website_label("cbiot.fr")
        self.dialog.set_website("https://github.com/CyrilleBiot//encoder_mots/")
        self.dialog.set_website_label("GIT ")
        self.dialog.set_authors(authors)
        self.dialog.set_documenters(documenters)
        self.dialog.set_translator_credits("Cyrille BIOT")
        self.dialog.connect("response", self.on_about_reponse)
        self.dialog.run()

    def on_about_reponse(self, dialog, response):
        """
        Fonction fermant la boite de dialogue About
        :param widget:
        :param response:
        :return:
        """
        self.dialog.destroy()

    def toggled_cb_motif(self, button):
        self.motif_tri = button.get_label()
        #print(self.motif_tri)

    def toggled_cb_theme(self, button):
        self.theme_tri = button.get_label()
        print(self.theme_tri)


def main():
    """
    La boucle de lancement
    :return:
    """
    win = EcrireMot()
    win.gtk_style()
    win.connect("destroy", Gtk.main_quit)
    win.move(10, 10)
    win.show_all()
    Gtk.main()


"""
 Boucle main()
"""
if __name__ == "__main__":
    # execute only if run as a script
    main()

