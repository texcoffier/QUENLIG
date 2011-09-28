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
    required=["manuel:chercher", "sh:répertoire courant",
              "sh:répertoire connexion"],
    question="""Quel est le nom de la commande permettant de trouver
    des fichiers dans une hiérarchie de fichier&nbsp;?""",
    tests=(
    reject('ls', "<tt>ls</tt> permet de les voir, pas de les chercher"),
    reject('grep', "<tt>grep</tt> cherche dans les fichiers pas les fichiers"),
    good("find"),
    ),
    indices=("C'est le mot 'trouver' en anglais",
             ),
    )

find_required = require("find",
                        "Pour chercher des fichiers on utilise <tt>find</tt>")

find_dot_required = require("find .",
                            """On demande à <tt>find</tt> de chercher partout
                            dans le répertoire courant.
                            <p>
                            Les premiers arguments de <tt>find</tt> sont
                            les endroits où l'on cherche.
                            Il est possible de chercher à un seul endroit.
                            <p>
                            Ne pas indiquer l'endroit ou l'on cherche
                            fonctionne peut-être sous linux,
                            mais pour beaucoup d'autres systèmes UNIX
                            cela ne fonctionnera pas.
                            """)

find_usr_lib_required = require("find /usr/lib",
                                """On demande à <tt>find</tt> de chercher
                                partout dans <tt>/usr/lib</tt>""",
                                replace=(('  ',' '),))

find_name_required = require(
    "-name",
    """Il faut indiquer que le critère de recherche est le nom""")

find_dash_required = reject(
    (" type", " name", " o", " size"),
    """Vous oubliez le <tt>-</tt> devant l'option""")

find_pattern_protect_required = reject(
    " *",
    """Il faut protéger le <em>pattern</em> sinon c'est le shell
    qui fait la substitution et le <tt>find</tt> ne verra
    pas le <em>pattern</em>""")

find_tilde_required = require("~",
                              "On cherche dans le répertoire de connexion.")

dumb_replace = (
    ("./ ", ". "),
    ("~/ ", "~ "),
    ("GIF", "gif"),
    ("PNG", "png"),
    ("JPG", "jpg"),
    ("Gg", "gG"), ("Ii", "iI"), ("Ff", "fF"),
    ('-or', '-o'),
    ('-and', '-a'),
    (' -print', ''),
    (' a-x ', ' -x '),
    (' a+x ', ' +x '),
    )

dumb_replace_remove_type_f = list(dumb_replace) + [('-type f', '')]

add(name="simple",
    required=["intro"],
    question="""Quelle ligne de commande permet d'afficher
    les noms des répertoires et fichiers (de n'importe quel type)
    qui se nomment <tt>toto</tt>
    dans la hiérarchie dont la racine est le répertoire courant&nbsp;?""",
    tests=(
    shell_good("find . -name toto", dumb_replace=dumb_replace),
    shell_bad(("find toto", "find ./toto"),
              """<tt>toto</tt> est la hiérarchie ou la commande <tt>find</tt>
              va lister tous les fichiers quelque soit leurs noms.
              <p>
              Elle ne va donc pas chercher les fichiers nommés
              <tt>toto</tt> dans le répertoire courant"""),
    shell_bad("find -name toto",
              """Cette ligne de commande fonctionne peut être
              sur votre machine, mais pas sur un Unix standard.
              Vous devez spécifier le(s) répertoires où chercher.
              """),
    reject("-iname",
           """On ne veut pas trouver les fichiers TOTO en majuscule.
           Il ne faut donc pas utiliser <tt>-iname</tt>"""),
    find_required, find_dot_required, find_name_required,
    reject("*",
           """On veut les fichiers qui se nomment <tt>toto</tt>
           pas ceux qui commence ou finissent par <tt>toto</tt>"""),
    reject("./", """Utilisez <tt>.</tt> plutôt que <tt>./</tt>"""),
    shell_display,
    ),
    indices=("Le test doit être réalisé sur le nom (<em>name</em>) du fichier",
             ),
    )

