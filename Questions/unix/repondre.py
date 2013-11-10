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

add(name="bonjour",
    before="""<IMG SRC="Sunrise_over_the_sea.jpg" align="right">
    <p>
    Bonjour.
    <p>
    Pour répondre aux questions, c'est très simple&nbsp;:
    vous tapez le texte de votre réponse dans le champ texte
    ci-dessous et vous tapez sur la touche qui s'appelle
    &lt;Return&gt;
    ou &lt;Enter&gt;
    ou &lt;Entrée&gt;
    <p>
    Normalement, vous n'avez besoin de la souris que pour
    faire le copier/coller.
    En effet, s'il n'y a pas de réponse à donner,
    le lien sur la prochaine question est activé (il a le <em>focus</em>)
    et il vous suffit de taper &lt;Return&gt;
    pour suivre le lien.""",
    question="Répondez 'bonjour' à cette question.",
    tests=(
    good('bonjour'),
    good("'bonjour'",
     """Je vous accorde la réponse mais les apostrophes
     étaient là uniquement pour séparer le mot du reste de la phrase.
     """),
    good("Bonjour",
     """Je vous accorde la réponse, mais vous ne deviez
     pas mettre de majuscule.
     """),
    reject("echo", "Ce n'est pas une question Unix"),
    ),
    indices=(
    """Vous devez taper la réponse dans
    la zone de saisie qui normalement est blanche et qui est
    juste au dessus.""",
    ),
    good_answer="""La réponse attendue à toutes les questions
    que vous aurez à donner par la suite sera <b>la plus courte</b>.
    Les réponses qui ne sont pas minimales en nombre de caractères
    seront refusées.""",
    )

add(name="intro",
    required=["bonjour"],
    question="""Ces exercices ne sont pas notés.
    Néanmoins, si vous trichez en utilisant une liste de bonnes réponses
    vous n'apprendrez rien du tout.
    <p>
    Répondez OUI si vous avez compris.
    """,
    tests = (
    yes("""Alors appelez un enseignant pour qu'il vous explique."""),
    ),
    )


add(name="combien de titres",
    required=["intro"],
    question="""Combien y-a-t-il de titres de boites dans la colonne
    de gauche de cette page web&nbsp;?""",
    tests=(
    good("5"),
    bad("4", """N'oubliez pas de faire défiler la fenêtre pour voir si
    vous n'en oubliez pas"""),
    require_int(),
    ),
    )


class check_nr_possible_questions(TestWithoutStrings):
    def test(self, student_answer, string, state=None):
        if state:
            return len(state.student.answerables()) == int(student_answer)


add(name="questions possibles",
    required=["intro"],
    question="""Combien y-a-t-il de questions différentes
    dans la liste des questions que vous avez le droit
    de choisir maintenant (en comptant celle-ci)&nbsp;?""",
    tests=(
    require_int(),
    check_nr_possible_questions(),
    ),
    )

class check_nr_questions(TestWithoutStrings):
    def test(self, student_answer, string, state=None):
        if state:
            return len(questions) == int(student_answer)

add(name="questions en tout",
    required=["intro"],
    question="""Quel est le nombre total de questions
    qui sont prévues dans ce sujet de TP&nbsp;?""",
    tests=(
    require_int(),
    check_nr_questions(),
    ),
    indices=(
             "C'est indiqué dans les statistiques",
             "C'est le nombre de questions en tout."
             ),
    )

class check_nr_items(TestWithoutStrings):
    def test(self, student_answer, string):
        import server
        nb = server.get_file("help.html").content.count('<li')
        nb2 = server.get_file("help.html").content.count('<li ')
        a = int(student_answer)
        if a == nb:
            return True
        if a == nb - nb2:
            return True, "Mais vous avez oublié les puces de deuxième niveaux"
        return False, "Recomptez, vous vous êtes trompé"

add(name="aide",
    required=["questions en tout"],
    before="Lisez la page d'aide/explication.",
    question="""Combien de puces (<em>item</em>) sont affichées
    sur la page d'aide accessible dans le menu de gauche&nbsp;?""",
    tests=(
    require_int(),
    bad('0', """Une puce est un petit dessin à gauche d'un élément
    d'une énumération"""),
    check_nr_items(),
    ),
    indices=("""La puce est le petit symbole que l'on trouve
    à gauche d'un paragraphe quand on fait une énumération""",
             ),
    good_answer = """Maintenant vous n'aurez pas le droit de dire
    que vous ne savez pas comment ce passe le TP'""",
    )

