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

from QUENLIG.questions import *
from .check import *

add(name="intro",
    required=["archiver:création"],
    before="""La compression et la décompression d'un fichier
    peut être faite avec différents outils.
    <table>
    <tbody>
    <tr>
    <th>Extension</th><th>compresseur</th><th>décompresseur</th><th>Commentaire</th>
    </tr>
    <tr>
    <td>.Z</td><td><tt>compress</tt></td><td><tt>uncompress</tt></td>
    <td>Outils standard unix maintenant totalement obsolète</td>
    </tr>
    <tr>
    <td>.gz</td><td><tt>gzip</tt></td><td><tt>gunzip</tt></td>
    <td>Outils le plus couramment utilisé (<a href="http://www.gnu.org/licenses/licenses.fr.html">licence GPL</a>)</td>
    </tr>
    <tr>
    <td>.bz2</td><td><tt>bzip2</tt></td><td><tt>bunzip2</tt></td>
    <td>Plus performant que <tt>gzip</tt></td>
    </tr>
    </tbody>
    </table>""",
    question="""Quel compresseur permet d'obtenir des fichiers <tt>gz</tt>&nbsp;?""",
    tests=(
    bad('zip',
        """Cet outil (non proposé dans la liste) est un archiveur/compresseur,
        Ce n'est donc pas un simple compresseur"""),
    good("gzip"),
    ),
    )

add(name="comprimons",
    required=["intro"],
    question="""Quelle commande tapez-vous pour comprimer
    le fichier <tt>toto</tt>""",
    tests=(
    reject(("<",">"), "On veut la version simple sans redirection"),
    reject('tar', """On ne veut pas créer une archive contenant
    plusieurs fichiers mais simplement comprimer un fichier"""),
    require("gzip",
            """Je ne trouve pas le nom du compresseur dans votre réponse.
            Pourtant vous l'avez donné dans une question précédente"""),
    shell_good("gzip toto"),
    shell_bad("gzip -c toto", "L'option <tt>-c</tt> est inutile"),
    shell_display,
    ),
    good_answer="""Vous remarquerez que votre fichier <tt>toto</tt>
    à disparu, il n'y a que <tt>toto.gz</tt>""",
    )

add(name="garde l'original",
    required=["intro", "sh:'Bonjour' dans 'toto'", "variable:lire ligne"],
    question="""Quelle commande tapez-vous pour comprimer
    le fichier <tt>toto</tt> mais en gardant l'original
    et en stockant le résultat dans <tt>toto.gz</tt>.""",
    tests=(
    reject('-', "Vous n'avez besoin d'aucune option."),
    expect('toto.gz'),
    expect('gzip'),
    reject(("-c", "-N"),
              """Pourquoi s'embêter à apprendre toutes les options&nbsp;?
              Votre commande est peut-être juste, mais refaite là sans
              l'option <tt>-c</tt> ou <tt>-N</tt>"""),
    require(("<",">"),
            """Il suffit de rediriger l'entrée et la sortie standard
            et de ne donner AUCUN paramètre à la commande <tt>gzip</tt>
            """),
    shell_good("gzip <toto >toto.gz"),
    shell_bad("gzip <toto.gz >toto",
              """Cette commande compresse <tt>toto.gz</tt> (cela sert à rien)
              et stocke le fichier comprimé deux fois dans <tt>toto</tt>"""),
    shell_display,
    ),
    )

add(name="décomprimons",
    required=["comprimons"],
    question="""Quelle commande tapez-vous pour décomprimer
    le fichier <tt>toto.gz</tt>""",
    tests=(
    reject(("<",">"), "On veut la version simple sans redirection"),
    require('toto.gz', "C'est <tt>toto.gz</tt> que vous voulez décomprimer"),
    shell_good("gzip -d toto.gz",
               """La commande que vous avez indiquée est excellente
               pour les scripts, mais en interactif <tt>gunzip</tt>
               est plus courte.
               Seul celle-ci sera acceptée dans la suite du TP."""),
    shell_good("gunzip toto.gz"),
    shell_display,
    ),
    good_answer="""Vous remarquerez que votre fichier <tt>toto.gz</tt>
    à disparu, il n'y a que <tt>toto</tt>""",
    )

add(name="garde le compressé",
    required=["décomprimons","sh:'Bonjour' dans 'toto'","variable:lire ligne"],
    question="""Quelle commande tapez-vous pour décomprimer
    le fichier <tt>toto.gz</tt> mais en gardant l'original
    et en stockant le résultat dans <tt>toto</tt>.""",
    tests=(
    Reject(";", "Une seule commande est nécessaire, donc pas de ';'"),
    expect('toto.gz'),
    reject("-c",
              """Pourquoi s'embêter à apprendre toutes les options&nbsp;?
              Votre commande est peut-être juste, mais refaite la sans
              utiliser l'option <tt>-c</tt> (mais en modifiant la commande),
              votre réponse sera plus courte."""),
    require(("<",">"),
            "Il suffit de rediriger l'entrée et la sortie standard"),
    shell_bad("gzip <toto.gz >toto",
              "<tt>gzip</tt> sert à compresser, pas à décompresser"),
    shell_good("zcat <toto.gz >toto", "Le &lt; est inutile"),
    shell_good("zcat toto.gz >toto"),
    shell_good("gunzip <toto.gz >toto", "<tt>zcat</tt> est plus court"),
    shell_good("gzip -d <toto.gz >toto",
               """Pour ma part, je trouve que c'est plus lisible
               d'utiliser la commande <tt>gunzip</tt> ou <tt>zcat</tt>"""),
    reject(('<toto ','< toto '),
           """Vous redirigez l'entrée standard vers <tt>toto</tt> alors
           qu'il n'existe pas encore"""),
    shell_display,
    ),
    )

