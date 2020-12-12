def cliquer_sur_bouton_a_propos(self, widget):
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
    logo = GdkPixbuf.Pixbuf.new_from_file("apropos.png")
    if logo != None:
        self.dialog.set_logo(logo)
    else:
        print("A GdkPixbuf Error has occurred.")
    self.dialog.set_name("Gtk.AboutDialog")
    self.dialog.set_version(version)
    self.dialog.set_copyright("(C) 2020 Cyrille BIOT")
    self.dialog.set_comments("pwgen.py.\n\n" \
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
    self.dialog.set_website("https://github.com/CyrilleBiot/")
    self.dialog.set_website_label("GIT ")
    self.dialog.set_authors(authors)
    self.dialog.set_documenters(documenters)
    self.dialog.set_translator_credits("Cyrille BIOT")
    self.dialog.connect("response", self.on_about_reponse)
    self.dialog.run()