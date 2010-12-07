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

add(name="routeur eth0",
    required=["tp2:test branchement"],
    before="""Vous devez configurer l'interface ethernet du routeur.""",
    question="""Quelle suite de commandes tapez-vous après être
    passé en mode administrateur avec <tt>enable</tt>&nbsp;?""",
    nr_lines = 5,
    tests = (
    expect("no shutdown"),
    require(("interface {C0.remote_port.host.E0.port.name}",
		"interface {C0.remote_port.host.E0.port.name_without_space}"),
            """Vous n'avez pas indiqué la commande pour passe en mode
            configuration de l'interface ethernet (ou le nom de l'interface
            n'est pas reconnu (pas d'abbréviation SVP)""",
            uppercase=True, all_agree=True,
            parse_strings=host),
    require("{C0.remote_port.host.E0.port.ip}",
            "Je ne vois pas l'adresse IP du port (ou il est faux)",
            parse_strings=host),
    require("{C0.remote_port.host.E0.mask}",
            "Je ne vois pas le masque définissant le réseau (ou il est faux)",
            parse_strings=host),
    require("ip address {C0.remote_port.host.E0.port.ip} {C0.remote_port.host.E0.mask}",
            "Je ne vois pas la ligne configurant l'adresse IP et le masque",
            parse_strings=host),
    good_if_contains('', "Cela devrait être bon. Exécutez les commandes."),
    ),
    )

for i in (0,1):
    add(name="routeur serial%d" % i,
        required=["tp2:test branchement"],
        before="Vous devez configurer l'interface série '%d' du routeur." % i ,
        question="""Quelle suite de commandes tapez-vous après être
        passé en mode administrateur avec <tt>enable</tt>&nbsp;?""",
        nr_lines = 5,
        tests = (
        expect("no shutdown"),
        require(("interface {C0.remote_port.host.S%d.port.name}\n" % i,
                 "interface {C0.remote_port.host.S%d.port.name_without_space}\n" %i),
                """Vous n'avez pas indiqué la commande pour passer en mode
                configuration de l'interface série""",
                uppercase=True, all_agree=True,
                parse_strings=host),
        require("ip address {C0.remote_port.host.S%d.port.ip} {C0.remote_port.host.S%d.mask}" % (i, i),
                "Je ne vois la ligne configurant l'adresse IP et le masque",
                parse_strings=host),
        reject("clockrate",
               """<tt>rate</tt> est un argument de <tt>clock</tt>,
               il manque donc un espace entre les deux mots"""),
        require("{C0.remote_port.host.S%d.port.clock}" % i,
                "Il manque la définition de l'horloge",
                parse_strings=host),
        reject("{C0.remote_port.host.S%d.port.type}" % i,
               "Il ne faut pas mettre la définition de l'horloge",
               replace=( ('clock', 'DTE'), ),
               parse_strings=host),
        good_if_contains('', "Cela devrait être bon. Exécutez les commandes."),
        ),
        )
    add(name="serial%d ?" % i,
        required=["routeur serial%d" % i],
        question="""Répondez OUI quand votre routeur pourra pinguer
        son interface série %d (sinon ne répondez pas à la question)""" % i,
        tests = (
        yes("On vous a dit de répondre OUI"),
        ),
        )


for i in (0,1):
    add(name="remote s%d" % i,
        required=["serial%d ?" % i],
        question="""Donnez la commande complète permettant de pinguer
        le routeur distant via la liaison série %d.
        <p>
        Donnez votre réponse même si le ping échoue.
        """ % i,
        tests = (
        reject(('ip','IP'), "Le paramètre IP ne sert à rien."),
        good("ping {C0.remote_port.host.S%d.remote_port.ip}" % i,
             parse_strings=host),
        ),
        )
    add(name="remote s%d OK" % i,
        required=["remote s%d" % i],
        question="""Répondez OUI quand le ping fonctionnera en direction
        du routeur distant via la liaison série %d.""" % i,
        tests = (
        yes("On vous a dit de répondre OUI quand cela marchera"),
        ),
        )

add(name="routeur>pc",
    required=["pc:vers routeur eth0 ?"],
    question="""Quelle commande tapez-vous sur le routeur
    pour pinguer votre PC en utilisant une adresse IP&nbsp;?
    <p>
    Donnez votre réponse même si le ping échoue.
    """,
    tests = (
    good("ping {E0.port.ip}",parse_strings=host),
    ),
    )

add(name="routeur>pc ?",
    required=["routeur>pc"],
    question="Répondez OUI si votre routeur peut pinguer votre PC.",
    tests = (
    yes("""C'est impossible, ce ping doit fonctionner&nbsp;!"""),
    ),
    )