add(name="commentaire",
    required=["indices"],
    before="""Le cadre «Faites un commentaire» en bas à gauche permet de taper
    des commentaires à propos des questions pour améliorer ce sujet
    de TP d'une fois sur l'autre&nbsp;:
    <ul>
    <li> L'énoncé vous pose un problème (ambigu, fautes d'orthographe, ...)
    <li> Une réponse correcte est refusée sans explication.
    <li> Les indices ne sont pas suffisants ou faux.
    <li> Il manque des prérequis.
    <li> ...
    </ul>
    Après avoir tapé un commentaire il faut cliquer
    sur le bouton pour l'envoyer.
    <p>
    <b>Tout</b> ce que vous faites
    est enregistré afin que les enseignants puissent
    évaluer votre travail.
    """,
    question="""Combien de lignes de commentaires peut-on écrire
    dans la zone de commentaires sans que le texte tapé
    se décale vers le haut&nbsp;?
    La zone suivante contient 3 lignes&nbsp;:
    <pre>1
2
3</pre>

    """,
    tests=(
    good( ("10", "11", "12") ),
    require_int(),
    ),
    )

add(name="indices",
    required=["intro"],
    question="""Combien d'indices vous donne-t-on pour répondre
    à cette question&nbsp;?""",
    tests=(
    good("2"),
    bad("0", """Si on ne vous donnais pas d'indice pour répondre à la question,
    il n'y aurais pas de lien nommé&nbsp;: «Donnez-moi un indice»"""),
    bad("1",
        """S'il n'y avait qu'un seul indice, le lien se serait nommé.
        <p>
        <em>Donnez-moi l'indice</em>
        <p>
        Et non :
        <p>
        <em>Donnez-moi un indice</em>
        """),
    require_int(),
    ),
    indices=("Je suis le premier indice",
             "Je suis le deuxième indice"),
    )

add(name="humour",
    required=["indices"],
    question="Quelle est la réponse à cette question&nbsp;?",
    tests=(
    good("42"),
    bad("humour", "Très astucieux, félicitation. Mais ce n'est pas ça."),
    require_int(),
    comment("Vous ne pouvez pas répondre à la question sans regarder l'indice"),
    ),
    indices=("La réponse à cette question est <tt>42</tt>", ),
    )

add(name="meta",
    required=["humour"],
    question="<tt>Quel</tt> est la réponse à cette question.",
    tests=(
    good("Quel"),
    good("quel", "Accepté, mais c'était avec une majuscule"),
    reject("meta", "Lisez les indices."),
    ),
    indices=(
    """Lisez bien la phrase en séparant les mots qui font partie
    de la phrase de ceux qui sont le sujet de la phrase.
    <p>
    A ne pas lire pendant la séance de TP : <A HREF='http://www.abbottandcostello.net/who.htm'>Who's On First</A>""",
    """Avez-vous remarqué que les mots de la phrase
    ne sont pas tous dans la même fonte&nbsp;?""",
    """La question n'a pas de point d'interrogation, ce n'est
    donc pas une question, mais une réponse :-)""",
             ),
    good_answer = """Vous comprenez maintenant qu'il faut faire attention
    à tous les détails quand on lit une documentation ou bien
    les questions qui vous sont posées.""",
    )


class check_nr_good_answers(TestWithoutStrings):
    def test(self, student_answer, string, state=None):
        if state:
            try:
               return state.student.number_of_good_answers()== int(student_answer)
            except ValueError:
               return False

add(name="répondre",
    required=["combien de titres", "questions possibles", "questions en tout",
              "commentaire"],
    before="""Vous savez maintenant utiliser ce programme pour
    répondre aux questions.""",
    question="""A combien de questions avez vous répondu correctement
    sans compter celle-ci&nbsp;?""",
    tests=(
    check_nr_good_answers(),
    require_int(),
    ),
    )
