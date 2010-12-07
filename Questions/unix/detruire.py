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
    required=["sh:console"],
    question="""Quel est le nom de la commande permettant
    de faire disparaître (détruire) les fichiers&nbsp;?""",
    tests=(
    good("rm"),
    bad("kill", "C'est pour envoyer un signal à une processus"),
    bad("rmdir", "C'est pour détruire un répertoire vide, pas des fichiers"),
    ),
    indices=("En anglais cela vient du mot <em>remove</em>",
             """Elle est dans la liste affichée par :
             <tt>man -k 'remove.*file'</tt>""",
             ),
    )

add(name="simple",
    question="""Quelle commande permet de détruire les
    deux fichiers nommés :
    <ul>
    <li><tt>a</tt> (donc dans le répertoire courant)
    <li><tt>/tmp/a</tt>
    </ul>""",
    tests=(
    shell_good("rm a /tmp/a"),
    shell_good("rm /tmp/a a", "Pourquoi avez-vous changé l'ordre&nbsp;?"),
    reject('-', "On a pas besoin d'options"),
    shell_require("<argument>a</argument>",
                  "On veut détruire <tt>a</tt> dans le répertoire courant."),
    shell_require("<argument>/tmp/a</argument>",
                  "On veut détruire <tt>a</tt> dans le répertoire <tt>/tmp</tt>"),
    shell_require("<argument>rm</argument>",
                  "On utilise la commande <tt>rm</tt>"),
    reject((";","|","&"), "On veut lancer qu'une seule commande"),
    reject("~/a",
           "<tt>a</tt> dans le répertoire courant, pas celui de connexion"),
    reject("./a",
           """Il y a plus court que <tt>./a</tt> pour indiquer <tt>a</tt>
           dans le répertoire courant"""),
    shell_display,
    ),
    )
    

add(name="problèmes",
    required=["simple", "sh:affiche étoile", "lister:spécial"],
    question="""Quelle commande permet de détruire les
    fichiers (pas répertoire) nommés <tt>*</tt> et <tt>-z</tt>""",
    tests=(
    shell_good("rm '*' -z"),
    shell_good("rm '*' ./-z",
               """Le <tt>./</tt> devant <tt>z</tt>
               est inutile car on considère qu'il n'y a plus d'options
               après la première chose qui n'est pas une option (<tt>*</tt>
               dans cet exemple)"""),
    shell_good("rm ./-z '*'",
               "La réponse attendue était <tt>rm '*' -z</tt>"),
    expect('rm'),
    number_of_is('rm', 1, "On lance la commande une seule fois."),
    shell_reject("<argument>./*</argument>",
                 "Le <tt>./</tt> devant l'étoile ne sert à rien"),
    shell_reject("<pattern_char>*</pattern_char>",
                 "Il faut protéger l'étoile car <tt>rm</tt> doit la voir"),
    reject((" ./* ", " * "),
           "Cela détruit tous les fichiers du répertoire&nbsp;!"),
    shell_require("<argument>*</argument>",
                   """La commande <tt>rm</tt> ne voit pas l'étoile"""),
    reject(" -- ",
           """C'est bien d'avoir trouvé l'astuce du <tt>--</tt>
           mais elle n'est pas portable..."""),
    require("-z", "Il faut détruire <tt>-z</tt>"),
    shell_display,
    ),
    )
    

add(name="pattern",
    required=["simple", "pattern:final"],
    question="""Donnez la ligne de commande permettant de détruire
    tous les fichiers dont le nom se termine par <tt>.o</tt>
    dans le répertoire courant""",
    tests=(
    shell_good("rm *.o"),
    shell_bad("rm '*.o'",
              """Comme vous avez protégé le <em>pattern</em> la commande
              essaye de détruire un fichier dont le nom est vraiment
              <tt>*.o</tt>"""),
    expect(".o"),
    reject("./*.o", """On peut faire un <em>pattern</em> plus court."""),
    reject('-f',
           """L'option <tt>f</tt> de <tt>rm</tt> est dangereuse.
           Il faut l'utiliser en connaissance de cause."""),
    reject('-', "On a besoin d'aucune option pour répondre."),
    reject('/', """Le caractère <tt>/</tt> indique que l'on
    indique une nom dans un autre répertoire, hors les fichiers à détruire
    sont dans le répertoire courant, ce n'est donc pas la peine"""),
    answer_length_is(6, "La réponse à cette question est en 6 caractères"),
    expect('rm'),
    shell_display,
    ),
    )

