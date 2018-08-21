# -*- coding: latin-1 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2010 Thierry EXCOFFIER, Universite Claude Bernard
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
import random

add(name="ip",
#    required = [],
    required=["tp1_route:machine>routeur s1",
              "tp1_serie:routeur>local s1",],
    question = "Que veux dire IP&nbsp;?",
    tests = (
        Good(UpperCase(Contain('INTERNET') & Contain('PROTOCOL'))),
        ),
    )

add(name="adresses",
    required=["ip"],
    question = "Quel est le nom des adresses Ethernet&nbsp;?",
    tests = (
        Good(UpperCase(Contain('MAC'))),
        Bad(Comment(UpperCase(Contain('IP')),
                    "<b>ETHERNET</b> pas Internet !"))
        ),
    )

# XXX Accepte CSMA ?
add(name="protocol",
    required=["ip"],
    question = """Quel est l'acronyme du protocole bas niveau utilis� pour
    communiquer sur Ethernet (pour envoyer les paquets/trames en
    �vitant les collisions)&nbsp;?""",
    tests = (
        # Good(UpperCase(Contain('CSMA') & Contain('CD'))),
        Good(UpperCase(Contain('CSMA'))),
        Bad(Comment(UpperCase(Contain('HDLC')),
                    "C'est le protocole utilis�e pour la liaison s�rie.")),
        Bad(Comment(UpperCase(Contain('MAC')),
                    "C'est la mani�re de d�finir les adresses ethernet.")),
        Bad(Comment(UpperCase(Contain('IP')
                              | Contain('TCP')
                              | Contain('UDP')
                              ),
                    """La r�ponse est le protocole utilis� par IP
                    pour envoyer les trames.""")),
        Bad(Comment(Contain('802'),
                    "Pas le nom du standard, le nom du protocole")),
        ),
    )

add(name="longueur",
    required=["adresses"],
    question = "Une adresse MAC est d�finie sur combien d'octets&nbsp;?",
    tests = (
        Good(Int(6)),
        ),
    )

add(name="loop",
    required=["ip"],
    question = """Quelle adresse IP standard (la m�me partout)
    permettant de communiquer avec la machine locale&nbsp;?""",
    tests = (
        Good(Equal('127.0.0.1')),
        Bad(Comment(Equal('127.0.0.0'),
                    "C'est un adresse de r�seau, pas une adresse de machine")),
        ),
    )

add(name="mini",
    required=["ip"],
    question = """Quel est le <em>netmask</em> (IPV4) du plus petit r�seau
    (celui qui contient le moins d'adresse)
    qui puisse servir � quelque chose&nbsp;?""",
    tests = (
        Good(Equal('255.255.255.252')),
        Bad(Comment(Equal('255.255.255.254'),
                    """Ce r�seau contient 2 adresse IP et donc
                    une fois que l'on a enlev� l'adresse de r�seau
                    et l'adresse de <em>broadcast</em> on peut
                    mettre ZERO machines dans le r�seau.
                    Ce r�seau ne servira pas � grand chose..."""
                    )),
        Bad(Comment(Equal('255.255.255.255'),
                    """Ce r�seau contient ZERO adresse IP.
                    Comment allez-vous l'utiliser&nbsp;?""")),
        Bad(Comment(~Contain('.'), "Donnez la notation x.y.z.t")),
    ),
    )