add(name="fichier",
    required=["intro"],
    question="""Quelle ligne de commande permet d'afficher
    tous les fichiers de type texte (qui ne sont pas des répertoire,
    ni des liens symboliques, ni des périphériques...)
    dans la hiérarchie dont la racine est le répertoire courant&nbsp;?""",
    tests=(
    shell_good("find . -type f", dumb_replace=dumb_replace),
    find_required, find_dot_required, find_dash_required,
    require("-type",
            """Vous avez oubliez d'imposer le type de fichier recherché"""),\
    number_of_is('-', 1, """On a besoin que d'un seule option pour cette
    commande&nbsp;: celle qui indique le type de fichier recherché"""),
    reject(('*', 'name'), "On ne doit pas faire de test sur le nom"),
    reject('!', """Pas besoin de négation, on veut seulement
    les objets de type <tt>f</tt> comme fichier"""),
    shell_display,
    ),
    indices=("Le test doit être réalisé sur le type du fichier",
             ),
    )

add(name="taille",
    required=["intro"],
    question="""Quelle ligne de commande permet d'afficher
    tous les noms de fichiers (ou répertoires) de plus de 1024ko
    qui sont dans la hiérarchie
    dont la racine est </tt>/usr/lib</tt>&nbsp;?""",
    tests=(
    find_required, find_usr_lib_required, find_dash_required,
    require("-size",
            """Vous devez mettre l'option indiquant que le critère
            de recherche est la taille"""),
    reject("1M", """Avec 1M ce n'est pas portable, c'est-à-dire qu'il y
    a des systèmes Unix pour lesquels cette option ne fonctionnera pas
    car elle n'est pas standard"""),
    require("1024", "Il faut indiquer la taille"),
    require("1024k", "Il faut indiquer l'unité de mesure de taille"),
    require("+1024k",
            """Il faut indiquer que vous recherchez les fichiers
            plus grand que <tt>1024k</tt> pas seulement ceux
            qui font exactement cette taille."""),
    reject("ko",
           """L'unité kilo-octet est spécifié par <tt>k</tt>
           pas par <tt>ko</tt>"""),
    reject("-size 1024",
            """Il faut indiquer que vous êtes intéressé par
            les fichiers qui sont plus grand que"""),
    reject("*", """Pas besoin d'étoile la commande cherche
    dans toute l'arborescence"""),
    reject("-type", """Pas besoin de chercher un type particulier,
    on veut tous les types de fichiers possibles"""),
    shell_good("find /usr/lib -size +1024k",
               dumb_replace=dumb_replace_remove_type_f),
    shell_display,
    ),
    indices=(
    """Les arguments numériques de <tt>find</tt> peuvent
    être précédés de <tt>-</tt> pour dire 'moins de' et
    <tt>+</tt> pour dire 'plus de'.""",
    ),    
    )

add(name="vide",
    required=["taille"],
    question="""Afficher les noms de tous les fichiers de la
    hiérarchie <tt>/etc</tt> qui sont vides (contiennent 0 octets)""",
    tests=(
    reject(('-0','+0'), """La taille recherchée n'est ni plus grande
    ni plus petite que 0, donc pas de symbole moins ou plus"""),
    find_required, find_dash_required,
    reject('-empty', """C'est bien, vous avez trouvé l'option <tt>empty</tt>.
    Votre commande marche peut être.
    Mais n'est ce pas plus simple d'écrire que la taille est nulle&nbsp;?
    <p>
    Il est plus rapide d'utiliser ce que l'on connait déjà plutôt
    que de chercher dans la documentation des options
    qui n'existent peut-être pas.
    """),
    require('/etc', "On veut chercher dans <tt>/etc</tt>"),
    require('0', "Un fichier vide a une taille de 0 !"),
    number_of_is('/', 1, "Pas besoin de mettre des / inutiles"),
    reject('=', """Il faut un espace, pas un égale entre le
    paramètre et sa valeur"""),
    shell_good(("find /etc -size 0",
                "find /etc -size 0k",
                "find /etc -size 0b",
                "find /etc -size 0c",
                ),
               dumb_replace=dumb_replace_remove_type_f),
    shell_display,
    ),
    indices=("On n'a pas besoin d'indiquer les unités pour zéro&nbsp!",
             ),
    )


