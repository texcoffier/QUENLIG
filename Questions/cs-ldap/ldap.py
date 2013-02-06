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

general = """
    On souhaite mettre en place un annuaire LDAP qui permette&nbsp;:
    <ul>
    <li> la gestion et l'authentification sous Unix des utilisateurs de
    votre salle de TP&nbsp;;
    <li> la gestion de groupes d'utilisateurs sous Unix&nbsp;;
    <li> la gestion des noms et adresses des machines de la salle.
    </ul>
    <p>
    Réfléchissez au modèle d'information de votre annuaire
    (c'est-à-dire les objets dont vous avez besoin et les schémas LDAP
    que vous allez utiliser) ainsi qu'à l'organisation du DIT (Directory
    Information Tree) que vous allez mettre en place (modèle de nommage).
    """

add(name="informations",
    required=["intro:avantages", "intro:inconvénients"],
    before = general,
    question = """Réflexions sur le modèle d'information&nbsp;:
    Pour chaque type d'objet que vous allez stocker indiquez
    ce qu'ils contiennent et à quoi cela sert.""",
    nr_lines = 5,
    tests = (good_if_contains(''),),
    )

add(name="DIT ?",
    required=["informations"],
    before = general,
    question = """Expliquez avec vos mots ce qu'est le DIT.""",
    nr_lines = 5,
    tests = (good_if_contains(''),),
    )


add(name="DIT",
    required=["DIT ?"],
    question = """Proposez une architecture du DIT&nbsp;:
    Pourquoi ce choix&nbsp;?
    Combien de niveaux&nbsp;?""",
    nr_lines = 5,
    tests = (good_if_contains(''),),
    )

add(name="DN",
    required=["informations"],
    question = """Quelle caractéristique essentielle doit respecter le DN
    (<em>Distinguish Name</em>) d'une entrée&nbsp;?""",
    nr_lines = 2,
    tests = (good_if_contains(''),),
    )

add(name="schema ?",
    required=["informations"],
    question = "Expliquez avec vos mots ce qu'est un <em>schema</em>&nbsp;?",
    nr_lines = 2,
    tests = (good_if_contains(''),),
    )

add(name="DN racine",
    required=["DN"],
    before = """Pour le choix de votre DN racine, on vous demande de
    respecter les conseils de l'IETF qui sont de le construire à partir
    des <tt>dc</tt> (<em>domain components</em>)
    correspondant à l'identité de votre zone DNS.
    Renseignez-vous auprès des binômes en charge du DNS&nbsp;!
    Entendez-vous également avec les autres binômes éventuels mettant un
    annuaire LDAP en place dans la même zone DNS
    (par exemple, si deux binômes font LDAP dans la salle <tt>tpR1</tt>, l'un
    prendra <tt>dc=tpR1A</tt> et l'autre <tt>dc=tpR1B</tt> comme
    <tt>DN</tt> racine).""",
    question = """Que choisissez-vous comme DN racine&nbsp;?
    Pourquoi ce choix&nbsp;?""",
    nr_lines = 5,
    tests = (good_if_contains(''),),
    )

add(name="le DIT",
    required=["DIT"],
    question = """Indiquez les DN que vous avez choisis pour les différentes
    entités du DIT.""",
    nr_lines = 15,
    tests = (good_if_contains(''),),
    )

for i in range(5):
    add(name="DIT entrée %d" % i,
        required=["le DIT"],
        question = "Donnez les informations sur une sorte d'entrée (ou ne répondez pas si vous avez déjà expliqué toutes les sortes d'entrée).",
        nr_lines = 5,
        default_answer = """DN de l'entrée :
C'est un conteneur ou une feuille :
Objet structurel :
Autres objets :
Schéma(s) Nécessaire(s) :""",
        tests = (good_if_contains(''),),
        )


add(name="schéma",
        required=["le DIT", "schema ?"],
        question = "Comment voir dans quel schéma un objet est stocké&nbsp;?",
        nr_lines = 5,
        tests = (good_if_contains(''),),
        )

add(name="pre-installation",
    required=["le DIT"],
    before = """Installez les packages nécessaires à la mise en place
    d'un serveur LDAP.
    <p>
    En cas de mauvaise configuration suite à l'installation des packages,
    vous pouvez reconfigurer votre serveur LDAP avec la commande
    <tt>dpkg-reconfigure slapd</tt>""",
    question = """Quelles informations avez-vous données lors de
    l'installation des <em>packages</em>)&nbsp;?""",
    nr_lines = 5,
    tests = (good_if_contains(''),),
    )

