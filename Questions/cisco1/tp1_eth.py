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

from QUENLIG.questions import *
from .check import *
from .configuration_salles import *

add(name="cable ethernet",
    required=["tp1:nom routeur"],
    before = """Le cables ethernet 'normaux' servent � relier une machine
    � un commutateur ou � un hub.
    <p>
    On utilise un cable 'invers�' pour relier 2 mat�riels de m�me type.
    <ul>
    <li> 2 machines
    <li> 2 hub ou commutateur
    </ul>
    <p>
    Un routeur est consid�r� comme une machine.
    <p>
    Parfois, une croix est dessin�e � cot� du connecteur pour indiquer
    que celui-ci est invers�.""",
    question = """Branchez le cable ethernet entre&nbsp;:
    <ul>
    <li> Le port ethernet qui est sur une carte d'extension de votre PC.
         Il y en a deux, choisissez celui qui correspond � <tt>eth0</tt>,
         Normalement c'est celui du haut, mais sans garantit.
         <b>Ne touchez pas au c�ble ethernet qui est sur la carte m�re.</b>
    <li> le premier port ethernet de votre routeur.
    </ul>
    <p>
    Au fait, est-il pr�f�rable de mettre un cable invers�&nbsp;?""",
    tests=(
    yes("""Et bien c'est oui car ce cable connecte 2 machines.
    <p>
    Cela peut n�anmoins fonctionner avec un mauvais cable
    car les cartes r�seaux r�centes inverse automatiquement
    les fils s'il y a un probl�me.
    Mais cela ralentie la mise en place du r�seau"""),
    ),
    )

add(name="config ethernet",
        required=["cable ethernet", "ethernet:configure",
                  "tp1_serie:routeur>local s0 OK", "tp1_serie:routeur>local s1 OK"],
        question="""Voici la suite de commande pour configurer
        dans le routeur, son interface ethernet&nbsp;:
        <pre>ip address IP_INTERFACE MASK_INTERFACE</pre>
        Mettez en route l'interface en enlevant la commande <tt>shutdown</tt>.
        <pre>no shutdown</pre>
        <p>
        La r�ponse � cette question est la liste des commandes que
        vous avez tap�es.
        """,
        nr_lines=4,
        tests = (
        expect('ip address'),
	expect("no shutdown"),
        require("{C0.remote_port.host.E0.port.ip}",
                "Il manque l'adresse IP (ou elle n'est pas bonne)",
                parse_strings=host),
        require("{C0.remote_port.host.E0.mask}",
                "Il manque le masque (ou il n'est pas bon)",
                parse_strings=host),
        require("ip address {C0.remote_port.host.E0.port.ip} {C0.remote_port.host.E0.mask}",
                "Je ne vois la ligne configurant l'adresse IP et le masque",
                parse_strings=host),
        good_if_contains('', "Cela devrait �tre bon. Ex�cutez les commandes."),
        ),
        )

add(name="routeur>local eth",
    required=["config ethernet"],
    question="""Donnez la ligne commande que vous tapez sur votre routeur
    pour <em>pinguer</em> l'interface locale de votre liaison ethernet""",
    tests = (
    require_ping,
    require("{C0.remote_port.host.E0.port.ip}",
            "Je ne vois pas l'adresse IP du port ethernet de votre routeur.",
            parse_strings=host),
    good("ping {C0.remote_port.host.E0.port.ip}",
         parse_strings=host),
    good("ping ip {C0.remote_port.host.E0.port.ip}",
             """C'est pas la peine de mettre le param�tre <tt>ip</tt>,
             les r�ponses suivantes avec ce param�tre seront refus�es""",
         parse_strings=host),
    ),
    )

add(name="routeur>local eth OK",
    required=["routeur>local eth"],
    before = "Normalement le cable ethernet est branch�",
    question = """R�pondez OUI � cette question seulement
    si le ping local sur le port ethernet a fonctionn� correctement.
    Sinon vous attendez.""",
    tests = ( yes('Tapez OUI'), ),
    )

add(name="eth OK",
    required=["routeur>local eth OK", "serie:affiche"],
    question="""R�pondez OUI � cette question seulement si
    la ligne ethernet
    est : <tt>up, line protocol is up</tt>.
    <p>
    Si ce n'est pas le cas, v�rifiez ou est branch� le cable ethernet.
    """,
    tests = ( yes('Tapez OUI'), ),
    )

