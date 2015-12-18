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

add(name="connecteur série",
    required=["admin:administrateur"],
    question="""Quel est le type (pas le genre) du connecteur RS232C
    qui est sur le PC et sur lequel vous branchez le cable console
    du routeur CISCO&nbsp;?""",
    tests = (
        good(('DB9','DE9'), uppercase=True, replace=((' ',''),('-',''))),
        bad(('DCE', 'DTE'),
            "Le PC n'a pas de connexion série pour faire du réseau...",
            uppercase=True),
        bad('COM',
            "C'est le nom logique sous Windows, pas le nom du connecteur"),
        answer_length_is(3, "La réponse est en 3 caractères"),
    ),
    indices = ("""La réponse est sur <a href="http://www.google.com/search?q=serial+connector">Google</a>""", ),
    )

add(name="route par défaut",
    required=["lien:routeur>pc ?"],
    question="""Donnez la commande permettant de configurer la route
    par défaut de votre ordinateur pour quelle passe par votre routeur.""",
    tests = (
    require("{C0.remote_port.host.E0.port.ip}",
            "Je ne vois pas l'adresse IP du port éthernet de votre routeur",
             parse_strings=host),
    Good(HostReplace(Equal(
        "ip route add default via {C0.remote_port.host.E0.port.ip}"))),
    good("route add default gw {C0.remote_port.host.E0.port.ip}",
         parse_strings=host),
    good(("route add -net 0.0.0.0/0 gw {C0.remote_port.host.E0.port.ip}",
          "route add -net 0.0.0.0 netmask 0.0.0.0 gw {C0.remote_port.host.E0.port.ip}"),
         """Il est plus simple de faire <tt>add default</tt> au lieu
         de spécifier <tt>-net 0.0.0.0...</tt>.""",
         parse_strings=host),    
    expect('ip route',
           "Sous unix, on définit les routes avec la commande <tt>ip route</tt>"),
    # expect('gw'),
    ),
    good_answer = "N'oubliez pas de configurer la route !",
    )

add(name="si loin de moi",
    required=["route par défaut"],
    before = """Cette question est compliquée, vous avez besoin
    d'un papier et d'un crayon pour répondre.
    <p>
    On suppose que les paquets empruntent la route la plus courte.
    """,
    question="""Combien d'équipements sont <b>traversés</b>
    au maximum par les paquets qui partent de votre PC&nbsp;?""",
    tests = (
    require_int(),
    MaxDistance(),
    ),
    indices = ("""L'algorithme est simple, vous notez -1 sur votre PC.
    <p>
    Tant qu'il y a des équipements sans numéro :
    <ul>
    <li> <em>n := n + 1</em>
    <li> Numérotez n tous les équipements actifs non numérotés
    accessibles à partir
    d'un équipement noté <em>n - 1</em>
    </ul>
    <p>
    Le plus grand nombre que vous aurez noté sur un PC sera
    la réponse à cette question.
    """,
               ),
    )

add(name="traceroute",
    required=["Hop s1 OK", "Hop s0 OK"],
    before="""L'utilitaire <tt>traceroute</tt> sous Linux
    (ou <tt>tracert</tt> sous Windows) permet
    d'afficher les routeurs traversés par un paquet.""",
    question="""Utilisez la commande <tt>traceroute</tt> sur
    les chemins les plus longs.
    <p>
    En supposant que les machines les plus éloignées (en nombre de routeurs
    réseau) fonctionnent,
    combien de lignes numérotées la commande vous affiche-t-elle
    quand vous tracez la route&nbsp;?
<pre>traceroute to ksup.univ-lyon1.fr (134.214.126.72), 30 hops max, 40 byte packets
 1  psrl142 (134.214.142.1)  0.347 ms  0.300 ms  0.283 ms
 2  crialteon (134.214.126.85)  0.691 ms  0.688 ms  0.636 ms
 3  crialteon (134.214.126.85)  0.736 ms  0.750 ms  0.639 ms
</pre>
<p>
La commande précédente en affiche 3.
    """,
    tests = (
    require_int(),
    MaxDistanceRouteur(),
    ),
    good_answer = """On ne peut pas tracer le passage à travers
    les équipements qui ne font pas de routage (les <em>switchs</em>).""",
    indices = ("""Testez avec des petits chemins qui fonctionnent pour
    savoir ce que représentent les lignes affichées par <tt>traceroute</tt>""",
               ),
    )