add(name="fichier config",
    required=["pre-installation"],
    question = """Où est stockée la configuration du serveur&nbsp;?""",
    tests = (good_if_contains(''),),
    )

add(name="configuration",
    required=["fichier config"],
    before = """Configurez votre machine pour qu'elle devienne serveur LDAP.
    Prenez garde à modifier, si nécessaire, les champs déjà
    pré-remplis lors de l'installation des packages.""",
    question = """Quelles modifications avez-vous faites dans le
    fichier de configuration du serveur&nbsp;?""",
    nr_lines = 5,
    tests = (good_if_contains(''),),
    )

add(name="redémarrer",
    required=["pre-installation"],
    question = "Comment redémarrer le serveur LDAP&nbsp;?",
    nr_lines = 5,
    tests = (good_if_contains(''),),
    )

add(name="quand",
    required=["redémarrer"],
    question = "Quand est-il nécessaire de redémarrer le serveur LDAP&nbsp;?",
    nr_lines = 5,
    tests = (good_if_contains(''),),
    )

add(name="log",
    required=["pre-installation"],
    question = "Où se trouvent les logs du serveur LDAP&nbsp;?",
    tests = (good_if_contains(''),),
    )


add(name="gq",
    required=["log"],
    before = """Pour voir si votre serveur LDAP fonctionne,
    essayez de vous y connecter avec l'utilitaire <tt>lima</tt>.
    <p>
    Pour savoir comment configurer un client LDAP,
    vous pouvez consulter la page de manuel de <tt>ldap.conf</tt>.
    """,
    question = "Donnez les paramètres de connexion avec <tt>lima</tt>&nbsp;:",
    nr_lines = 5,
    tests = (good_if_contains(''),),
    )


add(name="contenu",
    required=["gq"],
    question = "Quelles sont les entrées présentes dans l'annuaire juste après l'installation (c'est-à-dire avant d'ajouter des entrées)&nbsp;?",
    nr_lines = 5,
    tests = (good_if_contains(''),),
    )

add(name="ldif",
    required=["gq"],
    question = """Ecrivez un fichier au format LDIF
    contenant la description d'une entrée pour chaque type de feuilles
    <p>
    Vous aurez 0 points si vous dépassez 50 lignes dans la réponse.
    """,
    nr_lines = 50,
    tests = (good_if_contains(''),),
    )

add(name="ldapadd",
    required=["ldif"],
    before = """Utilisez la commande <tt>ldapadd</tt> pour ajouter dans
    l'annuaire les entrées que vous venez de décrire dans le fichier LDIF.""",
    question = """Ligne de commande que vous avez utilisé&nbsp;:""",
    tests = (good_if_contains(''),),
    )

add(name="tester",
    required=["ldapadd"],
    question = """Proposez un méthode pour vérifier que les entrées
    ont effectivement été ajoutées&nbsp;?""",
    nr_lines = 5,
    tests = (good_if_contains(''),),
    )

add(name="ajout binome",
    required=["tester"],
    before = """Avec l'utilitaire <tt>lima</tt>
    et en vous appuyant sur les entrées précédentes,
    ajoutez dans l'annuaire une entrée par binôme présent
    dans votre salle de TP et un groupe correspondant à l'ensemble de ces
    binômes.
    <p>
    Vous prendrez comme <em>uid</em> <tt>b1</tt> pour le binôme1, <tt>b2</tt>
    pour le binôme2, ...
    <p>
    Vous prendrez comme répertoire de connexion <tt>/nfshome/b1</tt>
    pour le binôme1...
    <p>
    Pour l'instant, vous mettrez comme mot de passe, l'<em>uid</em>
    du binôme en clair.""",
    question = "Comment procédez-vous&nbsp;?",
    nr_lines = 5,
    tests = (good_if_contains(''),),
    )

add(name="ajout machines",
    required=["tester"],
    before = """Ecrivez un programme ou script qui génère un fichier LDIF
    décrivant toutes les machines de <b>votre</b> zone DNS.
    <p>
    Quelques exemples d'adresse IP&nbsp;:
    <ul>
    <li> <tt>m7.tpR1/192.168.1.7</tt>
    <li> <tt>m9.tpR2/192.168.2.9</tt>
    </ul>""",
    question = """Indiquez le nom de votre zone DNS, le nom canonique
    de votre machine et donnez votre programme ou script&nbsp;:""",
    nr_lines = 15,
    tests = (good_if_contains(''),),
    )

