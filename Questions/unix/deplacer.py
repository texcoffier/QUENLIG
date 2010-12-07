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

mv_required = require("mv", "On déplace/renomme les fichiers avec <tt>mv</tt>")

mv_shorter = reject("./a",
                    "<tt>a</tt> c'est plus court à écrire que <tt>./a</tt>")


add(name="intro",
    required=["manuel:chercher"],
    before="""La commande permettant de déplacer (<em>move</em> en anglais)
    les fichiers d'un endroit à l'autre permet de les renommer.
    <p>
    Attention, si le fichier destination existe, il est détruit
    pour être remplacé par le nouveau.
    <p>
    Attention, vous avez le droit de déplacer un fichier si vous
    avez le droit d'écriture dans le répertoire.
    Si c'est le cas, vous avez le droit de déplacer des fichiers
    sur lesquels vous n'avez aucun droit.
    """,
    question="""Quelle est la commande permettant de renommer
    le fichier <tt>a</tt> en <tt>b</tt> dans le répertoire courant&nbsp;?""",
    indices=("La commande pour déplacer est <tt>mv</tt>",),
    tests=(
    reject('move', """Généralement, les noms des commandes les plus utilisées
    sont sur 2 caractères pour être plus rapide à taper."""),
    shell_good("mv a b"),
    shell_good( ("mv ./a ./b", "mv a ./b", "mv ./a b"),
                "<tt>mv a b</tt> est plus simple et plus court"),
    reject(("A", "B"), "Sous Unix majuscule et minuscule sont différentes."),
    reject("rm", "C'est pour détruire ! Pas pour déplacer !"),
    reject("cp", "C'est pour copier ! Pas pour déplacer !"),
    require(("a", "b"), "Vous voulez déplacer quoi&nbsp;?"),
    require('mv',
            "Je ne vois pas le nom de la commande permettant de renommer"),
    shell_display,
    ),
    )

add(name="répertoire",
    question="""Donnez la commande la plus courte pour
    déplacer le fichier <tt>a</tt> du répertoire courant
    pour le mettre dans le répertoire <tt>/tmp</tt>
    sans lui changer son nom.""",
    tests=(
    shell_good("mv a /tmp"),
    shell_good("mv a /tmp/", "Le / final est inutile"),
    shell_bad(("mv a /tmp/a", "mv a /tmp/."), "Ce n'est pas la plus courte"),
    mv_required,
    mv_shorter,
    require('tmp', 'Et le répertoire de destination, il est où&nbsp;?'),
    require('/tmp', """Pas dans le <tt>tmp</tt> du répertoire courant,
    celui qui est à la racine"""),
    reject('-', "Vous n'avez pas besoin d'indiquer d'options"),
    shell_display,
    ),
    indices=("""Quand la destination est un répertoire, les fichiers
    sont déplacés dans le répertoire sans changer de nom""",),
    )

add(name="répertoire et renomme",
    before="On suppose que <tt>/tmp/A</tt> n'existe pas",
    question="""Donnez la commande la plus courte pour
    déplacer le fichier <tt>a</tt> du répertoire courant
    pour le mettre dans le répertoire <tt>/tmp</tt>
    en le nommant <tt>A</tt>.""",
    tests=(
    shell_good("mv a /tmp/A"),
    shell_bad("mv a /tmp A",
              "Votre commande déplace <tt>a</tt> et <tt>tmp</tt> dans <tt>A</tt>"),
    shell_bad("mv a A /tmp",
              "Votre commande déplace <tt>a</tt> et <tt>A</tt> dans <tt>/tmp</tt>"),
    shell_bad("mv a tmp/A",
              "Dans le <tt>tmp</tt> de la racine, pas du répertoire courant"),
    mv_required,
    mv_shorter,
    require("/tmp/A",
            "Il faut indiquer le nom de la destination (le nouveau nom)"),
    reject('-', "Vous n'avez pas besoin d'indiquer d'options"),
    shell_display,
    ),
    )






