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
from .configuration_salles import *

good_default = "<pre>ip route add default via ???.???.???.???</pre>"

add(name="defaut pc",
    required=["tp1_eth:machine>routeur 2 ?", "tp1_eth:routeur>remote eth OK"],
    question="""Quelle commande tapez-vous pour ajouter une route par
    défaut à votre ordinateur pour qu'il envoie tout au routeur&nbsp;?""",
    tests = (
    Good(HostReplace(Equal("ip route add default via {E0.remote_port.ip}"))),
    require_startswith("ip route",
                       """Vous devez utiliser la commande <tt>ip route</tt>
                       pour indiquer la route par défaut"""
                       ),
    good("route add -net 0.0.0.0 netmask 0.0.0.0 gw {E0.remote_port.ip}",
         "On préfère utiliser le mot clef <tt>default</tt>" + good_default,
         parse_strings=host),
    good("route add -net 0.0.0.0/0 gw {E0.remote_port.ip}",
         "Pas sûr que cela soit portable, on conseille&nbsp;:" + good_default,
         parse_strings=host),
    require("default", """Je ne vois pas le mot clef <tt>default</tt>
    indiquant que vous voulez définir la route par défaut"""),
    require("{E0.remote_port.ip}",
            "Je ne vois pas l'adresse IP du routeur connecté à votre machine",
            parse_strings=host),
    Reject("dev", """Pas la peine d'indiquer le périphérique, en effet
                     on peut le retrouver à partir de l'adresse IP.
                     <p>Cette option est seulement utile quand
                     il y a 2 liaisons IP physiques reliant directement les mêmes
                     2 machines, ce qui arrive rarement."""), 
#    require("gw", "Je ne vois pas le mot clef obligatoire <tt>gw</tt>"),
    good("route add default gw {E0.remote_port.ip}", parse_strings=host),
    ),
    good_answer="Exécutez la commande",
    indices = (
    """Tapez <tt>man ip-route</tt>""",
    ),
    )

add(name="defaut pc OK",
    required=["defaut pc", "tp1_eth:machine>routeur OK"],
    question = """Répondez OUI à cette question seulement
    si le ping de votre ordinateur vers le port série 0
    de votre routeur fonctionne.""",
    tests = ( yes('Tapez OUI'), ),
    )

add(name="machine>routeur s0",
    required=["defaut pc OK", "routeur>s0 routeur ?"],
    before="""Vous pouvez pinguer les interfaces de votre routeur
    à partir de votre PC, mais pouvez-vous pinguer les autres
    routeurs&nbsp;?""",
    question="""Donnez la ligne commande que vous tapez sur votre ordinateur
    pour <em>pinguer</em> le routeur connecté au port série 0
    de votre routeur
    (vous pinguez l'interface réseau la plus proche de vous).""",
    tests = (
    require_ping,
    require("{E0.remote_port.host.S0.remote_port.ip}",
            "Je ne vois pas l'adresse IP du port série du routeur connecté au votre.",
            parse_strings=host),
    good("ping {E0.remote_port.host.S0.remote_port.ip}",
         parse_strings=host),
    ),
    )

add(name="machine>routeur s1",
    required=["defaut pc OK", "tp1_serie:routeur>s1 routeur ?"],
    before="""Vous pouvez pinguer les interfaces de votre routeur
    à partir de votre PC, mais pouvez-vous pinguer les autres
    routeurs&nbsp;?""",
    question="""Donnez la ligne commande que vous tapez sur votre ordinateur
    pour <em>pinguer</em> l'interface série du routeur connecté au port série 1
    de votre routeur.""",
    tests = (
    require_ping,
    require("{E0.remote_port.host.S1.remote_port.ip}",
            "Je ne vois pas l'adresse IP du port série du routeur",
            parse_strings=host),
    good("ping {E0.remote_port.host.S1.remote_port.ip}",
         parse_strings=host),
    ),
    )

add(name="machine>routeur s1 OK",
    required=["machine>routeur s1",
              "tp1_serie:routeur>remote s1 OK",
              ],
    question = """Répondez OUI quand le ping de votre ordinateur
    vers le routeur connecté au port série 1 de votre routeur fonctionnera.
    <p>
    Ceci fonctionnera quand <b>tous</b> les routeurs de la boucle
    auront configuré leur route par défaut.
    """,
    tests = (
    yes('Répondez OUI'),
    ),
    )

add(name="machine>routeur s0 OK",
    required=["machine>routeur s0",
              "tp1_serie:routeur>remote s0 OK",
              "machine>routeur s1 OK",
              ],
    question = """Répondez OUI quand le ping de votre ordinateur
    vers le routeur connecté au port série 0 de votre routeur fonctionnera.
    <p>
    Ceci fonctionnera quand <b>tous</b> les routeurs de la boucle
    auront configuré leur route par défaut.
    """,
    tests = (
    yes('Répondez OUI'),
    ),
    )


