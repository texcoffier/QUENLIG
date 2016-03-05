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

from QUENLIG.questions import *
from .check import *

reject_space = reject((" =", "= "),
           """S'il y a des blancs autour du <tt>=</tt> le shell
           va croire qu'il faut exécuter une commande et non
           faire une affectation.
           Testez votre commande en vrai s'il vous plais.""")

require_dollar = require("$",
                         """Pour changer le contenu de la variable
                         <tt>PATH</tt>
                         il est nécessaire d'accéder à l'ancien contenu
                         hors, je ne vois pas le <tt>$</tt> qui permet
                         de le faire.""")

add(name="intro",
    required=["sh:affiche paramètre"],
    question="""Donnez la ligne de commande permettant d'afficher le
    contenu de la variable d'environnement PATH sur la
    sortie standard.""",
    tests=(
    shell_good(("echo $PATH", 'echo "$PATH"')),
    shell_bad("set", "Le contenu de PATH, pas celle des autres."),
    shell_reject("cat", "<tt>cat</tt> sert à afficher le contenu de fichiers"),
    shell_require("PATH", "On est <tt>PATH</tt>&nbsp;?"),
    shell_require("echo", "On utilise <tt>echo</tt> pour afficher."),
    require_dollar,
    shell_display,
    ),
    )

add(name="affectation",
    question="""Quelle commande permet
    de mettre la chaine de caractère <tt>toto</tt> dans la
    variable <tt>A</tt> sans l'exporter.""",
    tests=(
    expect('A'),
    expect('toto'),
    shell_good("A=toto"),
    shell_bad("toto=A",
              """Vous venez de mettre la valeur <tt>A</tt>
              dans la variable <tt>toto</tt>"""),
    require("=",
            "Comment faites-vous une affectation sans signe <tt>=</tt> ?"),
    require("A",
            "Je ne vois pas le nom de la variable !"),
    reject_space,
    reject("$",
           """On ne veut le contenu d'aucune variable,
           pourquoi y-a-t-il un <tt>$</tt> dans votre
           ligne de commande&nbsp;?"""),
    reject('export', "On vous a dit de ne pas l'exporter"),
    reject('set', """La commande <em>builtin</em> ne permet de pas
    d'affecter des variables.
    <em>Ne confondez pas le <tt>Bourne shell</tt> avec le <tt>C shell</tt></em>
    """),
    shell_display,
    ),
    )

add(name="concatenation",
    question="""Quelle commande permet
    d'ajouter '<tt>:.</tt>' (deux points suivi de point) à la fin de la variable <tt>PATH</tt>""",
    tests=(
    shell_good(("PATH=$PATH:.", 'PATH="$PATH:."')),
    expect('PATH'),
    Bad(Comment(NumberOfIs(':', 2),
                """Pourquoi on trouve 2 fois le symbole ':' dans votre
                   réponse ?""")),
    require(":.",
            "Ou est le '<tt>:.</tt>' que je vous demande d'ajouter&nbsp;?"),
    require("=",
            """Pour changer le contenu d'une variable, on fait une affectation
            mais je ne vois pas de <tt>=</tt> dans votre commande"""),
    reject("export", "On ne vous a pas demandé d'exporter la variable"),
    require_dollar,
    reject_space,
    reject_startswith('$', """Vous avez déjà fait une affectation
    (regardez les prérequis).
    Vous voyez bien qu'à gauche du signe égal on met le nom
    de la variable et non son contenu."""),
    reject('+', """Remarque : <tt>echo a + b</tt> affiche <tt>a + b</tt>
    et non <tt>ab</tt>.
    En effet l'opération concaténation n'existe pas, il suffit
    d'écrire les deux chaines l'une derrière l'autre"""),
    shell_display,
    ),
    )

add(name="lire ligne",
    required=["intro", "sh:redirection entrée"],
    question="""Quelle commande <em>builtin</em> du shell permet
    de lire la première ligne de <tt>/etc/passwd</tt>
    et de la stocker dans la variable <tt>A</tt>""",
    tests=(
    shell_good("read A </etc/passwd"),
    shell_good(("A=$(head -1 /etc/passwd)",
                "A=$(head -n1 /etc/passwd)",
                ),
               "La réponse attendue était <tt>read A &lt;/etc/passwd</tt>"),
    reject("$", """On a pas besoin de '$' dans la réponse car on regarde
           pas le contenu des variables."""),
    reject(("head",'='),
           """Il y a des réponses qui utilisent <tt>head</tt>
           ou l'affectation avec <tt>=</tt>
           mais elles sont plus compliquée que la réponse
           attendue.
           <p>
           En effet, la commande (<em>builtin</em>)
           permettant de lire une ligne de l'entrée
           standard pour la mettre dans une variable
           prend la première ligne qu'elle trouve.
           """),
    require("read",
            """La commande <em>builtin</em> pour lire l'entrée
            standard et la mettre dans une fichier est <tt>read</tt>"""),
    reject(">",
           "Vous venez de vider le fichier au lieu de lire son contenu"),
    require("/etc/passwd",
            "Ou est la référence au fichier dans lequel on doit lire&nbsp;?"),
    require("<",
            """La commande <tt>read</tt> lit son entrée standard,
            il faut donc la rediriger pour que la lecture se
            fasse dans le fichier <tt>/etc/passwd</tt>"""),
    shell_reject("<fildes><direction>&lt;</direction><where><argument>A</argument>",
                 """Vous avez redirigé l'entrée standard pour lire
                 le contenu du fichier nommé <tt>a</tt>"""),
    require('A', "Je ne vois pas le nom de la variable"),
    shell_reject('<fildes><direction>&lt;</direction><where><argument>read</argument>',
                 """L'entrée standard est un fichier nommé <tt>read</tt>
                 au lieu de <tt>/etc/passwd</tt>"""),
    shell_display,
    ),
    )

add(name="lire mots",
    required=["lire ligne"],
    question="""Si vous tapez&nbsp;:
    <pre>echo Je suis une phrase &gt;xxx
read A B C &lt;xxx
</pre>
Que contiennent <tt>A</tt>, <tt>B</tt> et <tt>C</tt>&nbsp;?
""",
    nr_lines=3,
    default_answer="""A=
B=
C=""",
    tests=(
    good("A=Je\nB=suis\nC=unephrase",
         replace=((' ',''),('\n\n', '\n'),('"',''),("'",''))),
    require("Je", "Je ne vois pas le mot <tt>Je</tt>"),
    require('phrase',
            """S'il vous plais, essayez la commande pour voir ce qu'elle
            fait réellement plutôt que de répondre au hasard."""),
    ),
    )

    
add(name="toutes",
    question="""Quelle commande permet d'afficher les noms et contenu
    de toutes les variables manipulées par le shell&nbsp;?""",
    tests=(
    good("set"),
    bad("env",
        """Cette commande n'affiche que les variables de l'environnement,
        pas celles du shell"""),
    bad("export", "Cela n'affiche que les variables exportées"),
    bad('cat', "Cela affiche le contenu de fichiers"),
    Reject("@", """$@ représente tous les paramètres d'un script
    shell, pas toutes les variables"""),
    ),
    indices=("""Cette commande est listée quand vous tapez 'help'
    car c'est une commande <em>builtin</em>""",
             "C'est une commande de 3 lettres",
             """Cette commande sert à spécifier des options
             de fonctionnement pour le shell.
             C'est en l'utilisant sans paramètres
             qu'elle affichera la liste des variables.""",
             ),
    )



