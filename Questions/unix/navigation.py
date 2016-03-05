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

from QUENLIG.questions import *

image = "<img src='boxes.png'>"

add(name="intro",
    required=["repondre:répondre"],
    before="""
    Voici une représentation du système de fichier.
    Les cases noires contiennent les noms courts des fichiers.
    Les vertes sont des fichiers de données exécutables
    ou non et les jaunes des fichiers représentant des périphériques.
    La plus grande boite est la racine et ne porte pas de nom.
    Les cases <tt>.</tt> et <tt>..</tt> apparaissent
    dans tous les répertoires.
    <p>
    """ + image,
    question="""Combien de répertoires <b>différents</b> sont visibles
    sur la figure&nbsp;?""",
    tests=(
    good("11"),
    bad(("6","7"),
        "Vous avez compté que les répertoires directement sous la racine"),
    bad("10", "Avez-vous compté le répertoire racine&nbsp;?"),
    bad("12", "Presque !"),
    require_int(),
    ),
    indices=("""Ne comptez pas les cases <tt>..</tt> et <tt>.</tt> vous les
    avez déjà comptées par ailleur.""",
             ),
    )

reject_double_slash = reject("//",
           """Mettre plus d'un '<tt>/</tt>' revient à en mettre un seul,
           Comme dans la suite des questions on vous demande tous
           le temps la réponse la plus courte,
           celle-ci ne sera pas acceptée""")

reject_space = reject(" ","On fait les concaténations sans ajouter d'espaces.")

reject_dot = reject(".",
                    """On vous a dit d'enlever tous les
                    <tt>.</tt>, <tt>..</tt> pour que cela soit court."""
                    )

reject_trailing_slash = reject_endswith(
    '/',
    """Mettre un <tt>/</tt> à la fin d'un nom n'est utile
    que dans le cas du lien symbolique
    quand on veux spécifier ce qui est pointé
    par le lien symbolique plutôt que le lien symbolique lui-même.
    <p>
    Ce <tt>/</tt> final n'est pas incorrecte mais vos réponses
    seront néanmoins refusées si vous le mettez"""
    )

require_absolute_name = require_startswith(
    "/", "Un chemin absolu commence par <tt>/</tt>")

require_relative_name = reject_startswith(
    "/", "Un chemin relatif ne commence pas par <tt>/</tt>")

add(name="nom absolu",
    required=["intro"],
    before="""
    Pour obtenir un nom absolu, vous partez de la boite la plus extérieure
    jusqu'à celle qui vous intéresse.
    Le nom absolu est la concaténation de tous les noms courts
    de ces boites en les séparant par un caractère '<tt>/</tt>'
    <p>
    """ + image + """
    <p>
    Bien que la boite extérieur ne porte pas de nom court
    son nom absolu n'est pas vide, c'est&nbsp;: <tt>/</tt>
    """,
    question="""Quel est le nom absolu de la boite dont le nom est <tt>etc</tt>
    sur la figure&nbsp;?""",
    tests=(
    good("/etc"),
    bad("//etc",
        """Cette réponse fonctionne mais est à éviter car elle
        est non-portable."""),
    require("etc",
            """Je ne vois pas <tt>etc</tt> comment
            est-ce que cela peut le désigner&nbsp;?"""),
    require_absolute_name,
    reject_trailing_slash,
    reject_double_slash,
    reject_space,
    ),
    indices=(
    """Comme <tt>etc</tt> est dans la plus grande boite
    la réponse est&nbsp;: <tt>nom court de la racine/nom court de la boite etc</tt>""",
    """Le nom court de la racine est une chaine de caractère vide.""",
    ),
    )