add(name="exécuter",
    required=["simple", "copier:simple"],
    before="""La commande <tt>find</tt> peut déclencher l'exécution
    d'une ligne de commande shell chaque fois qu'elle trouve
    un fichier.
    La ligne suivante affiche les fichiers trouvés avec <tt>ls</tt>&nbsp;:
    <pre>find . -name "*.c" -exec ls -ld {} \;</pre>""",
    question="""Modifiez la ligne précédente, pour faire
    une copie de tous les fichiers qui se terminent par <tt>.c</tt>
    en leur ajoutant l'extension <tt>.bak</tt>.
    Par exemple <tt>toto.c</tt> doit être copié dans <tt>toto.c.bak</tt>
    """,
    tests=(
    require(("find", "-exec", '"*.c"', ' . '),
            "Repartez de la ligne donnée en exemple"),
    require("cp",
            "Pour faire la copie, on utilise la commande <tt>cp</tt>"
            ),
    require("{}",
            """<tt>find</tt> remplace tous les <tt>{}</tt>
            qui sont après le <tt>-exec</tt>
            et exécute la commande pour chacun
            des fichiers qu'il trouve."""
            ),
    require("{}.bak",
            """Le nom du fichier destination n'apparaît pas.
            C'est le nom du fichier trouvé avec <tt>.bak</tt> derrière.
            C'est donc&nbsp;: <tt>{}.bak</tt>
            """
            ),
    number_of_is("{}", 2,
                 """La commande <tt>cp</tt> utilise 2 arguments,
                 le nom de l'original et le nom de la copie.
                 Vous n'en fournissez qu'un seul"""),
    require("\\;",
            """Vous avez oublié le <tt>\\;</tt> final
            qui indique la fin de l'action <tt>-exec</tt>"""
            ),
    require(" \\;",
            """Il faut un espace avant le <tt>\\;</tt> final"""),
    reject("ls", """On vous demande pas de lister les informations
    sur les fichiers, on veut les copier"""),
    shell_good("find . -name '*.c' -exec cp {} {}.bak \;",
               dumb_replace=dumb_replace + (('-type f ',''),)),
    shell_display,
    ),
    )

add(name="xargs",
    required=["exécuter", "pipeline:intro"],
    before="""Quand il y a beaucoup de fichiers à traiter, utiliser
    l'option <tt>-exec</tt> est long car cela lance un processus à chaque fois.
    <p>
    Pour éviter ce problème, on utilise la commande <tt>xargs</tt>
    qui lance la commande passée en argument en lui ajoutant les
    valeurs lues sur l'entrée standard.
    <p>
    S'il y a beaucoup d'arguments, alors la commande sera lancées plusieurs
    fois pour ne pas mettre trop d'arguments.
    """,
    question="""Qu'est-ce que la commande suivante affiche&nbsp;?
    <pre>echo 'a
*
b     B
c
d' | xargs echo</pre>
    """,
    tests = (
        Good(Equal('a * b B c d')),
        )
    )

add(name="xargs rm",
    required=["xargs", "detruire:simple"],
    before = """Si vous avez des milliers de fichiers dans un répertoire,
    la commande <tt>rm *</tt> ne va pas se lancer car il y en a trop.
    Il faut alors procéder autrement.""",
    question = """On supposera que les fichiers ne contiennent pas
    de caractères spéciaux.
    <p>
    Donnez la ligne de commande détruisant tous les fichiers du répertoire
    courant, même s'il y en a beaucoup&nbsp;:""",
    tests = (
        Good(Shell(Equal("echo * | xargs rm"))),
        Good(Shell(Equal("ls | xargs rm"))),
        Bad(Shell(Comment(Equal("rm *"),
                          "On vous a dit que cela ne fonctionnait pas!"))),
        Expect('rm'),
        Expect('xargs',
               """La commande <tt>xargs</tt> sert à découper en morceaux
               plus petits"""),
        Expect('|',
               """On utilise un pipeline pour ne pas passer par un fichier
               intermédiaire."""),
        ),
    )
    
