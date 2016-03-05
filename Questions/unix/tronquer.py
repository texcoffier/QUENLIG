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

require_passwd = require('/etc/passwd',
                         '''Je ne vois pas le fichier <tt>passwd</tt>
                         dans votre ligne de commande''')

require_tail = require("tail", "On utilise <tt>tail</tt> bien sur")

add(name="intro",
    required=["manuel:chercher"],
    question="""Quelle commande permet de n'afficher que la fin
    d'un fichier&nbsp;?""",
    tests=(
    good("tail"),
    bad('last', """Cette commande affiche la liste des dernières personnes
    à s'être connectées"""),
    bad('$', """Ça c'est le caractère représentant la fin de ligne
    dans les expressions régulières"""),
    reject( (" ", "-"), "Que le nom de la commande, pas d'options"),
    ),
    indices=("C'est la 'queue' du fichier mais en anglais",
             "Essayez <tt>man -k last</tt>",
             ),
    )

add(name="simple",
    question="""Donnez une ligne de commande affichant les
    dernières lignes (sans spécifier le nombre)
    du fichier <tt>/etc/passwd</tt>""",
    tests=(
    reject( "-",
            "Il n'y a pas besoin d'options pour répondre à la question"),
    require_passwd,
    require_tail,
    shell_good(("tail /etc/passwd", "tail </etc/passwd")),
    shell_display,
    ),
    )

add(name="dernière",
    question="""Donnez une ligne de commande affichant la dernière ligne
    du fichier <tt>/etc/passwd</tt>""",
    tests=(
    require_tail,
    require_passwd,
    shell_good(("tail -1 /etc/passwd",
                "tail -1 </etc/passwd",
                "tail -n1 /etc/passwd",
                "tail -n1 </etc/passwd",
                )),
    shell_bad("tail /etc/passwd -n1",
              """Il est possible que cette commande fonctionne.
              Mais si c'est le cas c'est un bug de la commande.
              En effet les options sont toujours avant
              les noms des fichiers"""),
    shell_bad(("tail -n /etc/passwd",
               "tail 1 /etc/passwd",
               ),
              "Vous n'avez même pas essayé la commande"),
    shell_bad("tail /etc/passwd",
              "Cela affiche les dernières, pas LA dernière."),
    require('1', """Je ne vois pas le 1 indiquant que vous voulez seulement
    afficher une seule ligne"""),
    reject('f', "Vous n'avez pas besoin de l'option <tt>f</tt>"),
    shell_display,
    ),
    )

add(name="moitié",
    required=["dernière", "compte:ligne", "calculer:division",
              "sh:remplacement"],
    question="""Afficher la deuxième moitié du fichier
    <tt>/etc/passwd</tt> (c'est-à-dire du milieu jusqu'à la fin).
    <p>
    Votre commande ne devra pas utiliser de variable shell.""",
    tests=(
    reject("tail -l",
           "N'auriez-vous pas confondu le chiffre 1 et la lettre l ?"),
    reject('|', "Pas besoin de pipeline pour cette question"),
    reject('=', "Pas besoin d'affection et de variables pour cette question"),
    reject('"', "Pas besoin de guillemets pour cette question"),
    require_tail,
    require_passwd,
    require('wc', """Vous devez utiliser <tt>wc</tt> pour trouver
    le nombre de lignes contenus dans le fichier"""),
    require('expr', """Vous devez utiliser <tt>expr</tt> pour
    trouver le milieu en nombre de lignes"""),
    require(('/', '2'), "Ou est la division par 2 pour trouver le milieu ?"),
    require('/ 2', "Il manque un espace pour la division par 2"),
    shell_good("tail -$(expr $(wc -l </etc/passwd) / 2) /etc/passwd"),
    shell_good("tail -$(expr $(wc -l </etc/passwd) / 2) </etc/passwd"),
    shell_good("tail -n $(expr $(wc -l </etc/passwd) / 2) </etc/passwd"),
    shell_good("tail -n $(expr $(wc -l </etc/passwd) / 2) /etc/passwd"),
    shell_good("tail -n$(expr $(wc -l </etc/passwd) / 2) </etc/passwd"),
    shell_good("tail -n$(expr $(wc -l </etc/passwd) / 2) /etc/passwd"),
    shell_require('-l', """Où est l'option de <tt>wc</tt> indiquant
    que l'on veut compter les lignes"""),
    shell_require('fildes><direction>&lt;</direction><where><argument>/etc/passwd</argument></where></fildes>',
                  """La commande <tt>wc</tt> doit lire sur l'entrée standard
                  sinon elle va afficher le nom du fichier et il y aura
                  une erreur dans l'évaluation de <tt>expr</tt>"""),
    number_of_is('/etc/passwd', 2,
                 """Le fichier <tt>/etc/passwd</tt> doit être lu deux fois.
                 Une fois pour compter le nombre de lignes et une
                 pour l'afficher. Donc son nom doit être présent
                 deux fois dans la commande."""),
    shell_display,
    ),
    )

    
