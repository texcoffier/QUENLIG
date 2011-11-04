# -*- coding: latin-1 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2006 Thierry EXCOFFIER, Universite Claude Bernard
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
    required=["copier:recursif"],
    question="""Quel est le nom de la commande permettant d'archiver
    une hiérarchie de fichier dans un seul fichier&nbsp;?""",
    tests=(
    reject('cp', """<tt>cp</tt> copier des fichiers, il ne permet
    pas de transformer un hiérarchie en un seul fichier."""),
    reject(' ', "On veut seulement un nom de commande, pas d'argument"),
    good("tar"),
    bad("cpio",
        """Cette commande est standard mais n'est pas beaucoup utilisée.
        Vous ne trouver pas de fichiers <tt>cpio</tt> sur
        Internet, mais des fichiers...."""),
    ),
    indices=(
    """C'est la contraction de <tt>Tape archival</tt>, <em>tape</em>
    veut dire 'bande'.""",
    ),
    good_answer="""Il est intéressant d'utiliser une telle archive
    pour stocker sur une clef USB par exemple car on a l'assurance
    de ne pas perdre d'information sur les noms et les
    droits des fichiers.
    Ce qui n'est pas le cas si l'on utilise la commande <tt>cp</tt>""",
    )

dumb_replace = ( ('-fc', '-cf'), ('-fx', '-xf'), ('v', ''),
                 ('-x -f', '-xf'),
                 ('&&', ';'), (' ;', ';'), ('; ', ';'), (' \\;', '\\;'))

add(name="création",
    required=["intro"],
    question="""Donnez la ligne de commande permettant
    d'archiver la hiérarchie <tt>PratiqueUnix</tt>
    dans le fichier <tt>PratiqueUnix.tar</tt>""",
    tests=(
    require('-', """Même si la commande accepte que l'on ne mette
    pas le tiret devant les options il est conseillé de le mettre."""),
    require('tar', "On vous dit d'utiliser <tt>tar</tt>&nbsp;!"),
    shell_bad("tar -cf - PratiqueUnix >PratiqueUnix.tar",
              """C'est juste, mais il y a plus court (sans
              le <tt>-</tt> et le <tt>&gt;</tt>""",
              dumb_replace=dumb_replace),
    shell_bad("tar -cf PratiqueUnix PratiqueUnix.tar",
              """Vous n'avez pas essayé, il y a un problème d'ordre
              des arguments""",
               dumb_replace=dumb_replace),
    reject('>', """Faite cette commande en utilisant l'option <tt>f</tt>
    à la place d'une redirection"""),
    require('f', """Vous devez utiliser l'option <tt>f</tt> pour
    indiquer le fichier destination"""),
    require('c', """Vous devez utiliser l'option <tt>c</tt> pour
    indiquer que c'est une création d'archive"""),
    reject(('-c -f', '-f -c'), "Il est plus court d'écrire <tt>-cf</tt>"),
    shell_good("tar -cf PratiqueUnix.tar PratiqueUnix",
               dumb_replace=dumb_replace),
    shell_good("tar -cf PratiqueUnix.tar PratiqueUnix/",
               """Le <tt>/</tt> final n'est utile que dans le cas
               ou le répertoire <tt>PratiqueUnix</tt> est un lien symbolique.
               En effet, si c'est le cas, alors sans le <tt>/</tt>
               c'est le lien qui serait sauvez et non le répertoire pointé.""",
               dumb_replace=dumb_replace),
    number_of_is('PratiqueUnix', 2,
                 """Je ne vois pas deux fois le mot <tt>PratiqueUnix</tt>
                 dans votre réponse"""),
    shell_display,
    ),
    good_answer = """C'est une très mauvaise idée de faire&nbsp;:
    <pre>tar -cf PratiqueUnix.tar .</pre>
    Car&nbsp;:
    <ul>
    <li> La commande va essayer d'archiver le fichier <tt>PratiqueUnix.tar</tt>
    dans lui-même.
    <li> Et si l'on corrige le problème précédent en mettant
    <tt>/tmp/PratiqueUnix.tar</tt> alors c'est pénible pour la personne
    qui extrait l'archive dans son répertoire de connexion
    car cela va lui ajouter tous les fichiers de l'archive dedans :-(.
    </ul>""",
    indices = (
    """Le nom du répertoire à sauver est un argument et non une option
    il se trouve donc naturellement à la fin de la ligne de commande.""",
    ),
    )

