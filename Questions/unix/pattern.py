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

etc_required = require("/etc", "On cherche dans <tt>/etc</tt>")
echo_required= require("echo", "On vous dit d'utiliser <tt>echo</tt>")

add(name="intro",
    required=["sh:affiche paramètre", "sh:configurer"],
    question="""En utilisant la commande <tt>echo</tt>&nbsp;:
    Donner la commande affichant la liste des fichiers et
    répertoires contenus dans <tt>/etc</tt> dont le nom
    commence par la lettre 'a'""",
    tests=(
    shell_good("echo /etc/a*"),
    shell_bad(("echo /etc/*a", "echo /etc/*a*"),
              "On vous a dit : <b>commence par la lettre <tt>a</tt></b>"),
    etc_required, echo_required,
    reject('|', """On utilise que la commande <tt>echo</tt>, aucune autre
    commande n'est utile"""),
    reject("ls",
           """On a pas besoin de <tt>ls</tt> car le
           remplacement du <em>pattern</em> fait
            le même travail"""),
    reject("find",
           """<tt>find</tt> cherche en profondeur
           ici on veut simplement les fichiers
           qui sont directement dans <tt>/etc</tt>"""),
    expect('a'),
    require('*', """Vous avez besoin de l'étoile pour indiquer la chaine
    de caractères quelconque qui est après le 'a'"""),
    reject('-', "Pas besoin d'arguments"),
    number_of_is(' ', 1, "Il y a un seul espace dans la réponse"),
    ),
    )

require_star = require("*",
                       """Il faut utiliser un <em>pattern</em>
                       représentant une chaine de caractères
                       quelconques de longueur quelconque.
                       On peut l'utiliser plusieurs fois.""")

reject_dot_slash = reject("./",
                           """Pourquoi indiquer le répertoire courant avec
                           <tt>./</tt>&nbsp;?,
                           par défaut, les noms des fichiers sont relatifs
                           par rapport à lui.""")

star_indice = """Le symbole représentant une chaine de quelconque
    est <tt>*</tt>"""

add(name="tout",
    required=['intro'],
    question="""En utilisant la commande <tt>echo</tt>&nbsp;:
    Donner la commande affichant la liste des fichiers et
    répertoires contenus dans le répertoire courant.
    <p>
    On ne tiendra pas compte des fichiers cachés.""",
    tests=(
    shell_good("echo *"),
    shell_bad("echo *.*", "Seul les noms contenant un point seront affichés"),
    echo_required,
    require_star,
    reject_dot_slash,
    reject('~', "Dans le répertoire courant, pas celui de connexion"),
    ),
    indices=(star_indice,
             ),
   )

add(name="début fin",
    question="""En utilisant la commande <tt>echo</tt>&nbsp;:
    Donner la commande affichant la liste des fichiers et
    répertoires contenus dans <tt>/etc</tt> qui commencent
    par une majuscule et qui se terminent par un chiffre.
    """,
    tests=(
    shell_good("echo /etc/[A-Z]*[0-9]"),
    etc_required, echo_required,
    reject("[1-9]", "Zéro est un chiffre&nbsp;!"),
    reject('Q', "Vous n'allez quand même pas lister tout l'alphabet&nbsp;!"),
    reject('2', "Vous n'allez quand même pas lister tous les chiffres&nbsp;!"),
    require(('[',']'), """On utilise les crochets pour indiquer une liste
    de caractères"""),
    require('-', """On utilise le tiret pour indiquer un interval
    de caractères"""),
    require("[0-9]", "On cherche un chiffre"),
    require("[A-Z]", "On cherche une lettre majuscule"),
    reject('.*', """La syntaxe <tt>.*</tt> est pour les expressions régulìeres,
    par pour les <em>pattern</em>"""),
    ),
   )

add(name="0 au milieu",
    question="""En utilisant la commande <tt>echo</tt>&nbsp;:
    Donner la commande affichant la liste des fichiers et
    répertoires contenus dans <tt>/etc</tt> qui contiennent
    le chiffre '0' n'importe ou dans leur nom.
    """,
    tests=(
    shell_good("echo /etc/*0*"),
    shell_good("echo /etc/*[0]*", "<tt>echo /etc/*0*</tt> était plus simple"),
    shell_bad("echo /etc/*0",
              """Cela n'affiche que les fichiers dont le nom ce termine par
              un caractère <tt>0</tt>"""),
    shell_bad("echo /etc/0*",
              """Cela n'affiche que les fichiers dont le nom commence par
              un caractère <tt>0</tt>"""),
              
    etc_required, echo_required,
    require("0", "Ne confondez pas zéro avec la lettre 'o'"),    
    reject("[0]",
           "Pourquoi mettre <tt>[0]</tt> alors que <tt>0</tt> suffit&nbsp;?"),
    ),
   )