add(name="filtre",
    required=["tester"],
    question = """Citez trois méthodes différentes vous permettant
    de voir tout le contenu de l'annuaire.
    Vous indiquerez le filtre utilisé (permettant de lister toutes
    les entrées).""",
    nr_lines = 15,
    tests = (good_if_contains(''),),
    )

add(name="verif",
    required=["filtre"],
    before = """Essayez une de ces méthodes pour voir si votre
    annuaire contient bien ce que vous y avez mis jusqu'à présent.""",
    question = "C'est bon&nbsp;?",
    tests = (yes('Et bien trouvez pourquoi cela ne marche pas&nbsp;!!!'),),
    )

navigateur = """Si ce n'est déjà fait,
Ouvrez un navigateur pour interroger votre annuaire.
<p>
Sous unix, vous pouvez lancer <tt>konqueror</tt>."""


add(name="filtre rdn",
    required=["filtre"],
    before = navigateur,
    question = """URL pour afficher <b>uniquement</b>
    les <tt>rdn</tt> (<em>relative distinguish name</em>)
    répertoriées de l'annuaire&nbsp;:""",
    nr_lines = 5,
    tests = (good_if_contains(''),),
    )

add(name="filtre membres",
    required=["filtre"],
    before = navigateur,
    question = """URL pour afficher <b>uniquement</b> les membres (nom, uid)
    du groupe contenant l'ensemble des binômes de la salle&nbsp;:""",
    nr_lines = 5,
    tests = (good_if_contains(''),),
    )

add(name="filtre utilisateurs",
    required=["filtre"],
    before = navigateur,
    question = """URL pour afficher <b>uniquement</b> la liste des
    utilisateurs (nom, uid) qui n'appartiennent pas à l'ensemble
    des binômes de la salle&nbsp;:""",
    nr_lines = 5,
    tests = (good_if_contains(''),),
    )

add(name="filtre machine",
    before = navigateur,
    required=["filtre"],
    question = """URL pour afficher <b>uniquement</b> la liste des machines
    répertoriées dans l'annuaire avec son/ses nom(s)
    et son adresse IP&nbsp;:""",
    nr_lines = 5,
    tests = (good_if_contains(''),),
    )

add(name="mot de passe",
    required=["ajout binome"],
    question = """Donnez la ligne de commande <tt>ldapsearch</tt> avec l'option
    <tt>-LLL</tt> qui permet d'afficher pour chaque utilisateur
    référencé dans l'annuaire son <tt>uid</tt> et son mot de passe.""",
    nr_lines = 5,
    tests = (good_if_contains(''),),
    )

add(name="mot de passe admin",
    required=["mot de passe"],
    question = """Qu'affiche la commande <tt>ldapsearch</tt> que vous avez
    donné quand elle est exécutée en tant qu'administrateur&nbsp;:""",
    nr_lines = 5,
    tests = (good_if_contains(''),),
    )

add(name="mot de passe b1",
    required=["mot de passe"],
    question = """Qu'affiche la commande <tt>ldapsearch</tt> que vous avez
    donné quand elle est exécutée en tant qu'utilisateur <tt>b1</tt>&nbsp;:""",
    nr_lines = 5,
    tests = (good_if_contains(''),),
    )

add(name="mot de passe ?",
    required=["mot de passe admin", "mot de passe b1"],
    question = """Affichage des mots de passe par un admin ou non,
    que constatez-vous ? Expliquez.""",
    nr_lines = 5,
    tests = (good_if_contains(''),),
    )

add(name="autorisation",
    required=["mot de passe"],
    before = """Modifiez le fichier <tt>slapd.conf</tt>
    (<tt>man slapd.access</tt>) afin de faire en sorte que l'attribut
    <tt>homeDirectory</tt>&nbsp;:
    <ul>
    <li> ne soit modifiable que par l'administrateur de la base
    <li> ne soit lisible que par les utilisateurs authentifiés.
    </ul>
    Testez si vos modifications sont bien entrées en vigueur
    (vous pourrez utiliser <tt>lima</tt> pour tenter de
    changer la valeur de l'attribut).
    """,
    question = """Quelles sont vos modifications dand <tt>slapd.conf</tt>
    <p>
    Vous aurez 0 points si vous dépassez 10 lignes dans la réponse.
    """,
    nr_lines = 10,
    tests = (good_if_contains(''),),
    )