add(name="traceroute -n",
    required=["traceroute"],
    before = """Complétez <tt>/etc/hosts</tt> avec quelques noms de machines
    qui sont traversées par les paquets""",
    question="""Testez l'option <tt>-n</tt> de <tt>traceroute</tt>.
    <p>
    En une phrase, donnez les différences de fonctionnement entre la version
    avec et sans l'option. Des mots clefs sont suffisants,
    il y a deux choses à remarquer.
    """,
    tests = (
    require(("DNS", "LOGIQUE", "DOMAIN", "NOM", "IP"),
            "L'affichage est-il le même&nbsp;?",
            all_agree = True, uppercase = True,          
            ),
    require(("RAPID","LENT", "VIT", 'TEMPS'),
            """Et dans la vie réelle, le fait de ne pas faire d'interrogation
            DNS change quoi à part ce qui change sur l'écran&nbsp;?""",
            all_agree = True, uppercase = True,          
            ),
    good_if_contains(""),
    ),
    indices = ("""Faire un requêtes DNS implique de questionner
    un serveur et ceci prend du temps.""", ),
    )

for i in (0,1):
    add(name="vers routeur s%d" % i,
        required=["route par défaut", "lien:serial%d ?" % i],
        question="""Quelle commande tapez-vous sur le PC pour pinguer
        l'interface série %d du routeur&nbsp;?
        <p>
        Donnez votre réponse même si le ping échoue.
        """ % i,
        tests = (
        good("ping {C0.remote_port.host.S%d.port.ip}"%i, parse_strings=host),
        ),
        )
    add(name="vers routeur s%d ?" % i,
        required=["vers routeur s%d" % i],
        question="""Répondez OUI si votre ordinateur peut pinguer l'interface
        série %d de votre routeur.
        """ % i,
        tests = (
        yes("""Ce n'est vraiment pas normal.
        Avez-vous mis la route par défaut sur l'ordinateur&nbsp;?"""),
        ),
        )

add(name="eth0",
    required=["tp2:test branchement", "rip:RIP", "admin:relance routeur"],
    before="Indiquez le <em>netmask</em> même s'il n'est pas obligatoire",
    question="""Quelle commande tapez-vous pour configurer l'interface
    <tt>eth0</tt> de l'ordinateur&nbsp;:""",
    tests = (
    good("ifconfig {E0.port.name} {E0.port.ip} netmask {E0.mask}",
         parse_strings=host),
    good("ifconfig {E0.port.name} {E0.port.ip}/{E0.nr_bits_netmask}",
         parse_strings=host),
    Good(HostReplace(Equal(
        "ip a add {E0.port.ip}/{E0.nr_bits_netmask} dev {E0.port.name}"))),
    Good(HostReplace(Equal(
        "ip addr add {E0.port.ip}/{E0.nr_bits_netmask} dev {E0.port.name}"))),
    Bad(Comment(~Contain('/') & ~Contain('netmask'),
                """Vous devez ajouter le masque de réseaux soit
                avec la syntaxe utilisant <tt>/</tt> soit avec
                le mot clef <tt>netmask</tt>""")),
    require('{E0.port.name}',
            "Je ne vois pas le nom du port éthernet du PC",
             parse_strings=host),
    require('{E0.port.ip}',
            "Je ne vois pas l'adresse IP de l'interface réseau.",
             parse_strings=host),
    # expect('ifconfig'),
    Bad(Comment(~Start('ip'), "Vous devez utiliser la commande <tt>ip</tt>")),
    ),
    )

