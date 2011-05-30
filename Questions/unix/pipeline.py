# -*- coding: latin-1 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2005-2006 Thierry EXCOFFIER, Universite Claude Bernard
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
    before='''La suite de commandes qui vous est proposée liste
    la hiérarchie de fichier du répertoire courant dans
    un fichier temporaire, puis elle affiche les lignes
    du fichier temporaire contenant ' -> '.''',
    required=["sh:console", "cribler:simple", "intro:pipe"],
    question="""Réécrire la suite de commandes suivante
    en utilisant un pipeline
    <pre>ls -lR >/tmp/xxx
grep ' -&gt; ' &lt;/tmp/xxx</pre>""",
    tests=(
    shell_good("ls -lR | grep ' -> '"),
    shell_bad("grep ' -> ' | ls -lR",
              """Les données vont de gauche à droite.
              C'est la commande <tt>ls</tt> qui génère les données
              et le <tt>grep</tt> qui les traite."""),
    reject('xxx',
           '''Comme on utilise un pipeline, on a plus
           besoin du fichier temporaire'''),
    require(('ls', '-lR', "' -> '", "grep"),
            '''Il faut recopier exactement les différents
            morceaux de la commande proposée'''),
    require('|', "Où est le symbole du pipe&nbsp;?"),
    shell_display,
    ),
    good_answer="""Cette commande est fausse car elle peut trouver
    des fichiers qui ne sont pas des liens symboliques.
    La bonne commande est plutôt&nbsp;:
    <pre>find . -type l</pre>"""
    )

import chercher
import remplacer

add(name="extensions",
    required=["intro", "chercher:pattern", "remplacer:intro",
              "trier:unique", "expreg:spécial", "remplacer:enlève sans point"],
    question="""Donnez le pipeline permettant d'afficher la liste
    des extensions que vous utilisez dans votre répertoire de connexion
    et tous ses sous répertoires.
    <ul>
    <li> Il faut d'abord lister les fichiers et répertoires
    qui ont une extension dans votre hiérarchie.
    <li> Dans cette liste, ont enlève tout ce qui est à gauche du <tt>.</tt>
    (le caractère <tt>.</tt> aussi)
    <li> On utilise la commande <tt>sort</tt> pour trier
    et n'afficher qu'une seule fois chaque extension.
    </ul>
    """,
    tests=(
    reject("^", """Le '^' est inutile car le <tt>.*</tt> va prendre
    la plus longue chaine"""),
    reject('-r', "L'option <tt>-r</tt> n'est pas utile"),
    expect('find'),
    expect('sed'),
    expect('sort'),
    expect('-name'),
    reject('-iname',
           """Pas besoin de <tt>iname</tt> il n'y a pas de lettres à trouver,
           donc pas de différences minuscules/majuscules"""),
    
    reject( ('(', ')'), "On a pas besoin des parenthèses pour répondre"),
    require('~', "Je ne vois pas le répertoire de connexion"),
    reject('~/', "Mettez <tt>~</tt> au lieu de <tt>~/</tt> s'il vous plais"),
    
    shell_good(("find ~ -name '*.*' | sed 's/.*\\.//' | sort -u",
                "find ~ -name '[!.]*.*' | sed 's/.*\\.//' | sort -u",
                ),
               dumb_replace = list(chercher.dumb_replace) \
               + list(remplacer.dumb_replace)),
    shell_require('<argument>*.*</argument>',
                  """Il faut protéger les <em>patterns</em>
                  sinon <tt>find</tt> risque de chercher
                  le mauvais nom...
                  Par exemple, s'il y a <tt>toto.c</tt>
                  dans le répertoire courant, il va
                  le chercher dans toute la hiérarchie.
                  """),
    reject("/g",
           "L'option <tt>g</tt> est inutile car il n'y a qu'une substitution"),
    number_of_is('/', 3, """Quand on fait une substitution avec
    la commande <tt>sed</tt> il doit y avoir 3 <em>slash</em>
    sinon il y a une erreur de syntaxe"""),
    
    shell_display,
    ),
    indices=("""Pour lister les fichiers avec extension il faut
    utiliser la commande <tt>find</tt>""",
             """Pour enlever ce qui est à gauche de l'extension
             on utilise <tt>sed</tt>""",
             ),
    )
    
