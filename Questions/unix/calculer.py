# -*- coding: latin-1 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2005-2007 Thierry EXCOFFIER, Universite Claude Bernard
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
from .check import *

expr_required = require('expr', 'On utilise <tt>expr</tt> évidemment')

add(name="intro",
    required=["manuel:chercher"],
    question="""Quel est le nom de la commande utilisée pour
    faire des petits calculs sur les entiers et manipuler
    des chaines de caractères&nbsp;?""",
    tests=(
    bad(('bc','dc'),
        "C'est un langage de programmation non vu en cours"),
    bad('test',
        "Cette commande permet seulement d'obtenir un résultat booléen"),
    good('expr'),
    ),
    indices=("""C'est l'abréviation de <tt>expression</tt>""",
             )
    )

add(name="division",
    required=["intro"],
    question="""Donnez la commande qui fait afficher le résultat du calcul de 7 divisé par 2""",
    tests=(
    reject(('3', '3.5', '4'),
           """C'est la machine qui doit faire le calcul, pas vous.
           Relisez la question, elle est parfaitement claire.
           """),
    reject('echo', """La commande <tt>expr</tt> affiche sur la sortie standard.
    Donc, pas de besoin de faire un <tt>echo</tt>"""),
    require('/', 'On indique la division avec le symbole <tt>/</tt>'),
    expr_required,
    shell_bad('expr 7/2', 'Il faut des espaces autour des opérateurs'),
    shell_good('expr 7 / 2'),
    shell_bad("$(expr 7 / 2)",
              """Si vous vous étiez donné la peine d'exécuter cette commande,
              vous auriez vu un message d'erreur qui vous aurait appris
              beaucoup de choses."""),
    reject(('(', ')'), "Pourquoi avez-vous besoin de parenthèses&nbsp;?"),
    shell_display,
    ),
    )

add(name="multiplication",
    required=["division", "sh:affiche étoile"],
    question="""Donnez la commande qui fait afficher le résultat du calcul de 2 fois 3""",
    tests=(
    require('*', 'On indique la multiplication avec le symbole <tt>*</tt>'),
    reject('echo', """Pas besoin de faire <tt>echo</tt> car <tt>expr</tt>
    écrit sur la sortie standard"""),
    expr_required,
    reject(('3 * 2', '3 \\* 2', '3 "*" 2', "3 '*' 2", "3*2"),
           """Quand on vous dit de calculer 2 fois 3 ce n'est pas 3 fois 2.
           Il faut répondre avec précision aux questions
           sinon le système les refusera"""),
    reject('2*3', 'Il faut des espaces autour des opérateurs'),
    shell_good('expr 2 "*" 3'),
    shell_bad(('expr "2 * 3"', 'expr 2\*3'),
              """Vous n'avez pas tapé la commande...<br>
              <tt>expr</tt> veut un argument par opérateur et opérande.
              """),
    shell_bad('expr 3 "*" 2', "On vous demande 2 fois 3, pas l'inverse !"),
    shell_bad('expr 2 * 3',
              """Le seul cas ou cette commande fonctionne c'est quand
              le répertoire est vide car l'étoile reste une étoile.
              Sinon elle est remplacée pour tous les noms d'entités
              contenues dans le répertoire courant.
              """),
    shell_display,
    ),
    )

add(name="longueur",
    required=["division", "variable:intro"],
    question="""Quelle ligne de commande permet d'afficher
    la longueur de la chaine de caractères contenue dans
    la variable shell <tt>PATH</tt>""",
    tests=(
    reject("wc",
           """Il ne faut pas utiliser <tt>wc</tt> car cette commande
              va compter la fin de ligne envoyée par <tt>echo</tt>.
              Vous devez obligatoirement utiliser <tt>expr</tt>
              au lieu de <tt>wc</tt>"""
              ),
    reject('${#PATH}',
           """Cela marche peut-être, mais ce n'est pas du shell
           standard, on vous demande d'utiliser <tt>expr</tt>"""),
    require('expr', "Vous devez utiliser la commande <tt>expr</tt>"),
    require('PATH', "Je ne vois pas <tt>PATH</tt> dans votre commande."),
    require('$PATH', """Pour accéder au contenu d'une variable, on met
    un <tt>$</tt> devant."""),
    reject('echo', """Pourquoi utiliser <tt>echo</tt>, vous n'avez
    pas besoin d'écrire la variable sur la sortie standard."""),
    require('length', "Longueur en anglais, c'est <tt>length</tt>") ,
    require('"', """Il faut protéger les espaces qui pourraient
    être contenus dans la variable PATH, il faut donc des guillemets."""),
    reject('+', """Laissez nous un commentaire pour nous dire
    pourquoi vous avez mis un + !!! Quel est son utilité&nbsp;?"""),
    shell_good("expr length \"$PATH\""),
    shell_bad("expr length $PATH",
              """Cela ne fonctionnera pas si la variable
              contient des espaces."""),
    reject('-', "Vous n'avez pas besoin de '-' pour répondre"),
    reject('$(', "Pourquoi utilisez-vous $(....) ?"),
    shell_display,
    ),
    )