add(name="nom absolu 2",
    required=["nom absolu"],
    before=image,
    question="""Quel est le nom absolu de la boite
    dont le nom est <tt>xemacs</tt> sur la figure&nbsp;?""",
    tests=(
    good("/usr/bin/xemacs"),
    bad("/bin/xemacs", "Dans la boite <tt>/bin</tt> il n'y a que <tt>ls</tt>"),
    reject("etc", """Le chemin qui mène à <tt>xemacs</tt>
    ne passe pas par <tt>etc</tt>"""),
    require_absolute_name,
    reject_trailing_slash,
    reject_double_slash,
    reject_space,
    require("xemacs", "Où est <tt>xemacs</tt> dans votre réponse&nbsp;?"),
    require("bin/xemacs", "Dans quel répertoire se trouve <tt>xemacs</tt>&nbsp;?"),
    ),
    indices=(
    """La réponse est&nbsp;:
    <tt>nom court racine/nom court 1/nom court 2/nom court xemacs</tt>""",
    ),
    )

add(name="point",
    required=["nom absolu 2"],
    before="""Le contenu de la boite <tt>.</tt> est le même que
    celui de la boite qui la contient.
    C'est à dire que <tt>/etc/.</tt> est la même chose que
    <tt>/etc</tt><p>""" + image,
    question="""Donnez le chemin absolu le plus court qui
    représente la même chose que <tt>/./home/././p0123456/Toto/.</tt>
    """,
    tests=(
    reject_trailing_slash,
    reject_double_slash,
    reject_space,
    reject_dot,
    good("/home/p0123456/Toto"),
    good("~p0123456/Toto"),
    require("Toto",
            """Quand on dit <tt>Toto</tt>, c'est pas <tt>toto</tt>
            ni <tt>TOTO</tt> ni <tt>ToTo</tt> ni ..."""),
    require(("home", "p0123456", "Toto"),
            "Il manque des noms courts dans votre chemin"),
    reject('~', """N'utilisez pas le tilde s'il vous plais"""),
    require_absolute_name,
    ),
    )

add(name="point point",
    required=["nom absolu 2"],
    before="""Le contenu de la boite <tt>..</tt> est la même que
    celui de la boite qui la contient.
    C'est-à-dire que <tt>/usr/include/..</tt> est la même boite que
    <tt>/usr</tt>
    <p>
    Et <tt>/..</tt> est un cas particulier car il n'y a pas
    de boite au dessus et il représente la même
    chose que <tt>/</tt>
    <p>
    """ + image,
    question="""Donnez le nom absolu le plus court qui
    représente la même chose que <tt>/home/p0123456/Toto/..</tt>
    même si vous n'êtes pas l'utilisateur <tt>p0123456</tt>""",
    tests=(
    good("/home/p0123456"),
    good("~p0123456"),
    reject(('~','$HOME'), """Votre identité n'est pas <tt>p0123456</tt> donc
    vous ne devez pas utiliser le tilde ou <tt>$HOME</tt>."""),
    reject_trailing_slash,
    reject_double_slash,
    reject_space,
    reject_dot,
    bad("/home/p0123456/Toto",
        "C'est la même chose que <tt>/home/p0123456/Toto/.</tt>"),
    expect('p0123456'),
    number_of_is('/',2, """Il doit y avoir 2 / dans votre réponse
    puisqu'en remontant d'un niveau on perd un /"""),
    ),
    )
    
add(name="point point 2",
    required=["point point", "point"],
    before=image,
    question="""L'utilisateur veut créer le fichier <tt>/./home/./p0123456/../../toto</tt>
    <p>
    Donnez le nom absolu le plus court qui
    représente le nom du fichier créé.""",
    tests=(
    good("/toto"),
    reject_trailing_slash,
    reject_double_slash,
    reject_space,
    reject_dot,
    bad("/home/toto", "Presque... Soyez rigoureux."),
    bad("/home/p0123456/toto",
        """Le <tt>..</tt> fait remonter au père, vous ne l'avez pas fait"""),
    require_absolute_name,
    require("toto",
            "Le nom de fichier que vous donnez doit contenir <tt>toto</tt>"),
    
    ),
    )