add(name="défaut routeur",
    required=["doc:intro",
              "tp1_serie:routeur>s0 routeur ?",
              "tp1_serie:routeur>s1 routeur ?"],
    before="""Les routeurs étant organisés sous la forme d'une boucle,
    nous allons faire circuler les informations sur la boucle
    jusqu'à ce qu'un routeur les route lui-même
    ou que les paquets se retrouvent avec un TTL de 0.""",
    question="""Quelle commande tapez-vous sur le routeur pour configurer
    la route par défaut en direction du routeur connecté sur le port
    série 0&nbsp;?
    <p>
    Attention, n'utilisez pas <tt>s0</tt> ou <tt>s1</tt> dans
    votre réponse comme c'est indiqué dans la documentation.
    Je veux ABSOLUMENT l'adresse IP de la passerelle.
    <p>
    N'oubliez pas de d'exécuter la commande quand vous aurez répondu
    correctement à cette question.
    """,
    tests = (
    bad("ip default-gateway {C0.remote_port.host.S0.remote_port.ip}",
        """Cette commande fonctionne seulement pour le <em>boot</em>.
        En utilisation normal, elle n'est pas utilisée.""",
         parse_strings=host),
    reject(("{C0.remote_port.host.S1.name}",
         "{C0.remote_port.host.S1.remote_port.ip}"),
         "Vous faites tourner les paquets dans le mauvais sens."),
    good("ip route 0.0.0.0 0.0.0.0 {C0.remote_port.host.S0.name}",
        """Attention, cette commande ne fonctionne que dans le cas
        d'une liaison bipoint mais pas sur un réseau éthernet car le paquet
        n'est pas adressé à une passerelle.
        <p>
        Normalement vous devriez indiquer l'adresse IP de la passerelle.
        """,
        parse_strings=host),
    require('ip', "Il faut utiliser la commande <tt>ip</tt>"),
    require('0.0.0.0',
            "Je ne vois pas l'adresse du réseau par défaut (il contient tout)"
            ),
    number_of_is('0.0.0.0', 2,
                 """Je ne vois pas le <em>netmask</em> du réseau par défaut
                 (il contient tout)"""),
    require("{C0.remote_port.host.S0.remote_port.ip}",
            "Je ne vois pas l'adresse IP de la passerelle par défaut",
            parse_strings=host),
    good("ip route 0.0.0.0 0.0.0.0 {C0.remote_port.host.S0.remote_port.ip}",
         parse_strings=host),
    ),
    good_answer = "Et bien tapez cette commande.",
    )

add(name="routeur>s0 routeur ?",
    required=["défaut routeur", "tp1_serie:routeur>s0 routeur"],
    question = """Le ping à partir de votre routeur
    via le port série 0 sur l'autre port série
    du routeur distant fonctionne-t-il correctement&nbsp;?""",
    tests = ( yes("""Cela aurai du fonctionner car maintenant
    votre routeur sait où envoyer le paquet et l'autre sait répondre."""),
              ),
    )


add(name="les routes",
    required=["cli:show liste",
              "routeur>s0 routeur ?", "defaut pc OK"],
    before="""Attention, les routes ne sont pas affichées si la liaison
    qu'elles utilisent n'est pas branchée.""",
    question="""Quelle commande tapez-vous sur le routeur pour lister
    les routes&nbsp;?""",
    tests = (
    expect('show'),
    good("show ip route"),
    ),
    indices = (
        'Cela commence par <tt>show ip</tt>',
        ),
    )

add(name="combien",
    required=["les routes"],
    before = """Avant de répondre à la question, vérifiez que vos
    interfaces réseaux sur le routeur fonctionnent.""",
    question = "Combien votre routeur affiche-t-il de routes&nbsp;?",
    tests = (
    require_int(),
    good("4"),
    ),
    )

add(name="statiques",
    required=["les routes"],
    question="Combien votre routeur affiche-t-il de routes statiques&nbsp;?",
    tests = (
    require_int(),
    good("1"),
    ),
    )

add(name="connectées",
    required=["les routes"],
    question="""Combien votre routeur affiche-t-il de routes connectées,
    c'est-à-dire pour lesquels la destination est directement connectée
    au routeur&nbsp;?""",
    tests = (
    require_int(),
    good("3"),
    ),
    )

add(name="arp",
    required=["les routes"],
    question="""Quelle commande tapez-vous sur le routeur pour afficher
    le contenu de la table ARP&nbsp;?""",
    tests = (
        Good(UpperCase(Equal('show arp'))),
        Good(Comment(UpperCase(Equal('show ip arp')),
                     "<tt>show arp</tt> est plus court")),
    ),
    )

add(name="arp nombre",
    required=["arp"],
    question="Combien la table ARP du routeur contient de lignes (hors titre)&nbsp;?",
    tests = (
    require_int(),
    good("2"),
    ),
    )



    



    
