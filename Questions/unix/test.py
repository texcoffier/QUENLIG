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
    required=["sh:valeur de retour"],
    before="""La commande <tt>test</tt> permet d'évaluer des expressions
    concernant les entiers, fichiers et chaines de caractères.
    <p>
    Sa valeur de retour est <tt>0</tt> si le test est réussi.
    La valeur VRAI en shell est 0, les valeurs autres sont des codes d'erreur.
    """,
    question="""Commande <tt>test</tt> retournant vrai si <tt>toto</tt>
    est un fichier texte (pas un répertoire) qui existe.""",
    tests = (
        Reject("-d", """Il ne faut pas tester si ce n'est pas un répertoire
        mais tester si c'est un simple fichier texte"""),
        Bad(Comment(~Contain('test') & ~Contain('['),
                    "Il manque la commande <tt>test</tt>"
                    )),
        Expect('toto'),
        Expect('-', """Il manque l'option de <tt>test</tt> lui indiquant
        que l'on veut tester l'existence du fichier."""),
        Good(Shell(Equal('test -f toto'))),
        Good(Shell(Equal('[ -f toto ]'))),
        Bad(Comment(Shell(Equal('test -e toto') | Equal('[ -e toto ]')),
                    "Votre test retourne vrai si c'est un répertoire."
                    )),
        ),
    )


        