def max_adresse():
    return [8*random.randrange(1,256//8) for dummy_i in range(3)] + [0]

def max_netmask():
    addr = max_adresse()
    for i in range(32):
        if addr[-1 - i//8] & (2**(i%8)):
            break
    
    return int_to_dot(int_to_netmask(32-i))

def int_to_dot(value):
    dot = []
    for dummy_i in range(4):
        dot.append( '%d' % (value & 255) )
        value //= 256
    dot.reverse()
    return '.'.join(str(i) for i in dot)

def int_to_netmask(i):
    j = 0
    for k in range(i):
        j += 2**(31-k)
    return j

def max_question():
    return "Quel est le <em>netmask</em> du plus grand r�seau r�alisable (on ne tient pas compte des classes) dont l'adresse est " + \
           '.'.join([str(i) for i in max_adresse()])

add(name="max",
    required=["ip"],
    question = max_question,
    tests = (
        Good(TestFunction(lambda answer, state:
                          (answer == max_netmask(), ''))),
        Bad(Comment(~Contain('.'), "Donnez la notation x.y.z.t")),
    ),
    )


def taille_adresse(state):
    if not state:
        return 0
    try:
        return state.taille_adresse
    except AttributeError:
        state.taille_adresse = random.randrange(4,28)
        return state.taille_adresse

def taille_taille(state):
    return 2**(32-taille_adresse(state)) - 2

def taille_question(state):
    return """Combien d'adresses de machine sont disponibles sur
    le r�seau dont le <em>netmask</em> est : """ + \
           int_to_dot(int_to_netmask(taille_adresse(state)))


add(name="taille",
    required=["ip"],
    question = taille_question,
    tests = (
        Good(TestFunction(lambda answer, state:
                          (answer == str(taille_taille(state)), ''))),
        Bad(Comment(TestFunction(lambda answer, state:
                                 (answer == str(taille_taille(state)+2), '')),
                    'Certaines adresses IP ne sont pas autoris�es...')),
        Bad(IntGT(0)),
    ),
    )

def sous_adresse(state):
    if not state:
        return (0, 0)
    try:
        return state.sous_adresse
    except AttributeError:
        state.sous_adresse = (random.randrange(4,20),
                              2**random.randrange(2,8))
        return state.sous_adresse

def sous_taille(state):
    netmask, nombre = sous_adresse(state)
    return 2**(32-netmask) - 2*nombre

def sous_question(state):
    netmask, nombre = sous_adresse(state)
    return """On d�coupe le r�seau d�fini par le <em>netmask</em> %s en %d
    sous r�seaux. Combien a-t-on d'adresse de machine disponible sur l'ensemble des r�seaux&nbsp;?""" % (
    int_to_dot(int_to_netmask(netmask)), nombre )

add(name="sous",
    required=["taille"],
    question = sous_question,
    tests = (
        Good(TestFunction(lambda answer, state:
                          (answer == str(sous_taille(state)), ''))),
        Bad(IntGT(0)),
    ),
    )

add(name="ping",
    before = "Vous devez utiliser <tt>wireshark</tt>",
    required=["ip"],
    question = """Quelle est la valeur en hexa du 13<sup>�me</sup> octet
    que <tt>wireshark</tt> r�cup�re sur le r�seaux lors d'un <tt>ping</tt>""",
    tests = (
        Good(Replace((('0x',''),('0X','')),
                     Equal('08') | Equal('8'))),
    ),
    )

add(name="255",
    required=["ip"],
    question = """Combien vaut le nombre d�cimal 255 en hexad�cimal&nbsp;?
    <p>N'utilisez pas un convertisseur, vous n'apprendrez rien.""",
    tests = (
        Good(UpperCase(Replace((('0X',''),),
                               Equal('FF')))),
    ),
    )

add(name="bigone",
    required=["ip"],
    question = """Quelle est l'adresse du r�seau � usage priv� dont
    le <em>netmask</em> est 255.0.0.0&nbsp;?""",
    tests = (
        Good(Equal('10.0.0.0') | Equal('10.0.0.0/8')),
        Bad(Comment(Start('127'),
                    """Ce r�seau est le <em>loopback</em>, il ne permet
                    pas de communiquer entre deux machines""")),
    ),
    )

add(name="smallone",
    required=["bigone"],
    question = """Quelle est l'adresse du <b>premier</b> r�seau � usage priv�
    dont le <em>netmask</em> est 255.255.255.0&nbsp;?""",
    tests = (
        Good(Equal('192.168.0.0')),
        Bad(Comment(Start('172'),
                    """Le <em>netmask</em> de <tt>172.16.0.0</tt> est
                    <tt>255.240.0.0</tt>""")),
        Bad(Comment(End('.1'),
                    """Il est impossible que le dernier bit d'une adresse
                       de r�seau soit � 1. Cela voudrait dire que ce r�seau
                       ne contient aucune machine.""")),
    ),
    )

add(name="find MAC",
    required=["adresses"],
    question="""Quel est le nom du protocole permettant d'obtenir l'adresse MAC
    � partir de l'adresse IP&nbsp;?""",
    tests = (
        Good(UpperCase(Equal('ARP'))),
    ),
    )

add(name="broadcast",
    required=["adresses"],
    question="""Quelle est l'adresse MAC de broadcast&nbsp;?""",
    tests = (
        Good(UpperCase(Replace(((':',''),('-',''),(' ',''),('.', '')),
                               Equal('FFFFFFFFFFFF')))),
        Bad(Comment(Equal('255.255.255.255'),
                    "Vous avez donn� une adresse IP, par ethernet")),
    ),
    )

add(name="switch",
    required=["mini"],
    question="Un <em>switch</em> filtre les paquets en fonction de leur...",
    tests = (
        Good(UpperCase(Contain('mac'))),
        Bad(Comment(UpperCase(Contain('IP')),
                    "Ce sont les routeurs qui regardent les adresses IP.")),
        Bad(Comment(UpperCase(Contain('DESTI')),
                    "Qu'est-ce qui d�fini la destination ?")),
    ),
    )

add(name="logique",
    required=["ip"],
    before="""Sur un m�me <em>switch</em> (sans VLAN) il y a des
    machines configur�es comme suit&nbsp;:
    <ul>
    <li> A: 192.168.0.1/24
    <li> B: 192.168.0.2/16 
    <li> C: 192.168.1.3/24
    </ul>
    Ces machines n'ont pas de table de routage ni de routeur par d�faut.
    """,
    question = """Qui peut envoyer un paquet � qui&nbsp;?
    <p>
    Indiquez dans votre r�ponse sous la forme&nbsp;: <tt>XY XZ ZX</tt>
    pour dire que X peut envoyer des paquets � Y,
    X peut envoyer des paquets � Z et Z peut envoyer des paquets
    � X.""",
    tests = (
        Bad(UpperCase(~Contain('AB'))),
        Bad(UpperCase(~Contain('BA'))),
        Bad(UpperCase(Comment(Contain('AC'),
                              """L'adresse de C n'est pas
                              dans le r�seau de A"""))),
        Bad(UpperCase(Comment(~Contain('BC'),
                              """L'adresse de C est dans le r�seau de B"""))),
        Bad(UpperCase(Comment(Contain('CA'),
                              """L'adresse de A n'est pas
                              dans le r�seau de C"""))),
        Bad(UpperCase(Comment(Contain('CB'),
                              """L'adresse de B n'est pas
                              dans le r�seau de C"""))),
        Good(Contain(' ')),
    ),
    )
    










