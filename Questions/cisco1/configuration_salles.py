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

from check import *
import configuration
import os
import sys

# Le nombre de postes permet de calculer la topologie
# du réseau pour qu'elle soit adaptée à la répartition
# de la salle en ilot de 4 machines.


en_mode_normal = "Mettez-vous en mode utilisateur."
en_mode_root   = "Mettez-vous en mode privilégié."
en_mode_config = "Mettez-vous en mode configuration (<tt>configure terminal</tt>)."
en_mode_serial = "Mettez-vous en mode configuration de liaison série."
en_mode_eth    = "Mettez-vous en mode configuration de liaison ethernet."
en_mode_router = "Mettez-vous en mode configuration du routage."


Host.default_nr_interfaces = 3

# Ordre important
ips = [ip for ip, nom, cisco in postes]

confs = (
    0,
    1,
    2,
    ( (0,1,2), ),
    ( (0,1,2,3), ),
    ( (0,1,2,3,4), ),
    ( (0,1,2), (4,5,6), ),
    ( (0,1,2,3), (4,5,6), ),
    ( (0,1,2,3), (4,5,6,7), ),
    ( (0,1,2), (4,5,6), (8,9,10) ),
    ( (0,1,2,3), (4,5,6), (8,9,10) ),
    ( (0,1,2,3), (4,5,6,7), (8,9,10) ),
    ( (0,1,2,3), (4,5,6,7), (8,9,10,11) ),
    ( (0,1,2,3), (4,5,6), (8,9,10), (12,13,14) ),
    ( (0,1,2,3), (4,5,6,7), (8,9,10), (12,13,14) ),
    ( (0,1,2,3), (4,5,6,7), (8,9,10,11), (12,13,14) ),
    ( (0,1,2,3), (4,5,6,7), (8,9,10,11), (12,13,14,15) ),
    )

network = Network(os.path.join(configuration.root, configuration.questions))

hosts = [Host(nom, ip=ip) for ip,nom, cisco in postes]
ciscos = [cisco('R' + nom) for ip,nom,cisco in postes]

boucles = confs[nombre_de_postes]

paires = []
for i in boucles:
    for j in i:
        paires.append((hosts[j], ciscos[j]))
        network.append((hosts[j], ciscos[j]))

for i, (h, cisco) in enumerate(paires):
    ConsoleLink(port=Port(h), remote_port=Port(cisco))
    EthLink(24,
            Port(h, "192.168.%d.2" % (i+128)),
            Port(cisco, "192.168.%d.1" % (i+128)),
            )


for ib, boucle in enumerate(boucles):
    for ic, cisco in enumerate(boucle):
        icn = (ic + 1) % len(boucle)
        SerialLink(30,
                   Port(ciscos[cisco], "192.168.%d.%d" % (cisco, 1), "DCE"),
                   Port(ciscos[boucle[icn]], "192.168.%d.%d" % (cisco, 2),
                        key="S1"),
                   )

for h in hosts:
    if h.name in ('A3', 'E3', 'I3', 'M3'):
        legend = h

import statistics

old = statistics.graph_dot

def graph_dot():
    old()
    i = 0
    for h in hosts:
        if h.name in ('A3', 'E3', 'I3', 'M3'):
            i += 1
            network.dot("plan%d" % i, start=40, network_nodes=True,from_node=h,
                        legend = h == legend)

statistics.graph_dot = graph_dot
