# -*- coding: latin-1 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2008 Thierry EXCOFFIER, Universite de Lyon
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

"""
Creating session :

QUESTIONS="Questions/unix-devoir2"
SESSION="unix-devoir2"
HOST="proxy710.univ-lyon1.fr"
PORT="10001"
ADMIN="thierry.excoffier"

./main.py $SESSION create $QUESTIONS $PORT url "http://$HOST:$PORT/"
echo "
!gui_smiley
!question_pixel_map_see
" >Students/$SESSION/acls.student
./main.py $SESSION admin $ADMIN start
}

#####################################
Create HTML page for corrections
#####################################
A FAIRE
./corrections.py

"""

from questions import *

add(name="intro",
    before="""
    Avant de commencer à répondre, vous devez avoir lu
    <a href="http://www710.univ-lyon1.fr/~exco/COURS/COURS/UNIX2/unix.html">
    les notes de cours</a> jusqu'à la fin du chapitre sur le <em>shell</em>.
    <p>
    Si vous répondez en recopiant des morceaux venant du cours
    ou bien du web vous n'aurez pas de points.
    """,
    question="Répondez OUI si vous avez compris et si vous avez lu votre cours.",
    tests = ( yes("Répondez OUI"), ),
    )

add(name="réponse unique",
    before="""
    Une fois que vous aurez répondu à une question vous ne pourrez
    plus changer votre réponse.
    <p>
    Vous pouvez changer de question sans y répondre, mais ce que
    vous aurez tapé sera perdu, et vous devrez le retaper après
    être revenu sur la question.
    <p>
    Vous pouvez arrêter de travailler et reprendre plus tard
    si vous le désirez.
    <p>
    Après avoir répondu à certaines questions, d'autres apparaîtront.
    <p>
    Vous devez répondre à toutes les questions jusqu'à ce que cela
    affiche qu'il n'y a plus de questions.
    <p>
    Le logiciel est stupide et affiche «Bonne réponse» pour toutes
    vos réponses même si elles sont fausses.
    """,
    question="Répondez OUI si vous avez compris",
    tests = ( yes("Répondez OUI"), ),
    )



add(name="variable",
    required = ['réponse unique'],
    question="Indiquez le contenu de la variable d'environnement nommée PATH et comment vous avez fait pour afficher ce contenu&nbsp;?",
    nr_lines = 2,
    tests = ( Good(Contain('')), ),
    )

add(name="contexte",
    required = ['variable'],
    question="Quand vous modifiez une variable d'environnement dans un terminal, sa valeur change-t-elle dans les autres&nbsp;? Pourquoi&nbsp;?",
    nr_lines = 2,
    tests = ( Good(Contain('')), ),
    )

add(name="executable",
    required = ['variable'],
    question="Vous avez écrit votre propre programme en langage C, vous le compilez et l'exécutez, le processus peut-il accéder au contenu des variables d'environnement&nbsp;? Pourquoi&nbsp;?",
    nr_lines = 2,
    tests = ( Good(Contain('')), ),
    )

add(name="changement",
    required = ['variable'],
    question="Comment modifiez-vous une variable d'environnement&nbsp;?",
    nr_lines = 2,
    tests = ( Good(Contain('')), ),
    )

add(name="guillemets",
    required = ['variable'],
    question="À quoi servent les guillemets et les cotes (apostrophes)&nbsp;? Expliquez les différences.",
    nr_lines = 6,
    tests = ( Good(Contain('')), ),
    )


add(name="in-out",
    required = ['réponse unique'],
    question="À quoi servent les <em>fildes</em> 0, 1 et 2&nbsp;?",
    nr_lines = 2,
    tests = ( Good(Contain('')), ),
    )

add(name="fichier",
    required = ['in-out'],
    question="Comment lancez-vous une commande pour qu'elle lise son entrée standard à partir d'un fichier et que ce qu'elle écrit sur sa sortie standard soit écrit dans un autre fichier&nbsp;?",
    nr_lines = 2,
    tests = ( Good(Contain('')), ),
    )

