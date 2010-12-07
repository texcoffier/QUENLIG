# -*- coding: latin-1 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2005-2006 Thierry EXCOFFIER, Universite Claude Bernard
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

add(name="intro",
    required=["sh:console", "sh:répertoire courant",
              "sh:répertoire connexion"],
    question="""Quel est le nom de la commande permettant d'avoir
    des informations sur les fichiers et le contenu des répertoires.""",
    tests=(
    good("ls"),
    bad("cat",
        "Cette commande permet d'afficher le <b>contenu</b> des fichiers"),
    bad('file',
        """Cette commande est très utile, mais elle ne permet pas de lister
        le contenu des répertoires"""),
    
    reject(" ", "Seulement le nom de la commande, pas d'options"),
    ),
    )

add(name="nommé",
    required=["intro"],
    question="""Donnez la commande permettant de lister les noms des fichiers (et répertoires) qui se trouvent dans <tt>/usr</tt>""",
    tests=(
    shell_good("ls /usr"),
    shell_bad("ls /usr/",
              "Cela fonctionne mais, on peut faire un caractère plus court"),
    shell_bad("ls usr",
              """Cela ne fonctionne que si votre répertoire courant
              est <tt>/</tt>"""),
    shell_bad("ls /usr/*",
              """Cela va trop en lister, en effet cela va lister le contenu
              des répertoires qui se trouvent dans <tt>/usr</tt>
              alors que l'on ne veut que leur nom."""),
    require("/usr",
            
            """Comment pouvez-vous lister le contenu de <tt>/usr</tt>
            sans faire référence à <tt>/usr</tt> dans la
            ligne de commande&nbsp;?"""),
    reject("-", "Il n'y a pas besoin de donner des options à <tt>ls</tt>"),
    shell_display,
    ),
    )

add(name="affichage long",
    required=["intro"],
    question="""Quelle ligne de commande utilisant <tt>ls</tt>
    permet d'afficher plus d'informations sur les fichiers&nbsp;?""",
    tests=(
    shell_good("ls -l"),
    reject("a",
           """L'option <tt>-a</tt> permet de voir les fichiers
           cachés, cela permet de voir plus de fichier mais ne permet pas
           d'avoir plus d'informations"""),
    require("ls",
            "Donnez la ligne de commande complète, pas seulement l'option"),
    answer_length_is(5, """La bonne réponse fait 5 caractères
    en comptant l'espace"""),
    shell_display,
    ),
    indices=("""Pour s'en rappeler&nbsp;: c'est pour afficher une
    <b>l</b>ongue liste d'information sur les fichiers""",
             "Tapez <tt>ls --help</tt> pour lister les options",
             ),
    )


f = """La commande <tt>ls -l /tmp/toto</tt> affiche (si votre langue est le français)&nbsp;:
    <pre>-rwxr-xr-x   1 exco   liris      18 Jan 19  2005 /tmp/toto</pre>"""

add(name="nom court",
    required=["affichage long"],
    question=f + """Quel est le nom court du fichier (pas le chemin)&nbsp;?""",
    tests=(
    good("toto"),
    reject("/",
           """Un nom court ne peut contenir de <tt>/</tt>
           contrairement au nom relatif ou absolu (un chemin)"""),
    reject('exco', "C'est le propriétaire du fichier"),
    reject('liris', "C'est le groupe propriétaire du fichier"),
    ),
    )

add(name="taille",
    required=["affichage long"],
    question=f + """Quel est le nombre d'octets contenu dans le fichier&nbsp;?""",
    tests=(
    good("18"),
    bad("1", "Ça c'est le nombre de noms différents que porte le fichier"),
    bad("2005", "C'est l'année de modification du fichier"),
    bad("19", "C'est date (jour du mois) de modification du fichier"),
    bad("4", "Nombre d'octets dans le fichier, pas dans son nom"),
    bad("10", """Je pense que vous avez un problème de vue,
    peut-être faut-il augmenter la taille des caractères&nbsp;?"""),
    bad("0", "Expliquez à votre enseignant pourquoi vous avez répondu cela"),
    require_int(),
    ),
    )

