# -*- coding: latin-1 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2008 Thierry EXCOFFIER, Olivier GLÜCK, Universite de Lyon
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

add(name="zone",
    required=["intro:avantages", "intro:inconvénients"],
    before = """On vous propose dans cette partie de :
    <ul>
   <li> mettre en place un serveur DNS primaire qui soit serveur de source
   autorisée pour la zone de votre salle de TP dont vous avez la charge&nbsp;;
   <li> tester le bon fonctionnement local du serveur à partir des machines
   clientes de la salle&nbsp;;
   <li> mettre en place un serveur racine (primaire ou secondaire)
   et tester l'interrogation du serveur DNS de l'autre salle de TP&nbsp;;
   <li> analyser les échanges de requêtes/réponses DNS entre les différents
   serveurs.
   </ul>
   <p>
   Pour simplifier, les zones DNS seront des TLD (Top Level Domain)
   et les machines seront nommées par le biais de leur adresse IP.
   <p>
   Par exemple, les machines de la salle TPR1 seront dans la
   zone <tt>.tpR1.</tt> et seront référencées dans le serveur DNS
   de la façon suivante&nbsp;;:
   <ul>
   <li> <tt>m1.tpR1</tt> pour <tt>192.168.1.1</tt>
   <li> <tt>m10.tpR1</tt> pour <tt>192.168.1.10</tt>
   </ul>
   <p>
   Si plusieurs binômes mettent en place un serveur DNS dans la même salle,
   mettez en place une zone par binôme en vous répartissant les plages
   d'adresses IP gérées de manière équitable.
   <p>
   Si par exemple deux binômes sont en charge du DNS dans la salle TPR2&nbsp;:
   <ul>
   <li> Le binôme A sera en charge de la zone <tt>.tpR2A.</tt>
   son serveur DNS primaire référencera les machines ayant une adresse
   IP impaire.
   <li> Le binôme B sera en charge de la zone <tt>.tpR2B.</tt>
   son serveur DNS primaire référencera les machines ayant une adresse
   IP paire.
   </ul>
   """,
    question = "Quelle est votre zone DNS&nbsp;?",
    tests = (good_if_contains(''),),
    )

add(name="plage",
    required=["intro:avantages", "intro:inconvénients"],
    question = "Quelle est votre plage d'adresse IP&nbsp;?",
    tests = (good_if_contains(''),),
    )

add(name="install",
    required=["zone", "plage"],
    question = """Quelle commande tapez-vous pour installer les paquets
    nécessaires à la mise en place d'un serveur DNS&nbsp;?""",
    tests = (good_if_contains(''),),
    )



add(name="named.conf",
    required=["install"],
    question = """Que modifiez-vous dans le fichier <tt>named.conf</tt>
    pour configurer votre machine afin qu'elle soit un serveur DNS&nbsp;?
    <p>
    Vous aurez 0 points si vous dépassez 10 lignes dans la réponse.
    """,
    nr_lines = 10,
    tests = (good_if_contains(''),),
    )

add(name="zones",
    required=["install"],
    question = """Que modifiez-vous dans les fichiers de zone.
    Donnez uniquement pour chaque fichier de zone <b>un ou deux</b>
    exemples de chaque type de RR (<em>Resource Record</em>) utilisé.
    <p>
    Vous aurez 0 points si vous dépassez 30 lignes dans la réponse.
    """,
    nr_lines = 30,
    tests = (good_if_contains(''),),
    )

add(name="creation zone",
    required=["install"],
    before = """Le nombre de machines à renseigner étant important,
    on vous suggère de générer automatiquement vos fichiers de zone à l'aide
    d'un petit programme C ou script shell par exemple.
    <p>
    N'oubliez pas de renseigner la zone inverse.""",
    question = """Expliquez comment vous générez les fichiers de zone,
    donnez l'algorithme ou le programme.""",
    nr_lines = 10,
    tests = (good_if_contains(''),),
    )

add(name="lancement",
    required=["named.conf", "zones", "creation zone"],
    before = """Démarrez le serveur DNS""",
    question = "Quelle commande permet de démarrer le serveur DNS&nbsp;?",
    tests = (good_if_contains(''),),
    )

add(name="logs",
    required=["named.conf", "zones", "creation zone"],
    question = """Où sont les fichiers de logs du serveur DNS&nbsp;?""",
    indices = ('Cherchez dans <tt>/var/log</tt>',),
    good_answer = '''Pensez à regarder les logs du serveur DNS à chaque démarrage du serveur.''',
    tests = (good_if_contains(''),),
    )

