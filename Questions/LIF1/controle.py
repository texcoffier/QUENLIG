# -*- coding: latin-1 -*-
# QUENLIG: Questionnaire en ligne (Online interactive tutorial)
# Copyright (C) 2011 Thierry EXCOFFIER, Eliane PERNA, Universite Claude Bernard
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

from questions import *
from check import C


add(name = "tant que",
    required = ['structure:mots-clefs'],
    question = """Quel est le mot clef en langage C qui traduit
    le <em>tant que</em> algorithmique&nbsp;?""",
    tests = (
        Good(Equal('while')),
        ),
    )

add(name = "que fait while",
    required = ["tant que", "operateurs:division entière"],
    question = """Combien vaut la variable <tt>nombre</tt>
    à la fin de la boucle&nbsp;?
    <pre>int main(void) 
{
int nombre = 0 ;
int valeur = 10000 ;
while( valeur != 0 )
   {
   valeur = valeur / 10 ;
   nombre = nombre + 1 ;
   }
return 0 ;
}</pre>""",
    tests = (
        Good(Int(5)),
        ),
    )

prog2 = r"""int main(void) 
{
int s = 0 ;
int i = 1 ;
while( COMPLETER_ICI )
   {
   s = COMPLETER_ICI ;
   }
return 0 ;
}"""

# A CORRIGER, manque l'incrémentation.

# add(name = "mon while",
#     required = ["que fait while"],
#     question = """Compléter le programme suivant afin de calculer la somme
#     des entiers entre 1 et 10 inclus dans la variable <tt>s</tt>
#     <pre>%s</pre>""" % prog2,
#     default_answer = prog2,
#     nr_lines = 10,
#     tests = (
#         Good(C(Replace((('i<11', 'i!=11'),
#                         ('i<=10', 'i!=11'),
#                         ('i+s', 's+i')),
#                        Equal('''
#                        int main(void) 
#                        {int s = 0 ;int i = 1 ;while( i != 11 )
#                        { s = s + i ; } return 0 ; }''')))),
#         )
#     )
#  



