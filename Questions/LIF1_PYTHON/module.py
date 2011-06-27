# -*- coding: latin-1 -*-
# QUENLIG: Questionnaire en ligne (Online interactive tutorial)
# Copyright (C) 2011 Thierry EXCOFFIER, Eliane PERNA Universite Claude Bernard
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# Contact: Thierry.EXCOFFIER@bat710.univ-lyon1.fr
#

"""
Script and modules
"""

from questions import *
from check import *

add(name="math",
    required = ["io:print", "idem:division", "idem:flottant",
                "idem:commentaire", "control:def"],
    before = """Comme en langage C, on peut utiliser des fonctions qui
    sont définies dans des bibliothèques.
    Pour importer la bibliothèque mathématique&nbsp;:
    <pre>import math</pre>
    <p>
    Pour utiliser une fonction (ou variable) de la biliothèque,
    vous le préfixez par le nom de la bibliothèque suivi d'un caractère point.
    <pre>math.pi</pre>
    """,
    question = """On suppose que la librairie mathématique a été
    importée.
    <p> Donnez la ligne Python affichant le cosinus de Pi/2&nbsp;?""",
    tests = (
        Good(P(Equal("print(math.cos(math.pi/2))"))),
        Reject('3', "Vous devez utiliser <tt>math.pi</tt>"),
        Reject('0', """On ne vous demande pas d'afficher le résultat
        mais de le calculer"""),
        expects(('print', 'cos', 'pi', '2')),
        Bad(Comment(~NumberOfIs('math', 2),
                    """Vous devez utilisez deux fois le module mathématique,
                    une fois pour Pi et une fois pour le cosinus""")),
        Bad(Comment(~NumberOfIs('(', 2) | ~NumberOfIs(')', 2),
                    """Il faut des parenthèses pour la fonction <tt>print</tt>
                    et d'autres pour la fonction <tt>cos</tt>""")),
        ),
    good_answer = """Avez-vous fait afficher le résultat&nbsp;?
    <p>
    Ce n'est malheureusement pas zéro,
    en informatique il faut manipuler les nombres à virgules (les flottants)
    avec de très grandes précautions""",
    )

add(name="créer",
    required = ["math", "exercices:sum", "io:print"],
    before = """Pour créer votre propre module, il suffit d'écrire votre
    programme Python dans un fichier dont le nom
    se termine par <b><tt>.py</tt></b>
    <p>
    Écrivez dans le fichier <tt>exo.py</tt> la fonction
    <tt>somme</tt> que vous aviez faites.
    """,
    question = """La réponse à cette question sont les deux lignes permettant
    d'utiliser votre fonction <tt>somme</tt> pour afficher
    la somme du tableau vide.""",
    nr_lines = 3,
    tests = (
        Good(P(Equal("import exo\nprint(exo.somme([]))"))),
        P(expects(('import', 'exo', 'print', 'somme', '[]',
                'exo.somme', 'import exo', 'somme([])'))),  
        Bad(Comment(~NumberOfIs('(', 2) | ~NumberOfIs(')', 2),
                    """Il faut des parenthèses pour la fonction <tt>print</tt>
                    et d'autres pour la fonction <tt>somme</tt>""")),
        ),
    good_answer = """ATTENTION: les noms des fichiers Python doivent
    seulement contenir des caractères autorisés dans les variables.
    C'est-à-dire&nbsp;: alphanumérique sans accents et le souligné (_).""",
    )


add(name="script",
    required = ["créer", "io:print"],
    before = """Si vous ajoutez en première ligne de votre module&nbsp;:
    <pre>#!/usr/bin/python3</pre>
    Quand vous allez demander à faire exécuter le fichier alors
    l'interpréteur Python que vous avez indiqué sera lancé et les lignes
    suivantes seront exécutées par Python.""",
    question = """Que devez vous mettre dans un fichier pour qu'il
    affiche <tt>Bonjour</tt> quand vous l'exécutez&nbsp;?""",
    nr_lines = 3,
    tests = (
        Good(P(Equal('#!/usr/bin/python3\nprint("Bonjour")'))),
        Good(P(Equal('#!/usr/bin/python3\nprint(\'Bonjour\')'))),
        P(expects(('#!/usr/bin/python3', 'print', 'Bonjour', '(', ')',
                   '"Bonjour"'))),\
        ),
    )
    
