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
Les entrées/sorties en Python
"""

from questions import *
from check import *

add(name="print",
    required = ["idem:chaine", "idem:multiplication"],
    before = """La fonction <tt>print</tt> en Python affiche sur l'écran
    ses paramètres&nbsp;:""" + python_html("""
    >>> a = 6
    >>> print("a=", a, "!")
    a= 6 !
    >>> """) + """
    <p>ATTENTION, il ne faut pas mettre les parenthèses quand on utilise
    Python version 2.
    <p>
    Les réponses attendues par ce logiciel
    doivent utiliser les parenthèses.""",
    question="""Par quoi faut-il remplacer <tt>VOTRE COMMANDE</tt>
    pour que le bout de programme qui suit affiche le bon résultat
    quelque soit les valeurs des variables <tt>a</tt> et <tt>b</tt>&nbsp;?
    """ + python_html("""
    >>> a = 6
    >>> b = 7
    >>> VOTRE COMMANDE
    6 * 7 = 42
    >>>"""),

    tests = (
        Good(P(Equal('print(a, "*", b, "=", a*b)'))),
        Expect('print', """Pour faire afficher quelque chose sur l'écran
        on utilise la fonction <tt>print</tt>"""),        
        Bad(Comment(Contain('6') | Contain('7') | Contain('42'),
                    """On veut que votre réponse fonctionne quelque soit les
                    valeurs contenues dans <tt>a</tt> et </tt>b</tt>.
                    Vous ne pouvez donc pas avoir de valeurs numériques
                    dans votre réponse""")),
        Bad(Comment(~Contain('a') | ~Contain('b'),
                    """Votre réponse doit utiliser les variables <tt>a</tt>
                    et <tt>b</tt>.
                    Sinon, comment manipule-t-elle leurs valeurs&nbsp;?""")),
        Expect('('),
        Expect(')'),
        Expect(',', """On utilise la virgule pour séparer les paramètres
        passés à la fonction"""),
        Bad(Comment(~NumberOfIs(',', 4),
                    """Vous devez appeler la fonction <tt>print</tt>
                    avec 5 paramètres&nbsp;:
                    <ul>
                    <li> La variable <tt>a</tt>
                    <li> La chaine contenant l'étoile
                    <li> La variable <tt>b</tt>
                    <li> La chaine contenant le égal
                    <li> La formule donnant le résultat
                    </ul>
                    Il doit donc y avoir 4 « , » dans votre réponse.
                    """)),
        Bad(Comment(~NumberOfIs('"', 4),
                    """Vous devez afficher 2 chaines de caractères,
                    La première contient « * » et la deuxième « = »""")),
        Bad(Comment(~NumberOfIs('*', 2),
                    """Il doit y avoir deux fois le caractère « * » dans
                    votre réponse, la première fois pour l'afficher
                    et la deuxième fois pour faire la multiplication""")),
                
        ),

    good_answer = """ATTENTION, par défaut un espace est automatiquement
    ajouté entre chacun des paramètres affiché.
    <tt>print("a", "b")</tt> affiche <tt>a b</tt> avec un espace entre les deux
    """,
    )

