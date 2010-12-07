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

from questions import *
from check import *




two_spaces = """Il y a deux espaces au lieu d'un dans la phrase,
mais ce n'est pas grave."""

add(name="un grand chien",
    required=['texte:multiplication texte', 'dis:multiple'],
    question="""Fais afficher à Python la phrase&nbsp;:<br>
    <em>Un très très très très très très très très très très grand chien.</em><br>
    Plutôt que d'écrire 10 fois le mot <em>très</em>
    il faut faire une multiplication.""",
    tests=(
    print_required,
    space_required,
    apostrophe_required,
    multiply_required,
    require('10',
            'Il y a 10 fois le mot <em>très</em>, il faut donc multiplier par 10.'),
    require('U', 'La phrase commence par une majuscule.'),
    require('.', 'La phrase se termine par un point.'),
    python_answer_good('Un' + ' très'*10 + ' grand chien.\n', 'Parfait !'),
    python_answer_good('Un' + ' très'*10 + '  grand chien.\n', two_spaces),
    python_answer_good('Un ' + ' très'*10 + ' grand chien.\n', two_spaces),
    ),    
    )

add(name="remplace",
    required=['texte:remplacer', 'pour:compter de 2 en 2'],
    question="""Fais afficher par python la phrase
    <tt>Un * qui aime les *s et les *tons</tt>
    en remplaçant le caractère <tt>*</tt> par <tt>chat</tt>,
    puis par <tt>chien</tt> puis par <tt>ours</tt>""",
    default_answer="print 'Un * qui aime les *s et les *tons'",
    tests=(
    do_not_cheat(rejected='chats'),
    replace_required,
    python_answer_good('''Un chat qui aime les chats et les chattons
Un chien qui aime les chiens et les chientons
Un ours qui aime les ourss et les ourstons
'''),
    ),
    indices=(
    """Il faut faire&nbsp;: pour chaque <em>animal</em>
    dans le classeur contenant
    <tt>chat</tt> et <tt>chien</tt> et <tt>ours</tt>&nbsp;:
    dis <tt>Un * qui aime les *s et les *tons</tt> en remplaçant
    l'étoile par l'<em>animal</em>.""",
    )
    )

def poeme():
    s = ''
    for sujet in ['un chat', 'un chien', 'un cheval']:
        for verbe in ['mange', 'regarde']:
            for complement in ['des salades', 'un poisson']:
                s += "%s %s %s\n" % (sujet, verbe, complement)
    return s.replace(' ', '')


add(name="poème",
    required=['pour:imbriqués'],
    question="""Faire afficher toutes les phrases construite avec
    <ul>
    <li> un sujet parmi les suivants&nbsp;:
         <em>un chat</em> ou <em>un chien</em> ou <em>un cheval</em>
    <li> un verbe parmi les suivants&nbsp;:
         <em>mange</em> ou <em>regarde</em>
    <li> le complément d'objet direct parmi les suivants&nbsp;:
         <em>des salades</em> ou <em>un poisson</em>
    </ul>    
    """,
    nr_lines=5,
    tests=(
    print_required,
    space_required,
    apostrophe_required,
    square_bracket_required,
    for_required,
    number_of_is('for', 3,
                 """Il faut 3 <tt>for</tt> pour cet exercice, un pour le sujet,
                 un pour le verbe et un pour le complément"""),
    python_answer_good(poeme(), remove_spaces=True),
    ),
    indices=(
    """Un exemple :
    <pre>for a in ['m', 's']:
    for b in ['o', 'e']:
        for c in ['n', 'r']:
            print a,b,c</pre>
    Affiche :
    <pre>m o n
m o r
m e n
m e r
s o n
s o r
s e n
s e r</pre>
""",
    ),
    )


def conjugue():
    i = ''
    for verbe in ('jou', 'travaill', 'soup', 'ronfl'):
        for sujet, suffixe in (('je','e'),('tu','es'),('il','e'),
                      ('nous','ons'),('vous','ez'),('ils','ent')):
            i += sujet + ' ' + verbe + suffixe + '\n'
        i += '\n'
    return i


add(name="-er présent",
    required=['pour:multi lignes', 'texte:addition texte', 'dis:rien'],
    question="""Fais afficher la conjugaison de jouer, travailler, souper, ronfler
    au présent&nbsp;:
<pre>je joue
tu joues
il joue
nous jouons
vous jouez
ils jouent

je mange
tu manges
...</pre>
    <p>
    Utilise un boucle pour feuilleter les verbes et dans la boucle
    fais 6 <tt>print</tt> pour faire <em>je tu il nous vous ils</em>.
    <p>
    N'oublie pas la ligne vide après chaque verbe.
    """,
    nr_lines = 8,
    tests=(
    print_required,
    space_required,
    square_bracket_required,
    for_required,
    python_answer_good(conjugue()),
    ),
    indices = (
    """Il faut feuilleter un classeur contenant les verbes
    sans le <em>er</em> de la fin.
    Comme cela, il suffit d'ajouter la fin.""",
    ),
    )

def voyelle():
    s = ''
    for i in 'un grand chien':
        if i in 'aeiou':
            s += i + ' '
    return s[:-1]

add(name='enlève voyelles',
    required=['booleen:dans', 'pour:dé + dé = 7', 'dis:même ligne'],
    question="""Fais écrire la phrase '<b>u</b>n gr<b>a</b>nd ch<b>ie</b>n' en écrivant
    que les voyelles (on trouve les voyelles dans le texte
    <tt>'aeiou'</tt>).
    <p>
    Python doit écrire&nbsp;:
    <pre>%s</pre>""" % voyelle(),
    nr_lines = 4,
    tests=(
    print_required,
    space_required,
    for_required,
    if_required,
    comma_required,
    in_required,
    require("'aeiou'", "La liste des voyelles est <tt>'aeiou'</tt>"),
    require("'un grand chien'", "Il est où le grand chien&nbsp;?"),
    python_answer_good(voyelle() + '\n'),
    ),
    indices=(
    """Tu dois faire faire à Python&nbsp;:
    <em>pour toutes les lettres de 'un grand chien' :
    si la lettre est dans 'aeiou' alors affiche la lettre.""",
    ),
    )
    
    
