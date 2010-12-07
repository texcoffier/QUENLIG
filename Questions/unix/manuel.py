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
    question="""Quelle est la commande standard sous UNIX pour
    pouvoir accéder au manuel d'utilisation&nbsp;?""",
    tests=(
    good("man"),
    bad("help",
        "C'est la page d'aide sur le shell, pas sur les commandes Unix"),
    reject_startswith('-', "On veut un nom de commande, pas une option"),
    bad("MAN", "Attention à la casse (majuscule / minuscule)"),
    bad("info", "Cette commande n'est pas standard, c'est une commande GNU"),
    ),
    )

add(name="commande",
    required=["intro", "paginer:navigation"],
    question="""Que tapez-vous pour avoir le manuel
    de la commande <tt>man</tt>&nbsp;?""",
    tests=(
    reject('info', "<tt>info</tt> n'est pas une commande standard"),
    shell_good("man man"),
    shell_good("man 1 man", "<tt>man man</tt> est plus court"),
    shell_bad(("man --help", "man -h"),
              "Ce n'est pas un manuel, seulement une page d'aide"),
    shell_bad("man",
              "Vous n'avez pas essayé, cela retourne un message d'erreur"),
    ),
    )

add(name="section",
    required=["commande"],
    before="""Quand vous affichez une page de manuel,
    le nom de la page ainsi que la section du manuel ou
    a été trouvée cette page sont affichés en haut.""",
    question="Dans quelle numéro de section du manuel trouve-t-on <tt>fstab</tt>&nbsp;?",
    tests=(
    good("5"),
    require_int(),
    ),
    )

man_is_required = require("man", "On doit utiliser la commande <tt>man</tt>")

add(name="chercher",
    required=["commande", "section"],
    before="""Avoir des informations sur une commande ou le format
    d'un fichier est facile quand on connait son nom.
    Mais comment trouver ce nom&nbsp;?""",
    question="""Que tapez-vous pour avoir la liste des
    commandes qui ont le mot <tt>image</tt> dans leur description&nbsp;?""",
    tests=(
    shell_good("man -k image"),
    shell_bad("man image", """Vous êtes en train de demander d'afficher
    le manuel de la commande qui s'appelle <tt>image</tt>."""),
    shell_bad('apropos image',
              """Votre commande fonctionne mais elle n'a pas été vue en cours.
              À la place, utilisez la commande <tt>man</tt> avec
              la bonne option."""),
    man_is_required,
    require("-",
            """Vous devez utiliser une option de la commande <tt>man</tt>"""),
    require("-k",
            """Vous n'avez pas trouvé la bonne option.
            Mot-clef en anglais ce dit <em>keyword</em>"""),
    expect('image'),
    shell_display,
    ),
    bad_answer="""Lisez le manuel de la commande <tt>man</tt> pour avoir
    la réponse""",
    )

add(name="voir aussi",
    required=["commande"],
    before="""Dans la documentation, une des choses les plus importantes
    mais la moins visible est la liste des autres documentations
    qui sont liées à celle-ci.
    En effet cette liste est à la fin de la documentation.
    C'est dans la section <b>SEE ALSO</b> du manuel.
    """,
    question="Citez l'une des <b>commandes</b> liées à <tt>man</tt>",
    tests=(
    good_if_contains(("manpath", "apropos", "whatis", "less", "nroff", "troff",
          "groff", "zsoelim", "mandb", "catman", "less", "setlocale",
          "ascii", "latin1")),
    reject((" ", "-"),
           """On veut un nom de commande, pas une ligne de commande"""),
    ),
    bad_answer = "Essayer un autre nom de commande, vous n'avez peut-être pas la même version du manuel que moi",
    indices=("Faites <tt>man man</tt>",)
    )

add(name="section commande",
    required=["section"],
    before="""Quand on cherche la documentation de <tt>passwd</tt> cela peut
    être celle du fichier <tt>/etc/passwd</tt> qui contient
    la description des utilisateur ou bien celle
    de la commande <tt>/usr/bin/passwd</tt> qui permet de changer
    son mot de passe""",
    question="""Quelle ligne de commande utilisant <tt>man</tt>
    permet d'avoir la description
    du format du fichier <tt>/etc/passwd</tt>&nbsp;?""",
    tests=(
    shell_bad(("man /etc/passwd", "man 5 /etc/passwd"),
        """Ne voyez-vous pas que ce qui est affiché n'est pas une page
        du manuel mais le contenu du fichier&nbsp;?"""),
    reject("/etc/passwd",
           """Quand vous demandez le manuel sur la commande
           <tt>ls</tt> vous ne tapez pas <tt>man /bin/ls</tt>"""),
    expect('man'),
    require("passwd",
            """Comment la commande <tt>man</tt> va deviner
            que vous voulez des informations sur
            <tt>passwd</tt>. Par télépathie&nbsp;?"""),
    require("5",
            """Vous n'avez pas indiqué la bonne section.
            Vous devez chercher dans la section contenant
            la description des formats de fichier"""),
    shell_good("man 5 passwd"),
    shell_good("man -S 5 passwd", "Le <tt>-S</tt> est inutile"),
    shell_good("man -s 5 passwd", "Le <tt>-s</tt> est inutile"),
    shell_display,
    ),
    )
