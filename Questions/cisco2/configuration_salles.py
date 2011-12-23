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
import math


en_mode_normal = "Mettez-vous en mode utilisateur."
en_mode_root   = "Mettez-vous en mode privilégié."
en_mode_config = "Mettez-vous en mode configuration." # Term
en_mode_serial = "Mettez-vous en mode configuration de liaison série."
en_mode_eth    = "Mettez-vous en mode configuration de liaison ethernet."
en_mode_router = "Mettez-vous en mode configuration du routage."


Host.default_nr_interfaces = 3

if nombre_de_postes % 1:
    nombre_de_postes += 1

postes = postes[0:nombre_de_postes]

network = Network(configuration.questions, display_eth1 = True)


hosts = [Host(nom, ip=ip,
                    pos=(1000+1500*math.cos(i*math.pi/len(postes)),
                         1000+1500*math.sin(i*math.pi/len(postes))
                         )
              ) for i, (ip, nom, cisco) in enumerate(postes)]
ciscos = [cisco('R' + nom,
                    pos=(1000+1000*math.cos(i*math.pi/len(postes)),
                         1000+1000*math.sin(i*math.pi/len(postes))
                         )
                    )
          for i, (ip, nom, cisco) in enumerate(postes)  ]
switches = [Switch('S' + nom) for ip, nom, cisco in postes[1::2]]

network.append(hosts + ciscos + switches)


for i, (h, cisco) in enumerate(zip(hosts, ciscos)):
    ConsoleLink(port=Port(h), remote_port=Port(cisco))
    EthLink(24,
            Port(h, "192.168.%d.%d" % (i/2, 1 + 2*i)),
            Port(switches[i/2]),
            )
    EthLink(24,
            Port(cisco, "192.168.%d.%d" % (i/2, 1 + 2*i+1)),
            Port(switches[i/2]),
            )
    if i & 1:
        SerialLink(30,
                   Port(cisco, "192.168.128.%d" % (1+4*i),type="DCE"),
                   Port(ciscos[(i+1)%len(ciscos)], "192.168.128.%d" % (2+4*i)),
                   )
    else:
        if len(postes) == 6:
            d = 3
        else:
            d = 5
        
        SerialLink(30,
                   Port(cisco, "192.168.128.%d" % (1+4*i),type="DCE"),
                   Port(ciscos[(i+d)%len(ciscos)], "192.168.128.%d" % (2+4*i)),
                   weight=0.,
                   length=2,
                   )

for i, h in enumerate(hosts):
    if i & 1:
        EthLink(30,
                Port(h                      , "192.168.200.%d" % (4*i+1)),
                Port(hosts[(i+1)%len(hosts)], "192.168.200.%d" % (4*i+2)),
                )

import statistics
old = statistics.graph_dot

def graph_dot():
    old()
    network.dot("plan", start=13,network_nodes=False, label_distance=1.1)

statistics.graph_dot = graph_dot