add(name="authentification",
    required=["mot de passe"],
    before = """On souhaite maintenant permettre aux utilisateurs
    de la salle de s'authentifier <em>via</em> votre annuaire.""",
    question = """Quel(s) fichier(s) modifier et comment&nbsp;?
    Sur le client ou sur le serveur LDAP&nbsp;?""",
    nr_lines = 20,
    tests = (good_if_contains(''),),
    )

add(name="change passwd",
    required=["authentification"],
    before = """On souhaite maintenant permettre aux utilisateurs
    de la salle de changer leur mot de passe.""",
    question = """Quel(s) fichier(s) modifier et comment&nbsp;?
    Sur le client ou sur le serveur LDAP&nbsp;?""",
    nr_lines = 20,
    tests = (good_if_contains(''),),
    )

add(name="vérification",
    required=["authentification"],
    question = """Contrôle du bon fonctionnement avec les commandes
    <tt>id</tt>, <tt>su</tt> ou <tt>telnet</tt>,
    <tt>chown</tt>, <tt>chgrp</tt>, ...
    <p>
    Expliquez et commentez les tests effectués&nbsp;:""",
    nr_lines = 10,
    tests = (good_if_contains(''),),
    )


add(name="passwd",
    required=["change passwd"],
    question = """Après avoir modifié le mot de passe avec la commande
    <tt>passwd</tt>, regardez le contenu de l'attribut <tt>userPassword</tt>
    avec <tt>ldapsearch</tt>.
    <p>
    Commentaire&nbsp;:""",
    nr_lines = 5,
    tests = (good_if_contains(''),),
    )

add(name="hostname",
    required=["vérification"],
    before = """On souhaite maintenant permettre la résolution
    de noms via l'annuaire LDAP.""",
    question = "Que suffit-il de faire&nbsp;?",
    nr_lines = 5,
    tests = (good_if_contains(''),),
    )

add(name="alias",
    required=["hostname"],
    question = """Comment ajoutez-vous un alias sur un nom de machine&nbsp;?
    Le <tt>ping</tt> vers cet alias fonctionne t-il&nbsp;?""",
    nr_lines = 5,
    tests = (good_if_contains(''),),
    )

add(name="wireshark",
    required=["hostname"],
    before = """Mettez en place un moyen de visualiser les échanges entre
    le client et le serveur LDAP.""",
    question = "Quel filtre de capture utilisez-vous&nbsp;?",
    tests = (good_if_contains(''),),
    )

add(name="id",
    required=["wireshark"],
    before = """Exécutez la commande <tt>id b1</tt> à partir d'une autre
    machine que votre serveur LDAP qui soit configurée pour permettre
    l'authentification Unix via votre annuaire.""",
    question = """Résumez brièvement et commentez les échanges LDAP observés
    entre le client et le serveur (nombre de messages, lisibilité des données
    véhiculant dans les requêtes/réponses, ...)&nbsp;:""",
    nr_lines = 20,
    tests = (good_if_contains(''),),
    )

add(name="nouveau",
    required=["id"],
    before = """On suppose que les quatre services sont correctement
    configurés et que vous êtes promus administrateur de l'ensemble du réseau.
    <p>
    Un nouvel utilisateur arrive dans l'organisation avec une machine neuve
    installée sous Linux.
    <p>
    Cet utilisateur devra pouvoir s'authentifier sur n'importe quelle machine
    du réseau et sa machine devra être accessible aux autres par son nom.
    """,
    question = """Citez précisément les opérations que vous devez effectuer
    afin d'intégrer complètement ce nouvel utilisateur et sa machine dans
    votre réseau (vous donnerez un nom de machine et un nom de login à ce
    nouvel arrivant).""",
    nr_lines = 20,
    tests = (good_if_contains(''),),
    )


add(name="total",
    required=["nouveau"],
    before = """Configurez une machine qui soit à la fois client NFS,
    client NIS, client LDAP et client DNS.
    <p>
    Testez le bon fonctionnement des quatre services.
    <p>
    Changez l'ordre d'utilisation des services en configurant le fichier
    <tt>nsswitch.conf</tt>.""",
    question = "Comment testez-vous que tout fonctionne correctement&nbsp;?",
    nr_lines = 20,
    tests = (good_if_contains(''),),
    )














