add(name="pattern",
    required=["simple", "sh:affiche étoile", "pattern:fini par tilde"],
    question="""Quelle ligne de commande permet d'afficher
    tous les fichiers et répertoires (de n'importe quel type)
    dont le nom se termine par <tt>~</tt> (tilde)
    dans la hiérarchie dont la racine est le répertoire courant&nbsp;?""",
    tests=(
    shell_good("find . -name '*~'", dumb_replace=dumb_replace),
    find_required, find_dot_required, find_name_required,
    find_pattern_protect_required,
    reject("*.*",
           """Vous n'allez pas trouver les fichiers dont
           le nom ne contient pas de caractère '<tt>.</tt>'"""),
    reject('\\~', """Pas la peine de protéger le tilde
    il est spécial seulement en première lettre"""),
    reject('[~]', """Pourquoi mettre le tilde entre crochets,
    c'est un caractère qui n'a pas de signification
    pour les <em>patterns</em>"""),
    require("*~", """Je ne vois pas le <em>pattern</em> indiquant
    que le nom du fichier se termine par <tt>~</tt>"""),
    reject('[*~]', """Le <em>pattern</em> indique que c'est une étoile
    ou un tilde"""),
    number_of_is('.',1, """Votre commande n'a besoin que d'un seul point,
    celui qui indique ou chercher"""),
                 
    shell_display,
    ),
    indices=("""N'oubliez pas que le shell remplace
    les patterns non protégés qui sont sur la ligne de commande.""",
             ),
    )


add(name="et",
    required=["pattern", "taille", "fichier"],
    before="""Vous avez besoin de trouver les plus petites bibliothèques
    partagées du système. Comment faire&nbsp;?""",
    question="""Quelle ligne de commande permet d'afficher
    les noms des fichiers qui respectent les critères suivants
    (dans l'ordre)&nbsp;:
    <ul>
    <li> dans la hiérarchie <tt>/usr/lib</tt>
    <li> Des vrais fichiers : de type fichier texte, pas les liens symboliques
    ni les répertoires, ...
    <li> La taille est inférieure à 6 kilo octets.
    <li> Le nom se termine par <tt>.so</tt> (en respectant la casse).
    </ul>
    <p>
    <b>Respectez l'ordre des conditions sinon votre solution
    sera refusée.</b>
    """,
    tests=(
    reject('+6', """<b>Moins</b> de 6 kilo-octets on vous a dit, pas plus."""),
    shell_good("find /usr/lib -type f -size -6k -name '*.so'",
               dumb_replace=dumb_replace,
               ),
    shell_good("find /usr/lib -type f -a -size -6k -a -name '*.so'",
               """Les <tt>-a</tt> ou <tt>-and</tt> sont inutiles,
               le ET est fait par défaut.""",
               dumb_replace=dumb_replace,
               ),
    shell_good("find /usr/lib \\( -type f -a -size -6k -a -name '*.so' \\)",
               """Les <tt>\\(</tt> et <tt>\\)</tt> sont inutiles,
               car il n'y a pas d'ambiguité""",
               dumb_replace=dumb_replace,
               ),
    find_pattern_protect_required,
    reject("-6 ", """Il faut indiquer l'unité de mesure pour la taille"""),
    reject(' 6k', """Vous recherchez les fichiers dont la taille est exactement
    de <tt>6k</tt>, on veut les fichiers de taille inférieure."""),
    require("-6k", """Il faut indiquer la taille du fichier"""),
    reject('-iname', """On ne veut pas des fichiers avec l'extension <tt>.SO</tt> en majuscule, il faut donc respecter la casse."""),
    require('-name', """Où est l'option pour tester le nom&nbsp;?"""),
    require('-size', """Où est l'option pour tester la taille&nbsp;?"""),
    reject('/usr/lib/', """Le <tt>/</tt> après <tt>/usr/lib</tt>
    ne sert à rien car ce n'est pas un lien symbolique mais un répertoire"""),
    require('.so', """On cherche les fichiers dont le nom se termine
    par <tt>.so</tt>"""),
    require('*.so', """Avant le <tt>.so</tt> il peut y avoir n'importe
    quoi, vous avez oublié quelque chose."""),
    expect('/usr/lib'),
    require(' f ', "Le type d'un fichier texte normal est <tt>f</tt>"),
    reject('-a', "Simplifiez votre commande en enlevant les <tt>-a</tt>"),
    shell_display,
    ),
    bad_answer = """N'oubliez pas de faire les tests dans l'ordre
    indiqué dans la question""",
    indices=("""N'oubliez pas que le shell remplace les patterns non protégés
    qui sont sur la ligne de commande.""",
             """Avez-vous mis les paramètres dans l'ordre indiqué dans
             la question&nbsp;?""",
             ),
    )

    
    