add(name="vers routeur eth0",
    required=["eth0", "lien:routeur eth0"],
    question="""Quelle commande tapez-vous sur votre PC
    pour pinguer votre routeur&nbsp;?
    <p>
    Donnez votre réponse même si le ping échoue.
    """,
    tests = (
    good("ping {C0.remote_port.host.E0.port.ip}",parse_strings=host),
    expect('ping'),
    ),
    )


add(name="vers routeur eth0 ?",
    required=["vers routeur eth0"],
    before = """Si le ping ne fonctionne pas, vérifiez&nbsp;:
    <ul>
        <li> Que l'interface réseau que vous avez configuré correspond
        bien à celui sur lequel vous avez branché le cable.
        Utilisez <tt>dmesg</tt> pour voir si c'est le cas.
        <li> Que le cable fonctionne (changez le).
        <li> Que vous avez branché le cable sur le bon port du routeur.
        </ul>
        """,
    question="Répondez OUI si votre ordinateur peut pinguer votre routeur.",
    tests = (
    yes("""Vérifiez les cables et les commandes que vous avez exécuté,
    vérifiez que eth0 est bien sur la carte mère en utilisant <tt>dmesg</tt>.
    <p>
    Prévenez un enseignant si cela ne fonctionne toujours pas"""),
    ),
    )

for i in (0,1):
    add(name="Hop s%d OK" % i,
        required=["rip:Et Hop s%d OK" % i, "vers routeur s%d ?" % i],
        question="""À partir de votre ordinateur,
        le ping du port ethernet du routeur distant (via serial%d)
        a-t-il fonctionné&nbsp;?""" % i,
        tests = (
        yes("""Cela devrait fonctionner. Un cable c'est débranché&nbsp;?"""),
        ),
        )

add(name="table routage",
    required=["route par défaut"],
    question="""Quelle commande tapez-vous sous UNIX pour voir
    la liste des routes""",
    tests = (
    good(("ip route", "netstat -r")),
    reject('show', 'Sous UNIX, pas sur le CISCO'),
    reject('netstat', 'Il y a une commande plus courte et plus logique'),
    ),
    )

add(name="application",
    required=["admin:password telnet"],
    question="""Proposez une application du PC permettant de tester la couche
    application du routeur
    (une application se connectant au routeur lui-même).""",
    tests = (
    good("telnet"),
    bad(('putty','ssh'), "Il n'y a pas de serveur SSH sur ce routeur."),
    bad('FTP', "Il n'y a pas de serveur FTP sur ce routeur.", uppercase=True),
    ),
    indices = ("Une application permettant de se connecter à distance",
               ),
    )

add(name="vitesse",
    required=["traceroute"],
    before = """
    Pour pinguer TOUTES les machines (PC) vous pouvez compléter la liste
    des machines et lancer la boucle suivante sous UNIX&nbsp;:

    <pre>for I in 0.1 0.3 1.5 1.7 2.9 2.11 .....
do
    ping -c 1 -s 1000 -W 1 192.168.$I |
    tail -n 1 |
    sed -e 's/.* = //' -e 's/\// /' |
    (read A B ; echo "$A millisecondes pour transmettre 60Ko à 192.168.$I")
done</pre>
<p>
Vous pouvez la lancer plusieurs fois et prendre le minimum.
    """,
    question="""Combien de ``classes´´ de temps trouvez-vous&nbsp;?
    <p>
    On entend par classe des valeurs suffisamment différentes pour
    que la différence ne soit pas le fruit du hasard.
    Un facteur 2 n'est pas significatif.
    """,
    tests = (
    require_int(),
    good("3"),
    bad("2",
        """Le <em>ping</em> peut traverser un câble série (lent),
        un câble ethernet ou ne pas passer par le réseau car local
        à la machine.
        Il ne peut donc pas y avoir moins de 3 classes de temps."""),
    ),
    )

add(name="réparé ?",
    required=["vitesse", "tp2:démontage"],
    question="""Pouvez-vous pinguer toutes les machines
    à partir de votre PC&nbsp;?""",
    tests = (
    yes("""2 câbles on été débranchés en trop ou bien vous n'avez
    pas attendu que les tables de routages soient à jour."""),
    ),
    )



