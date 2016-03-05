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

from .check import *
from QUENLIG import configuration
import math

add(name="intro",
    question="to be done",
    tests = (Good(Contain('')),),
    )

Host.default_nr_interfaces = 3

postes = postes[0:4]

network = Network(configuration.questions)

routeur1 = Cisco('routeur1')
routeur2 = Cisco('routeur2')
routeur3 = Cisco('routeur3')
routeur4 = Cisco('routeur4')
routeur5 = Cisco('routeur5')
r16 = Cisco('r16')
r17 = Cisco('r17')

switchA = Switch('A')
switchB = Switch('B')
switchC = Switch('C')
switchD = Switch('D')

network.append([routeur1, routeur2, routeur3, routeur4, routeur5,
                r16, r17,
                switchA, switchB, switchC, switchD] )

EthLink.dot_style = "solid"

length = 1

prefix = ''
prefix = '10.'


EthLink(24, Port(routeur1, prefix + "100.110.2"),
        Port(r16, prefix + "100.110.1"), length=length)
EthLink(24, Port(routeur1, prefix + "100.120.2"),
        Port(routeur3, prefix + "100.120.1", key='E1'), length=length)
EthLink(24, Port(routeur1, prefix + "100.140.2"),
        Port(routeur5, prefix + "100.140.1", key='E1'), length=length)

EthLink(24, Port(routeur2, prefix + "100.130.2"),
        Port(r16, prefix + "100.130.1", key='E3'), length=length)
EthLink(24, Port(routeur2, prefix + "100.160.2"),
        Port(routeur5, prefix + "100.160.1", key='E2'), length=length)
EthLink(24, Port(routeur2, prefix + "100.200.1"),
        Port(routeur4, prefix + "100.200.2"), length=length)

EthLink(24, Port(routeur3, prefix + "50.50.1"),
        Port(switchB), length=length)
EthLink(24, Port(routeur3, prefix + "100.150.1"),
        Port(routeur5, prefix + "100.150.2"), length=length)

EthLink(24, Port(routeur4, prefix + "100.180.2"),
        Port(r16, prefix + "100.180.1", key='E2'), length=length)
EthLink(24, Port(routeur4, prefix + "10.10.1"),
        Port(switchA), length=length)
EthLink(24, Port(routeur4, prefix + "100.190.2"),
        Port(r17, prefix + "100.190.1", key='E2'), length=length)

EthLink(24, Port(routeur5, prefix + "100.170.1"),
        Port(r17, prefix + "100.170.2", key='E1'), length=length)

EthLink(24, Port(r16, prefix + "20.20.1"),
        Port(switchC), length=length)

EthLink(24, Port(r17, prefix + "90.90.1"),
        Port(switchD), length=length)

# Link.dot_option = ",color=magenta"

from QUENLIG import statistics
old = statistics.graph_dot

def graph_dot():
    old()

    network.dot("plan_circo",
                start = 4,
                network_nodes = False,
                label_distance = 3,
                table = False,
                showip = True,
                legend = False,
                dot_command = "circo",
                )
    network.dot("plan_neato",
                start = 1,
                network_nodes = False,
                label_distance = 1.4,
                table = False,
                showip = True,
                legend = False,
                dot_command = "neato",
                )
    network.dot("plan_dot",
                start = 4,
                network_nodes = False,
                label_distance = 2,
                table = False,
                showip = True,
                legend = False,
                dot_command = "dot",
                )
statistics.graph_dot = graph_dot