add(name="casse insensible",
    required=["pattern", "sh:répertoire connexion"],
    question="""Donner la ligne de commande permettant de rechercher
    toutes les images dont le nom se termine par <tt>.GIF</tt>
    dans votre répertoire de connexion (et au dessous).
    Malheureusement, la casse n'est pas toujours
    respectée et peut être&nbsp;: <tt>.GIF</tt>, <tt>.gif</tt>,
    <tt>.Gif</tt>, ...
    <p>
    Vous ne devez pas lister tous les cas possibles
    en utilisant les crochets (<tt>[Gg][Ii][Ff]</tt>)
    """,
    tests=(
    reject('-type', "Réessayez sans donner l'option <tt>-type</tt>"),
    shell_good("find ~ -iname '*.gif'", dumb_replace=dumb_replace),
    shell_bad("find ~ -name '*.[gG][iI][fF]'",
              "Cela fonctionne, mais il y a plus simple (<tt>-iname</tt>)",
              dumb_replace=dumb_replace
              ),
    shell_bad(("find ~ -name *.gif", "find ~ -iname *.gif"),
              """On vous a déjà expliqué que la command <tt>find</tt>
              ne verrait pas le <em>pattern</em> s'il y avait un <tt>.gif</tt>
              dans le répertoire courant car
              le shell ferait la substitution""",
              dumb_replace=dumb_replace
              ),    
    require("find", "Vous devez utiliser la commande <tt>find</tt>"),
    find_tilde_required,
    require('*', """Vous devez donner un <em>pattern</em> indiquant
    qu'il y a n'importe quoi avant <tt>.gif</tt> vous devez
    donc utilisez une étoile"""),
    require("name",
            """Vous n'avez pas indiqué que le critère de recherche
            est le nom du fichier"""),
    reject("-name",
            """<tt>-name</tt> permet de chercher en respectant la casse,
            ce n'est donc pas cette option qu'il faut utiliser"""),
    reject("-ilname",
           """-lname cherche dans le nom du fichier pointé
           par le lien symbolique"""),
    reject(("'.gif'", "'.GIF'", '".GIF"', '".gif"'),
           """Vous cherchez les fichiers s'appellant '.gif'
           pas se terminant par '.gif'"""),
    require('.GIF',
            "Vous devez chercher les fichiers se terminant par <tt>.gif</tt>",
            uppercase=True
            ),
    require(' ~ ', """La façon la plus courte d'indiquer votre répertoire
    de connexion est la chaine de caractère <tt>~</tt> (tilde)"""),
    reject('wholename',
           """L'option <tt>wholename</tt> n'a pas été vue en cours.
           D'autre part cette option teste le chemin complet et pas
           le nom court du fichier"""),
    
    shell_display,
    ),
    )