add(name="config pc eth",
    required=["eth OK"],
    before = """N'oubliez pas de passer super-utilisateur
    avec la commande <tt>su</tt> avant de configurer Unix.
    Le mot de passe est <tt>moi</tt>
    <p>
    Si par hasard la liaison ethernet <b>ne fonctionne PAS</b>&nbsp;:
    <ul>
    <li> Utilisez la commande <tt>dmesg</tt> pour savoir quel
    est le nom de la carte r�seau sur laquelle vous avez branch� le cable.
    <li> V�rifiez dans quels connecteurs vous avez branch� les cables.
    <li> Changez de cable.
    <li> Appelez l'enseignant.
    </ul>
    """,
    question = """Quelle ligne de commande tapez-vous sous Unix pour
    configurer le port ethernet pour qu'il puisse communiquer
    avec le routeur CISCO&nbsp;?""",
    tests = (
    require('{E0.port.name}', "Je ne vois pas le nom de l'interface r�seau",
            parse_strings=host),
    reject('up', "Le 'up' est inutile"),
    reject('broadcast',
           """D�finir l'adresse de <em>broadcast</em> est inutile
           car on peut la calculer � partir de l'adresse r�seau et
           du <em>netmask</em>.
           L'indiquer ne peut provoquer que des erreurs."""),
    require('{E0.port.ip}',
            "Je ne vois pas l'adresse IP de l'interface (ou elle est fausse)",
            parse_strings=host),
    
    bad("ifconfig {E0.port.name} {E0.port.ip} {E0.mask}",
        "Il manque le param�tre <tt>netmask</tt> avant le netmask",
        parse_strings=host),
    good("ifconfig {E0.port.name} {E0.port.ip} netmask {E0.mask}",
         parse_strings=host),
    good("ifconfig {E0.port.name} {E0.port.ip}/{E0.nr_bits_netmask}",
         parse_strings=host),
    good("ifconfig {E0.port.name} {E0.port.ip}",
         """ATTENTION, cette commande n'est juste que si le <em>netmask</em>
         correspond � la classe d'adresse IP utilis�e (ABCD)
         Ceci est le cas pour cette adresse.""",
         parse_strings=host),
    Good(HostReplace(Equal(
        "ip a add {E0.port.ip}/{E0.nr_bits_netmask} dev {E0.port.name}"))),
    Good(HostReplace(Equal(
        "ip addr add {E0.port.ip}/{E0.nr_bits_netmask} dev {E0.port.name}"))),
    Good(HostReplace(Equal(
        "ip address add {E0.port.ip}/{E0.nr_bits_netmask} dev {E0.port.name}"))),
    #require('ifconfig', "Vous devez utiliser la commande <tt>ifconfig</tt>"),
    Bad(Comment(~Start('ip'), "Vous devez utiliser la commande <tt>ip</tt>")),
    ),
    )




add(name="routeur>remote eth",
    required=["eth OK", "routeur>local eth OK", "config pc eth"],
        before="""Puisque le ping local fonctionne, on va aller plus loin
        et franchir le cable ethernet.""",
    question="""Donnez la ligne commande que vous tapez sur votre routeur
    pour <em>pinguer</em> votre ordinateur.""",
    tests = (
    require_ping,
    require("{E0.port.ip}",
            "Je ne vois pas l'adresse IP de votre ordinateur",
            parse_strings=host),
    good("ping {E0.port.ip}",
         parse_strings=host),
    ),
    )
add(name="routeur>remote eth OK",
        required=["routeur>remote eth"],
        question = """R�pondez OUI � cette question seulement
        si le routeur a pu pinguer votre ordinateur.""",
        tests = ( yes('Tapez OUI'), ),
        )

add(name="machine>routeur",
    required=["eth OK", "routeur>local eth OK", "config pc eth"],
        before="""Puisque le ping local fonctionne, on va aller plus loin
        et franchir le cable ethernet.""",
    question="""Donnez la ligne commande que vous tapez sur votre ordinateur
    pour <em>pinguer</em> votre routeur.""",
    tests = (
    require_ping,
    require("{E0.remote_port.ip}",
            "Je ne vois pas l'adresse IP de votre routeur",
            parse_strings=host),
    good("ping {E0.remote_port.ip}",
         parse_strings=host),
    ),
    )

add(name="machine>routeur OK",
        required=["machine>routeur"],
        question = """R�pondez OUI � cette question seulement
        si le ping de l'ordinateur vers le port ethernet du routeur
        a fonctionn� correctement""",
        tests = ( yes('Tapez OUI'), ),
        )

add(name="machine>routeur 2",
    required=["machine>routeur OK"],
        before="""Puisque le ping sur le port ethernet du routeur fonctionne
        nous allons essayer de faire un <em>ping</em> sur l'interface
        s�rie 0 du routeur � partir de votre ordinateur.""",
    question="""Donnez la ligne commande que vous tapez sur votre ordinateur
    pour <em>pinguer</em> le port s�rie 0 de votre routeur.""",
    tests = (
    require_ping,
    require("{E0.remote_port.host.S0.port.ip}",
            "Je ne vois pas l'adresse IP du port s�rie 0 de votre routeur",
            parse_strings=host),
    good("ping {E0.remote_port.host.S0.port.ip}",
         parse_strings=host),
    ),
    )

add(name="machine>routeur 2 ?",
    required=["machine>routeur 2"],
    question = """Le ping entre votre ordinateur et le port s�rie 0
    de votre routeur fonctionne-t-il (oui ou non)&nbsp;?""",
    tests = ( no("""Il est impossible que ce ping ait fonctionn�
    correctement car votre ordinateur n'a pas de route par d�faut"""), ),
    good_answer = """C'est normal, l'ordinateur ne sait pas � qui envoyer
    ce paquet car il n'a aucune route""",
    highlight = True,
    )
