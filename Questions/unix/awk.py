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

awk_compte = "awk '{T[$0]++} END {for(i in T) print T[i],i}'"

add(name="compte",
    required=["manuel:chercher", "intro:copier coller"],
    before="""La commande <tt>awk</tt> permet de faire des traitements
    sur un flux de données.
    Elle est très performante, mais il n'est pas recommandé de l'utiliser
    pour faire de gros programmes.""",
    question="""La réponse est ce qu'affiche la commande suivante :
    <pre>echo 'un
deux
trois
deux
zero
un
deux' | %s</pre>""" % awk_compte,
    nr_lines = 5,
    tests = (
        Good(SortLines(Equal('3 deux\n1 trois\n2 un\n1 zero'))),
        ),
    )
