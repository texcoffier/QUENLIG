# -*- coding: latin-1 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2006 Thierry EXCOFFIER, Universite Claude Bernard
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
    required=["manuel:section commande"],
    question="""Quel est le nom de la commande permettant
    de regarder les <b>diff</b>érences entre 2 fichiers&nbsp;?
    """,
    tests=(
    good("diff"),
    bad('sdiff', """Cette commande n'est pas dans le support de cours.
    La commande que l'on attend fait un caractère de moins..."""),
    bad('cmp',
        "Cela dit s'ils sont différents, cela montre pas les différences"),
    
    ),
    indices=("La réponse est dans la question",),
    )

creation = """Lancez la suite de commande dans un terminal&nbsp;:
    <pre>cat &gt;xxx.v0 &lt;&lt;%%FIN%%
ligne 1
ligne 2
Ligne 3
ligne 4
ligne 5
ligne 6
%%FIN%%
cat &gt;xxx.v1 &lt;&lt;%%FIN%%
ligne 0
ligne 1
ligne 2
ligne 3
ligne 4
ligne 6
%%FIN%%
</pre>
<p>
Faites un copié/collé de cette liste de commandes
dans le terminal, sinon vous allez vous tromper.
Je vous rappelle que sous Unix on fait le copié avec le bouton
de gauche et le collé avec le bouton du milieu.
Il n'y a pas besoin de menu ni du clavier&nbsp;!
"""

add(name="essayer",
    required=["intro"],
    before=creation,
    question="""Que vous affiche <tt>diff</tt> quand vous lui demandez
    ce qui a changé entre <tt>xxx.v0</tt> et <tt>xxx.v1</tt>&nbsp;?
    <p>
    Attention, la différence n'est pas symétrique.
    """,
    nr_lines = 9,
    tests=(
    reject('+', "On verra l'option <tt>-u</tt> plus tard"),
    good("""0a1
> ligne 0
3c4
< Ligne 3
---
> ligne 3
5d5
< ligne 5"""),
    ),
    good_answer="""Cette liste indique les lignes qui ont été
    ajoutées et enlevées pour passer du fichier <tt>xxx.v0</tt>
    au fichier <tt>xxx.v1</tt>.
    <p>
    C'est utile&nbsp;:
    <ul>
    <li> Pour trouver ce qui a changé dans un fichier entre
    deux versions différentes.
    <li> Pour fabriquer des <em>patchs</em>.
    La commande <tt>patch</tt> permet à partir du
    fichier original <tt>xxx.v0</tt> et du fichier des différences de retrouver
    le fichier <tt>xxx.v1</tt>.
    Elle est même assez intelligente pour intégrer les changements
    même si le fichiers original n'est pas exactement identique.
    </ul>""",
    )

add(name="plus lisible",
    required=["essayer"],
    before=creation,
    question="""Que vous affiche <tt>diff</tt> quand vous lui demandez
    ce qui a changé entre <tt>xxx.v0</tt> et <tt>xxx.v1</tt>
    en lui donnant l'option <tt>-u</tt>&nbsp;?
    <p>
    Attention, la différence n'est pas symétrique.
    """,
    nr_lines = 12,
    tests=(
    good_if_contains("""@@ -1,6 +1,6 @@
+ligne 0
 ligne 1
 ligne 2
-Ligne 3
+ligne 3
 ligne 4
-ligne 5
 ligne 6"""),
    ),
    
    )
