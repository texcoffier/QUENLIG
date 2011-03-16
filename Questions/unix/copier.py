# -*- coding: latin-1 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2005-2006 Thierry EXCOFFIER, Universite Claude Bernard
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

a = "<tt>mv a b</tt> est plus simple et plus court"

add(name="intro",
    required=["manuel:chercher"],
    question="""Quelle commande permet de copier des fichiers&nbsp;?""",
    tests=(
    good("cp"),
    reject('mv', "<tt>mv</tt> permet de déplacer/renommer des fichiers"),
    reject('^C',
           """Votre réponse n'est pas un nom de commande mais un raccourci
           clavier.
           D'ailleurs, dans un terminal, <tt>^C</tt> stop la commande
           en cours de fonctionnement.
           """,
           uppercase=True),
    ),
    indices=("Abbréviation de <em>copy</em> en anglais", ),
    )

add(name="simple",
    question="""Donnez la ligne de commande permettant de copier le fichier
    texte <tt>A</tt> dans le fichier texte <tt>B</tt>""",
    tests=(
    shell_good("cp A B"),
    shell_bad("cp a b",
              """<tt>A</tt> dans <tt>B</tt>, pas <tt>a</tt> dans <tt>b</tt>.
              Avec unix, minuscules et majuscules sont différentes."""),
    expect(('cp', 'A', 'B')),
    shell_bad("cat A >B",
              """Cela fonctionne, mais on vous demande d'utiliser
              la commande de copie"""),
    reject("./", "Le <tt>./</tt> est inutile"),
    shell_display,
    ),
    )

add(name="recursif",
    required=["simple"],
    question="""Donnez la commande permettant de copier la hiérarchie
    de fichiers <tt>A</tt> sous le nom <tt>B</tt> que l'on
    suppose ne pas exister.""",
    tests=(
    expect('cp'),
    require(('A','B'), "Vous voulez copier quoi dans quoi&nbsp;?"),
    reject('f', "L'option <tt>f</tt> est dangereuse..."),
    shell_good("cp -a A B"),
    shell_good("cp -R A B",
               "L'option standard est avec <tt>-r</tt> pas <tt>-R</tt>"),
    shell_require('-r', "Et l'option indiquant la récursion&nbsp;?"),
    shell_good("cp -r A B"),
    shell_display,
    ),
    )
    

