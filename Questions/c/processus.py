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

from QUENLIG.questions import *

add(name="intro",
    before="""Quand l'ordinateur démarre un programme il commence
    l'exécution du <b>processus</b> en appelant la fonction
    <tt>main</tt> définie dans l'exécutable et en lui
    indiquant les paramètres qui lui ont été passés en ligne de commande.
    <p>
    Quand le <b>processus</b> se termine, il retourne une valeur
    entière au processus qui l'a lancé.
    <p>
    Pour voir la valeur retourné par un processus qui vient de se terminer,
    on peut lancer la commande <tt>echo $?</tt> dans le shell. 
    """,
    question="""Quelle valeur retourne le processus lancé par
    la ligne de commande <tt>test 5 = 6</tt>""",
    tests = ( Int(1), ),
    good_answer = "Un processus qui c'est bien passé doit retourner 0.",
    )
