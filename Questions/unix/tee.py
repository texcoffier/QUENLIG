# -*- coding: latin-1 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2011 Thierry EXCOFFIER, Universite Claude Bernard
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#    Contact: Thierry.EXCOFFIER@bat710.univ-lyon1.fr
#

from questions import *
from check import *

add(name="intro",
    required=["pipeline:intro", "navigation:rép. connexion"],
    before="""La commande <tt>tee</tt> lit son entrée standard et écrit
    ce qui a été lu sur sa sortie standard ainsi que dans le fichier
    dont le nom est passé en paramètre.
    <p>
    <tt>tee</tt> se prononce comme la lettre <tt>T</tt> en anglais.
    Cela rentre par le bas et cela sort par deux endroits.""",
    question="""Complétez la commande afin de lister
    tous les noms de fichiers/répertoires contenus dans votre répertoire
    de <b>connexion</b> sur votre écran ainsi que dans le fichier nommé
    <tt>liste</tt>""",
    default_answer = "ls -R ",
    tests=(
        Reject('>', """On a pas besoin de rediriger la sortie standard,
        puisque l'on veut afficher sur l'écran."""),
        Expect('tee'),
        Expect('liste'),
        Expect('ls -R '),
        Expect('~', "Vous n'avez pas indiqué votre répertoire de connexion"),
        Expect('|', """Il faut que la commande <tt>tee</tt> lise sur son
              entrée standard ce que la commande <tt>ls</tt> écrit sur
              sa sortie standard."""),
        Good(Shell(Equal("ls -R ~ | tee liste"))),
        Good(Comment(Shell(Equal("ls -R ~/ | tee liste")),
                     'Le / après le ~ est inutile dans ce cas'
                     )),
        shell_display
        ),
    )
