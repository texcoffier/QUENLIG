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
    required=["sh:console"],
    question="""Quelle commande permet de changer les droits
    d'accès à des fichiers et répertoires.""",
    tests=(
    good("chmod"),
    ),
    )

class mode_display(TestExpression):
    def do_test(self, student_answer, state=None):
        n = int(student_answer, 8)
        s = ''
        for i in range(9):
            if n & (1<<(9-i-1)):
                s += 'rwxrwxrwx'[i]
            else:
                s += '-'
        return True, "Le mode numérique <tt>%s</tt> représente <tt>%s</tt>"%(
            student_answer, s)


add(name="numérique",
    required=["intro"],
    question="""A quelle valeur numérique écrite en octal correspond
    le mode <tt>rwxr-x---</tt>""",
    tests=(
    good("750"),
    require_int(),
    answer_length_is(3, "Le mode en octal vu en cours est sur 3 chiffres"),
    reject(('8','9'), "En octal, les chiffres 8 et 9 n'existent pas"),
    Bad(mode_display()),
    ),
    indices=(
    """Remplacez les lettres par des 1 et les - par des zéros.
    Convertissez le nombre binaire en octal (base 8) :
    <tt>101010011 = 101 010 011 = 523</tt>
    """,
    ),
    )

b = """De nombreuses réponses correctes sont possibles.
Toutes ne sont pas acceptées.
Pour augmenter vos chances vous devez donnez la réponse la plus courte.
Si vous utilisez les modes 'r', 'w' et 'x' il faut qu'ils
soient utilisés de préférence dans cet ordre."""

chmod_required = require("chmod", "Vous devez utiliser <tt>chmod</tt>")

umask = """Cela marche peut-être pour votre configuration,
mais pas dans tous les cas.
<p>
En effet quand vous utilisez <tt>+x</tt> le mode 
est modifié en tenant compte de la valeur courante du <tt>umask</tt>.
<p>
Pour plus d'informations, regardez <tt>man 2 umask</tt>"""

add(name="simple",
    required=["numérique"],
    before=b,
    question="""Quelle ligne de commande permet d'affecter
    le mode <tt>rwxr-xr-x</tt> au fichier <tt>essai.sh</tt>
    en utilisant la syntaxe en octal.""",
    tests=(
    shell_good((
    "chmod 755 essai.sh",
    "chmod u=rwx,go=rx xxx essai.sh",
    "chmod a=rx,u+w essai.sh",
    )),
    chmod_required,
    shell_bad(("chmod rwxr-xr-x essai.sh",
               "chmod u=rwx go=xr essai.sh"),
              "Vous n'avez même pas essayé la commande elle fait une erreur"),
    shell_bad("chmod essai.sh 755",
              """La syntaxe de <tt>chmod</tt> est simple : le premier
              argument est le mode, les autres sont des noms d'entités"""),
    require("essai.sh", "On veut modifier le mode de <tt>essai.sh</tt>"),
    require("755", "Vous vous êtes trompé en calculant le mode en octal."),
    shell_display,
    ),
    good_answer="""Le plus court est <tt>chmod 755 essai.sh</tt>""",
    indices=("""Réécrire la suite de lettre en remplaçant les '-'
    par des '0' et les lettres par des '1' et convertir le nombre
    binaire en octal (base 8)""",),
    )


add(name="ajouter",
    required=["simple"],
    question="""Quelle ligne de commande permet d'ajouter le droit
    d'exécuter pour l'utilisateur au fichier <tt>essai.sh</tt>""",
    tests=(
    shell_good("chmod u+x essai.sh"),
    shell_bad("chmod +x essai.sh", umask),
    shell_bad("chmod u+X essai.sh",
              """Le droit d'exécution ne sera ajouté que si
              <tt>essai.sh</tt> est un répertoire"""),
    chmod_required,
    require("essai.sh",
            """Vous voulez changer le mode de <tt>essai.sh</tt>
            le minimum est de l'indiquer"""),
    reject('[', """Les crochets utilisés pour donner la syntaxe de la commande.
    indiquent que le contenu est facultatif.
    Vous ne devez pas avoir de crochets dans votre réponse."""),
    require("+",
            """Vous ne voulez pas modifier complètement la valeur
            du mode mais seulement <b>ajouter</b> un droit
            suplémentaire"""),
    reject("+ ", "Il ne faut pas d'espace après le <tt>+</tt>"),
    require("+x",
            """Vous voulez ajouter le droit d'exécution,
            pas de faire autre chose"""),
    require("u+",
            """C'est seulement pour l'utilisateur que vous
            voulez ajouter le droit d'exécution"""),
    shell_display,
    ),
    indices=("""On ne connais pas l'ancien mode, on utilise donc
    la syntaxe <tt>[u][g][o][a][+|-][r][w][x]</tt>""",
             ),
    )