add(name="tuyauterie",
    required = ['in-out'],
    question="Comment lancez-vous les commandes <tt>C1</tt> et <tt>C2</tt> pour que ce qui est écrit sur la sortie standard de la commande <tt>C1</tt> soit lu par la commande <tt>C2</tt> sur son entrée standard <b>sans passer par un fichier disque intermédiaire</b>&nbsp;?",
    nr_lines = 2,
    tests = ( Good(Contain('')), ),
    )

add(name="filtre",
    required = ['in-out'],
    before="Un filtre est une commande qui lit son entrée standard, fait un traitement sur ce qui a été lu et écrit le résultat sur sa sortie standard.",
    question="Citez une commande qui est un filtre et qui est indiquée dans le début du cours.",
    nr_lines = 2,
    tests = ( Good(Contain('')), ),
    )

add(name="for",
    required = ['réponse unique'],
    before = "Pensez à utiliser la commande <tt>help</tt> pour avoir des explications courtes sur les commandes du shell (ou <tt>man sh</tt> pour en avoir des longues)",
    question="Pourquoi la boucle <tt>for</tt> du shell ne travaille par sur des nombres&nbsp;?",
    nr_lines = 2,
    tests = ( Good(Contain('')), ),
    )

add(name="sauvegarde",
    required = ['for'],
    question="Donnez la ligne de commande utilisant <tt>for</tt> copiant tous les fichiers se terminant par <tt>.c</tt> dans le répertoire courant en ajoutant <tt>.bak</tt> à la fin.<p>Par exemple <tt>toto.c</tt> est copié sous le nom <tt>toto.c.bak</tt>",
    nr_lines = 2,
    tests = ( Good(Contain('')), ),
    )

add(name="while1",
    required = ['for'],
    question="Expliquez comment fonctionne le premier exemple donné dans le cours pour la boucle <tt>while</tt>.",
    nr_lines = 10,
    tests = ( Good(Contain('')), ),
    )

add(name="while2",
    required = ['for'],
    question="Expliquez comment fonctionne le deuxième exemple donné dans le cours pour la boucle <tt>while</tt>.",
    nr_lines = 10,
    tests = ( Good(Contain('')), ),
    )

add(name="case",
    required = ['for'],
    question="Expliquez comment fonctionne l'exemple donné dans le cours pour la commande <tt>case</tt>.",
    nr_lines = 10,
    tests = ( Good(Contain('')), ),
    )


add(name="if",
    required = ['for'],
    question="Expliquez comment fonctionne l'exemple donné dans le cours pour la commande <tt>if</tt>.",
    nr_lines = 10,
    tests = ( Good(Contain('')), ),
    )


add(name="interprète",
    required = ['réponse unique'],
    question="Si vous tapez le nom d'un fichier exécutable dont la première ligne contient <tt>#!/usr/bin/python</tt> que se passe-t-il&nbsp;?",
    nr_lines = 4,
    tests = ( Good(Contain('')), ),
    )


add(name="séquence",
    required = ['réponse unique'],
    question="Comment taper deux commandes sur la même ligne en les faisant s'exécuter l'une après l'autre&nbsp;?",
    nr_lines = 2,
    tests = ( Good(Contain('')), ),
    )

add(name="esperluette",
    required = ['réponse unique'],
    question="Que se passe-t-il quand vous lancez une commande en la terminant par un caractère <tt>&amp;</tt>&nbsp;?",
    nr_lines = 3,
    tests = ( Good(Contain('')), ),
    )

add(name="substitution",
    required = ['réponse unique'],
    question="Que fait la commande <tt>cat $(cat toto)</tt> en supposant que <tt>toto</tt> contienne <tt>f1 f2 f3</tt>&nbsp;?",
    nr_lines = 3,
    tests = ( Good(Contain('')), ),
    )

add(name="création",
    required = ['fichier'],
    question="Comment créer un fichier texte sous Unix&nbsp;?",
    nr_lines = 3,
    tests = ( Good(Contain('')), ),
    )

























  
    