add(name="ou simple",
    required=["pattern"],
    question="""Ligne de commande permettant de rechercher
    tous les fichiers/répertoires de la hiérarchie courante dont
    le nom se termine par
    <tt>.sh</tt> ou <tt>.pl</tt> ou <tt>.py</tt>
    (Ne changez pas l'ordre des 3 extensions dans votre commande.)
    """,
    tests=(
    reject('(-', "Il manque un espace après la parenthèse ouvrante"),
    reject(('"\\)',"'\\)"), "La parenthèse fermante est un paramètre. Il manque un espace quelque part..."),
    shell_good(("find . -name '*.sh' -o -name '*.pl' -o -name '*.py'",
                "find . \\( -name '*.sh' -o -name '*.pl' -o -name '*.py' \\)",
                ),
               dumb_replace=dumb_replace),
    shell_good(("find . -name '*.sh' -o -name '*.p[ly]'",
                "find . \\( -name '*.sh' -o -name '*.p[ly]' \\)",
                ),
               """Vous êtes plus fort que le prof, pourquoi
               faites-vous cette UE&nbsp;?""",
               dumb_replace=dumb_replace),
    reject('-iname', """Il ne faut pas utiliser <tt>-iname</tt>
    car celui ci va trouver <tt>toto.SH</tt> et on ne le vous
    demande pas"""),
    find_required, find_dot_required, find_name_required,
    find_pattern_protect_required,
    reject('|', """Le <tt>|</tt> n'existe pas dans les <em>patterns<em>
    utilisés par <tt>find</tt> et pour le <em>shell</em>, il
    n'est utilisé que pour le <tt>case</tt>."""),
    require(("*.sh", "*.py", "*.pl"),
            """Il manque au moins un <em>pattern</em> indiquant
            l'une des extensions à rechercher"""),
    number_of_is('-name',3,"Il faut répéter 3 fois <tt>-name</tt>"),
    reject("-name -o",
           """<tt>-name -o</tt> indique que l'on recherche un fichier
           nommé <tt>-o</tt>"""),
    reject('|', """Le <em>ou</em> n'est pas dans le <em>pattern</em>
    donné comme paramètre de <tt>-name</tt>, c'est un paramètre
    spécifique à la commande <tt>find</tt>"""),
    require("-o", """N'oubliez pas d'indiquer que vous faites un ou"""),
    number_of_is(' ', 9,
                 """Dans la solution la plus courte, il y a 9 paramètres
                 qui sont passés à la commande <tt>find</tt>
                 (pensez à ne pas oublier d'espaces)"""),
    shell_display,
    ),
    indices=("Lire ce qu'écrit <tt>find --help</tt>",
             "'Ou' c'est <tt>-o</tt> ou <tt>-or</tt>",
             """N'oubliez pas d'indiquer l'option <tt>-name</tt>
             après chaque <tt>-o</tt>""",
             "Faites attention aux espaces",
             ),
    )



add(name="images",
    required=["ou simple", "casse insensible"],
    question="""Donner la ligne de commande permettant d'afficher
    les noms de toutes les images <tt>.GIF</tt>, <tt>.JPG</tt>, <tt>.PNG</tt>
    qui sont dans votre répertoire de connexion ou au dessous.
    Évidemment on ne tient pas compte de la casse.
    <p>
    Respectez l'ordre <tt>.GIF</tt>, <tt>.JPG</tt>, <tt>.PNG</tt>
    sinon la réponse sera refusée.
    """,
    tests=(
    require("-o", """N'oubliez pas d'indiquer que vous faites un
    <tt>ou</tt>. En effet par défaut c'est un <tt>et</tt> et aucun
    fichier ne pourra correspondre."""),
    require('*', "S'il n'y a pas d'étoile, vous cherchez un nom exact."),
    shell_good(("find ~ -iname '*.gif' -o -iname '*.jpg' -o -iname '*.png'",
                "find ~ \\( -iname '*.gif' -o -iname '*.jpg' -o -iname '*.png' \\)",
                ),
               dumb_replace=dumb_replace),
    reject("-name", "On va a dit de ne pas tenir compte de la casse"),
    require('-iname', """On a vu dans un exercice précédent comment
    test sans tenir compte de la casse"""),
    find_tilde_required,
    require(('*.gif', '*.jpg', '*.png'),
                 """Je ne vois pas les 3 <em>pattern</em> testant
                 les 3 extensions""",
            replace=dumb_replace),
    number_of_is('-iname',3,"Je ne vois pas 3 tests sur les noms de fichiers"),
    number_of_is('-o',2, "Je ne vois pas 2 <tt>ou</tt>"),
    reject('(-', "N'auriez-vous pas oublié un espace après la parenthèse ouvrante&nbsp;?"),
    shell_display,
    ),
    indices=("Lire ce qu'écrit <tt>find --help</tt>",
             "ou = -o = -or",
             "Ne changez pas l'ordre des tests",
             "Faites attention aux espaces",
             ),
    )


    