add(name="répertoire courant",
    required=["nom absolu 2"],
    before="""
    Tous les processus ont un répertoire courant,
    le répertoire courant permet d'écrire des noms
    de fichier relatif qui sont beaucoup plus court
    à écrire que les noms de fichier absolu.
    <p>
    Le chemin absolu du fichier indiqué en relatif
    est la concaténation du chemin absolu du répertoire
    courant d'un <tt>/</tt> et du chemin relatif.
    <p>
    Les chemins relatifs ont l'avantage de pouvoir être exprimés
    sans référence à l'endroit ou sont stockés les fichiers.
    <p>
    Si <tt>/usr</tt> est le répertoire courant
    alors le chemin relatif <tt>include</tt>
    indique le répertoire <tt>/usr/include</tt>.    
    <p>
    """ + image,
    question="""Si <tt>/usr</tt> est le répertoire courant,
    quel est le chemin relatif le plus court indiquant
    <tt>/usr/bin</tt>&nbsp?""",
    tests=(
    good("bin"),
    require_relative_name,
    reject_trailing_slash,
    reject_dot,
    reject_space,
    expect('bin'),
    ),
    )

add(name="relatif",
    required=["répertoire courant"],
    before=image,
    question="""Si <tt>/usr</tt> est le répertoire courant,
    quel est le chemin relatif le plus court indiquant
    <tt>/usr/bin/xemacs</tt>""",
    tests=(
    reject_double_slash,
    reject_space,
    reject_dot,
    bad("/bin/xemacs",
           """Premièrement votre chemin est absolu et non relatif.
           et deuxièmement, il n'y a aucun fichier <tt>xemacs</tt>
           dans <tt>/bin</tt>"""),
    require_relative_name,
    reject("usr/xemacs",
           "Il n'y a aucun fichier <tt>xemacs</tt> dans <tt>usr</tt>"),
    require('xemacs', "Il y a forcément <tt>xemacs</tt> dans la réponse"),
    bad('xemacs', """Le chemin complet du fichier que vous venez
    d'indiquer est <tt>/usr/xemacs</tt> et non <tt>/usr/bin/xemacs</tt>"""),
    
    good("bin/xemacs"),
    ),
    )


add(name="ici",
    required=["répertoire courant", "point"],
    question="""Donnez le nom relatif le plus court indiquant le répertoire courant""",
    tests=(
    good("."),
    bad("/",
        "C'est la racine du système de fichier, pas le répertoire courant"),
    bad("/.", "C'est la même chose que <tt>/</tt> la racine"),
    bad("~",
        "Ce n'est pas le répertoire courant mais le répertoire de connexion"),
    bad("pwd",
        """C'est le nom d'une commande affichant le répertoire courant.
        On vous demande un nom de fichier, pas une commande à exécuter"""),
    reject_trailing_slash,
    ),
    indices=("La réponse tient sur un caractère",
             ),
    )

add(name="père",
    required=["répertoire courant", "point point"],
    question="""Donnez le nom relatif le plus court indiquant le père du répertoire courant""",
    tests=(
    good(".."),
    reject("/..", "Ça c'est le père de la racine, donc... la racine :-)"),
    bad(('/',"/."), "C'est la racine du système de fichier."),
    reject_trailing_slash,
    reject('.', "C'est le répertoire courant, pas son père."),
    ),
    indices=("La réponse tient sur deux caractères",
             ),
    )

add(name="relatif 2",
    required=["relatif", "point point"],
    before=image,
    question="""Si <tt>/usr/include</tt> est le répertoire courant,
    quel est le chemin relatif le plus court indiquant
    <tt>/usr/bin/xemacs</tt>""",
    tests=(
    good("../bin/xemacs"),
    reject("usr", "Essayez de ne pas écrire <tt>usr</tt>"),
    expect('xemacs'),
    require_relative_name,
    reject_double_slash,
    reject_space,
    reject_trailing_slash,
    require('..', """<tt>/usr/bin/xemacs</tt> n'est pas au dessous
    de <tt>/usr/include</tt>, il faut donc remonter dans la hiérarchie
    en utilisant le <tt>..</tt>"""),
    ),
    )

