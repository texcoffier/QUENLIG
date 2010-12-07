# -*- coding: latin-1 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2007 Thierry EXCOFFIER, Universite Claude Bernard
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

add(name="intro",
    before="""Ce sujet de TP va vous faire découvrir le langage C
    et l'environnement standard de développement sous Unix.
    <ul>
    <li> Makefile
    <li> Compilation
    <li> Langage C
    <li> Débuggage
    </ul>
    """,
    question="""En utilisant un terminal,
    créer un répertoire nommé <tt>TPC1</tt> et allez dedans.<br>
    <big>Est-ce fait&nbsp;?</big>

    <em>Si vous ne savez pas comment faire, allez voir l'indice.</em>""",
    tests = ( Good(Yes()), ),
    indices = ("""Les commandes à taper sont les suivantes :
<pre>mkdir TPC1
cd TPC1</pre>""", )
    )