add(name="noms logiques",
    required=["lancement"],
    before = """On vous demande maintenant de donner des noms plus parlants
    à certaines machines telles que les serveurs NFS, les serveurs NIS,
    les serveurs DNS, les serveurs LDAP, et ce sans changer le nom canonique.
    <p>
    On pourra par exemple donner des noms tels que <tt>dns1.tpR1</tt>,
    <tt>nfs1.tpR2</tt>, <tt>nis2.tpR2A</tt>, ...
    <p>
    Pour ce faire, vous demanderez aux binômes de votre zone les
    services qu'ils mettent en place et les adresses IP qu'ils utilisent.
    """,
    question = """Comment procédez vous&nbsp;?
    <p>
    Mettez en place cettenouvelle configuration.
    <p>
    Vous aurez 0 points si vous dépassez 10 lignes dans la réponse.
    """,
    nr_lines = 10,
    tests = (good_if_contains(''),),
    )


add(name="client",
    required=["noms logiques"],
    before = """Configurez un client DNS de votre zone avec comme nom de
    domaine par défaut celui de votre zone et comme serveur DNS local
    le serveur primaire de la zone (le vôtre !).""",
    question = "Comment avez-vous fait&nbsp;?",
    nr_lines = 10,
    tests = (good_if_contains(''),),
    )

add(name="dig",
    required=["client"],
    question = """Dans la commande <tt>dig @server name type</tt>,
    précisez ce que signifie chaque paramètre.""",
    nr_lines = 5,
    tests = (good_if_contains(''),),
    )

add(name="dig host",
    required=["dig"],
    question = """Donnez la syntaxe équivalente à
    <tt>dig @server name type</tt>
    avec la commande <tt>host</tt>""",
    nr_lines = 5,
    tests = (good_if_contains(''),),
    )






add(name="connue",
    required=["dig"],
    question = """Quelle ligne de commande permet de vérifier que votre
    machine cliente est bien enregistrée dans le serveur DNS
    de votre zone&nbsp;?""",
    nr_lines = 5,
    tests = (good_if_contains(''),),
    )

add(name="inverse",
    required=["dig"],
    question = """Quelle ligne de commande permet de vérifier que votre
    machine cliente est bien enregistrée dans la zone inverse&nbsp;?""",
    nr_lines = 5,
    tests = (good_if_contains(''),),
    )

add(name="serveurs",
    required=["dig"],
    question = """Quelle ligne de commande permet de lister les serveurs
    primaire et secondaires de votre zone&nbsp;?""",
    nr_lines = 5,
    tests = (good_if_contains(''),),
    )

add(name="contact",
    required=["dig"],
    question = """Quelle ligne de commande permet de connaître l'adresse
    e-mail de l'administrateur de la zone&nbsp;?""",
    nr_lines = 5,
    tests = (good_if_contains(''),),
    )

add(name="alias",
    required=["dig"],
    question = """Quelle ligne de commande permet de lister tous les alias
    de votre zone (et uniquement eux)&nbsp;?""",
    nr_lines = 5,
    tests = (good_if_contains(''),),
    )

add(name="tout",
    required=["dig"],
    question = """Quelle ligne de commande permet de connaître l'ensemble
    des enregistrements référencés par votre serveur DNS&nbsp;?""",
    nr_lines = 5,
    tests = (good_if_contains(''),),
    )


add(name="commentaire",
    required=["connue", "inverse", "serveurs", "contact", "alias", "tout"],
    question = """Pour les différentes commandes que vous avez essayé
    (elles sont listées sur cette page)
    indiquez si vous avez bien obtenu le résultat escompté&nbsp;:""",
    nr_lines = 5,
    tests = (good_if_contains(''),),
    )

# 5.3

add(name="racine",
    required=["commentaire"],
    before = """Entendez-vous avec les autres binômes s'occupant du DNS
    pour configurer une machine en tant que passerelle entre les deux salles
    de TP.
    <p>
    Vérifier à l'aide de la commande <tt>ping</tt> que vous
    arrivez à joindre le serveur DNS de l'autre salle.
    <p>
    N'oubliez pas de configurer sur les machines clientes la route par
    défaut vers la passerelle&nbsp;!
    <p>
    Vous prendrez comme passerelle la machine à côté
    du switch central avec les adresses IP 192.168.1.1 et 192.168.2.1
    """,
    question = """Indiquez les zones DNS, machines et adresses IP pour
    l'enseble des deux salles&nbsp;:""",
    nr_lines = 20,
    tests = (good_if_contains(''),),
    )

