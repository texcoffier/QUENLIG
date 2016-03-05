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

"""
Questions portant sur la syntaxe et la structuration d'un programme C
"""

from QUENLIG.questions import *

add(name="mots-clefs",
    required = ["intro:intro"],
    before = """Un programme en langage C est constitué d'un ensemble
    de fonctions dont l'une d'entre elles est particulière&nbsp;:
    la fonction <tt>main</tt> 
    """,
    question="""<PRE>
#include <iostream>   // Cette ligne est du C++ et non du C 
int main(void)
{
  cout << "Bonjour" << endl ;
  return 0 ;
}</PRE>
Parmi tous les termes utilisés dans le programme ci-dessus,
énumérez ceux qui sont des mots clefs du langage C.""",   
    
    tests = (
        Good(Contain("return") & Contain("char") & Contain("int")),
        Bad(Comment(Contain("include"),
                    """<tt>include</tt> n'est pas un mot clef du langage
                    mais une directive du préprocesseur""")) |
        Bad(Comment(Contain("stdio"),
                    """<p><tt>iostream</tt> n'est pas un mot clef du langage
                    mais le nom d'un fichier""")) |
        Bad(Comment(Contain("main"),
                    """<p><tt>main</tt> n'est pas un mot clef du langage
                    mais le nom de la fonction principale du programme""")),
        Bad(Comment(Contain("argc")|Contain("argv"),
                    """<p><tt>argc</tt> et <tt>argv</tt>
                    ne sont pas des mots clefs
                    du langage mais des noms de variables""")) |
        Bad(Comment(Contain("cout"),
                    """<p><tt>cout</tt> n'est pas un mot clef du langage
                    mais le nom d'une variable""")) |
        Bad(Comment(Contain("endl"),
                    """<p><tt>endl</tt> n'est pas un mot clef du langage
                    mais le nom d'une constante""")) |
        Bad(Comment(UpperCase(Contain("BONJOUR")),
                    """<p><tt>bonjour</tt> n'est pas un mot clef du langage
                    mais une chaine de caractères""")),
        Bad(Comment(Contain(''), "<p>Il manque des mots clefs")),
        # XXX et { } 0
    ),
)
