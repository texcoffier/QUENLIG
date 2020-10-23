#- coding: latin-1 -*-
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

"""
Questions portant sur la syntaxe et la structuration d'un programme C
"""

from QUENLIG.questions import *
from .check import C

prog1 = r"""/*
Ce programme affiche les entiers de 0 � 9 inclus.
C'est mon premier programme.
*/
#include <iostream>   // Cette ligne est du C++ et non du C 
#include <stdlib.h>   // Pour pouvoir utiliser EXIT_SUCCESS
using namespace std ; // Pour pouvoir �crire 'cout' au lieu de 'std::cout'
int main(void)
{
  /* On d�clare les variables avant les instructions
     Cela permet de s�parer l'algorithme du reste */
  int i ;
  for(i=0; i<10; i++)
     cout << "i=" << i << endl ; // Affiche le compteur sur une ligne
  return EXIT_SUCCESS ; // Indique que tout c'est pass� sans probl�me
}"""

add(name="commentaires",
    required = ["intro:intro"],
    before = """
    Lorsque l'on �crit un programme,
    on a souvent besoin d'ins�rer des commentaires dans le <i>code source</i>.
    <span style="color:green">Ah, le code source, mais c'est quoi&nbsp;:
    le code source&nbsp;?
    Encore du jargon d'informaticien?</span>
    <p>
    On appelle <i>code source</i> l'ensemble des instructions �crites
    dans un langage de programmation de haut niveau.
    <p>
    Les commentaires sont des lignes qui n'influence pas le d�roulement
    du programme mais qui servent uniquement � apporter
    des informations sur le programme, exemple&nbsp;:
    date de cr�ation, auteur du programme ...
    <ul>
    <li> En langage C  un commentaire d�bute par : <tt>/*</tt>
    et se termine par : <tt>*/</tt> 
    <li> Un commentaire peut-�tre plac� n'importe o� dans le code source,
    d�s lors qu'il est encadr� par les caract�res <b>/* </b>
    au d�but et <b> */</b> � la fin.  
    <li> On ne peut pas imbriquer des commentaires
    <li> On peut commenter la fin d'une ligne en mettant <tt>//</tt>
    </ul>""",   
    question = """La r�ponse � cette question est le programme suivant
    sans ses commentaires&nbsp;:   
    <pre>%s</pre>""" % html.escape(prog1),
    nr_lines = 13,
    default_answer = prog1,
    tests = (
        Good(C(Equal(r'''#include <iostream>#include <stdlib.h>
	using namespace std ;int main(void)
        {int i;for(i=0;i<10;i++)cout <<"i="<<i<<endl;return EXIT_SUCCESS;}''')
               )),
        ),
    bad_answer = """Il y a 7 commentaires � enlever.
    Si vous les avez tous enlev�, vous avez peut-�tre d�truit
    des choses en trop.""",
    )




  