add(name="propriétaire",
    required=["affichage long"],
    question=f + """Qui est l'utilisateur propriétaire de ce fichier&nbsp;?""",
    tests=(
    good("exco"),
    bad('liris', "Non, ça c'est le groupe propriétaire"),
    ),
    )

add(name="jour",
    required=["affichage long"],
    question=f + """Quel jour du mois de janvier ce fichier a été modifié&nbsp;?""",
    tests=(
    bad("18", "Vous venez d'indiquer la taille du fichier en octet"),
    good("19"),
    require_int(),
    ),
    )

w = "Les \" ou ' ne changent pas le fait que <tt>-z</tt> est compris comme une option par la commande."

add(name="spécial",
    required=["intro"],
    question="""Donnez la ligne de commande pour lister
    avec l'option <tt>-l</tt> les informations sur
    le fichier nommé <tt>-z</tt>
    <p>
    Vous n'avez pas besoin de lire les manuels pour répondre
    à cette question.
    """,
    tests=(
    reject('--',
           """Le -- n'est pas standard, on ne le trouve que dans
           les commandes créées par la FSF (GNU).
           Trouver une autre astuce portable."""),
    shell_good("ls -l ./-z"),
    reject((" '-z'", ' "-z"', ' \\-z'),
           """Les \" ou ' ou \\ ne changent pas le fait que <tt>-z</tt>
           soit compris comme une option par la commande car
           elle ne voit pas les caractères d'échappement du shell.
           En effet, le tiret n'est pas un caractère spécial pour le shell.
           """),
    shell_bad("ls -l -z", "<tt>ls</tt> croit que <tt>-z</tt> est une option"),
    reject(("*z", "?z", "[-]z"),
           """Le fait d'utiliser un <em>pattern</em> ne change rien.
           En effet, après la substitution faite par
           le shell la commande <tt>ls</tt> recevra
           un argument <tt>-z</tt> qu'elle prendra
           pour une option"""),
    require("-l", "Ou est passée l'option <tt>-l</tt>&nbsp;?"),
    require("-z", "Je ne vois nulle part le nom du fichier <tt>-z</tt>"),
    reject(' /', """Vous faites référence à un fichier dans la racine,
    ce n'est pas le cas de <tt>-z</tt>"""),
    reject(';', """Vous n'avez pas besoin d'utilisez d'autre commandes
    que <tt>ls</tt>"""),
    reject('\\-', """Cela ne sert à rien de protéger le tiret car
    ce n'est pas un caractère spécial vis à vis du shell"""),
    answer_length_is(len("ls -l ./-z"),
                     """La réponse attendue fait %d caractères""" % len("ls -l ./-z")),
    shell_display,
    ),                 
    indices=("Utilisez un autre nom pour ce fichier afin qu'il ne commence pas par un caractère <tt>-</tt>",
             "Le répertoire courant est <tt>.</tt>",
             "Faites un chemin relatif au répertoire courant",
             ),
    )

f = """La commande <tt>ls -l</tt> affiche&nbsp;:
    <pre>lrwxrwxrwx   1 exco   liris      13 Jan 19  2005 /tmp/toto -> ../etc/passwd</pre>"""


