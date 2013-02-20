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

cut_required = require("cut",
                       """Comme vous le savez déjà la commande pour
                       extraire des colonnes d'un fichier est <tt>cut</tt>""")

ordre = """Il est plus logique d'indiquer le séparateur avant
de spécifier la colonne que l'on veut"""

add(name="extraire",
    required=["manuel:chercher"],
    before="""De nombreux fichiers ou résultats de commandes
    sont organisés sous la forme d'un tableau de donnée avec
    une ligne par donnée et des champs délimités par un
    séparateur.
    <p>
    Par exemple le fichier  <tt>/etc/passwd</tt>
    """,
    question="""Quel est le nom de la commande permettant
    d'extraire une colonne (ou plusieurs) d'un fichier&nbsp;?""",
    tests=(
    bad("awk",
        """Cette commande permet de le faire, mais cela nécessite
        l'écriture d'un programme."""),
    bad("colrm",
        """Cette commande ne comprend pas la notion de champs et de
        délimiteurs. Elle travaille seulement avec des caractères."""),
    bad("column", "Cette commande recrée un tableau à partir de colonnes"),
    good("cut"),
    ),
    indices=("C'est le verbe 'couper' en anglais",
             "C'est en trois lettres",
             "C'est le mot employé dans l'expression 'couper/coller'",
             ),
    )

add(name="les shells",
    required=["extraire", "manuel:section commande"],
    question="""Commande permettant d'extraire du fichier
    <tt>/etc/passwd</tt> seulement
    la colonne contenant le nom du programme (le shell) qui
    est lancé au moment de la connexion.""",
    tests=(
    shell_good("cut -d: -f7 /etc/passwd"),
    shell_good("cut -f7 -d: /etc/passwd", ordre),
    cut_required,
    reject("<", "Ne faites pas de redirections inutiles"),
    shell_require("<argument>-d:</argument>",
                  "Vous devez indiquer que ':' est le délimiteur"),
    shell_require("<argument>-f7</argument>",
                  """Vous devez indiquer la colonne que vous voulez extraire.
                  Le shell est indiqué dans la dernière colonne."""),
    shell_require("<argument>/etc/passwd</argument>",
                  """Vous devez indiquer le nom du fichier
                  ou extraire la colonne"""),
    shell_display,
    ),
    )

add(name="utilisateurs",
    required=["les shells", "sh:remplacement"],
    question="""Donnez la commande permettant de stocker
    dans la variable <tt>A</tt> la liste des logins
    d'utilisateurs définis dans <tt>/etc/passwd</tt>.""",
    tests=(
    reject("<", "Ne faites pas de redirections inutiles"),
    require("1", "Vous n'indiquez pas que la colonne des utilisateurs est la première"),
    require("$", """Les prérequis vous indiquent
    qu'il faut faire un remplacement en utilisant <tt>$(...)</tt>"""),
    shell_require('-d:', "Où avez-vous indiqué que le délimiteur est ':'"),
    require('A', "Où est indiquée la variable A&nbsp;?"),
    shell_good((
    "A=$(cut -d: -f1 /etc/passwd)",
    'A="$(cut -d: -f1 /etc/passwd)"'
                ) ),
    shell_good((
    "A=$(cut -f1 -d: /etc/passwd)",
    'A="$(cut -f1 -d: /etc/passwd)"'), ordre),
    reject((' =', '= '), "Il ne faut pas d'espace autour de l'affectation"),
    shell_display,
    ),
    )

import remplacer

add(name="espaces multiples",
    required=["les shells", "remplacer:intro", "pipeline:intro"],
    question="""Donnez la ligne de commande permettant d'extraire
    la cinquième colonne de l'entrée standard sachant que
    les colonnes sont séparées par de multiples espaces et non un seul.""",
    tests=(
    require('sed', "On utilise <tt>sed</tt> pour faire le remplacement"),
    require('/g', """Il y a plusieurs substitutions à faire sur la ligne,
    pas une seule. Il manque donc un 'g' pour <em>global</em> quelque part."""),
    cut_required,
    reject('/ *//',
           """Votre expression régulière remplace un espace par rien.
           Les colonnes vont donc disparaître"""),
    reject('/ */ /',
           """Votre expression régulière ajoute un espace entre chaque
           paires de caractères.
           En effet l'étoile peut répéter zéro fois."""),
    reject('[ ]', "À quoi servent les crochets autour de l'espace&nbsp;?"),
    
    shell_good("sed 's/  */ /g' | cut -d' ' -f5",
               dumb_replace=remplacer.dumb_replace),
    shell_good("sed 's/ * / /g' | cut -d' ' -f5",
		"""Il est conseillé d'écrire <tt>__*</tt>
		plutôt que <tt>_*_</tt>""",
               dumb_replace=remplacer.dumb_replace),
    shell_good("sed -r 's/ +/ /g' | cut -d' ' -f5",
               dumb_replace=remplacer.dumb_replace),
    shell_bad("sed 's/ +/ /g' | cut -d' ' -f5",
              """Le symbole <tt>+</tt> fait parti des expressions
              régulières étendues. Mais par défaut la commande
              <tt>sed</tt> ne les utilise pas.
              <p>
              Ajouter l'option indiquant à <tt>sed</tt> d'utiliser
              les expressions régulières étendues""",
               dumb_replace=remplacer.dumb_replace),
    require((' *', ' +'),
            "Il faut utiliser l'étoile ou le plus pour répéter l'espace.",
            all_agree=True),
    require("5", "Vous n'avez pas indiqué le numéro de la colonne à extraire"),
    shell_require('<argument>-d </argument>',
                  """Vous n'avez pas indiqué à <tt>cut</tt> que le séparateur
                  était l'espace"""),
    shell_bad(("sed -r 's/\\ +/ /g' | cut -d' ' -f5",
               "sed -r 's/\\ +/\\ /g' | cut -d' ' -f5",
               "sed 's/\\ \\ */ /g' | cut -d' ' -f5",
               "sed 's/\\ \\ */\\ /g' | cut -d' ' -f5",
               ),
              """L'espace n'est pas un caractère spécial pour les expressions
              régulière, donc pas besoin de le protéger""",
               dumb_replace=remplacer.dumb_replace),
    require('[', "Vous devez faire un pipeline"),
    Bad(Comment(~End('5'),
                 """Dans la commande <tt>cut</tt>, il est plus intuitif
                    d'indiquer le séparateur de champs avant d'indiquer
                    le numéro du champ à extraire""")),
    shell_display,
    ),
    indices=(
    """Utilisez un filtre pour remplacer les suites de blancs
    par un seul blanc et envoyez le résultat à la commande
    qui extrait des colonnes.
    Aidez-vous des réponses aux questions précédentes.""",
    ),
    )
    

    
