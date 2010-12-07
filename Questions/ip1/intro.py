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

Host.default_nr_interfaces = 3
Host("134.214.142.30", 'A', eth0="192.168.0.24/24")
Host("134.214.142.31", 'B', eth0="192.168.0.25/24")

        

add(name="votre poste",
    before="""Vous devez avoir sous les yeux le plan du réseau que
    vous allez tous configurer.""",
    question="Quelle est la lettre associée à votre poste sur le plan&nbsp;?",
    tests=(
    answer_length_is(1, "La réponse est UNE lettre"),
    good("{letter}", parse_strings=host, uppercase=True),
    ),
    )

add(name="interfaces",
    required=["votre poste"],
    before = """La commande <tt>dmesg</tt> affiche les messages
    du noyau contenant notemment la liste des périphériques détectés.
    <p>
    Les péripériques ethernet, contiennent généralement <tt>eth</tt>
    dans leur nom.
    <p>
    Vous rappelez-vous du pipe et de la commande <tt>grep</tt>&nbsp;?
    """,
    question="""Votre machine dispose de combien
    de périphériques réseau&nbsp;?""",
    tests=(require_int(), HostInterfaces(),),
    good_answer = """Sur les machines en salle de TP :
    <ul>
    <li> <tt>eth0</tt> : La carte réseau sur la carte mère.
    <li> <tt>eth1</tt> : La carte réseau additionnelle.
    <li> <tt>eth2</tt> : Le convertisseur USB/Ethernet : NE PAS TOUCHER.
    </ul>""",
    )
    

add(name="ip eth0",
    required=["interfaces"],
    question="Quelle adresse IP devez-vous affecter à <tt>eth0</tt>&nbsp;?",
    tests=(
    require_ip(),
    good("{eth0ip}", parse_strings=host),
    ),
    )