add(name="extraction",
    required=["création"],
    question="""Donnez la ligne de commande permettant
    d'extraire le contenu du fichier <tt>PratiqueUnix.tar</tt>
    en le mettant dans le répertoire courant.""",
    tests=(
    require('tar', "On utilise <tt>tar</tt>"),
    require('-x', """Vous devez utiliser l'option <tt>x</tt> pour
    indiquer que c'est une extraction d'archive"""),
    require('f', """Il faut l'option <tt>f</tt> pour indiquer
    le nom du fichier contenant l'archive"""),
    reject(' .', """L'extraction est toujours faite dans le répertoire courant,
    ce n'est donc pas la peine de l'indiquer."""),
    shell_good("tar -xf PratiqueUnix.tar", dumb_replace=dumb_replace),
    shell_good("tar -f PratiqueUnix.tar -x", dumb_replace=dumb_replace),
    number_of_is(' ', 2,
                 """Normalement, le premier argument de la commande
                 <tt>tar</tt> contient les options et le deuxième
                 le nom de l'archive à extraire"""),
    reject('z', "Pourquoi l'option <tt>z</tt> ?"),
    expect('PratiqueUnix.tar'),
    shell_display,
    ),
    )

add(name="copie distante",
    required=["création", "extraction", "distancer:des commandes",
              "pipeline:intro", "sh:aller dans"],
    question="""On suppose que le répertoire <tt>/tmp/toto</tt>
    sur la machine <tt>b201pc34</tt> existe et est vide.
    <p>
    Donner la ligne de commande permettant de copier la hiérarchie
    courante (donc <tt>.</tt>)
    dans le répertoire <tt>/tmp/toto</tt> de la machine <tt>b201pc34</tt>
    <p>
    Vous connaissez déjà tout ce qui est nécessaire pour le faire.
    """,
    tests=(
    shell_good(("tar -cf - . | ssh b201pc34 'cd /tmp/toto;tar -xf -'",
                "tar -cf - . | ssh b201pc34 cd /tmp/toto\;tar -xf -"
                ),
               dumb_replace=dumb_replace),
    reject('.tar', """Vous n'avez pas besoin de passer par un fichier
    <tt>.tar</tt> puisque vous utilisez un pipeline"""),
    reject(('scp', 'rcp'), """Avec <tt>scp</tt> ou <tt>rcp</tt> c'est bien,
    mais on vous demande de répondre avec ce que vous avez déjà vu
    durant ce TP (regardez les prérequis)."""),
    reject('z', 'On ne vous demande pas de comprimer'),
    reject('C', """Utiliser l'option <tt>C</tt> est un bonne idée,
    mais plutôt que de cherche des solutions compliquées,
    utilisez ce que vous connaissez déjà&nbsp; la commande <em>builtin</em>
    <tt>cd</tt> permet de changer de répertoire."""),
    require(';', """Sur la machine distante il faut faire exécuter
    deux commandes&nbsp;: le <tt>cd</tt> et le <tt>tar</tt>"""),
    require('tar',
            "Il faut utiliser <tt>tar</tt> pour copier une hiérarchie"),
    number_of_is('tar', 2,
                 "Il faut 2 tar, un pour créer l'archive, un pour l'extraire"),
    require('|',
            "On utilise un <em>pipeline</em> pour connecter les <tt>tar</tt>"),
    require('ssh',
            "On utilise <tt>ssh</tt> pour exécuter une commande à distance."),
    require('.', """Il faut donner au <tt>tar</tt> qui crée l'archive
    le nom du répertoire à sauvegarder"""),
    require('tar -cf - .',
            """Je ne vois pas le <tt>tar</tt> qui crée l'archive,
            ou bien il est faux.""",
            replace=dumb_replace),
    require('tar -xf -',
            """Je ne vois pas le <tt>tar</tt> qui extrait l'archive
            ou bien il est faux.""",
            replace=dumb_replace),
    require('cd /tmp/toto',
            """Je ne vois pas le changement de répertoire.""",
            replace=dumb_replace),
    shell_bad("tar -c . | ssh b201pc34 'cd /tmp/toto;tar -x'",
              """Cette commande fonctionne en effet.
              Mais elle n'est pas 100%% portable,
              indiquez-lui explicitement les fichiers d'entrée/sortie""",
              dumb_replace=dumb_replace),
#     shell_require(("<argument>cd /tmp/toto;tar -xf -</argument>",
#                    "<argument>cd /tmp/toto;tar -xf -</argument>"
#                    ),
#                   """Si le <tt>;</tt> n'est pas protégé il s'exécutera
#                   sur la machine locale""",
#                   dumb_replace=dumb_replace),
    shell_display,
    ),
    )
    



    
