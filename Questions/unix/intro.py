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
    required=['repondre:répondre'],
    before="""Cette série de question est là pour que l'on
    soit d'accord sur le nom que l'on donne aux caractères""",
    question="Tapez un arobase (le 'a' commercial) comme réponse",
    tests=(good("@"),),
    indices=("C'est le 'a' dans la spiral", ),
    )


add(name="apostrophe",
    question="""Tapez maintenant une apostrophe comme réponse.
    L'apostrophe est appelée <em>quote</em> en anglais.
    L'apostrophe est verticale bien qu'historiquement
    elle est eu la forme de l'accent aigu.
    Il est possible que sur votre clavier elle n'apparaisse
    pas verticale.
    """,
    tests=(
    good("'"),
    bad("´", "Vous venez de taper un accent aigu"),
    bad('"', "Vous venez de taper un guillemet"),
    bad(',', "Vous venez de taper une virgule !"),
    bad("`", """Vous venez de taper une anti-apostrophe
    (appelé aussi <em>anti-quote</em> ou  <em>left-quote</em>)
    """),
    ),
    required=['intro'],
    )

add(name="guillemet",
    question="""Tapez maintenant un guillemet.
    Le guillemet ressemble à une double apostrophe.
    Il n'est pas penché d'un coté ou de l'autre.
    Ce n'est donc ni le « » qui encadrent les citations
    à la française ou celles à l'anglaise &#8220; &#8221;
    qui sont souvent mal affichées.
    """,
    tests=(
    good('"'),
    bad("''","Vous venez de taper une double apostrophe et pas un guillemet"),
    answer_length_is(1, "La réponse attendue contient un seul caractère"),
    ),
    required=['apostrophe'],
    )

add(name="anti-apostrophe",
    question="""Tapez maintenant une anti-apostrophe
    appelée en anglais <em>anti-quote</em>.
    On l'appelle 'anti' par ce qu'historiquement
    elle était penchée dans l'autre sens par rapport
    à l'apostrophe.
    Sa dénomination officielle est maintenant 'accent grave'.
    Pour certaines fontes de caractère l'accent grave
    et l'apostrophe gauche peuvent être identique&nbsp;: ` &#8216;
    <p>
    Ne faites pas de copié/collé pour répondre à cette question,
    vous devez apprendre à utiliser le clavier.
    """,
    tests=(
    good('`'),
    bad("'", "Vous venez de taper une apostrophe"),
    bad("´", "Vous venez de taper un accent aigu"),
    bad('"', "Vous venez de taper un guillemet"),
    bad("‘", """Vous venez de taper un accent grave WINDOWS&nbsp;!
    Ceci n'a que peut d'utilité car 99.99%% des systèmes d'exploitation
    du monde ne le comprendront pas car il ne respecte aucun standard.
    Comment avez-vous fait cela alors que vous êtes
    normalement sur une machine Linux&nbsp;?"""),
    
    ),
    required=['apostrophe'],
    good_answer = """À garder dans vos signets pour avoir
    toutes les explications~: <a href="http://www.cl.cam.ac.uk/~mgk25/ucs/quotes.html">http://www.cl.cam.ac.uk/~mgk25/ucs/quotes.html</a>""",
    )

add(name="dièse",
    before="""Le caractère dièse est utilisé dans les notations musicales.
    C'est une abréviation anglaise signifiant 'nombre de' ou 'numéro'.""",
    question="""Tapez maintenant un caractère dièse""",
    tests=(
    good("#"),
    ),
    required=['intro'],
    )

add(name="esperluette",
    question="""Tapez maintenant un caractère esperluette.""",
    tests=(
    good("&"),
    bad('@', "C'est un arobase."),
    ),
    indices=("Son autre nom est : 'et commercial'",),    
    required=['intro'],
    )

t = """total 812
  1 drwxr-xr-x   7 exco   liris    896 Apr 14 13:40 ADMIN
  1 drwxr-xr-x   5 exco   liris   1480 Feb 25 17:13 ARCHIVES
 20 -rw-rw-rw-   1 exco   liris  16533 Jan 10  2005 AdobeFnt.lst
  1 drwxr-xr-x  18 exco   liris   1192 Dec  2  2004 DATA
  0 drwxr-xr-x   2 exco   liris     48 Feb 11 09:22 Desktop"""

add(name="copier coller",
    before="""Pour faire du copier/coller sous X11
    (c'est le serveur qui gère le graphique), c'est très simple.
    Le bouton gauche permet de faire une sélection
    qui est automatiquement copiée quand vous relachez
    le bouton de la souris (pas besoin de faire ^C)
    et le bouton du milieu fait le collé.""",
    question="""
    La réponse à la question est le texte suivant&nbsp;:
    <pre>%s</pre>""" % t,
    tests=(
    good(t),
    ),
    nr_lines=7,
    required=['intro'],
    )

add(name="pipe",
    question="""Tapez un caractère ``pipe´´""",
    tests=(
    good("|"),
    answer_length_is(1, "La réponse tient bien sur en UN caractère"),
    reject(('/','-','_'), "Une barre verticale, pas horizontale&nbsp;!"),
    reject('¦', """Ce caractère lui ressemble beaucoup mais ce n'est
           pas la réponse."""),
    ),
    indices=("C'est une barre verticale",
             "Sur certains claviers le symbole est coupé en son centre",
             ),
    required=['intro'],
    )

add(name="back slash",
    question="""Tapez un caractère ``backslash´´ aussi nommé anti-slash ou barre oblique inverse""",
    tests=(
    bad('/', "Perdu, vous venez de taper un <em>slash</em>"),
    good("\\"),
    ),
    indices=("Il apparaît comme séparateur dans les noms de fichier Windows",
             "C'est l'inverse de /",
             ),
    good_answer="""Ce symbole est très souvent utilisé pour banaliser
    le caractère qui suit (lui enlever toute signification spécial).
    Dans certain cas, c'est l'inverse, cela donne une signification
    au caractère qui suit.""",
    required=['intro'],
    )

add(name="final",
    question="""Pour terminer cette introduction,
    la réponse à cette question est&nbsp;: un dièse entre anti-apostrophes.""",
    tests=(
    answer_length_is(3, """Il y a un dièse et de chaque coté
    une anti-apostrophe, votre réponse doit donc faire 3 caractères."""),
    require('`', "Je ne vois pas les anti-apostrophes"),
    require('#', "Je ne vois pas le dièse"),
    good("`#`"),
    ),
    indices=("L'anti-apostrophes est l'accent grave",
             """Si on vous avait demandé un 9 entre guillemets
             vous auriez du répondre&nbsp;: <TT>"9"</TT>""",
             ), 
    # required=["copier coller", "esperluette", "dièse", "anti-apostrophe"],
    required=["copier coller", "anti-apostrophe", "pipe", "dièse",
              "back slash"],
    )


    
    
    