dig = """Pour cette question, vous utiliserez la commande <tt>dig</tt>
    sans PUIS avec l'option <tt>+trace</tt> pour voir plus précisément ce qui
    se passe (enchaînement des requêtes entre les différents serveurs DNS
    potentiels)."""


imaginaire = """A partir d'une machine cliente configurée pour interroger
votre serveur DNS, que se passe t-il si vous essayez de résoudre le nom
d'une machine imaginaire (par ex. <tt>www.google.fr</tt>) qui n'est
référencée dans aucun des serveurs DNS installés&nbsp;?"""

add(name="imaginaire",
    required=["commentaire"],
    before = dig,
    question = imaginaire,
    nr_lines = 10,
    tests = (good_if_contains(''),),
    )

autre = """A partir d'une machine cliente configurée pour interroger
votre serveur DNS, que se passe t-il si vous essayez de résoudre le nom
d'une machine est référencée dans un autre serveur DNS
(par exemple celui de l'autre salle)&nbsp;?"""

add(name="autre",
    required=["commentaire"],
    before = dig,
    question = autre,
    nr_lines = 10,
    tests = (good_if_contains(''),),
    )

directe = """Que se passe t-il si vous essayez de résoudre le nom
d'une machine est référencée dans un autre serveur DNS
(par exemple celui de l'autre salle) en interrogeant directement
l'autre serveur DNS&nbsp;?"""

add(name="directe",
    required=["commentaire"],
    before = dig,
    question = directe,
    nr_lines = 10,
    tests = (good_if_contains(''),),
    )




##add(name="trace",
##    required=["imaginaire", "autre", "directe"],
##    question = "Refaites les commandes avec <tt>+trace</tt>, conclusions&nbsp;?",
##    nr_lines = 10,
##    tests = (good_if_contains(''),),
##    )


add(name="racines",
    required=["imaginaire", "autre", "directe"],
    before = """Sur une autre machine que la vôtre (si possible),
    mettez en place un serveur racine qui référence l'ensemble des zones DNS
    mises en place.
    <p>
    Entendez-vous avec les autres binômes DNS pour savoir si vous êtes serveur
    racine primaire (zone de type <em>master</em>)
    ou secondaire (zone de type <em>slave</em> : <tt>man named.conf</tt>).
    <p>
    Vous prendrez comme adresse IP pour votre serveur racine&nbsp;:
    <ul>
    <li> 192.168.2.19 (ou .18) si vous êtes dans la salle TPR1
    <li> 192.168.1.19 (ou .18) si vous êtes dans la salle TPR2.
    </ul>""",
    question = """Pour votre serveur racine primaire ou secondaire
    indiquez l'adresse IP et les modifications faites dans <tt>named.conf</tt>.
    <p>
    Vous aurez 0 points si vous dépassez 10 lignes dans la réponse.
    """,
    nr_lines = 10,
    tests = (good_if_contains(''),),
    )

add(name="racines zone",
    required=["racines"],
    before = """Mettez à jour le fichier de zone racine de votre serveur DNS
    primaire et relancez le.""",
    question = """Contenu du fichier de la zone racine&nbsp;:
    <p>
    Vous aurez 0 points si vous dépassez 20 lignes dans la réponse.
    """,
    nr_lines = 20,
    tests = (good_if_contains(''),),
    )

dig = """<b><big>
Maintenant que le serveur DNS racine est configuré et fonctionne</big></b>"""

more = """<p>
Indiquez l'enchainement des requêtes/réponses DNS en précisant bien
la nature des serveurs DNS impliqués.
<p>
Vous préciserez également la nature des requêtes/réponses
(itérative ou récursive)."""

add(name="imaginaire2",
    required=["racines"],
    before = dig,
    question = imaginaire + more,
    nr_lines = 10,
    tests = (good_if_contains(''),),
    )

add(name="autre2",
    required=["racines"],
    before = dig,
    question = autre + more,
    nr_lines = 10,
    tests = (good_if_contains(''),),
    )

add(name="directe2",
    required=["racines"],
    before = dig,
    question = directe + more,
    nr_lines = 10,
    tests = (good_if_contains(''),),
    )


add(name="débranche",
    required=["imaginaire2", "autre2", "directe2"],
    question = """Que se passe t-il si vous débranchez le câble réseau
    du serveur racine primaire et que vous essayez des requêtes&nbsp;:""",
    nr_lines = 10,
    tests = (good_if_contains(''),),
    )

#

add(name="resolv",
    required=["racines"],
    before = """Sur une machine cliente, ajoutez les suffixes des autres
    zones DNS dans le fichier <tt>/etc/resolv.conf</tt>.""",
    question = """Les modifications que vous avez faites dans le fichier
    <tt>/etc/resolv.conf</tt>&nbsp;:""",
    nr_lines = 5,
    tests = (good_if_contains(''),),
    )

