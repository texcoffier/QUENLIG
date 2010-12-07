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

add(name="intro",
    required = ["intro:intro"],
    before="""La commande <tt>make</tt> permet de compiler,
    de lancer, de vérifier et plein d'autres choses sur vos projets,
    que ceux-ci soient du développement ou autre chose.""",
    question = """Lorsque vous lancez la commande <tt>make</tt>,
    combien cela affiche de lignes à l'écran&nbsp;?""",
    tests = ( Good(Comment(Int(1),
                           """La ligne qui est affichée vous indique
                           que la commande <tt>make</tt> n'a pas trouvé
                           la description de votre projet."""
                           )
                   ),
              Comment("""Votre réponse est impossible :
              <ul>
              <li> Si le répertoire courant est vide, montrez
              cela à un enseignant.
              <li> Si le répertoire courant n'est pas vide
              alors allez dans le bon répertoire
              (celui que vous venez de créer).
              </ul>""" + navigation),
              ),
    )


add(name="makefile",
    required = ["intro"],
    before="""Copiez le texte suivant dans le fichier nommé <tt>Makefile</tt>
    en utilisant un éditeur de texte (<tt>xemacs</tt> de préférence).
    <pre># Ce qui est à gauche des deux points est nommé un 'but' ou 'cible'.
# Ce qui est à droite est ce dont il dépend.
# Les lignes au dessous (en shell) indiquent comment réaliser le but/cible,

CFLAGS = -Wall -Werror -g      # Options de compilation par défaut
LDLIBS = -lm                   # Bibliothèques de fonctions par défaut

mon-projet <b>:</b> avant-compilation execute-mon-programme apres-compilation

avant-compilation <b>:</b>
	@echo "Début compilation à $$(date)"

execute-mon-programme <b>:</b> mon-programme

mon-programme <b>:</b>

apres-compilation <b>:</b>
	@echo "Fin compilation à $$(date)"

</pre>""",
    question = """Lorsque vous lancez la commande <tt>make</tt>,
    combien cela affiche de lignes à l'écran&nbsp;?""",
    tests = (
    Good(Comment(Int(2),
                 """Les deux lignes que vous avez sur l'écran indiquent
                 la date de début et de fin de compilation.
                 Cela a été rapide car il n'y a rien à compiler.
                 <pre>Début compilation : Sat Nov 24 18:05:18 CET 2007
Fin compilation   : Sat Nov 24 18:05:18 CET 2007</pre>"""
                 )
         ),
    Comment("""Vous n'avez pas réussi à faire correctement le copié collé
    pour mettre le texte indiqué sur l'écran.
    <ul>
    <li> Si le message affiché est du genre : <tt>Makefile:8: *** missing separator (did you mean TAB instead of 8 spaces?).  Stop.</tt>
    cela veut dire que les deux lignes qui commencent par <tt>@echo</tt>
    ne sont pas indentées avec une caractère tabulation mais
    avec des espaces.
    <li> Sinon, appelez un enseignant.
    </ul>"""),
    ),
    )

add(name="recompile",
    required = ["main:intro"],
    before = "On vous pose la même question de manière intentionnelle.",
    question = """Lorsque vous lancez la commande <tt>make</tt>,
    combien cela affiche de lignes à l'écran&nbsp;?""",
    tests = (
    Good(Comment(Int(2),
                 """La commande <tt>make</tt> s'est rendue compte en regardant
                 les dates de modification des fichiers que le programme
                 avait déjà été compilé et que c'était un perte de temps
                 de le recompiler""")),
    Comment("""Ne répondez pas au hasard, tapez <tt>make</tt> dans
    le terminal et comptez les lignes"""),
    ),
    )

add(name="exécuter",
    required = ["recompile"],
    before = """La commande <tt>make</tt> peut en plus lancer l'exécutable
    après la création si vous lui demandez.
    <p>
    Ajoutez dans votre fichier <tt>Makefile</tt> la ligne en jaune.
    <pre>...
execute-mon-programme <b>:</b> mon-programme
<span style="background:yellow">	mon-programme arg1 arg2 arg3</span>
...""",
    question = """Lorsque vous lancez la commande <tt>make</tt>,
    combien cela affiche de lignes à l'écran&nbsp;?""",
    tests = (
    Good(Comment(Int(3),
                 """La ligne du milieu indique que la commande
                 <tt>make</tt> a exécuté votre programme.
                 Mais celui-ci n'affiche rien :-(""")),
    Comment("""Ne répondez pas au hasard, tapez <tt>make</tt> dans
    le terminal et comptez les lignes"""),
    ),
    )

add(name="erreur compile",
    required = ["exécuter"],
    before = """Quand la commande <tt>make</tt> rencontre une erreur
    lors de la fabrication d'une cible, elle s'arrête.""",
    question = """Remplacez le <tt>return</tt> par <tt>Return</tt>
    dans le fichier <tt>mon=programme.c</tt> puis lancez <tt>make</tt>
    <p>
    Combien de lignes sont affichées&nbsp;?""",
    tests = ( Good(Comment(IntGT(6),
                           """Après le lancement de la compilation C
                           vous voyez de nombreux messages venant
                           du compilateur.
                           <ul>
                           <li> La première est la plus importante car
                           souvent elle déclenche les suivantes.
                           <li> Sur chaque ligne le nom du fichier
                           source et le numéro de ligne sont indiqués.
                           </ul>
                           
                           <p>
                           La dernière ligne est affichée par la commande
                           <tt>make</tt> et indique la cible qui
                           n'a pas pu être crée.
                           <p>
                           <b>Si vous avez lancé la commande <tt>make</tt>
                           à partir d'<tt>emacs</tt> ou <tt>xemacs</tt>
                           il vous suffit de taper <u><tt>^X `</tt></u>
                           (control-X puis anti-cote)
                           pour que votre curseur se positionne
                           automatiquement sur la prochaine erreur
                           de compilation</b>
                           <p>
                           <em>N'oubliez pas de remettre <tt>return</tt>
                           au lieu de <tt>Return</tt></em>
                           """)),
              Comment("""Avez-vous :
              <ul>
              <li> Mis une majuscule à <tt>return</tt>&nbsp;?
              <li> Sauvegardé le fichier&nbsp;?
              <li> Édité le bon fichier&nbsp;?
              </ul>"""),
              ),
    ),
add(name="erreur",
    required = ["exécuter"],
    before = """Quand la commande <tt>make</tt> rencontre une erreur
    lors d'une exécution, elle s'arrête.""",
    question = """Remplacez le <tt>return 0</tt> par <tt>return 1</tt>
    dans le fichier <tt>mon=programme.c</tt> puis lancez <tt>make</tt>
    <p>
    Quelle est la cible que la commande <tt>make</tt> n'arrive
    pas à créer&nbsp;?""",
    tests = ( Good(Comment(Equal('execute-mon-programme'),
                           """Maintenant remettez le <tt>return 0</tt>
                           car il indique que le programme c'est bien
                           exécuté""")),
              Comment("""La cible qui a échouée est indiqué sur la dernière
              ligne entre les crochets."""),
              ),
    ),
    


   


    
    
