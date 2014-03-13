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


from questions import *
from check import *

add(name="modèle cisco",
    required=["tp1:intro"],
    question="""Quel est le modèle du routeur CISCO
                que vous allez utiliser&nbsp;?
                La réponse est écrite sur la face avant.
             """,
    tests=(
    HostCiscoModele(),
    ),
    indices = ("C'est écrit sur la face avant du routeur.", ),
    )

add(name="nb série",
    required=['modèle cisco'],
    question="""Combien y-a-t-il de ports séries permettant de faire des
    liaisons réseaux sur le routeur CISCO&nbsp;?""",
    tests=(
    require_int(),
    HostCiscoNrSerials(),
    ),
    bad_answer = """Ne comptez pas le port console, c'est une liaison
    série, mais elle ne permet pas de faire du réseau""",
    )

add(name="nb ethernet",
    required=['modèle cisco'],
    question="Combien a-t-il de ports ethernet sur le routeur CISCO&nbsp;?",
    tests=(
    require_int(),
    HostCiscoNrEthernet(),
    ),
    indices = ("""Ou vous regardez sur la documentation, ou vous regardez
    derrière le routeur.
    Attention, ce n'est pas la forme du connecteur qui vous dit si
    c'est ethernet ou non...""", ),
    )

add(name="on off",
    required=['modèle cisco'],
    question="Le routeur CISCO a-t-il un interrupteur marche/arrêt&nbsp;?",
    tests=(
    HostCiscoOnOff(),
    ),
    )

add(name="console eth",
    required=['nb ethernet'],
    before = """On a besoin de détrompeur quand les trous dans lesquels
    on met les connecteurs se ressemblent suffisamment (ou sont identiques)
    pour que l'on se trompe.
    Par exemple&nbsp;:
    <ul>
    <li> La forme interne des connecteurs USB empêche de les brancher à l'envers.
    <li> La forme externe des RJ45, port série (DB-9/DB-25)
    et des cartes mémoires empêche de les brancher à l'envers.
    <li> Sur les connecteurs IDE/SATA et électrique que l'on branche
    à l'intérieur des PC des trous manquants empêchent de se tromper.
    <li> Il n'y a pas de détrompeur sur les prises audio
    et d'alimentation électrique en courant continu,
    on peut donc se tromper :-(.
    </ul>""",
    question="""Sur le routeur CISCO,
    y-a-t-il un détrompeur pour vous empêcher de connecter
    un cable ethernet RJ45 sur le connecteur nommé 'console'&nbsp;?""",
    tests=(
    no("Essayez de faire ce branchement pour vérifier."),
    ),
    good_answer= "Faites attention à ne pas vous tromper dans la suite du TP.",
    )


add(name="show",
    required=['modèle cisco', 'cli:show liste', 'cli:commande incomplète'],
    question="""Quelle commande tapez-vous pour voir la configuration
    <b>matérielle</b> du routeur CISCO&nbsp;?
    <p>
    Attention, pour des raisons mystérieuses il est possible
    que <tt>show ha?</tt> n'affiche pas la bonne réponse...
    """,
    tests=(
    expect('show'),
    good("show hardware"),
    good("show version",
        "Pas très logique comme réponse, comment dit-on matériel en anglais?"),
    ),
    indices = ("""Le paramètre est la traduction de <em>matériel</em>
    en anglais""", ),
    )


add(name="ram",
    required=['show'],
    before="""RAM : Random Access Memory
    <p>
    <em>Attention, ce que l'on appelle RAM n'est ni la mémoire
    <b>flash</b> ni la mémoire non volatile</em>
    <p>
    Attention, le routeur CISCO n'affiche pas la quantité
    de RAM totale mais la RAM libre et la RAM utilisée.
    <p>
    <table>
    <tr><th></th><th>Anglais</th><th>Français</th></tr>
    <tr><td>Booléen</td><td>bit</td><td>bit</td></tr>
    <tr><td>8 bits</td><td>byte</td><td>octet</td></tr>
    </table>
    """,
    question="""Combien de RAM (en kilo-octet)
    y-a-t-il dans le routeur CISCO&nbsp;?
    """,
    tests=(
    require_int(),
    HostCiscoRAM(),
    ),
    indices = (
    """Dans la ligne indiquant la quantité de mémoire,
    le premier chiffre est la mémoire libre, et le deuxième
    la mémoire utilisée par le système.""",
    ),
    )
add(name="nvram",
    required=['ram'],
    before="""NVRAM : Non Volatile RAM.
    <p>
    Cette mémoire est utilisée par le routeur pour sauvegarder
    sa configuration.
    Elle s'utilise comme de la mémoire normale bien que plus lente d'accès.
    """,
    question="""Combien de NVRAM (en kilo-octet)
    y-a-t-il dans le routeur CISCO&nbsp;?""",
    tests=(
    require_int(),
    HostCiscoNVRAM(),
    ),    
    )
add(name="flash",
    required=['nvram'],
    before="""<em>Flash</em> : C'est une sorte de NVRAM qui n'est pas cher mais
    qui lorsque que l'on écrit dedans nécessite d'effacer et de réécrire
    un gros bloc de donnée.
    <p>
    De plus les mémoires <em>flash</em> s'usent en quelque dizaines
    de milliers d'écritures.
    <p>
    De fait, dans les routeurs CISCO elles ne servent qu'à
    stocker l'image du système d'exploitation.
    <p>
    <a href="http://en.wikipedia.org/wiki/Flash_memory">wikipedia:flash</a>.
    """,
    question="""Quelle quantité de mémoire <em>flash</em> (en kilo-octet)
    y-a-t-il dans le routeur CISCO&nbsp;?""",
    tests=(
    require_int(),
    HostCiscoFlash(),
    ),    
    )


 



    



