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
    required=["trier:unique", "manuel:chercher"],
    before="""La commande <tt>tr</tt> permet de remplacer un caractère
    par un autre dans un flux de données.
    Par exemple :
    <ul>
    <li> <tt>tr "[a-z]" "[A-Z]"</tt> transforme les minuscules en majuscules
    <li> <tt>tr "XT" "AU"</tt> transforme les X en A et les T en U.
    <li> <tt>tr "[0-9]" "XXXXXXXXXX"</tt> transforme les chiffres en X
    </ul>
""",
    question="""Quel est le filtre qui à partir d'un texte fourni sur
    l'entrée standard crée la liste des mots utilisés dans le texte.
    <table>
    <tr><th>Entrée<th>Sortie attendue</tr>
    <tr><td><pre>Ceci est un texte court,
très court.</pre><td><pre>ceci
court
est
texte
très
un</pre></tr></table>
    La commande <tt>tr</tt> remplacera <b>dans l'ordre indiqué</b>&nbsp;:
    <ul>
    <li> Le majuscules par des minuscules.
    <li> Les caractères «,», «.», « » par un retour à la ligne
    </ul>

    """,
    nr_lines = 7,
    tests = (
        Reject('text', """Le texte « Ceci est un texte court, très court. »
               ne fait pas parti de votre réponse, c'était un exemple."""),
        Expect('sort'),
        Expect('tr'),
        Expect('|',
               """Il faut combiner la commande <tt>tr</tt>
               et la commande <tt>sort</tt> dans un pipeline"""),
        Expect('-u', """Utilisez l'option de <tt>sort</tt> pour ne lister
        chaque mot qu'une seule fois."""),
        Expect('[a-z]'),
        Expect('[A-Z]'),
        Bad(Comment(~ NumberOfIs('tr', 1),
                      """Vous ne devez lancer la commande <tt>tr</tt> qu'une
                      seule fois.""")),
        Good(Shell(Equal('tr "[A-Z],. " "[a-z]\n\n\n" | sort -u')
                   | Equal('tr "[A-Z],. " "[a-z]\\n\\n\\n" | sort -u')
                   | Equal('tr "[A-Z],. " "[a-z]\\012\\012\\012" | sort -u'))),
        Good(Comment(Shell(Equal('tr "[A-Z],. " "[a-z]\n" | sort -u')
                           | Equal('tr "[A-Z],. " "[a-z]\\n" | sort -u')
                           | Equal('tr "[A-Z],. " "[a-z]\\012" | sort -u')),
                     """Ceci fonctionne, mais il est conseillé de mettre le
                     même nombre de caractères dans les deux paramètres""")),
        shell_display,
        ),
    )