add(name="exec pattern",
    required=["ajouter", "pattern:0 au milieu"],
    before=b,
    question="""Quelle ligne de commande permet <b>d'ajouter</b>
    le mode 'x' pour l'utilisateur, le groupe et les autres
    à tous les fichiers du répertoire courant dont
    le nom se termine par <tt>.sh</tt>
    """,
    tests=(
    shell_good("chmod a+x *.sh"),
    shell_good(("chmod u+x,g+x,o+x *.sh", "chmod ugo+x *.sh", ),
               "<tt>chmod a+x *.sh</tt> est plus court"),
    shell_bad("chmod o+x *.sh",
              "Cela n'a pas ajouté le droit d'exécution à l'utilisateur"),
    shell_bad("chmod u+x *.sh",
              """Cela n'a pas ajouté le droit d'exécution au groupe
              et aux autres"""),
    shell_bad("chmod +x *.sh", umask),
    reject(";",
           "On ne veux utiliser <tt>chmod</tt> qu'une seule fois"),
    require("+",
            "Il faut indiquer que vous <b>ajoutez</b> des droits"),
    require('x',
            "Je ne vois pas le <tt>x</tt> indiquant le droit d'exécution"),
    reject("find",
           """On veux changer les droits dans le répertoire courant
           pas dans toute la hiérarchie"""),
    reject("./*",
           "Le <tt>./</tt> ne sert à rien ici"),
    reject("-R", """On ne veux pas changer le mode sur toute la hiérarchie,
    seulement dans le répertoire courant."""),
    shell_require("<argument><pattern_char>*</pattern_char>.sh</argument>",
                  """Je ne vois pas le <em>pattern</em> indiquant tous
                  les fichiers se terminant par <tt>.sh</tt> dans
                  le répertoire courant"""),
    number_of_is(' ', 2, """Il y a normalement seulement 2 espaces
    dans votre commande car elle a 2 paramètres&nbsp;: le changement
    de mode et le <em>pattern</em>"""),
    reject(('r', 'w'),
           "On ne veux pas ajouter le mode <tt>r</tt> ou <tt>w</tt>"),
    reject('uga', 'Petit rappel : u=user g=group o=other a=u+g+o'),
    
    shell_display,
    ),
    )

add(name="exec pattern 2",
    required=["exec pattern"],
    before=b,
    question="""Quel ligne de commande permet <b>d'ajouter</b>
    le mode 'w' pour l'utilisateur, le groupe et les autres
    à tous les fichiers du répertoire courant dont
    le nom se termine par <tt>.sh</tt>,
    """,
    tests=(
    shell_good("chmod a+w *.sh"),
    shell_good(("chmod u+w,g+w,o+w *.sh", "chmod ugo+w *.sh", ),
               "<tt>chmod a+w *.sh</tt> est plus court"),
    shell_bad("chmod +w *.sh",
               """Cela ne l'ajoute qu'à l'utilisateur"""),
    expect('chmod'),
    comment("""Il vous suffit de remplacer un <tt>x</tt> par
    un <tt>w</tt> dans la réponse que vous aviez donné pour
    ajouter le droit d'exécution dans une question précédente."""),
    shell_display,
    ),
    )

add(name="récursif",
    required=["ajouter"],
    before="""Il ne faut jamais dire au système que
    des fichiers de données sont exécutables
    car cela crée des problèmes de sécurité et en plus
    le double clique pour éditer le fichier l'exécutera
    au lieu de l'éditer...""",
    question="""Ajouter récursivement à partir du répertoire courant
    le mode '<tt>x</tt>' pour le propriétaire, le groupe et tout
    le monde, s'il <b>était déjà présent</b> pour quelqu'un.
    <pre>
    rwx------ devient rwx--x--x
    r-xr-xr-- devient r-xr-xr-x
    rw-r--r-- reste inchangé</pre>
    <p>
    On n'a pas besoin d'une commande autre que <tt>chmod</tt>.
    """,
    tests=(
    reject("find", "Pas besoin de <tt>find</tt> seulement <tt>chmod</tt>"),
    reject('ugo', 'On veut <tt>a</tt> à la place de <tt>ugo</tt>'),
    reject('/', "Pourquoi un <tt>/</tt>&nbsp;?"),
    reject(('1','3','5','7'),
           """Vous ne pouvez pas utiliser de mode numériques car
           les modes des fichiers modifiés ne sont pas tous les mêmes."""),
    require('+', "On veut ajouter un droit, il faut donc utiliser <tt>+</tt>"),
    reject('+x', "Non car les fichiers de données vont devenir exécutables") ,
    require('.', 'Et le répertoire courant, il est où&nbsp;?'),
    shell_require("-R","Il faut donner une option pour indiquer la récursion"),
    reject(" +X", """Relisez bien la documentation, cela ne fait
    pas comme <tt>a+X</tt>, il y a un <em>mais</tt> dans la phrase."""),
    shell_bad("chmod -R o+X .",
              "Cela n'ajoute pas le mode <tt>x</tt> au propriétaire"),
    shell_good("chmod -R a+X ."),
    shell_good("chmod a+X -R .",
               """Ceci n'est pas portable sur d'autres Unix,
               vérifiez l'ordre des options"""),
    require_endswith(' .',
                     """Le dernier argument de <tt>chmod</tt> doit être
                     le répertoire courant"""),
    shell_display,
    ),
    )


    

