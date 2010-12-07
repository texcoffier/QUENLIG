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

add(name="premier",
    required=["serie:prompt"],
    question="""Quelle commande tapez-vous pour avoir les informations
    sur le premier port éthernet de votre routeur&nbsp;?""",
    tests=(
    require("show", "Pour voir, on utilise la commande <tt>show</tt>"),
    good("show interfaces {C0.remote_port.host.E0.port.name}", parse_strings=host, uppercase=True),
    good("show interfaces {C0.remote_port.host.E0.port.name_without_space}", parse_strings=host, uppercase=True),
    good("show interface {C0.remote_port.host.E0.port.name}", parse_strings=host, uppercase=True),
    good("show interface {C0.remote_port.host.E0.port.name_without_space}", parse_strings=host, uppercase=True),
    ),
    )

add(name="protocole",
    required=["premier"],
    question="""Quelle est l'encapsulation utilisée
    sur les liaisons ethernet&nbsp;?""",
    tests=(
    good("ARPA", uppercase=True),
    bad("HDLC", "Non, ça c'est l'encapsulation de l'interface série",
        uppercase=True),
    ),
    )

# add(name="active",
#     required=["premier"],
#     question="""Qu'est-ce que le routeur CISCO vous affiche
#     pour indiquer qu'il n'y a pas de cable branché&nbsp;?""",
#     tests=(
#     good("line protocol is down"),
#     ),
#     )
# 
add(name="paquet",
    required=["premier"],
    question="""Quelle est la taille maximale en octet des paquets
    passant sur la liaison ethernet&nbsp;?""",
    tests=(
    good("1500"),
    ),
    )

add(name="fiabilité",
    required=["premier"],
    question="""Quelle est la fiabilité du premier port ethernet&nbsp;?""",
    tests=(
    good("255"),
    good("254"),
    good("253"),
    good("252"),
    good("255/255"),
    good("254/255"),
    good("253/255"),
    good("252/255"),
    bad("100%", "C'est juste, mais ce n'est pas ce qui est écrit"),
    ),
    )

add(name="configure",
    required=["serie:configure"],
    before=en_mode_config,
    question="""Que tapez-vous pour passer dans le mode de configuration
    de la première interface ethernet&nbsp;?""",
    tests=(
    reject("enable", "On considère que le <tt>enable</tt> est déjà fait"),
    reject("terminal", "On considère que l'on est déjà en mode configuration"),
    reject(".", """Enlevez le point (.) et ce qui suit dans le nom
    de l'interface."""),
    reject("serial", "Ethernet, pas série..."),
    good("interface {C0.remote_port.host.E0.port.name}", parse_strings=host, uppercase=True),
    good("interface {C0.remote_port.host.E0.port.name_without_space}", parse_strings=host, uppercase=True),
    ),
    )