add(name="chemin",
    question="""Dans '/etc' il y a des répertoires dont le nom commence
    par 'rc', ces répertoires contiennent des fichiers
    dont le nom commence par 'S2'.
    <p>
    Utilisez la commande <tt>echo</tt> et le <em>globbing</em>
    pour afficher la liste de ces fichiers.
    """,
    tests=(
    reject('cd', "Vous n'avez besoin que de <tt>echo</tt>"),
    shell_good("echo /etc/rc*/S2*"),
    etc_required, echo_required,
    require("/rc", "Le nom du deuxième niveau commence par <tt>rc</tt>"),    
    require("/S2", "Le nom du troisième niveau commence par <tt>S2</tt>"),
    reject("/rc/", """Le nom du répertoire n'est pas <tt>rc</tt> mais
    commence par <tt>rc</tt>"""),    
    require('S2*', """Le nom des fichiers n'est pas <tt>S2</tt> mais commence
    par <tt>S2</tt>"""),
    ),
    )

add(name="sous répertoires",
    question="""En utilisant la commande <tt>echo</tt>.
    Donner la commande affichant la liste des répertoires
    contenus dans <tt>/etc</tt> (<em>pas les fichiers,
    seulement les répertoires</em>).
    """,
    tests=(
    shell_good( ("echo /etc/*/.", "echo /etc/*/") ),
    etc_required, echo_required,
    shell_bad("echo /etc/*",
              "Cela affiche aussi les fichiers dans <tt>/etc</tt>"),
    shell_bad("echo /etc/.", "Cela affiche <tt>/etc/.</tt>"),
    reject('ls', 'On a pas besoin de <tt>ls</tt>'),
    reject('-', "On a pas besoin d'option"),
    ),
    indices=("Seul un répertoire peut contenir un fichier nommé '.'",
             """On peut mettre une étoile entre deux <tt>/</tt> elle
             sera alors remplacée par tous les noms de répertoires.""",
             ),
   )

add(name="fini par tilde",
    required=['intro'],
    question="""En utilisant la commande <tt>echo</tt>&nbsp;:
    Donner la commande affichant la liste des fichiers et
    répertoires contenus dans le répertoire courant dont le nom se
    termine par <tt>~</tt> (tilde)""",
    tests=(
    reject('echo ~',
           'Dans le répertoire courant, pas le répertoire de connexion'),
    shell_good("echo *~"),
    echo_required,
    require_star,
    reject_dot_slash,
    reject('/', "Pas besoin de / c'est dans le répertoire courant"),
    ),
   )

add(name=".c et .h",
    required=['fini par tilde'],
    question="""En utilisant la commande <tt>echo</tt>&nbsp;:
    Donner la commande affichant la liste des fichiers et
    répertoires contenus dans le répertoire courant dont le nom se
    termine par <tt>.c</tt> ou bien <tt>.h</tt>""",
    tests=(
    reject(('C','H'), "La casse compte"),
    shell_good(("echo *.[ch]", "echo *.[hc]")),
    shell_bad(("echo *.c *.h", "echo *.h *.c"),
              """Il y a plus court, avec une seule étoile."""),
    shell_bad('echo *[.c.h]',
              """Cela affiche les noms qui se terminent par un
              caractère '<tt>.</tt>' ou '<tt>c</tt>' ou '<tt>h</tt>'
              <p>
              De plus les crochets représentent un ensemble,
              cela ne sert à rien de mettre deux fois le même symbole dedans.
              """),
    reject(('[c]', '[h]'),
           """À quoi cela sert d'avoir une liste contenant
           un seul caractère&nbsp;?
           Autant taper le caractère lui même."""),
    echo_required,
    require_star,
    reject_dot_slash,
    number_of_is('*', 1,
                 """On attend une réponse avec une seule étoile
                 suivie d'un caractère qui est un <tt>c</tt>
                 ou un <tt>h</tt>"""),
    shell_bad("echo *[ch]",
              """S'il y a un fichier <tt>tic</tt> il sera affiché,
              et ce n'est pas ce que l'on demande"""),
    shell_bad("echo *.c .h",
              """Affiche la liste des fichiers dont le nom se termine
              par <tt>.c</tt><p> suivi de la chaine de caractère <tt>.h</tt>
              qui ne représente pas un fichier."""),
    shell_bad(("echo *[.ch]", "echo *[.hc]"),
              """Affiche les noms de fichier se terminant
    par <tt>.</tt> ou <tt>c</tt> ou <tt>h</tt>"""),
    reject("[c h]", """<tt>[c h]</tt> représente un <tt>c</tt> ou un
    <tt>espace</tt> ou un <tt>h</tt>"""),
    reject('|',
           """Le pipe (<tt>|</tt>) ne fait pas parti des <em>pattern</em>
           du <em>shell</em> mais des expressions régulières"""),
    require('.', "Il doit y avoir un caractère '.' dans le nom du fichier"),
    reject('{', "Les acolades ne sont pas standard. Ne les utilisez pas"),
    reject(',',
           "Il n'y a pas de virgule dans la syntaxe des <em>pattern</em>"),
    
    answer_length_is(11, "La réponse attendue fait 11 caractères"),
    ),
    indices=(star_indice,
             """Utilisez le pattern désignant un ensemble de caractères
             pour indiquer qu'après le <tt>.</tt> il y a <tt>c</tt>
             ou <tt>h</tt>""",
             """Il faut utiliser les crochets.""",
             ),
   )

