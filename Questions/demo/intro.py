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
import random
from questions import *
from check import *

reject_quotes = reject("'", "Il ne faut pas recopier les apostrophes&nbsp;!")

add(name="première",
    before="""Cette question s'affiche en premier car sans prérequis.""",
    question="Répondez 'bonjour'",
    tests=(reject_quotes,
           Good(Equal("bonjour")),
           Good(Comment(Equal("Bonjour"),
                "J'accepte la réponse bien que vous ayez mis une majuscule")),
           comment("Écrivez en bon français s'il vous plais"),
           ),
    indices=("Vous devez écrire 'bonjour' dans le rectangle blanc",
             "Après avoir écrit la réponse, il faut taper &lt;Return&gt;",
             ),
    good_answer="Pour passer à la question suivante, tapez sur return",
    )

def question_aleatoire():
    a = random.randrange(0,100)
    b = random.randrange(0,100)
    return "%d + %d = ?" % (a, b)


class reponse_aleatoire(TestWithoutStrings):
    def test(self, student_answer, string):
        r = random.randrange(0,100) + random.randrange(0,100)
        if r == int(student_answer):
            return True, ""
        else:
            return False, "Vous vous trompez de %d" % (r - int(student_answer))

add(name='aléatoire',
    required = [ 'première' ],
    question=question_aleatoire,
    tests=(require_int(),
           reponse_aleatoire(),
           ),
    )

add(name='shell',
    required = [ 'première' ],
    before="""Ce système a été développé pour analyser des réponses
    qui sont des commandes shell.
    <ul>
    <li> Il canonise les lignes de commande shell
    <li> Il traduit même certaine options équivalentes.
    <li> Il affiche l'arbre syntaxique de la commande
    </ul>""",
    question="La réponse est 'ls -ls >toto'",
    tests=(shell_good('ls -ls >toto'),
           shell_display,
           ),
    nr_lines=15,
    default_answer="""
 ls $A $(A) '$A' "$A" "*" * \* |
 (
   read A
   echo $A >toto
   cat
 ) |
 while read A
 do
   for I in 1 2
      do
          echo $I
      done
 done >titi""",
    )

add(name='outils',
    required = [ 'première' ],
    before = """Il est facile de faire plein de petits
    outils pour tester les réponses.
    Certaines existent déjà :
    <tt>answer_length_is</tt>,
    <tt>number_of_is</tt>,
    <tt>require_int</tt>,
    <tt>comment</tt>,
    """,
    question = 'Répondre "[[]]"',
    tests = (reject_quotes,
             answer_length_is(4, 'La réponse tient sur 4 caractères !'),
             number_of_is('[',2, "Il y a deux '['"),
             number_of_is(']',2, "Il y a deux ']'"),
             good('[[]]'),
             comment('Et il faut les mettre dans le bon ordre !'),
             ),
    )
    

add(name='requis simple',
    required = [ 'aléatoire', 'shell', 'outils' ],
    before = """Pour répondre à cette question, il faut avoir
    répondu au 3 questions prérequises""",
    question = '?',
    tests = (good('?'), ),
    )

add(name='requis minuscule',
    required = [ 'première(^[a-z].*)' ],
    before = """Vous voyez cette question car vous avez répondu avec
    une minuscule à la première question""",
    question = '?',
    tests = (good('?'), ),
    )

add(name='requis majuscule',
    required = [ 'première(^[A-Z].*)' ],
    before = """Vous voyez cette question car vous avez répondu avec
    une majuscule à la première question""",
    question = '?',
    tests = (good('?'), ),
    )
