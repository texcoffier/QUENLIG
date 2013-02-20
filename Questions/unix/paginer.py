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

more_required = require("more", "On utilise la commande <tt>more</tt>")

add(name="intro",
    required=["sh:console"],
    question="""Quelle commande standard permet d'afficher sur la sortie
    standard (l'écran) le contenu d'un ou plusieurs fichiers,
    page par page&nbsp;?
    <p>
    Elle permet aussi de faire des recherches dans le texte
    qui est en train d'être affiché.""",
    tests=(
    good("more"),
    reject(' ', """On veut simplement le nom de la commande,
    aucune option n'est nécessaire"""),
    reject("cat", "La commande <tt>cat</tt> affiche tout d'un seul coup"),
    bad("less", "Cette commande n'est pas standard, c'est une commande GNU"),
    bad("pg", "Cette commande est obsolette, il ne faut plus l'utiliser"),
    bad("echo", "Cela affiche ses paramètres, cela ne manipule pas les fichiers"),
    bad(("find", "ls"),
        "On veut voir le contenu des fichiers, pas leur nom"),
    bad(("vi","emacs"),
        "C'est pour modifier les fichiers, pas pour les regarder"),
    bad('grep', "C'est pour faire des recherches, pas pour afficher"),
    ),
    indices=(
    "C'est un mot anglais qui veut dire 'plus' mais pas avec le sens addition",
    ),
    )

add(name="simple",
    required=["intro"],
    question="""Que tapez-vous pour voir le contenu du
    fichier <tt>/etc/group</tt> page par page&nbsp;?""",
    tests=(
    shell_bad("more </etc/group", "Il y a plus simple (sans redirection)"),
    shell_bad("cat /etc/group | more",
              """Il y a une solution beaucoup plus simple qui
              n'utilise pas de <em>pipe</em> ni de commande
              suplémentaire"""),
    shell_good("more /etc/group"),
    reject("cat", """C'est <tt>more</tt> qui affiche page par page,
    c'est pas <tt>cat</tt>"""),
    bad("more/etc/group",
        """Le shell va essayer d'exécuter une commande
        nommée <tt>group</tt> dans le répertoire <tt>more/etc</tt>
        à l'intérieur du répertoire courant.
        Il faut un séparateur entre le nom de la commande et ses paramètres.
        """),
    require("/etc/group", "Il faut indiquer le nom du fichier à afficher"),
    more_required,
    shell_display,
    ),
    )
    
add(name="navigation",
    required=["simple"],
    before="""Une fois la commande <tt>more</tt> lancée l'invite de commande
    ne revient pas car cette commande est interactive.
    Vous pouvez utilisez les touches page précédente/suivante
    pour vous promener dans le fichier.
    Comme pour beaucoup de commande interactive,
    on peut lui demander de l'aide en tapant 'h' ou '?'""",
    question="""Comment terminer cette commande sans taper <tt>^C</tt>&nbsp;?
    Indiquez simplement le caractère à taper.
    """,
    tests=(
    good('q'),
    good('Q',
         """Il est plus simple de taper une minuscule qu'une majuscule.
         Il est donc recommendé de taper <tt>q</tt>"""),
    bad(':q',
        "C'est pour <tt>vi</tt>, relisez la page d'aide de <tt>more</tt>"),
    reject(('^Z', '^z'),
           """Cela n'arrête pas la commande, elle tourne toujours
           en arrière plan (mais suspendue).
           Il faut taper <tt>fg</tt> pour la remettre au premier plan."""),
    answer_length_is(1, """Votre réponse doit être sur UN SEUL caractère
    comme c'est demandé dans la question."""),
    ),
    )

add(name="multiple",
    required=["simple", "navigation"],
    before="""Dans le répertoire courant il y a 2 fichiers,
    l'un est nommé <tt>A</tt> et l'autre <tt>B</tt>.""",
    question="""Que tapez-vous pour voir le contenu des 2 fichiers
    page par page&nbsp;?""",
    tests=(
    expect('more'),
    reject('cat', "On n'utilise pas la commande <tt>cat</tt>"),
    reject(("a", "b"), "Majuscule et minuscules sont différentes"),
    reject("./",
           """On a pas besoin de mettre <tt>./</tt> devant
           le nom d'un fichier pour indiquer qu'il est
           dans le répertoire courrant"""),
    reject((';','&'), "On veut lancer qu'une seule fois la commande."),
    require(("A", "B"),
            """Comment la commande sait de quels fichiers
            vous parlez&nbsp;?"""),
    shell_good("more A B"),
    require('more', """La seule commande dont vous ayez besoin est indiquée
    dans la liste des questions auxquelles vous avez déjà répondu."""),
    shell_display,
    ),
    )
    