add(name="inverse",
    required=["0 au milieu", ".c et .h"],
    question="""En utilisant la commande <tt>echo</tt>.
    Donner la commande affichant la liste des fichiers et
    répertoires contenus dans <tt>/etc</tt> dont le nom
    contient au moins un caractère qui ne soit PAS&nbsp;:
    <ul>
    <li> -
    <li> .
    <li>lettre minuscule
    <li>lettre majuscule
    <li>numérique
    </ul>
    Conservez l'ordre pour que votre réponse soit acceptée (j'ai pas
    envie de tester tous les cas possibles).
    <em>Pour que cela fonctionne dans la réalité, le tiret doit être en premier pour ne pas désigner un intervalle.</em>
    """,
    tests=(
    shell_good("echo /etc/*[!-.a-zA-Z0-9]*"),
    echo_required, etc_required,
    reject('\\',
           "Pas besoin d'<em>antislash</em> pour répondre à cette question"),
    shell_bad("echo /etc/[!-.a-zA-Z0-9]",
              """Vous ne trouvez que des noms de fichier ne comportant
              qu'un seul caractère"""),
    shell_bad("echo /etc/*[!-.a-zA-Z0-9]",
              """Vous ne trouverez pas <tt>/etc/=a</tt>
              qui contient un caractère interdit mais se termine
              par un caractère autorisé"""),
    shell_bad("echo /etc/[!-.a-zA-Z0-9]*",
              """Vous ne trouverez pas <tt>/etc/a=</tt>
              qui contient un caractère interdit mais commence
              par un caractère autorisé"""),
    reject(("]]", "]["), "N'imbriquez pas les crochets, une seule paire suffit"),
    reject('![', """Le <tt>!</tt> de la négation est juste après
    le crochet ouvrant, pas avant."""),
    require("!", "La négation s'indique avec le <tt>!</tt>"),
    number_of_is('!', 1, "Une seule négation est suffisante"),
    require("a-z", "Et les minuscules&nbsp;?"),
    require("A-Z", "Et les majuscules&nbsp;?"),
    require("0-9", "Et les nombres&nbsp;?"),
    require("-.", "Et le tiret et le point&nbsp;? Il faut conserver l'ordre."),
    require("-.a-zA-Z0-9", "Il faut conserver l'ordre"),
    ),
    good_answer="Si 'echo' vous affiche <tt>/etc/*[!-.a-zA-Z0-9]*</tt> c'est que '/etc' ne contient pas de tel fichier",
   )

add(name="final",
    required=["inverse", "sous répertoires"],
    question="""En utilisant la commande <tt>echo</tt>.
    affichez tous les fichiers avec l'extension <tt>.h</tt>
    qui sont dans des sous répertoires <em>directs</em>
    de <tt>/usr/include</tt>""",
    tests=(
    shell_good("echo /usr/include/*/*.h"),
    shell_bad("echo /usr/include/*/./*.h",
              "Il y a 2 caractères en trop dans votre commande"),
    echo_required,
    reject("/usr/include/*.h",
           """Vous indiquez les <tt>.h</tt> qui sont dans
           <tt>/usr/include</tt>, pas dans ses sous-répertoires"""),
    reject("[h]", """Il est plus simple d'écrire <tt>h</tt> que <tt>[h]</tt>
    et cela fait la même chose"""),
    require("/usr/include",
            "On vous demande de chercher dans <tt>/usr/include</tt>"),
    number_of_is('*', 2, """Il faut une étoile pour indiquer
    n'importe quel sous répertoire, et une autre pour indiquer
    qu'il y a n'importe quoi avant le <tt>.h</tt>"""),
    require_endswith(".h", """On veut lister les noms de fichiers qui
    se terminent par <tt>.h</tt>"""),
    ),
    )