import chercher

add(name="réparation",
    required=["ajouter", "chercher:exécuter", "chercher:images"],
    before="""Un administrateur maladroit à rendu tous vos fichiers
    exécutables&nbsp;: les fichiers texte, les images, les pages HTML, ...""",
    question="""Quelle ligne de commande permet d'enlever le bit <tt>x</tt>
    des images PNG et JPG de votre compte.
    <ul>
    <li> Il ne faudra pas tenir compte de la casse,
    <li> la solution la plus courte est recherchée.
    <li> dans votre réponse indiquez d'abord PNG puis JPG,
    <li> cela n'a pas de sens d'enlever le mode <tt>x</tt> à l'utilisateur
    et le laisser aux autres. Donc il faut l'enlever à tous.
    </ul>
    """,
    tests=(
    reject('/', "Vous n'avez pas besoin de <tt>/</tt> dans la réponse"),
    shell_good(
    (
    "find ~ \( -iname '*.jpg' -o -iname '*.png' \) -exec chmod -x {} \\;",
    "find ~ \( -iname '*.jpg' -o -iname '*.png' \) -exec chmod a-x {} \\;",
    ),
    "J'accepte la réponse, mais on vous avais dis d'abord PNG et après JPG",
    dumb_replace=chercher.dumb_replace),
    shell_good(
    (
    "find ~ \( -iname '*.png' -o -iname '*.jpg' \) -exec chmod -x {} \\;",
    "find ~ \( -iname '*.png' -o -iname '*.jpg' \) -exec chmod a-x {} \\;",
    ),
    dumb_replace=chercher.dumb_replace),
    shell_bad(
    ("find ~ -iname '*.png' -o -iname '*.jpg' -exec chmod -x {} \\;",
     "find ~ -iname '*.png' -o -iname '*.jpg' -exec chmod a-x {} \\;",
     ),
    """Le <tt>-exec</tt> va s'exécuter seulement pour les JPG
    pas pour les PNG. Vous devez parenthéser""",
    dumb_replace=chercher.dumb_replace),
    require("find", "Il faut utiliser <tt>find</tt>"),
    reject('$(', "N'utilisez pas <tt>$()</tt> mais <tt>-exec</tt>"),
    require("~",
            """Vous devez changer tous les fichiers
            à partir de la <b>racine de votre compte</b>"""),
    reject("ugo", "Utilisez <tt>a</tt> plutôt que <tt>ugo</tt>"),
    reject("regex",
           "Utilisez <tt>-iname</tt> plutôt qu'une expression régulière"
           ),
    require("-o", "Il faut faire un 'ou', donc il vous faut un <tt>-o</tt>"),
    require(("(", ")"),
            """Il faut parenthéser le 'ou' pour que le <tt>exec</tt>
            s'applique au deux"""),
    Bad(Comment(~(Contain("\\(") | Contain("'('") | Contain('"("'))
                | ~(Contain("\\)") | Contain("')'") | Contain('")"')),
    """N'oubliez pas de protéger les parenthèses,
    car elles sont spéciales pour le shell""")),
    Bad(Comment(~(Contain(" \\( ") | Contain(" '(' ") | Contain(' "(" '))
                | ~(Contain(" \\) ") | Contain(" ')' ") | Contain(' ")" ')),
            """N'oubliez pas les espaces autour des parenthèses.""")),
    shell_require(('png','jpg'), "Pour les images PNG et JPG on a dit.",
            dumb_replace=chercher.dumb_replace),
    number_of_is('-iname', 2, "Je ne vois pas deux <tt>-iname</tt>"),
    reject('u-x', """On ne veut pas enlever le droit d'exécution
    seulement à l'utilisateur, mais au groupe et aux autres"""),
    number_of_is(' ', 13, "Il y a 13 espaces dans la bonne solution"),
    require('-x', """Je ne vois pas l'option de <tt>chmod</tt> indiquant
    que vous voulez enlever le mode d'exécution"""),
    reject('xargs', 'Pas besoin de <tt>xargs</tt>'),
    
    
    shell_display,
    ),
    indices=("Il faut utiliser la commande <tt>find</tt>",
             """On veut enlever le mode <tt>x</tt> à l'utilisateur,
             au groupe et aux autres.
             N'oubliez pas, la réponse doit être la plus courte.""",
             ),
    )