from . import archiver

add(name="comp. archive",
    required=["garde l'original", "archiver:création", "pipeline:intro"],
    before="""Pour beaucoup de commandes Unix,
    le nom de fichier <tt>-</tt> (tiret ou moins)
    représente l'entrée ou la sortie standard.""",
    question="""Faites un archivage du répertoire <tt>PratiqueUnix</tt>
    et stockez l'archive compressée dans <tt>PratiqueUnix.tar.gz</tt>.
    <p>
    Attention&nbsp;:
    <ul>
    <li> Vous ne devez pas stocker un fichier non comprimé sur le disque.
    <li> Vous n'avez pas besoin de chercher une nouvelle option
    dans la documentation car vous connaissez déjà tout ce qui est nécessaire.
    <b>Surtout pas l'option 'z' qui n'est pas standard</b>
    </ul>
    """,
    tests=(
    reject('<', "Expliquez à un enseignant pourquoi vous utilisez '&lt;'"),
    reject('/',
           """Pas besoin de <tt>/</tt> (à moins que <tt>PratiqueUnix</tt>
           soit un lien symbolique)"""),
    require('-c',
            """Pour <tt>tar</tt>,
            ll faut indiquer l'option de création <tt>c</tt>,
            N'oubliez pas le tiret avant les options.
            Il faut le mettre même si cela marche sans."""),
    reject('gzip -', "Pas besoin d'option pour <tt>gzip</tt>"),
    require('gzip', "On comprime avec <tt>gzip</tt>"),
    require(' - ', """Où est le tiret indiquant que <tt>tar</tt>
    doit écrire l'archive sur la sortie standard&nbsp;?"""),
    require('|', """Il faut connecter la sortie standard de la
    commande <tt>tar</tt> à l'entrée standard de la commande <tt>gzip</tt>
    avec un <em>pipe</em>"""),
    require('>', """La sortie standard de <tt>gzip</tt> doit
    être redirigée vers le fichier compressé que l'on veut créer"""),
    expect('PratiqueUnix.tar.gz'),
    shell_good("tar -cf - PratiqueUnix | gzip >PratiqueUnix.tar.gz",
               dumb_replace=archiver.dumb_replace),
    require('f',
            "Il manque l'option <tt>f</tt> indiquant le fichier de sortie"),
    shell_bad("tar -cf PratiqueUnix - | gzip >PratiqueUnix.tar.gz",
              """Oups, la commande <tt>tar</tt> écrit l'archive du répertoire
              <tt>-</tt> dans le fichier <tt>PratiqueUnix</tt>"""),
    reject('<', "Pourquoi redirigez-vous l'entrée standard&nbsp;?"),

    shell_display,
    ),
    )

add(name="decomp. archive",
    required=["comp. archive", "décomprimons", "archiver:extraction"],
    question="""Décompressez <tt>PratiqueUnix.tar.gz</tt> et
    extrayez les fichiers dans le répertoire courant sans passer
    par un fichier intermédiaire.
    """,
    tests=(
    reject('>', "Expliquez à un enseignant pourquoi vous utilisez '&gt;'"),
    require('|', "Comme pour la compression, il faut un pipeline"),
    require('PratiqueUnix.tar.gz', "Je ne vois pas le nom de l'archive"),
    reject("gunzip PratiqueUnix.tar.gz",
              """Cela ne fonctionne pas, vous venez de décomprimer
              l'archive dans le répertoire courant sans l'extraire.
              En effet, la commande <tt>gunzip xxx.gz</tt> n'écrit rien
              sur la sortie standard.
              """,
              ),
    shell_good("gunzip <PratiqueUnix.tar.gz | tar -xf -",
               dumb_replace=archiver.dumb_replace),
    shell_good("gzip -d <PratiqueUnix.tar.gz | tar -xf -",
               dumb_replace=archiver.dumb_replace),
    shell_bad("gzip -d PratiqueUnix.tar.gz | tar -xf -",
              "<tt>gzip</tt> ne va rien écrire sur sa sortie standard.",
               dumb_replace=archiver.dumb_replace),
    reject((' -c', '-dc'),
              """Pourquoi s'embêter à apprendre toutes les options&nbsp;?
              Votre commande est juste, mais refaite là sans
              l'option <tt>c</tt>"""),
    shell_good("zcat PratiqueUnix.tar.gz | tar -xf -",
               dumb_replace=archiver.dumb_replace),
    require('f -', """Il faut dire à la commande <tt>tar</tt>
    de lire l'entrée standard (-)"""),
    reject_endswith(' .', """L'extraction de l'archive est faite dans le
    répertoire courant, pas besoin d'indiquer le <tt>.</tt> à la fin."""),
    require('-x', """Où est l'option indiquant que l'on veut extraire
    une archive&nbsp;?"""),
    require_endswith(' -',
                     """Lors de l'extraction de l'archive,
                     elle se fait automatiquement dans le répertoire
                     courant, pas besoin d'indiquer ou la mettre."""),
    shell_display,
    ),
    good_answer = """La commande <tt>tar</tt> supporte une option
    <tt>z</tt> mais je déconseille de l'utiliser car elle cache
    le programme utilisé pour comprimer/décomprimer""",
    )




    
 
