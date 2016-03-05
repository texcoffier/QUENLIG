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

add(name="administrateur",
    required=["tp2:votre poste"],
    question="""Passez en mode administrateur du routeur CISCO.
    Et répondez à cette question par le chiffre indiqué dans
    l'énumération suivante&nbsp:
    <ol>
    <li> J'ai réussi.
    <li> Il y a un mot de passe (autre que %s).
    <li> Je ne me souviens pas comment l'on fait (mauvais point).
    </ol>""" % mots_de_passe,
    tests = (
    require_int(),
    good("1"),
    bad("2",
        """Suivez la <a href="cisco_efface_passwd.html">
        procédure d'effacement de mot de passes</a>."""),
    bad("3", "Il faut taper <tt>enable</tt>."),
    ),
    )

add(name="nom routeur",
    required=['administrateur'],
    before = "Attention la casse compte.",
    question="""Quelle ligne de commande tapez-vous pour donner
    son nom à votre routeur&nbsp;?""",
    tests = (
    good("hostname {C0.remote_port.host.name}",
         "N'oubliez pas d'exécuter la commande", parse_strings=host),
    expect('hostname'),
    require('{C0.remote_port.host.name}',
            "Je ne vois pas le nom de votre routeur",
            parse_strings=host),
    ),
    )

add(name="sauve configuration",
    required=["rip:RIP"],
    before="""Si jamais il y a un problème vous pouvez perdre toute
    la configuration de votre routeur.""",
    question="Quelle commande tapez-vous pour sauver la configuration&nbsp;?",
    tests = (
    good("copy running-config startup-config"),
    expect('copy'),
    expect('running-config'),
    expect('startup-config'),
    ),
    good_answer = "VOUS DEVEZ LE FAIRE",
    )

add(name="relance routeur",
    required=["sauve configuration"],
    question="Quelle commande tapez-vous pour relancer le routeur&nbsp;? (Ne la lancez pas)",
    tests = (
        good("reload"),
        bad('restart', """Cela réinitialise certaines chose mais cela ne
        redémarre pas le routeur"""),
        bad('reboot',
            """Montrez à l'enseignant l'endroit
            où vous avez trouvé cette commande"""),
        ),
    )

add(name="AVANT DE PARTIR",
    required=["sauve configuration"],
    question=avant_de_partir,
    )



add(name="nommer votre pc",
    required=["tp2:votre poste", "pc:eth0", "rip:RIP"],
    before = "N'oubliez pas de respecter la casse (majuscule/minuscule)",
    question="""Quelle commande tapez-vous sur le routeur pour nommer
    votre PC&nbsp;?""",
    tests = (
    good("ip host {name} {E0.port.ip}", parse_strings=host),
    reject('hostname', "C'est pour se donner un nom à soit-même"),
    expect('ip host'),
    require('{name}', "Je ne vois pas le nom de votre machine",
            parse_strings=host),
    require('{E0.port.ip}', "Je ne vois pas l'adresse IP de la machine",
            parse_strings=host),
    ),
    )

add(name="telnet",
    required=["pc:eth0", "rip:Et Hop s0 OK", "rip:Et Hop s1 OK"],
    before="""On peut administrer le routeur avec sa liaison série,
    mais aussi via le réseau en utilisant <tt>telnet</tt>.
    <p>
    Il suffit de faire <tt>telnet une_ip_du_routeur</tt> à partir
    de votre ordinateur.""",
    question="""Pouvez-vous faire un <tt>telnet</tt> sur votre routeur
    et travailler dessus&nbsp;?""",
    tests = (
    no("Montrez cela à l'enseignant, c'est impossible."),
    ),
    good_answer = """Pour pouvoir utiliser <tt>telnet</tt>
    il faut avoir configuré les mots de passe.""",
    )


add(name="config telnet",
    required=["telnet"],
    question="""Quelle commande tapez-vous dans l'IOS
    pour passer en mode configuration
    de la console d'administration à distance numéro 0 (zéro)&nbsp;?""",
    tests = (
    good('line vty 0'),
    good('line VTY 0'),
    require_startswith("line",
                       "Il faut utiliser la commande <tt>line</tt>"),
    require('vty', """La console d'administration à distance utilise
    un <em><b>V</b>irtual <b>T</b>elet<b>Y</b>pe</em> (TTY virtuel)"""),
    Bad(Comment(UpperCase(Equal('line vty 0 4')),
                "Vous êtes en train de configurer les ligne VTY de 0 à 4.")),
    ),
    )

add(name="password telnet",
    required=["config telnet"],
    before="""La connexion avec <tt>telnet</tt> ne sera possible
    que quand vous aurez mis un mot de passe.""",
    question="""Une fois en mode configuration du VTY,
    quelle commande tapez-vous pour mettre
    le mot de passe <tt>cisco</tt>&nbsp;?""",
    tests = (
        good('password cisco'),
        good('password 0 cisco'),
        good('password 7 cisco'),
        Expect('cisco', "Je ne vois pas le mot de passe..."),
        ),
    good_answer="""On ne peut pas se connecter simultanément avec le même
    mot de passe.<p>
    On ne peut pas se connecter s'il n'y a pas de mot de passe.""",
    )

add(name="config console",
    required=["config telnet", "password telnet"],
    question="""Quelle commande tapez-vous pour passer en mode configuration
    de la <b>console</b> de contrôle du routeur&nbsp;?
    <p>
    C'est celle sur laquelle vous êtes en train de taper les commandes.
    """,
    tests = (
        require_startswith("line",
                           "Il faut utiliser la commande <tt>line</tt>"),
        Expect('console'),
        bad('line console',
            """Il peut y avoir plusieurs consoles branchée sur le même
            routeur. Vous devez indiquer laquelle configurer"""),
        good('line console 0'),
        ),
    )

add(name="password console",
    required=["config console"],
    question="""Une fois en mode configuration de la console,
    quelles commandes tapez-vous pour verrouiller l'accès à la console
    par le mot de passe 'cisco' qui sera demandé à chaque connexion
    sur la console de contrôle du routeur&nbsp;?
    <ul>
    <li> Un première commande indique que l'on veut un accès
    avec authentification pour la connexion.
    <li> La deuxième commande spécifie que le mot de passe.
    </ul>
    """,
    nr_lines = 2,
    tests = (
    require('cisco', "Je ne vois pas le mot de passe"),
    require('login', "La première commande indique que l'on veut un 'login'"),
    require('password',
            "La deuxième commande indique le mot de passe (pa...)"),
    good('login\npassword cisco'),
    good('login\npassword 0 cisco'),
    good('login\npassword 7 cisco'),
    good('password cisco\nlogin'),
    good('password 0 cisco\nlogin'),
    good('password 7 cisco\nlogin'),
    ),
    )

add(name="password enable",
    required=["password telnet"],
    question="""Quelle commande tapez-vous pour assigner le mot de passe
    (stocké chiffré) <tt>cisco</tt> au passage en mode privilégié
    avec <tt>enable</tt>&nbsp;?""",
    tests = (
    require_startswith("enable",
                       "Il faut utiliser la commande <tt>enable</tt>"),
    require('cisco', "Je ne vois pas le mot de passe"),
    reject('enable password', "Command obsolète car insécure"),
    good('enable secret cisco'),
    ),
    )