add(name="lien symbolique",
    required=["nom court", "propriétaire"],
    before="""Si le raccourci est un chemin relatif,
    alors il est évalué en fonction du répertoire
    dans lequel se trouve le lien.""",
    question=f + """Quel est le nom (chemin) absolu du fichier pointé
    par ce raccourci (<tt>../etc/passwd</tt>) &nbsp;?""",
    tests=(
    good("/etc/passwd"),
    good("/tmp/../etc/passwd", "Une réponse plus courte est '/etc/passwd'"),
    bad("../etc/passwd",
        """C'est bien le chemin relatif par rapport à <tt>/tmp</tt>
        mais on vous demande le chemin <b>absolu</b>"""),
    bad("/tmp/toto", """Non, ça c'est le nom du lien, pas le nom
    de la chose pointée"""),
    require("passwd",
            """Le nom court du fichier pointé est <tt>passwd</tt>
            Cela n'apparaît pas dans votre réponse"""),
    reject("toto",
            """Il n'y a <tt>toto</tt> nulle part dans le
            nom du fichier pointé par <tt>/tmp/toto</tt>"""),
    require("/",
            """On vous demande un chemin absolu,
            cela commence donc forcément par <tt>/</tt>"""),
    bad("/tmp/etc/passwd",
        """Votre réponse ne correspond pas à <tt>../etc/passwd</tt>
        en relatif par rapport à <tt>/tmp</tt>"""),
    bad("/passwd",
        """Réfléchissez encore.
        Le raccourci est vers <tt>../etc/passwd</tt>"""),
    require_startswith('/',
                       """On vous demande un chemin absolu,
                       il commence donc par un slash"""),
    expect('etc'),
    shell_display,
    ),
    bad_answer="C'est le chemin absolu le plus court qui est la bonne réponse",
    indices=(
    """Votre réponse ne dépend pas de votre répertoire courant""",
    """Pour trouver la réponse&nbsp;:
    <ul>
    <li> Concaténez le nom absolu du répertoire contenant le lien symbolique
    avec la valeur du lien symbolique.
    <li> Raccourcicez le nom du fichier en enlevant les <tt>..</tt>
    sans changer sa destination.
    </ul>""",
    ),
   
    )

ls_is_required=require("ls","""Vous devez utiliser la commande <tt>ls</tt>""")

add(name="trié par date",
    required=["jour"],
    question="""Quelle ligne de commande permet de lister les noms
    des fichiers (sans afficher les autres informations) en les triant
    par date de modification du contenu.""",
    tests=(
    shell_good("ls -t"),
    shell_bad("ls -c",
              """Cela trie par date de modifications des 'meta-informations'
              comme le propriétaire, le mode, ...
              Cela ne trie pas par date de modification du contenu"""
              ),
    ls_is_required,
    reject("-l",
           """Que les noms des fichiers, rien d'autre.
           Enlevez l'option inutile."""),
    reject('|', """N'utilisez pas un <em>pipe</em> cherchez la bonne option
    de la commande <tt>ls</tt>"""),
    shell_bad('ls', "Sans options ils sont triés dans l'ordre alphabétique"),
    reject('--sort', """Les options longues (avec 2 tirets) ne sont pas
    standards."""),
    shell_display,
    ),
    indices=("""Pour s'en rappeler&nbsp;: c'est pour
    trier par <em><b>t</b>ime</em> les fichiers""",
             "Tapez <tt>ls --help</tt> pour lister les options",
             ),
    )

add(name="trié par taille",
    required=["taille"],
    question="""Quelle ligne de commande permet d'afficher les noms fichiers
    en les triant par taille""",
    tests=(
    shell_good( ("ls -S",) ),
    ls_is_required,
    reject("-t", """L'option <tt>-t</tt> trie par date, pas par taille"""),
    reject("-l", """On ne vous demande pas d'afficher plein d'information
    sur les fichiers, seulement de les trier par taille"""),
    shell_bad("ls -s", "Cela affiche la taille mais ne trie rien"),
    reject('--size', """Les options longues (avec 2 tirets) ne sont pas
    standards."""),
    shell_display,
    ),
    indices=("""Pour s'en rappeler&nbsp;: c'est pour
    trier par <em><b>S</b>ize</em> les fichiers""",
             "Tapez <tt>ls --help</tt> pour lister les options",
             ),
    )

    

   
                  