add(name="ping",
    required=["resolv"],
    question = """Faites <tt>ping m138</tt> et notez l'adresse
    IP correspondante&nbsp;:""",
    tests = (good_if_contains(''),),
    )

add(name="ping2",
    required=["resolv"],
    before = """Changez l'ordre des suffixes dans <tt>/etc/resolv.conf</tt>
    puis refaites <tt>ping m138</tt>""",
    question = "Notez l'adresse IP correspondante.&nbsp;:""",
    tests = (good_if_contains(''),),
    )

add(name="différence",
    required=["ping", "ping2"],
    question = "Expliquez les conséquences du changement d'ordre des suffixes&nbsp;:",
    nr_lines = 5,
    tests = (good_if_contains(''),),
    )

#


add(name="expérience 1",
    required=["resolv"],
    before = """Vous pouvez expérimenter un échange de zones entre un serveur
    de noms racine primaire et un serveur racine secondaire.
    <p>
    Modifiez sur le serveur primaire le numéro de série dans l'enregistrement
    SOA (comme si vous aviez modifié le fichier de zone) et relancez
    le service.
    <p>
    Relancez ensuite le service sur le serveur de noms secondaire.
    """,
    question = """Que constatez-vous dans le fichier de zone du serveur
    secondaire&nbsp;?
    <p>
    Regardez également les dates de dernière modification du fichier.""",
    nr_lines = 10,
    tests = (good_if_contains(''),),
    )

add(name="expérience 2",
    required=["resolv"],
    before = """Vous pouvez expérimenter une autre procédure d'échange,
    mais cette fois sans relancer le serveur de noms secondaire.
    <p>
    Modifiez d'abord sur les deux serveurs le délai de rafraîchissement
    (refresh) et mettez-le à 2 minutes.
    <p>
    Relancez les services.
    <p>
    Modifiez sur le serveur primaire le numéro de série et relancez le
    service.""",
    question = """Que constatez-vous au bout de 2 minutes
    sur le serveur secondaire&nbsp;?""",
    nr_lines = 10,
    tests = (good_if_contains(''),),
    )

# 5.4

add(name="wireshark",
    required=["resolv"],
    before = """Visualiser avec <tt>wireshark</tt> les échanges de
    requêtes/réponses DNS correspondant à une résolution de nom vers
    une machine de l'autre salle pour laquelle vous n'avez encore jamais
    effectué la résolution de nom.""",
    question = """Indiquez le nombre de requêtes/réponses pour
    cette résolution ainsi que les fanions de la réponse DNS.""",
    nr_lines = 10,
    tests = (good_if_contains(''),),
    )

add(name="wireshark 2",
    required=["wireshark"],
    before = """Visualiser avec <tt>wireshark</tt> les échanges de
    requêtes/réponses DNS correspondant à la
    <b>deuxième</b> résolution du
    <b>même nom</b> de machine qu'à la question précédente.""",
    question = """Indiquez le nombre de requêtes/réponses pour
    cette résolution ainsi que les fanions de la réponse DNS.""",
    nr_lines = 10,
    tests = (good_if_contains(''),),
    )



add(name="nouvelle",
    required=["resolv"],
    before = """On suppose que les quatre services sont correctement
    configurés et que vous êtes promus administrateur de l'ensemble du réseau.
    Un nouvel utilisateur arrive dans l'organisation avec une machine neuve
    installée sous Linux.""",
    question = """Citez précisément les opérations que vous devez effectuer
    afin d'intégrer complètement ce nouvel utilisateur et sa machine dans
    votre réseau (vous donnerez un nom de machine et un nom de login à ce
    nouvel arrivant).
    <p>Cet utilisateur devra pouvoir s'authentifier sur n'importe quelle
    machine du réseau et sa machine devra être accessible aux
    autres par son nom.""",
    default_answer = "Nom de machine : .......... Nom de login : ........\n",
    nr_lines = 10,
    tests = (good_if_contains(''),),
    )

add(name="totale",
    required=["nouvelle"],
    question = """Configurez une machine qui soit à la fois client NFS,
    client NIS, client LDAP et client DNS.
    <p>
    Changez l'ordre d'utilisation des services en
    configurant le fichier <tt>nsswitch.conf</tt>.
    <p>
    Comment testez-vous que tout fonctionne correctement&nbsp;?""",
    nr_lines = 10,
    tests = (good_if_contains(''),),
    )




