add(name="relatif 3",
    required=["relatif", "point point"],
    before=image,
    question="""Si <tt>/home/p0123456/Toto</tt> est le répertoire courant,
    quel est le chemin relatif le plus court indiquant
    <tt>/home/p0123456/.profile</tt>""",
    tests=(
    require(".profile",
            """Le chemin relatif indique forcément sa destination&nbsp;:
            <tt>.profile</tt>"""),
    require_relative_name,
    reject_double_slash,
    reject_space,
    reject_trailing_slash,
    bad(".profile", """Le nom que vous venez de donner s'écrit
    <tt>/home/p0123456/Toto/.profile</tt> en absolu."""),
    good("../.profile"),
    bad("~/.profile", "On vous demande un chemin relatif"),
    require_startswith('../',
                       """On veut sortir du répertoire courant.
                       Il faut donc aller dans le père"""),
    ),
    )

add(name="intrus",
    required=["point point"],
    question="""Quel est l'intrus parmi la liste suivante&nbsp;?
    <ul>
    <li> <tt>/etc/./profile</tt>
    <li> <tt>/usr/../etc/profile</tt>
    <li> <tt>/etc/../profile</tt>
    <li> <tt>/etc/rc2.d/../profile</tt>
    </ul>
    """,
    tests=(
    bad(("/etc/./profile", "/usr/../etc/profile",
         "/etc/rc2.d/../profile"),
        "Ce chemin pointe vers <tt>/etc/profile</tt> et les autres&nbsp;?"),
    good("/etc/../profile",
         "C'est le seul ne représentant pas <tt>/etc/profile</tt>"),
    comment("Votre réponse ne figure pas dans la liste des choix possibles."),
    ),
    )




add(name="rép. connexion",
    required=["nom absolu 2"],
    before="""Quand un paramètre d'une commande commence
    par une certaine suite de caractères,
    le shell (l'interpréteur de commande, pas Unix)
    remplace cette séquence de caractères par
    le nom absolu du répertoire de connexion.""",
    question="""Quelle est la séquence de caractères qui
    est remplacée par le nom du répertoire de connexion&nbsp;?""",
    tests=(
    reject_double_slash,
    reject_space,
    reject_dot,
    good("~/"),
    good("~",
        """Non, car dans <tt>~toto/x</tt>, <tt>~toto</tt> est remplacé
        par le répertoire de connexion de <tt>toto</tt>.
        Je vous accorde la réponse car elle est valide s'il n'y
        a rien après le tilde.
        La bonne réponse qui marche dans tous les cas est <tt>~/</tt>
        """),
    bad("$HOME",
        """Non, car si la valeur de la variable <tt>HOME</tt> change,
        cela ne sera plus le répertoire de connexion.
        De plus, c'est un peu long à taper."""),
    bad("/", """Ce n'est pas le répertoire de connexion mais
    la racine du système de fichier."""),
    ),
    indices=("""La réponse est en 2 caractères, mais une réponse
    en un seul est acceptée""",
             ),
    )

image = "<a href='graphe.png'><img src='graphe_small.png'></a>"