t_redir = """Il aurait été plus logique de faire la redirection
sur la commande <tt>sed</tt> que sur la commande <tt>expr</tt>."""

add(name="somme",
    required=["division", "sh:remplacement", "remplacer:ajouter fin"],
    question="""Donner la ligne de commande affichant la somme
    des nombres entiers indiqués dans le fichier <tt>xxx</tt>
    <p>
    On supposera que chaque ligne du fichier contient un nombre unique.
    <p>
    Vous n'avez pas besoin de variables, de faire de boucles ou
    d'utiliser d'autres commandes que <tt>expr</tt> et <tt>sed</tt>.
    """,
    tests=(
    reject("=", """Vous n'avez pas besoin de l'affectation pour répondre
                à cette question"""),
    reject('&',
           """Vous avez utilisé un '&' pour ajouter en fin/début de lignes.
           Pourquoi ne pas utiliser la méthode que vous avez déjà employée
           dans une question précédente&nbsp;?
           Un petit '^' ou '$' par exemple..."""),
    reject('\\+', """Pas besoin d'échapper le '+' car il n'est pas spécial
                     pour une expression régulière non-étendue"""),
    shell_good("expr 0 $(sed <xxx 's/^/+ /')"),
    shell_good(("expr 0 $(sed 's/^/+ /') <xxx",
                "expr $(sed 's/$/ +/') 0 <xxx"
                ), t_redir),
    shell_good("expr $(sed <xxx 's/^/+ /')",
               """Je vous l'accorde, mais admettez que c'est bizard
               que <tt>expr + 6 + 7</tt> fonctionne avec un espace
               entre le 'plus' et le 'six'"""),
    shell_good("expr $(sed 's/^/+ /') <xxx",
               """Je vous l'accorde, mais admettez que c'est bizard
               que <tt>expr + 6 + 7</tt> fonctionne avec un espace
               entre le 'plus' et le 'six'.<p>""" + t_redir),
    shell_good("expr $(sed 's/$/ +/g') 0 <xxx",
               """Le <tt>/g</tt> est inutile (remplacement unique),
               mais j'accepte.<p>""" + t_redir),
    require("expr", "On utilise <tt>expr</tt> pour additionner"),
    require("sed",
            """On utilise <tt>sed</tt> pour ajouter des <tt>+</tt>
            aux bons endroits"""),
    require("$(",
            """Il faut faire un remplacement de commande pour mettre
            les opérations à faire (sortie de <tt>sed</tt>)
            comme paramètres de <tt>expr</tt>"""),
    reject("s/$/+/",
            """Vous ajoutez des <tt>+</tt> en fin de ligne
            sans mettre d'espace avant, <tt>expr</tt> ne pourra
            les évaluer"""),
    reject((" + /", "/ + "),
            """Il y a un espace inutile autour de votre '+'
            car le retour à la ligne joue le role de séparateur"""),
    require(("s/$/ +/", "s/^/+ /"),
            """Je ne vois pas la substitution disant à <tt>sed</tt>
            d'ajouter un <tt>+</tt> à la fin/début de chaque ligne.
            N'oubliez pas qu'il faut un espace autour des opérateurs.""",
            all_agree=True),
    require(" 0", """Pour que l'expression soit valide,
    il faut mettre un 0 à la fin ou au début de la somme."""),
    reject('-e',
           """On a pas besoin de <tt>-e</tt>
           car il n'y a qu'un seul argument"""),
    require("<", """On préfère rediriger l'entrée standard de <tt>sed</tt>
    plutôt que de donner le nom du fichier"""),
    shell_good("expr $(sed <xxx 's/$/ +/g') 0",
               """Le <tt>/g</tt> est inutile (remplacement unique),
               mais j'accepte"""),
    shell_good("expr $(sed <xxx 's/$/ +/') 0"),
    shell_bad("expr $(sed <xxx 's/$/ +/') + 0",
              """Cela fonctionne uniquement parce que <tt>expr 5 + + 0</tt>
              ne fait pas d'erreur"""),
    reject('/g', """Pas besoin de l'option <tt>g</tt> il y a seulement
    une substitution par ligne"""),
    expect('xxx'),


    shell_display,
    ),
    indices = (
    """L'algorithme est le suivant&nbsp;: <tt>expr</tt> <tt>0</tt> <em>le contenu de <tt>xxx</tt> auquel on ajoute des <tt>+ </tt> en début de ligne</em>""",
    ),
    )

# add(name="prefixe longueur",
#     required=["longueur", "sh:tant que"],
#    question="""Faites afficher chaque ligne lue dans l'entrée standard
#    en la préfixant par sa longueur suivie d'un espace.""",
#    tests=(
#        shell_good('while read A ; do echo $(expr length "$A") "$A" ; done'),
#        )
#    )
    
    
