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

add(name="genre",
    required=['type s�rie 0'],
    before="""Les cables r�seaux s�ries sont asym�triques,
    il y a un cot� DCE (C : contr�leur) et un cot� DTE.
    Le contr�leur est le cot� femelle.""",
    question="""Le cable que vous devez brancher sur le connecteur
    s�rie z�ro du routeur CISCO
    est-il male (M) ou femelle (F)&nbsp;?
    <p>
    ATTENTION : on ne vous demande pas le genre du connecteur
    que vous branchez sur le routeur CISCO (il est toujours le m�me)
    mais celui qui est � l'autre bout.
    """,
    tests = (
    answer_length_is(1, "Vous devez r�pondre avec M ou F"),
    good("{C0.remote_port.host.S0.port.type}", uppercase=True,
         replace=(('F','DCE'), ('M', 'DTE'),
                  ('FEMELLE','DCE'),('MALE', 'DTE')),
         parse_strings=host),
    ),
    )

for i in range(2):
    add(name="type s�rie %d" % i,
        required=['tp1:nom routeur'],
        before = """Sur la documentation CISCO, DCE est appel� ETCD
        et DTE est appel� ETTD""",
        question="""Quel est le type du cable s�rie que vous devez brancher
        sur votre routeur sur le connecteur s�rie '%d' (c'est
        indiqu� dans le tableau sur le sujet du TP (DCE/DTE))&nbsp;?""" % i,
        tests = (
        good("{C0.remote_port.host.S%d.port.type}" % i,
             uppercase=True, parse_strings=host),
        comment("La r�ponse est soit DCE soit DTE"),
        ),
        good_answer="""Les cables sont physiquement diff�rents,
        si vous utilisez les mauvais cables cela ne fonctionnera pas.
        """
        )

    add(name="routeur s�rie %d" % i,
        required=["tp1:nom routeur"],
        before="La r�ponse � cette question est sur le plan du r�seau",
        question="""Quel est le nom du routeur que vous allez connecter
        au votre via le cable s�rie branch� sur le port s�rie %d
        de votre routeur.""" % i,
        tests = (
        good("{C0.remote_port.host.S%d.remote_port.host.name}" % i,
             uppercase=True, parse_strings=host),
        ),
        )

    add(name="horloge %d" % i,
        required=["type s�rie %d" % i, "doc:intro"],
        question="""Quand vous allez configurer la liaison s�rie '%d' sur
        le routeur, avez-vous besoin de d�finir la fr�quence d'horloge&nbsp;?
        <p>
        R�pondez avec O ou N.""" % i,
        tests = (
        good("{C0.remote_port.host.S%d.port.type}" % i, uppercase=True,
             replace=(('O','DCE'), ('N', 'DTE')),
             parse_strings=host),        
        ),
        indices = ('<a href="http://www.google.com/search?q=serial+clock+dce+dte">Google</a>', ),
        )

    add(name="configure s�rie %d" % i,
        required=["horloge %d" % i, "branchement", "tp1:sauve config",
                  "serie:configure"],
        before=en_mode_serial,
        question="""
        Vous devez configurer l'interface s�rie %d de votre routeur.
        <p>
        Voici la suite de commande pour configurer :
        <pre>ip address IP_INTERFACE_SERIE MASK_INTERFACE_SERIE</pre>
        Si vous devez configurer l'horloge, faites&nbsp;:
        <pre>clock rate 56000</pre>
        Mettez en route l'interface en enlevant
        la commande <tt>shutdown</tt>&nbsp;:
        <pre>no shutdown</pre>
        <p>
        La r�ponse � cette question est la liste des commandes que
        vous avez tap�e.
        <b>Evidemment vous remplacez IP_INTERFACE_SERIE et MASK_INTERFACE_SERIE
        par les valeurs correctes pour votre interface s�rie...</b>
        """ % i,
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
                "Il manque la d�finition de l'horloge (ou elle n'est pas bonne)",
                parse_strings=host),
        reject("{C0.remote_port.host.S%d.port.type}" % i,
               "Il ne faut pas mettre la d�finition de l'horloge",
               replace=( ('clock', 'DTE'), ),
               parse_strings=host),
        good_if_contains('', "Cela devrait �tre bon. Ex�cutez les commandes."),
        ),
        )
    add(name="routeur>local s%d" % i,
        required=["configure s�rie %d" % i],
        before="""Malheureusement, quand une interface r�seau est configur�e,
        on ne peut pas pinguer son adresse locale
        quand le cable n'est pas branch�.
        <p>
        Pour pouvoir pinguer il faut que la liaison soit correctement
        branch�e et configur�e des 2 cot�s.""",
        question="""Donnez la ligne commande que vous tapez sur votre routeur
        pour <em>pinguer</em> l'interface locale de votre liaison
        s�rie '%d'""" % i,
        tests = (
        require_ping,
        require("{C0.remote_port.host.S%d.port.ip}" % i,
                "Je ne vois pas l'adresse IP du port s�rie local",
                parse_strings=host),
        good("ping {C0.remote_port.host.S%d.port.ip}" % i,
             parse_strings=host),
        good("ping ip {C0.remote_port.host.S%d.port.ip}" % i,
             """C'est pas la peine de mettre le param�tre <tt>ip</tt>,
             les r�ponses suivantes avec ce param�tre seront refus�es""",
             parse_strings=host),
        ),
        )

    add(name="routeur>local s%d OK" % i,
        required=["routeur>local s%d" % i],
        question = """R�pondez OUI � cette question seulement
        si le ping local sur le port s�rie '%d' a fonctionn� correctement.
        <p>
        Vous ne devez pas r�pondre <tt>non</tt>."""%i,
        tests = ( yes('Tapez OUI'), ),
        )

    add(name="s�rie %d OK" % i,
        required=["configure s�rie %d" % i, "serie:affiche"],
        question="""R�pondez OUI � cette question seulement si
        la ligne s�rie %d est <tt>up, line protocol is up</tt>.
        <p>
        Si ce n'est pas le cas&nbsp;:
        <ul>
        <li> Attendez que l'autre personne ait configur�e sa liaison s�rie.
        <li> V�rifiez si les param�tres de la ligne sont correctes.
        <li> V�rifiez si le cable n'a pas �t� d�branch�.
        </ul>
        """ % i,
        tests = ( yes('Tapez OUI'), ),
        )
    add(name="routeur>remote s%d" % i,
        required=["s�rie %d OK" % i, "routeur>local s%d OK" % i],
        before="""Puisque le ping local fonctionne, on va aller plus loin
        et franchir le cable.""",
        question="""Donnez la ligne commande que vous tapez sur votre routeur
        pour <em>pinguer</em> le routeur qui est connect� au votre
        via l'interface s�rie '%d'.""" % i,
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
        question = """R�pondez OUI � cette question seulement
        si le ping distant sur le port s�rie '%d' a fonctionn� correctement"""%i,
        tests = ( yes('Tapez OUI'), ),
        )

    # ATTENTION cela ne fonctionne que les S0 sont tous connect�s � des S1
    add(name="routeur>s%d routeur" % i,
        required=["routeur>remote s%d OK" % i],
        before="""Puisque le ping sur le routeur distant via
        l'interface s�rie '%d' fonctionne, nous allons aller un peu
        plus loin en pinguant l'autre interface s�rie du routeur
        distant.""" % i,
        question="""Donnez la ligne commande que vous tapez sur votre routeur
        pour <em>pinguer</em> l'autre interface s�rie du routeur connect�
        sur l'interface s�rie '%d' de votre routeur.
<pre>
              S%d           Sx        Sy
Votre routeur <------------> Routeur <----------

Vous voulez pinguer Sy <small>(il est possible que cela soit impossible,
r�pondez quand m�me � la question)</small>.
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
        question = """Le ping � partir de votre routeur
        via le port s�rie '%d' sur l'autre port s�rie
        du routeur distant a-t-il fonctionn� correctement
        (oui ou non)&nbsp;?""" % i,
        tests = ( no("""Il est impossible que ce ping ait fonctionn�
        correctement car votre routeur n'a pas de route par d�faut.
        Ceci veut dire que ne connaissant pas de routes,
        il peut seulement communiquer avec les r�seaux qui
        lui sont directement connect�s."""), ),
        good_answer = """C'est normal, le routeur ne sait pas � qui envoyer
        ce paquet car il ne connait aucune route""",
        highlight = True,
        )


add(name="branchement",
    required=["genre", "serie:affiche", "routeur s�rie 0",
              "routeur s�rie 1", 'tp1:arr�t marche'],
    before="""Branchez les c�bles s�ries entre votre routeur
    et les deux autres.
    <p>
    Des messages vont appara�tre automatiquement sur l'�cran,
    continuez � travailler sans en tenir compte.
    Ils indiquent qu'un c�ble a �t� branch�.
    <p>
    Attention, quand un message s'affiche alors que vous
    �tes en train de taper une commande,
    le routeur n'a pas oubli� ce que vous avez tap� avant.
    Si vous appuyez sur Return le d�but de la commande que
    vous avez tap� sera ex�cut�.
    """,
#     question="""Utilisez la commande <tt>show</tt>
#     pour voir les informations sur la connexion s�rie.
#     <p>
#     Qu'est-ce que le routeur CISCO vous affiche
#     pour indiquer qu'il y a un c�ble branch�&nbsp;?""",
#     tests=(
#    good("line protocol is up"),
    question = """Avez-vous bien branch� tous les c�bles en respectant
    les DCT/DTE indiqu�s sur les plans et sans avoir invers�
    le port s�rie 0 et 1&nbsp;?""",
    tests = (
    yes(),
    ),
    )
