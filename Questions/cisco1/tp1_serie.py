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
from configuration_salles import *

add(name="genre",
    required=['type série 0'],
    question="""Le cable que vous devez brancher sur le connecteur
    série zéro du routeur CISCO
    est-il male (M) ou femelle (F)&nbsp;?
    <p>
    ATTENTION : on ne vous demande pas le genre du connecteur
    que vous branchez sur le routeur CISCO (il est toujours le même)
    mais celui qui est à l'autre bout.
    """,
    tests = (
    answer_length_is(1, "Vous devez répondre avec M ou F"),
    good("{C0.remote_port.host.S0.port.type}", uppercase=True,
         replace=(('F','DCE'), ('M', 'DTE'),
                  ('FEMELLE','DCE'),('MALE', 'DTE')),
         parse_strings=host),
    ),
    )

for i in range(2):
    add(name="type série %d" % i,
        required=['tp1:nom routeur'],
        before = """Sur la documentation CISCO, DCE est appelé ETCD
        et DTE est appelé ETTD""",
        question="""Quel est le type du cable série que vous devez brancher
        sur votre routeur sur le connecteur série '%d' (c'est
        indiqué dans le tableau sur le sujet du TP (DCE/DTE))&nbsp;?""" % i,
        tests = (
        good("{C0.remote_port.host.S%d.port.type}" % i,
             uppercase=True, parse_strings=host),
        comment("La réponse est soit DCE soit DTE"),
        ),
        good_answer="""Les cables sont physiquement différents,
        si vous utilisez les mauvais cables cela ne fonctionnera pas.
        """
        )

    add(name="routeur série %d" % i,
        required=["tp1:nom routeur"],
        before="La réponse à cette question est sur le plan du réseau",
        question="""Quel est le nom du routeur que vous allez connecter
        au votre via le cable série branché sur le port série %d
        de votre routeur.""" % i,
        tests = (
        good("{C0.remote_port.host.S%d.remote_port.host.name}" % i,
             uppercase=True, parse_strings=host),
        ),
        )

    add(name="horloge %d" % i,
        required=["type série %d" % i, "doc:intro"],
        question="""Quand vous allez configurer la liaison série '%d' sur
        le routeur, avez-vous besoin de définir la fréquence d'horloge&nbsp;?
        <p>
        Répondez avec O ou N.""" % i,
        tests = (
        good("{C0.remote_port.host.S%d.port.type}" % i, uppercase=True,
             replace=(('O','DCE'), ('N', 'DTE')),
             parse_strings=host),        
        ),
        indices = ('<a href="http://www.google.com/search?q=serial+clock+dce+dte">Google</a>', ),
        )

    add(name="configure série %d" % i,
        required=["horloge %d" % i, "branchement", "tp1:sauve config",
                  "serie:configure"],
        before=en_mode_serial,
        question="""Voici la suite de commande pour configurer :
        <pre>ip address IP_INTERFACE_SERIE MASK_INTERFACE_SERIE</pre>
        Si vous devez configurer l'horloge, faites&nbsp;:
        <pre>clock rate 56000</pre>
        Mettez en route l'interface en enlevant
        la commande <tt>shutdown</tt>&nbsp;:
        <pre>no shutdown</pre>
        <p>
        La réponse à cette question est la liste des commandes que
        vous avez tapée.
        """,
        nr_lines=4,
        tests = (
        expect('ip address'),
        expect('no shutdown'),
        require("{C0.remote_port.host.S%d.port.ip}" % i,
                "Il manque l'adresse IP (ou elle n'est pas bonne)",
                parse_strings=host),
        require("{C0.remote_port.host.S%d.mask}" % i,
                "Il manque le masque (ou il n'est pas bon)",
                parse_strings=host),
        require("ip address {C0.remote_port.host.S%d.port.ip} {C0.remote_port.host.S%d.mask}" % (i,i),
                "Je ne vois pas la ligne configurant l'IP et le masque",
                parse_strings=host),
        require("{C0.remote_port.host.S%d.port.clock}" % i,
                "Il manque la définition de l'horloge (ou elle n'est pas bonne)",
                parse_strings=host),
        reject("{C0.remote_port.host.S%d.port.type}" % i,
               "Il ne faut pas mettre la définition de l'horloge",
               replace=( ('clock', 'DTE'), ),
               parse_strings=host),
        good_if_contains('', "Cela devrait être bon. Exécutez les commandes."),
        ),
        )
    add(name="routeur>local s%d" % i,
        required=["configure série %d" % i],
        before="""Malheureusement, quand une interface réseau est configurée,
        on ne peut pas pinguer son adresse locale
        quand le cable n'est pas branché.
        <p>
        Pour pouvoir pinguer il faut que la liaison soit correctement
        branchée et configurée des 2 cotés.""",
        question="""Donnez la ligne commande que vous tapez sur votre routeur
        pour <em>pinguer</em> l'interface locale de votre liaison
        série '%d'""" % i,
        tests = (
        require_ping,
        require("{C0.remote_port.host.S%d.port.ip}" % i,
                "Je ne vois pas l'adresse IP du port série local",
                parse_strings=host),
        good("ping {C0.remote_port.host.S%d.port.ip}" % i,
             parse_strings=host),
        good("ping ip {C0.remote_port.host.S%d.port.ip}" % i,
             """C'est pas la peine de mettre le paramètre <tt>ip</tt>,
             les réponses suivantes avec ce paramètre seront refusées""",
             parse_strings=host),
        ),
        )

    add(name="routeur>local s%d OK" % i,
        required=["routeur>local s%d" % i],
        question = """Répondez OUI à cette question seulement
        si le ping local sur le port série '%d' a fonctionné correctement.
        <p>
        Vous ne devez pas répondre <tt>non</tt>."""%i,
        tests = ( yes('Tapez OUI'), ),
        )

    add(name="série %d OK" % i,
        required=["configure série %d" % i, "serie:affiche"],
        question="""Répondez OUI à cette question seulement si
        la ligne série %d est <tt>up, line protocol is up</tt>.
        <p>
        Si ce n'est pas le cas&nbsp;:
        <ul>
        <li> Attendez que l'autre personne ait configurée sa liaison série.
        <li> Vérifiez si les paramètres de la ligne sont correctes.
        <li> Vérifiez si le cable n'a pas été débranché.
        </ul>
        """ % i,
        tests = ( yes('Tapez OUI'), ),
        )
    add(name="routeur>remote s%d" % i,
        required=["série %d OK" % i, "routeur>local s%d OK" % i],
        before="""Puisque le ping local fonctionne, on va aller plus loin
        et franchir le cable.""",
        question="""Donnez la ligne commande que vous tapez sur votre routeur
        pour <em>pinguer</em> le routeur qui est connecté au votre
        via l'interface série '%d'.""" % i,
        tests = (
        require_ping,
        require("{C0.remote_port.host.S%d.remote_port.ip}" % i,
                "Je ne vois pas l'adresse IP du routeur distant",
                parse_strings=host),
        good("ping {C0.remote_port.host.S%d.remote_port.ip}" % i,
             parse_strings=host),
        ),
        )

    add(name="routeur>remote s%d OK" % i,
        required=["routeur>remote s%d" % i],
        question = """Répondez OUI à cette question seulement
        si le ping distant sur le port série '%d' a fonctionné correctement"""%i,
        tests = ( yes('Tapez OUI'), ),
        )

    # ATTENTION cela ne fonctionne que les S0 sont tous connectés à des S1
    add(name="routeur>s%d routeur" % i,
        required=["routeur>remote s%d OK" % i],
        before="""Puisque le ping sur le routeur distant via
        l'interface série '%d' fonctionne, nous allons aller un peu
        plus loin en pinguant l'autre interface série du routeur
        distant.""" % i,
        question="""Donnez la ligne commande que vous tapez sur votre routeur
        pour <em>pinguer</em> l'autre interface série du routeur connecté
        sur l'interface série '%d' de votre routeur.
<pre>
              S%d           Sx        Sy
Votre routeur <------------> Routeur <----------

Vous voulez pinguer Sy.
        </pre>""" % (i,i),
        tests = (
        require_ping,
        require("{C0.remote_port.host.S%d.remote_port.host.S%d.port.ip}"% (i,i),
                "Je ne vois pas l'adresse IP du routeur distant",
                parse_strings=host),
        good("ping {C0.remote_port.host.S%d.remote_port.host.S%d.port.ip}" % (i,i),
             parse_strings=host),
        ),
        )

    add(name="routeur>s%d routeur ?" % i,
        required=["routeur>s%d routeur" % i],
        question = """Le ping à partir de votre routeur
        via le port série '%d' sur l'autre port série
        du routeur distant a-t-il fonctionné correctement
        (oui ou non)&nbsp;?""" % i,
        tests = ( no("""Il est impossible que ce ping ait fonctionné
        correctement car votre routeur n'a pas de route par défaut.
        Ceci veut dire que ne connaissant pas de routes,
        il peut seulement communiquer avec les réseaux qui
        lui sont directement connectés."""), ),
        good_answer = """C'est normal, le routeur ne sait pas à qui envoyer
        ce paquet car il ne connait aucune route""",
        highlight = True,
        )


add(name="branchement",
    required=["genre", "serie:affiche", "routeur série 0",
              "routeur série 1"],
    before="""Branchez les cables séries entre votre routeur
    et les deux autres.
    <p>
    Des messages vont apparaître automatiquement sur l'écran,
    continuez à travailler sans en tenir compte.
    Ils indiquent qu'un cable a été branché.
    <p>
    Attention, quand un message s'affiche alors que vous
    êtes en train de tapez une commande,
    le routeur n'a pas oublié ce que vous avez tapé avant.
    Si vous appuyez sur Return le début de la commande que
    vous avez tapé sera exécuté.
    """,
#     question="""Utilisez la commande <tt>show</tt>
#     pour voir les informations sur la connexion série.
#     <p>
#     Qu'est-ce que le routeur CISCO vous affiche
#     pour indiquer qu'il y a un cable branché&nbsp;?""",
#     tests=(
#    good("line protocol is up"),
    question = """Avez-vous bien branché tous les câbles en respectant
    les DCT/DTE indiqués sur les plans et sans avoir inversé
    le port série 0 et 1&nbsp;?""",
    tests = (
    yes(),
    ),
    )
