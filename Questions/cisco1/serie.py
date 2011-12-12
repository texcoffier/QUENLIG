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

from questions import *
from check import *
from configuration_salles import *

rien_de_branche = """Il ne doit pas y avoir de cable série (hors console)
    branchés sur le routeur CISCO"""


add(name="affiche",
    required=["cli:show liste", "hard:show"],
    question="""Quelle commande tapez-vous pour avoir les informations
    sur les <b>interfaces</b> réseaux de votre routeur&nbsp;?
    <p>
    Attention, pour des raisons mystérieuses <tt>show i?</tt>
    n'affiche pas toujours la commande alors qu'elle devrait.
    """,
    tests=(
    good("show interfaces"),
    reject("show ip interface",
           "Cela n'affiche que les interfaces configurées en IP"),
    bad(("show int", "show interface"),
        "Je refuse TOUTES les abbréviations, même d'une lettre."),
    ),
    indices = ("""C'est <tt>show interfaces</tt>""", ),
    )


add(name="premiere",
    required=["affiche"],
    question="""Quelle commande tapez-vous pour avoir les informations
    sur le premier port série de votre routeur&nbsp;?""",
    tests=(
    bad(("show int {C0.remote_port.host.S0.port.name}",
          "show int {C0.remote_port.host.S0.port.name}"
          ),
         "Je refuse TOUTES les abbréviations.",
         parse_strings=host),
    require('erial', """Je ne vois pas de référence à une interface série
    dans votre réponse"""),
    good("show interfaces {C0.remote_port.host.S0.port.name}",
         parse_strings=host, uppercase=True),
    good("show interfaces {C0.remote_port.host.S0.port.name_without_space}",
         parse_strings=host, uppercase=True),
    good("show interface {C0.remote_port.host.S0.port.name}",
         parse_strings=host, uppercase=True),
    good("show interface {C0.remote_port.host.S0.port.name_without_space}",
         parse_strings=host, uppercase=True),
    reject('1', 'Le <b>premier</b> port, pas le numéro <tt>1</tt>'),
    ),
    )

add(name="protocole",
    required=["affiche"],
    before=rien_de_branche,
    question="""Quelle est l'encapsulation utilisée
    sur les liaisons séries&nbsp;?""",
    tests=(
    good("HDLC", uppercase=True),
    bad("ARPA", "Vous avez regardé l'encapsulation ethernet, pas série",
        uppercase=True),
    ),
    )

# add(name="active",
#     required=["affiche"],
#     before=rien_de_branche,
#     question="""Qu'est-ce que le routeur CISCO vous affiche
#     pour indiquer qu'il n'y a pas de cable branché&nbsp;?""",
#     tests=(
#     good("line protocol is down"),
#     ),
#     )
# 
add(name="paquet",
    required=["affiche"],
    before=rien_de_branche,
    question="""Quelle est la taille maximale en octet des paquets
    passant sur la liaison série&nbsp;?""",
    tests=(
    good("1500"),
    reject("byte", """En vous demande la taille en octet,
    c'est pas la peine d'écrire 'byte' dans la réponse"""),
    reject('187',
           """Un informaticien se doit de parler anglais.
           Un <em>byte</em> c'est un octet."""),
    bad('MTU', "C'est ça, et il vaut combien&nbsp;?"),
    ),
    )

add(name="fiabilité",
    required=["affiche"],
    before=rien_de_branche,
    question="""Quelle est la fiabilité de la première ligne série&nbsp;?""",
    tests=(
    good(("255", "255/255")),
    good(("254","253","252","251","250"),
         """Normalement cela devrait être 255 car vous n'avez aucune
         perte de paquet puisque rien n'est branché""",
         replace=(('/255',''),)
         ),
    bad("100%", "C'est juste, mais ce n'est pas ce qui est écrit"),
    ),
    )

add(name="configure",
    required=["doc:intro", "affiche", "premiere", "terminal:quitter"],
    before=en_mode_config,
    question="""Que tapez-vous pour passer dans le mode de configuration
    de la première interface série&nbsp;?""",
    tests=(
    reject("enable", "On considère que le <tt>enable</tt> est déjà fait"),
    reject("terminal", "On considère que l'on est déjà en mode configuration"),
    reject(".", """Enlevez le point (.) et ce qui suit dans le nom
    de l'interface."""),
    require("interface",
            """Pour passer en mode de configuration d'une interface,
            on utilise la commande <tt>int......</tt>"""),
    reject("interfaces","Vous configurez UNE interface, alors pourquoi 's' ?"),
    good("interface {C0.remote_port.host.S0.port.name}", parse_strings=host,
         uppercase=True),
    good("interface {C0.remote_port.host.S0.port.name_without_space}", parse_strings=host,
         uppercase=True),
    reject('show', "On ne veut pas afficher, on veut modifier"),
    expect('serial'),
    ),
    )

add(name="prompt",
    required=["configure"],
    before=en_mode_serial,
    question="Quel-est le <em>prompt</em>&nbsp;?",
    tests = (
    good("Router(config-if)#"),
    expect('#'),
    expect('Router'),
    expect('(config-if)'),
    ),
    highlight = True,
    )