add(name="graphe",
    required=["relatif 3"],
    before=image,
    question="""Votre répertoire courant est <tt>/home/p0123456/Toto</tt>,
    quel est le chemin relatif le plus court indiquant
    <tt>/usr/bin</tt>""",
    tests=(
    require_relative_name,
    reject_double_slash,
    reject_space,
    reject_trailing_slash,
    reject('~', "Le <tt>~</tt> indique un chemin absolu et pas relatif"),
    require_startswith('..', """Le chemin doit commencer par <tt>..</tt>
    pour remonter dans le père"""),
    require_endswith('bin', """Le chemin doit se finir par <tt>bin</tt>
    car c'est bien de lui dont on parle"""),
    bad("/usr/bin", "On vous demande un chemin relatif, pas absolu."),
    require('usr',
            "Comment sait-il que <tt>bin</tt> est dans <tt>usr</tt>&nbsp?"),
    bad("../../usr/bin", "Ça c'est <tt>/home/usr/bin</tt>"),
    bad("../usr/bin", "Ça c'est <tt>/home/p0123456/usr/bin</tt>"),
    good("../../../usr/bin",
         """Si vous êtes certain que votre racine ne changera pas
         d'emplacement, <tt>/usr/bin</tt> est plus court.
         Mais dans certain cas, il est intéressant de tout
         faire en relatif."""),
    ),
    )

image = "<a href='graphe_cercle.png'><img src='graphe_cercle_small.png'></a>"

add(name="rép. connexion 2",
    required=["rép. connexion"],
    before=image,
    question="""Donnez le nom absolu
    (bien que ne commençant pas par <tt>/</tt>)
    le plus court désignant le fichier <tt>/home/p0123456/toto</tt>
    si vous êtes l'utilisateur <tt>p0123456</tt>""",
    good_answer="""Ce n'est pas un nom reconnu par Unix.
    C'est le shell qui fait la substitution.
    Cela ne fonctionne donc que dans la ligne de commande ou les scripts.""",
    tests=(
    good("~/toto"),
    bad("toto",
        """Ceci est juste seulement si votre répertoire courant
        est votre répertoire de connexion.
        Mais si ce n'est pas le cas&nbsp;?"""),
    require("~",
            """Vous savez déjà que <tt>~/</tt> est remplacé
            par le shell par votre répertoire de connexion"""),        
    require("~/",
            """Si le tilde n'est pas suivi d'un slash, alors ce
            qui suis est considéré comme un nom d'utilisateur.
            <tt>~jean/toto</tt> est le fichier <tt>toto</tt>
            dans le répertoire de connexion de l'utilisateur <tt>jean</tt>"""),
    reject_double_slash,
    reject_space,
    reject_trailing_slash,
    reject_dot,
    reject('~/p0123456/toto', """Le shell traduira cela en&nbsp;:
    <tt>/home/p0123456/p0123456/toto</tt>"""),
    expect('toto'),
    ),
    )

image = "<a href='tree.svg'><img border=0 src='tree_small.png'></a>"

add(name="arbre",
    required=["graphe"],
    before=image,
    question="""Dans la figure,
    combien <tt>/home</tt> contient de répertoires (sans compter
    les sous répertoires ni <tt>.</tt> et <tt>..</tt>)&nbsp;?""",
    tests=(
    good("1"),
    bad("2",
        """On vous demande le nombre de répertoires dans <tt>/home</tt>
        Il ne faut pas compter ceux qui sont dans ses sous répertoires."""),
    good("3",
         """J'accepte cette réponse car je suppose que vous
         avez compté <tt>.</tt> et <tt>..</tt> bien qu'ils ne
         soient pas affichés sur le dessin."""),
    require_int(),
    ),
    )
    
add(name="final",
    required=["point point 2", "père", "ici", "arbre",
              "relatif 2", "rép. connexion 2"],
    question="""Quel est le chemin absolu le plus court valide pour Unix&nbsp;?
    <p>
    Évidemment, le chemin vide (sans caractères) n'est pas valide.
    """,
    tests=(
    good("/"),
    bad("~",
        """Ceci est un pattern du shell,
        il est en effet remplacé par un nom absolu.
        Ce nom n'est pas connu par le noyau Unix.
        """),
    require_absolute_name,
    reject(('/.', '/..'), "Valide, mais il y a plus court"),
    ),
    )