dumb_replace=(("-R","-r"),("-type f", ""))

import chercher

add(name="pattern arbre",
    required=["simple", "sh:remplacement", "chercher:pattern", "chercher:exécuter"],
    question="""Donnez la ligne de commande permettant de détruire
    tous les fichiers texte dont le nom se termine par <tt>.o</tt>
    dans le répertoire courant et toute la hiérarchie de répertoires
    au dessous.""",
    tests=(
    reject('-delete',
           """On vous demande de répondre à cette question sans l'option
           <tt>-delete</tt>, en effet le but est d'apprendre à assembler
           des fonctionnalités ensemble et non d'apprendre plein
           d'options."""),
    require('rm', "On détruit les fichiers avec <tt>rm</tt>"),
    require('find',
            "On cherche les fichiers dans la hiérarchie avec <tt>find</tt>"),
    reject('~', "Pourquoi y-a-t-il un tilde dans votre réponse&nbsp;?"),
    reject('|', "On ne veut pas faire de <em>pipe</em>"),
    shell_good("find . -name '*.o' -exec rm {} \;",
               dumb_replace=dumb_replace),
    shell_good( ( "rm $(find . -name '*.o')",
                  "find . -name '*.o' | xargs rm" ),
                """Cette commande est dangereuse dans le cas ou les noms de
                fichiers contiennent des espaces ou des retours à la ligne
                car le shell considère que ce sont des séparateurs""",
                dumb_replace=dumb_replace
                ),
    shell_bad("rm -r '*.o'",
              """La commande <tt>rm</tt> va détruire récursivement
              l'unique fichier nommé <tt>*.o</tt> qu'il soit un fichier
              ou un répertoire.""",
              dumb_replace=dumb_replace,
              ),
    shell_bad("rm -r *.o",
              """Le shell remplace le <tt>*.o</tt> par tous les
              fichiers qui correspondent dans le répertoire courant.
              Ensuite <tt>rm</tt> les détruit résursivement.
              Du coup, un répertoire nommé <tt>toto.o</tt> voit
              son contenu détruit même s'il ne se termine pas par <tt>.o</tt>,
              Et le fichier <tt>toto/x.o</tt> n'est pas détruit.""",
              dumb_replace=dumb_replace,
              ),
    shell_bad("rm *.o",
              """Détruit les fichiers du répertoires courant,
              pas des sous répertoires.
              Il faut utiliser la commande <tt>find</tt>"""),
    require('*.o',
            """Où est le <em>pattern</em> indiquant que le nom
            du fichier se termine par <tt>.o</tt>&nbsp;?"""),
    shell_require("<argument>*.o</argument>",
                  """<tt>find</tt> ne voit pas le <em>pattern</em>
                  car le shell l'a peut-être substitué."""),
    require("find","Il faut utiliser <tt>find</tt> pour trouver les fichiers"),
    reject(("-R", "-r"), "Pourquoi détruire récursivement&nbsp;?"),
    require('-exec',
            "Il faut utiliser l'option <tt>exec</tt> de <tt>find</tt>"),
    require('{}',
            "Il faut indiquer à <tt>rm</tt> le nom du fichier à détruire"),
    reject('iname',
           "On ne veut pas détruire les <tt>.O</tt> en majuscule&nbsp;!"),
    reject('./', """La manière la plus courte d'indiquer le répertoire courant
    c'est <tt>.</tt>, pas <tt>./</tt>"""),
    expect('\\;'),
    reject('(', "Pas besoin de parenthésage dans cette exercice."),
    chercher.find_dot_required,
    shell_display,
    ),
    indices=("Il faut utiliser <tt>find</tt> pour trouver les fichiers",
             ),
    )



    

    
