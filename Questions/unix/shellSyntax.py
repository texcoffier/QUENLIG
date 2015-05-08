#!/usr/bin/env python
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

# TODO : # { } fonctions


import tpg
import os

def indent(xml):
    f = open("xxx", "w")
    f.write('<?xml version="1.0" encoding="UTF-8"?>')
    f.write(xml)
    f.close()
    os.system("xmllint --format xxx")
    print xml




def escape(value):
    return value.replace("&", "&amp;").replace(">", "&gt;").replace("<", "&lt;")

# Created from shell command (not escaped)

def escaped_char(value):
    return escape(value[1])

# Created from escaped values

class Word:
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return "<argument>" + self.value + "</argument>"

def word(value):
    return Word(value)

class Redirection:
    def __init__(self, direction, where):
        self.direction = direction
        self.where = where
    def __cmp__(self, other):
        return cmp(self.direction, other.direction)
    def __str__(self):
        return "<fildes><direction>" + self.direction + "</direction><where>" + str(self.where) + "</where></fildes>"
    
def redirection(r, w):
    return Redirection(r, w)

class Affectation:
    def __init__(self, variable, value):
        self.variable = variable
        self.value = value
    def __cmp__(self, other):
        return cmp(self.variable, other.variable)
    def __str__(self):
        return "<affectation>" + self.variable + "=" + str(self.value) + "</affectation>"

class Command:
    def __init__(self):
        self.args = []
        self.redirection = []
        self.affectation = []
    def __add__(self, x):
        if isinstance(x, Word):
            self.args.append(x)
        elif isinstance(x, Redirection):
            self.redirection.append(x)
        elif isinstance(x, Affectation):
            self.affectation.append(x)
        else:
            print x
            raise ValueError("?????")
        return self
    def __str__(self):
        s = "<command>"
        self.redirection.sort()
        for i in self.args:
            s += str(i)
        for i in self.redirection:
            s += str(i)
        for i in self.affectation:
            s += str(i)
        s += "</command>"
        return s

class Pattern:
    def __init__(self):
        self.pattern = []
    def __add__(self, x):
        self.pattern.append(x)
        return self
    def __str__(self):
        s = "<pattern>"
        for i in self.pattern:
            s += str(i)        
        s += "</pattern>"
        return s

class Selector:
    def __init__(self, pattern, sequence):
        self.pattern = pattern
        self.sequence = sequence
    def __str__(self):
        s = "<selector>"
        s += str(self.pattern)
        s += str(self.sequence)
        s += "</selector>"
        return s

class Case:
    def __init__(self, word):
        self.word = word
        self.selector = []
        self.redirection = []
    def __add__(self, x):
        if isinstance(x, Redirection):
            self.redirection.append(x)
        else:
            self.selector.append(x)
        return self
    def __str__(self):
        s = "<case>"
        self.redirection.sort()
        for i in self.redirection:
            s += str(i)
        s += str(self.word)
        for i in self.selector:
            s += str(i)
        s += "</case>"
        return s

class For:
    def __init__(self, word):
        self.word = word
        self.list = []
        self.redirection = []
        self.sequence = None
    def __add__(self, x):
        if isinstance(x, Redirection):
            self.redirection.append(x)
        elif isinstance(x, Sequence):
            self.sequence = x
        else:
            self.list.append(x)
        return self
    def __str__(self):
        s = "<for>"
        s += str(self.word)
        for i in self.list:
            s += str(i)
        s += str(self.sequence)
        self.redirection.sort()
        for i in self.redirection:
            s += str(i)
        s += "</for>"
        return s

class While:
    def __init__(self, command):
        self.command = command
        self.redirection = []
        self.sequence = None
    def __add__(self, x):
        if isinstance(x, Redirection):
            self.redirection.append(x)
        elif isinstance(x, Sequence):
            self.sequence = x
        else:
            raise ValueError("In while")
        return self
    def __str__(self):
        s = "<while>"
        s += str(self.command)
        s += str(self.sequence)
        self.redirection.sort()
        for i in self.redirection:
            s += str(i)
        s += "</while>"
        return s

class SubShell:
    def __init__(self, sequence=None):
        self.sequence = sequence
        self.redirection = []
    def __add__(self, x):
        self.redirection.append(x)
        return self
    def __str__(self):
        s = "<subshell>"
        self.redirection.sort()
        s += str(self.sequence)
        for i in self.redirection:
            s += str(i)
        s += "</subshell>"
        return s

class Replacement:
    def __init__(self, sequence):
        self.sequence = sequence
        self.double_quoted = 0
    def __str__(self):
        return "<replacement double_quoted='%d'>" % self.double_quoted + \
               str(self.sequence) + "</replacement>"

class Variable:
    def __init__(self, value):
        self.value = value
        self.double_quoted = False
    def __str__(self):
        return "<variable double_quoted='%d'>" % self.double_quoted + \
               self.value + "</variable>"

class Pipeline:
    def __init__(self):
        self.command = []
        self.background = 0
    def __add__(self, x):
        self.command.append(x)
        return self
    def __str__(self):
        if self.background:
            bg = " background='1'"
        else:
            bg = ""
        s = "<pipeline nrchild='%d'%s>" % (len(self.command), bg)
        for i in self.command:
            s += str(i)
        s += "</pipeline>"
        return s

class Or:
    def __str__(self):
        return "<or></or>"

class And:
    def __str__(self):
        return "<and></and>"

class Sequence:
    def __init__(self):
        self.pipeline = []
    def __add__(self, x):
        self.pipeline.append(x)
        return self
    def __str__(self):
        s = "<sequence nrchild='%d'>" % (len(self.pipeline))
        for i in self.pipeline:
            s += str(i)
        s += "</sequence>"
        return s

class If:
    def __init__(self, condition):
        self.condition = condition
        self.thenelse = []
        self.redirection = []
    def __add__(self, x):
        if isinstance(x, Redirection):
            self.redirection.append(x)
        else:
            self.thenelse.append(x)
        return self
    def __str__(self):
        s = "<if>" + str(self.condition)
        for i in self.thenelse:
            s += str(i)
        self.redirection.sort()
        for i in self.redirection:
            s += str(i)
        s += "</if>"
        return s

def double_quote_backslash(x):
    if x in "\"$\n":
        return x
    else:
        return "\\" + x
    
def quoted_backslash(x):
    if x == "'":
        return x
    else:
        return "\\" + x

def normal_backslash(x):
    if x == '\n':
        return ""
    else:
        return x

class Sh(tpg.Parser):
    """START/c -> $c=10$ ';' ;
    """


class Sh(tpg.VerboseParser):
    r"""
    set lexer = Lexer
        token variable_name_char: '[A-Za-z0-9_?]' ;
        token redirect: '[0-9]*(>>|<<|[><])' escape ;
        token fildes: '&[0-9]' escape;
        token command_separator: '[ \t\n]*;[ \t\n]*';
        token word_separator: '[ \t]+' ;
        token line_separator:   '[ \t\n]*\n[ \t\n]*' ;
        token background_separator:   '[ \t]*&[ \t\n]*' ;
        token selector_end: '[ \t\n]*;;';
        token pipe_separator: '[ \t]*\|[ \t\n]*';
        token or_separator: '[ \t]*\|\|[ \t\n]*';
        token and_separator: '[ \t]*&&[ \t\n]*';

        token escaped_char: '\\(.|\n)' escaped_char;

        token dollar: '\$' ;
        token open_brace: '\(';
        token close_brace: '\)';
        token diese: '#';
        token equal: '=';
        token other: '[-+/:.!,{}?\200-\377]|]' ;
        token for: 'for';
        token done: 'done' ;
        token do: 'do';
        token in: 'in';
        token case: 'case';
        token esac: 'esac';
        token if: 'if';
        token fi: 'fi';
        token then: 'then';
        token else: 'else';
        token while: 'while';
        token question_mark: '\?' ;
        token star: '\*' ;

        pattern/c -> '[[^]'/c | question_mark/c | star/c ;
    
	START/c -> (line_separator|word_separator)?
                   SEQUENCE/c 
                   (line_separator|word_separator)? ;

        COMMAND_SEPARATOR/c -> command_separator/c | line_separator/c ;
        
        VARIABLE_NAME/x -> $x=""$ (variable_name_char/y$x+=y$)+ ;


        REPLACEMENT1/$Replacement(r)$ -> dollar open_brace (line_separator|word_separator)? SEQUENCE/r (line_separator|word_separator)? close_brace ;
        REPLACEMENT2/$Replacement(r)$ -> '`' (line_separator|word_separator)? SEQUENCE/r (line_separator|word_separator)? '`' ;

        REPLACEMENT/x -> REPLACEMENT1/x | REPLACEMENT2/x ;

        VARIABLE/$Variable(v)$ -> dollar (VARIABLE_NAME/v|diese/v|'@'/v|star/v) ;

        KEYWORDS/x -> for/x | do/x | done/x | in/x | case/x | esac/x | if/x | fi/x | then/x | else/x | while/x ;

        DOUBLE_QUOTED/d -> $d=''$ '"' (
            variable_name_char/x $d+=x$
            | pipe_separator/x $ d+=x $
            | word_separator/x $ d+=x $
            | COMMAND_SEPARATOR/x $ d+=x $
            | background_separator/x $ d+=escape(x) $
            | selector_end/x $ d+=x $
            | diese/x $ d+=x $
            | equal/x $ d+=x $
            | REPLACEMENT/x $ x.double_quoted=1 ; d+=str(x) $
            | VARIABLE/x $ x.double_quoted=1 ; d+=str(x) $
            | dollar/x $ d+=x $
            | escaped_char/x $ d += double_quote_backslash(x) $
            | pattern/x $ d+=x $
            | redirect/x $ d+=x $
            | fildes/x $ d+=x $
            | open_brace/x $ d+=x $
            | close_brace/x $ d+=x $
            | or_separator/x $ d+=x $
            | and_separator/x $ d+=x $
            | '\\\\'/x $ d+='\\' $
            | '`'/x $ d+=x $
            | '~'/x $ d+=x $
            | '^'/x $ d+=x $
            | '\''/x $ d+=x $
            | star/x $ d+=x $
            | question_mark/x $ d+=x $
            | other/x $ d+=x $
            | KEYWORDS/x $ d+=x $
            )* '"' ;

        QUOTED/$escape(d[1:-1])$ -> '\'[^\']*\''/d ;

#        QUOTED/d -> $d=''$ "'" ( escaped_char/x $ d+=quoted_backslash(x) $
#                          | "[^']"/x $ d+=x $ )* "'" ;

        SAFE_PART/x -> variable_name_char/x
            | REPLACEMENT/x $ x = str(x) $
            | pattern/x $ x = "<pattern_char>" + x + "</pattern_char>" $
            | VARIABLE/x $ x = str(x) $
            | DOUBLE_QUOTED/x
            | QUOTED/x
            | diese/x
            | equal/x
            | '~'/x
            | '\\\\'/x $ x ='\\' $
            | other/x
            | escaped_char/x $ x = normal_backslash(x) $
            ;
        SAFE_WORD/$word(w)$ -> $ w="" $ ((TILDE/x$w+=x$)? (SAFE_PART/x $ w+=x $)+) | TILDE/w;

        PART/x ->  SAFE_PART/x | KEYWORDS/x ;

        TILDE/x -> '~'/y $ x = '<pattern_char>~</pattern_char>' $ ;

        WORD/$word(w)$ -> $ w="" $ ((TILDE/x$w+=x$)? (PART/x $ w+=x $)+) | TILDE/w ;

        AFFECTATION/$Affectation(v,w)$ -> VARIABLE_NAME/v equal WORD/w ;

        REDIRECTION/$redirection(r,w)$ -> redirect/r (word_separator? WORD/w | fildes/w) ;

        ITEM/x -> WORD/x | REDIRECTION/x ;

        COMMANDE/c -> $c=Command()$ ((AFFECTATION/x$c+=x$|REDIRECTION/x$c+=x$) word_separator?)* SAFE_WORD/x$c+=x$ (word_separator? ITEM/x$c+=x$)* ;

        AFFECTATIONS/c -> $c=Command()$ (AFFECTATION/x$c+=x$ word_separator?)+ ;

        

        SUBSHELL/s -> $s=SubShell()$ (word_separator* REDIRECTION/r$s+=r$)*
                      open_brace (line_separator|word_separator)?
                      SEQUENCE/c$s.sequence = c$
                      (line_separator|word_separator|command_separator)? close_brace
                      (word_separator? REDIRECTION/r$s+=r$)* ;


        BLOCK/b ->  CASE/b | FOR/b | WHILE/b | SUBSHELL/b | COMMANDE/b | AFFECTATIONS/b | IF/b ;


        PIPELINE/s -> $s=Pipeline()$ BLOCK/c$s+=c$
                      (pipe_separator line_separator? BLOCK/c $s+=c$)* ;


        
        SEQUENCE/s -> $s=Sequence()$ PIPELINE/c$s+=c$
                      ((COMMAND_SEPARATOR|background_separator$c.background=1$|or_separator$s+=Or()$|and_separator$s+=And()$) PIPELINE/c$s+=c$ )* (background_separator$c.background=1$)? ;


        CASE/c -> case word_separator WORD/w $c=Case(w)$ word_separator in ((line_separator|word_separator)? SELECTOR/s $c+=s$)* (line_separator|word_separator)? esac (word_separator? REDIRECTION/r $c+=r$)* ; 

        SELECTOR/$Selector(p,s)$ -> $p=Pattern()$ WORD/w $p+=w$ (pipe_separator WORD/w $p+=w$)* word_separator? close_brace (line_separator|word_separator)? SEQUENCE/s selector_end ;

       FOR/c -> for word_separator WORD/w $c=For(w)$ word_separator in (word_separator WORD/w$c+=w$)* COMMAND_SEPARATOR do (line_separator|word_separator) SEQUENCE/s$c+=s$ COMMAND_SEPARATOR done (word_separator? REDIRECTION/r$c+=r$)* ; 

       WHILE/w -> while word_separator COMMANDE/c$w=While(c)$
                  COMMAND_SEPARATOR do (line_separator|word_separator)
                  SEQUENCE/s$w+=s$
                  COMMAND_SEPARATOR done
                  (word_separator? REDIRECTION/r$w+=r$)* ;

       IF/i -> if word_separator COMMANDE/c$i=If(c)$
                    COMMAND_SEPARATOR
                    then (word_separator|line_separator)
                    SEQUENCE/s$i+=s$
                    (  COMMAND_SEPARATOR
                        else (word_separator|line_separator) SEQUENCE/s$i+=s$)?
                    COMMAND_SEPARATOR
                    fi
                    (word_separator? REDIRECTION/r$i+=r$)* ;
                    


"""
    verbose = 0


sh = Sh()

def test():
    print "DEBUT TEST"
    for a, b in [
(r'$(a )', "<sequence nrchild='1'><pipeline nrchild='1'><command><argument><replacement double_quoted='0'><sequence nrchild='1'><pipeline nrchild='1'><command><argument>a</argument></command></pipeline></sequence></replacement></argument></command></pipeline></sequence>"),
(r'` b ` $( a)', "<sequence nrchild='1'><pipeline nrchild='1'><command><argument><replacement double_quoted='0'><sequence nrchild='1'><pipeline nrchild='1'><command><argument>b</argument></command></pipeline></sequence></replacement></argument><argument><replacement double_quoted='0'><sequence nrchild='1'><pipeline nrchild='1'><command><argument>a</argument></command></pipeline></sequence></replacement></argument></command></pipeline></sequence>"),
(r'^', "<sequence nrchild='1'><pipeline nrchild='1'><command><argument><pattern_char>^</pattern_char></argument></command></pipeline></sequence>"),
(r'"^"', "<sequence nrchild='1'><pipeline nrchild='1'><command><argument>^</argument></command></pipeline></sequence>"),
(r'''echo "\\"''', "<sequence nrchild='1'><pipeline nrchild='1'><command><argument>echo</argument><argument>\</argument></command></pipeline></sequence>"),
(r"""echo "'" """, "<sequence nrchild='1'><pipeline nrchild='1'><command><argument>echo</argument><argument>'</argument></command></pipeline></sequence>"),
(r"""echo '"'"'"\\""", "<sequence nrchild='1'><pipeline nrchild='1'><command><argument>echo</argument><argument>\"'\</argument></command></pipeline></sequence>"),
(r"""echo '"'""", "<sequence nrchild='1'><pipeline nrchild='1'><command><argument>echo</argument><argument>\"</argument></command></pipeline></sequence>"),
('"\\."', "<sequence nrchild='1'><pipeline nrchild='1'><command><argument>\\.</argument></command></pipeline></sequence>"),
('"\\\""', "<sequence nrchild='1'><pipeline nrchild='1'><command><argument>\"</argument></command></pipeline></sequence>"),
("a ", "<sequence nrchild=\'1\'><pipeline nrchild=\'1\'><command><argument>a</argument></command></pipeline></sequence>"),
("a", "<sequence nrchild=\'1\'><pipeline nrchild=\'1\'><command><argument>a</argument></command></pipeline></sequence>"),
("a b", "<sequence nrchild=\'1\'><pipeline nrchild=\'1\'><command><argument>a</argument><argument>b</argument></command></pipeline></sequence>"),
("'a b'", "<sequence nrchild=\'1\'><pipeline nrchild=\'1\'><command><argument>a b</argument></command></pipeline></sequence>"),
("'a | b'", "<sequence nrchild=\'1\'><pipeline nrchild=\'1\'><command><argument>a | b</argument></command></pipeline></sequence>"),
("\"a | b\"", "<sequence nrchild=\'1\'><pipeline nrchild=\'1\'><command><argument>a | b</argument></command></pipeline></sequence>"),
("a\ b", "<sequence nrchild=\'1\'><pipeline nrchild=\'1\'><command><argument>a b</argument></command></pipeline></sequence>"),
("\"a b\"", "<sequence nrchild=\'1\'><pipeline nrchild=\'1\'><command><argument>a b</argument></command></pipeline></sequence>"),
("a' 'b", "<sequence nrchild=\'1\'><pipeline nrchild=\'1\'><command><argument>a b</argument></command></pipeline></sequence>"),
("a*b", "<sequence nrchild=\'1\'><pipeline nrchild=\'1\'><command><argument>a<pattern_char>*</pattern_char>b</argument></command></pipeline></sequence>"),
("'a*b'", "<sequence nrchild=\'1\'><pipeline nrchild=\'1\'><command><argument>a*b</argument></command></pipeline></sequence>"),
("a\*b", "<sequence nrchild=\'1\'><pipeline nrchild=\'1\'><command><argument>a*b</argument></command></pipeline></sequence>"),
("'\"\\'a", "<sequence nrchild=\'1\'><pipeline nrchild=\'1\'><command><argument>\"\\a</argument></command></pipeline></sequence>"),
("\"$A\"", "<sequence nrchild=\'1\'><pipeline nrchild=\'1\'><command><argument><variable double_quoted='1'>A</variable></argument></command></pipeline></sequence>"),
("'$A'", "<sequence nrchild=\'1\'><pipeline nrchild=\'1\'><command><argument>$A</argument></command></pipeline></sequence>"),
("$A", "<sequence nrchild=\'1\'><pipeline nrchild=\'1\'><command><argument><variable double_quoted='0'>A</variable></argument></command></pipeline></sequence>"),
("a ; b", "<sequence nrchild=\'2\'><pipeline nrchild=\'1\'><command><argument>a</argument></command></pipeline><pipeline nrchild=\'1\'><command><argument>b</argument></command></pipeline></sequence>"),
("a | b", "<sequence nrchild=\'1\'><pipeline nrchild=\'2\'><command><argument>a</argument></command><command><argument>b</argument></command></pipeline></sequence>"),
("a b >z", "<sequence nrchild=\'1\'><pipeline nrchild=\'1\'><command><argument>a</argument><argument>b</argument><fildes><direction>&gt;</direction><where><argument>z</argument></where></fildes></command></pipeline></sequence>"),
("a b >>z", "<sequence nrchild=\'1\'><pipeline nrchild=\'1\'><command><argument>a</argument><argument>b</argument><fildes><direction>&gt;&gt;</direction><where><argument>z</argument></where></fildes></command></pipeline></sequence>"),
("a b 2>>\ ", "<sequence nrchild=\'1\'><pipeline nrchild=\'1\'><command><argument>a</argument><argument>b</argument><fildes><direction>2&gt;&gt;</direction><where><argument> </argument></where></fildes></command></pipeline></sequence>"),
("a b 2>>&1", "<sequence nrchild=\'1\'><pipeline nrchild=\'1\'><command><argument>a</argument><argument>b</argument><fildes><direction>2&gt;&gt;</direction><where>&amp;1</where></fildes></command></pipeline></sequence>"),
("a b 2>&1", "<sequence nrchild=\'1\'><pipeline nrchild=\'1\'><command><argument>a</argument><argument>b</argument><fildes><direction>2&gt;</direction><where>&amp;1</where></fildes></command></pipeline></sequence>"),
("a >'*'", "<sequence nrchild=\'1\'><pipeline nrchild=\'1\'><command><argument>a</argument><fildes><direction>&gt;</direction><where><argument>*</argument></where></fildes></command></pipeline></sequence>"),
("(a)", "<sequence nrchild=\'1\'><pipeline nrchild=\'1\'><subshell><sequence nrchild=\'1\'><pipeline nrchild=\'1\'><command><argument>a</argument></command></pipeline></sequence></subshell></pipeline></sequence>"),
("(a )", "<sequence nrchild=\'1\'><pipeline nrchild=\'1\'><subshell><sequence nrchild=\'1\'><pipeline nrchild=\'1\'><command><argument>a</argument></command></pipeline></sequence></subshell></pipeline></sequence>"),
("( a )", "<sequence nrchild=\'1\'><pipeline nrchild=\'1\'><subshell><sequence nrchild=\'1\'><pipeline nrchild=\'1\'><command><argument>a</argument></command></pipeline></sequence></subshell></pipeline></sequence>"),
("(a;)", "<sequence nrchild='1'><pipeline nrchild='1'><subshell><sequence nrchild='1'><pipeline nrchild='1'><command><argument>a</argument></command></pipeline></sequence></subshell></pipeline></sequence>"),
("( a ) >b <c", "<sequence nrchild=\'1\'><pipeline nrchild=\'1\'><subshell><sequence nrchild=\'1\'><pipeline nrchild=\'1\'><command><argument>a</argument></command></pipeline></sequence><fildes><direction>&gt;</direction><where><argument>b</argument></where></fildes><fildes><direction>&lt;</direction><where><argument>c</argument></where></fildes></subshell></pipeline></sequence>"),
("(a)|b", "<sequence nrchild=\'1\'><pipeline nrchild=\'2\'><subshell><sequence nrchild=\'1\'><pipeline nrchild=\'1\'><command><argument>a</argument></command></pipeline></sequence></subshell><command><argument>b</argument></command></pipeline></sequence>"),
("( a ; b )", "<sequence nrchild=\'1\'><pipeline nrchild=\'1\'><subshell><sequence nrchild=\'2\'><pipeline nrchild=\'1\'><command><argument>a</argument></command></pipeline><pipeline nrchild=\'1\'><command><argument>b</argument></command></pipeline></sequence></subshell></pipeline></sequence>"),
("(a;b)", "<sequence nrchild=\'1\'><pipeline nrchild=\'1\'><subshell><sequence nrchild=\'2\'><pipeline nrchild=\'1\'><command><argument>a</argument></command></pipeline><pipeline nrchild=\'1\'><command><argument>b</argument></command></pipeline></sequence></subshell></pipeline></sequence>"),
("(a;b)2>>'('|(c|d;e)", "<sequence nrchild=\'1\'><pipeline nrchild=\'2\'><subshell><sequence nrchild=\'2\'><pipeline nrchild=\'1\'><command><argument>a</argument></command></pipeline><pipeline nrchild=\'1\'><command><argument>b</argument></command></pipeline></sequence><fildes><direction>2&gt;&gt;</direction><where><argument>(</argument></where></fildes></subshell><subshell><sequence nrchild=\'2\'><pipeline nrchild=\'2\'><command><argument>c</argument></command><command><argument>d</argument></command></pipeline><pipeline nrchild=\'1\'><command><argument>e</argument></command></pipeline></sequence></subshell></pipeline></sequence>"),
(" (a)", "<sequence nrchild=\'1\'><pipeline nrchild=\'1\'><subshell><sequence nrchild=\'1\'><pipeline nrchild=\'1\'><command><argument>a</argument></command></pipeline></sequence></subshell></pipeline></sequence>"),
("a\nb", "<sequence nrchild=\'2\'><pipeline nrchild=\'1\'><command><argument>a</argument></command></pipeline><pipeline nrchild=\'1\'><command><argument>b</argument></command></pipeline></sequence>"),
("a\\\nb", "<sequence nrchild=\'1\'><pipeline nrchild=\'1\'><command><argument>ab</argument></command></pipeline></sequence>"),
("\"a\\\nb\"", "<sequence nrchild=\'1\'><pipeline nrchild=\'1\'><command><argument>a\nb</argument></command></pipeline></sequence>"),
("case a in esac", "<sequence nrchild=\'1\'><pipeline nrchild=\'1\'><case><argument>a</argument></case></pipeline></sequence>"),
("case a in a) toto ;; b) titi ;; esac", "<sequence nrchild=\'1\'><pipeline nrchild=\'1\'><case><argument>a</argument><selector><pattern><argument>a</argument></pattern><sequence nrchild=\'1\'><pipeline nrchild=\'1\'><command><argument>toto</argument></command></pipeline></sequence></selector><selector><pattern><argument>b</argument></pattern><sequence nrchild=\'1\'><pipeline nrchild=\'1\'><command><argument>titi</argument></command></pipeline></sequence></selector></case></pipeline></sequence>"),
("case a in\na)x;;\nesac", "<sequence nrchild=\'1\'><pipeline nrchild=\'1\'><case><argument>a</argument><selector><pattern><argument>a</argument></pattern><sequence nrchild=\'1\'><pipeline nrchild=\'1\'><command><argument>x</argument></command></pipeline></sequence></selector></case></pipeline></sequence>"),
("case a in c | d)x;;esac", "<sequence nrchild=\'1\'><pipeline nrchild=\'1\'><case><argument>a</argument><selector><pattern><argument>c</argument><argument>d</argument></pattern><sequence nrchild=\'1\'><pipeline nrchild=\'1\'><command><argument>x</argument></command></pipeline></sequence></selector></case></pipeline></sequence>"),
("case a in c|d)x;;esac", "<sequence nrchild=\'1\'><pipeline nrchild=\'1\'><case><argument>a</argument><selector><pattern><argument>c</argument><argument>d</argument></pattern><sequence nrchild=\'1\'><pipeline nrchild=\'1\'><command><argument>x</argument></command></pipeline></sequence></selector></case></pipeline></sequence>"),
("case a in c| d)x;;esac", "<sequence nrchild=\'1\'><pipeline nrchild=\'1\'><case><argument>a</argument><selector><pattern><argument>c</argument><argument>d</argument></pattern><sequence nrchild=\'1\'><pipeline nrchild=\'1\'><command><argument>x</argument></command></pipeline></sequence></selector></case></pipeline></sequence>"),
("case a in c |d)x;;esac", "<sequence nrchild=\'1\'><pipeline nrchild=\'1\'><case><argument>a</argument><selector><pattern><argument>c</argument><argument>d</argument></pattern><sequence nrchild=\'1\'><pipeline nrchild=\'1\'><command><argument>x</argument></command></pipeline></sequence></selector></case></pipeline></sequence>"),
('case a in esac;a', '<sequence nrchild=\'2\'><pipeline nrchild=\'1\'><case><argument>a</argument></case></pipeline><pipeline nrchild=\'1\'><command><argument>a</argument></command></pipeline></sequence>'),
('case a in esac ; a', '<sequence nrchild=\'2\'><pipeline nrchild=\'1\'><case><argument>a</argument></case></pipeline><pipeline nrchild=\'1\'><command><argument>a</argument></command></pipeline></sequence>'),
('case a in esac | case a in esac', '<sequence nrchild=\'1\'><pipeline nrchild=\'2\'><case><argument>a</argument></case><case><argument>a</argument></case></pipeline></sequence>'),
('echo \\"a', '<sequence nrchild=\'1\'><pipeline nrchild=\'1\'><command><argument>echo</argument><argument>"a</argument></command></pipeline></sequence>'),
("case a in esac >x 2>>y", "<sequence nrchild=\'1\'><pipeline nrchild=\'1\'><case><fildes><direction>&gt;</direction><where><argument>x</argument></where></fildes><fildes><direction>2&gt;&gt;</direction><where><argument>y</argument></where></fildes><argument>a</argument></case></pipeline></sequence>"),
('for a in c d ; do x ; done', '<sequence nrchild=\'1\'><pipeline nrchild=\'1\'><for><argument>a</argument><argument>c</argument><argument>d</argument><sequence nrchild=\'1\'><pipeline nrchild=\'1\'><command><argument>x</argument></command></pipeline></sequence></for></pipeline></sequence>'),
('for a in c d\ndo\nx\ndone', '<sequence nrchild=\'1\'><pipeline nrchild=\'1\'><for><argument>a</argument><argument>c</argument><argument>d</argument><sequence nrchild=\'1\'><pipeline nrchild=\'1\'><command><argument>x</argument></command></pipeline></sequence></for></pipeline></sequence>'),
('$(a)', "<sequence nrchild=\'1\'><pipeline nrchild=\'1\'><command><argument><replacement double_quoted='0'><sequence nrchild=\'1\'><pipeline nrchild=\'1\'><command><argument>a</argument></command></pipeline></sequence></replacement></argument></command></pipeline></sequence>"),
('`a`', "<sequence nrchild=\'1\'><pipeline nrchild=\'1\'><command><argument><replacement double_quoted='0'><sequence nrchild=\'1\'><pipeline nrchild=\'1\'><command><argument>a</argument></command></pipeline></sequence></replacement></argument></command></pipeline></sequence>"),
('"$(a)"', "<sequence nrchild=\'1\'><pipeline nrchild=\'1\'><command><argument><replacement double_quoted='1'><sequence nrchild=\'1\'><pipeline nrchild=\'1\'><command><argument>a</argument></command></pipeline></sequence></replacement></argument></command></pipeline></sequence>"),
('" ; "', '<sequence nrchild=\'1\'><pipeline nrchild=\'1\'><command><argument> ; </argument></command></pipeline></sequence>'),
('" ;; "', '<sequence nrchild=\'1\'><pipeline nrchild=\'1\'><command><argument> ;; </argument></command></pipeline></sequence>'),
('\' ; \'', '<sequence nrchild=\'1\'><pipeline nrchild=\'1\'><command><argument> ; </argument></command></pipeline></sequence>'),
('\' ;; \'', '<sequence nrchild=\'1\'><pipeline nrchild=\'1\'><command><argument> ;; </argument></command></pipeline></sequence>'),
('\' & # >&1 () \'', '<sequence nrchild=\'1\'><pipeline nrchild=\'1\'><command><argument> &amp; # &gt;&amp;1 () </argument></command></pipeline></sequence>'),
('" & "', '<sequence nrchild=\'1\'><pipeline nrchild=\'1\'><command><argument> &amp; </argument></command></pipeline></sequence>'),
('" > "', '<sequence nrchild=\'1\'><pipeline nrchild=\'1\'><command><argument> &gt; </argument></command></pipeline></sequence>'),
('" 2>&3 "', '<sequence nrchild=\'1\'><pipeline nrchild=\'1\'><command><argument> 2&gt;&amp;3 </argument></command></pipeline></sequence>'),
('" ( "', '<sequence nrchild=\'1\'><pipeline nrchild=\'1\'><command><argument> ( </argument></command></pipeline></sequence>'),
('" ) "', '<sequence nrchild=\'1\'><pipeline nrchild=\'1\'><command><argument> ) </argument></command></pipeline></sequence>'),
('" & # >&1 () "', '<sequence nrchild=\'1\'><pipeline nrchild=\'1\'><command><argument> &amp; # &gt;&amp;1 () </argument></command></pipeline></sequence>'),
('\'\n\'', '<sequence nrchild=\'1\'><pipeline nrchild=\'1\'><command><argument>\n</argument></command></pipeline></sequence>'),
('"\n"', '<sequence nrchild=\'1\'><pipeline nrchild=\'1\'><command><argument>\n</argument></command></pipeline></sequence>'),
('/+- +5 -t: . ] !', '<sequence nrchild=\'1\'><pipeline nrchild=\'1\'><command><argument>/+-</argument><argument>+5</argument><argument>-t:</argument><argument>.</argument><argument>]</argument><argument>!</argument></command></pipeline></sequence>'),
('*[a]', '<sequence nrchild=\'1\'><pipeline nrchild=\'1\'><command><argument><pattern_char>*</pattern_char><pattern_char>[</pattern_char>a]</argument></command></pipeline></sequence>'),
('a=5 b', '<sequence nrchild=\'1\'><pipeline nrchild=\'1\'><command><argument>b</argument><affectation>a=<argument>5</argument></affectation></command></pipeline></sequence>'),
('a="5 b" b', '<sequence nrchild=\'1\'><pipeline nrchild=\'1\'><command><argument>b</argument><affectation>a=<argument>5 b</argument></affectation></command></pipeline></sequence>'),
('a=5', '<sequence nrchild=\'1\'><pipeline nrchild=\'1\'><command><affectation>a=<argument>5</argument></affectation></command></pipeline></sequence>'),
('a=5\nb=6', '<sequence nrchild=\'2\'><pipeline nrchild=\'1\'><command><affectation>a=<argument>5</argument></affectation></command></pipeline><pipeline nrchild=\'1\'><command><affectation>b=<argument>6</argument></affectation></command></pipeline></sequence>'),
("a&", "<sequence nrchild='1'><pipeline nrchild='1' background='1'><command><argument>a</argument></command></pipeline></sequence>"),
("a &", "<sequence nrchild='1'><pipeline nrchild='1' background='1'><command><argument>a</argument></command></pipeline></sequence>"),
("a & b &", "<sequence nrchild='2'><pipeline nrchild='1' background='1'><command><argument>a</argument></command></pipeline><pipeline nrchild='1' background='1'><command><argument>b</argument></command></pipeline></sequence>"),
("(a)&", "<sequence nrchild='1'><pipeline nrchild='1' background='1'><subshell><sequence nrchild='1'><pipeline nrchild='1'><command><argument>a</argument></command></pipeline></sequence></subshell></pipeline></sequence>"),
('" -> - é & | ;; ; < case esac in do done if # `"', "<sequence nrchild='1'><pipeline nrchild='1'><command><argument> -&gt; - é &amp; | ;; ; &lt; case esac in do done if # `</argument></command></pipeline></sequence>"),
('echo for do in done esac', "<sequence nrchild='1'><pipeline nrchild='1'><command><argument>echo</argument><argument>for</argument><argument>do</argument><argument>in</argument><argument>done</argument><argument>esac</argument></command></pipeline></sequence>"),
('a || b | c || d', "<sequence nrchild='5'><pipeline nrchild='1'><command><argument>a</argument></command></pipeline><or></or><pipeline nrchild='2'><command><argument>b</argument></command><command><argument>c</argument></command></pipeline><or></or><pipeline nrchild='1'><command><argument>d</argument></command></pipeline></sequence>"),
('AB=5', "<sequence nrchild='1'><pipeline nrchild='1'><command><affectation>AB=<argument>5</argument></affectation></command></pipeline></sequence>"),
('a&&b||c', "<sequence nrchild='5'><pipeline nrchild='1'><command><argument>a</argument></command></pipeline><and></and><pipeline nrchild='1'><command><argument>b</argument></command></pipeline><or></or><pipeline nrchild='1'><command><argument>c</argument></command></pipeline></sequence>"),
('a `b``c`"`d`"\'`e`\'', "<sequence nrchild='1'><pipeline nrchild='1'><command><argument>a</argument><argument><replacement double_quoted='0'><sequence nrchild='1'><pipeline nrchild='1'><command><argument>b</argument></command></pipeline></sequence></replacement><replacement double_quoted='0'><sequence nrchild='1'><pipeline nrchild='1'><command><argument>c</argument></command></pipeline></sequence></replacement><replacement double_quoted='1'><sequence nrchild='1'><pipeline nrchild='1'><command><argument>d</argument></command></pipeline></sequence></replacement>`e`</argument></command></pipeline></sequence>"),
('if a ; then x ; fi', "<sequence nrchild='1'><pipeline nrchild='1'><if><command><argument>a</argument></command><sequence nrchild='1'><pipeline nrchild='1'><command><argument>x</argument></command></pipeline></sequence></if></pipeline></sequence>"),
('if a>b;then x;fi', "<sequence nrchild='1'><pipeline nrchild='1'><if><command><argument>a</argument><fildes><direction>&gt;</direction><where><argument>b</argument></where></fildes></command><sequence nrchild='1'><pipeline nrchild='1'><command><argument>x</argument></command></pipeline></sequence></if></pipeline></sequence>"),
('if a\n then\n\tx\n fi', "<sequence nrchild='1'><pipeline nrchild='1'><if><command><argument>a</argument></command><sequence nrchild='1'><pipeline nrchild='1'><command><argument>x</argument></command></pipeline></sequence></if></pipeline></sequence>"),
('if a;then x;fi>x', "<sequence nrchild='1'><pipeline nrchild='1'><if><command><argument>a</argument></command><sequence nrchild='1'><pipeline nrchild='1'><command><argument>x</argument></command></pipeline></sequence><fildes><direction>&gt;</direction><where><argument>x</argument></where></fildes></if></pipeline></sequence>"),
('if a;then x ; else y ; fi', "<sequence nrchild='1'><pipeline nrchild='1'><if><command><argument>a</argument></command><sequence nrchild='1'><pipeline nrchild='1'><command><argument>x</argument></command></pipeline></sequence><sequence nrchild='1'><pipeline nrchild='1'><command><argument>y</argument></command></pipeline></sequence></if></pipeline></sequence>"),
('if a;then x;else y;fi', "<sequence nrchild='1'><pipeline nrchild='1'><if><command><argument>a</argument></command><sequence nrchild='1'><pipeline nrchild='1'><command><argument>x</argument></command></pipeline></sequence><sequence nrchild='1'><pipeline nrchild='1'><command><argument>y</argument></command></pipeline></sequence></if></pipeline></sequence>"),
("a b=5", "<sequence nrchild='1'><pipeline nrchild='1'><command><argument>a</argument><argument>b=5</argument></command></pipeline></sequence>"),
("{}", "<sequence nrchild='1'><pipeline nrchild='1'><command><argument>{}</argument></command></pipeline></sequence>"),
("\;", "<sequence nrchild='1'><pipeline nrchild='1'><command><argument>;</argument></command></pipeline></sequence>"),
("while a ; do b ; done", "<sequence nrchild='1'><pipeline nrchild='1'><while><command><argument>a</argument></command><sequence nrchild='1'><pipeline nrchild='1'><command><argument>b</argument></command></pipeline></sequence></while></pipeline></sequence>"), 
("while a\ndo\nb\ndone", "<sequence nrchild='1'><pipeline nrchild='1'><while><command><argument>a</argument></command><sequence nrchild='1'><pipeline nrchild='1'><command><argument>b</argument></command></pipeline></sequence></while></pipeline></sequence>"),
("a~b", "<sequence nrchild='1'><pipeline nrchild='1'><command><argument>a~b</argument></command></pipeline></sequence>"), 
("~b ~b", "<sequence nrchild='1'><pipeline nrchild='1'><command><argument><pattern_char>~</pattern_char>b</argument><argument><pattern_char>~</pattern_char>b</argument></command></pipeline></sequence>"), 
("A=~", "<sequence nrchild='1'><pipeline nrchild='1'><command><affectation>A=<argument><pattern_char>~</pattern_char></argument></affectation></command></pipeline></sequence>"), 
("a ~", "<sequence nrchild='1'><pipeline nrchild='1'><command><argument>a</argument><argument><pattern_char>~</pattern_char></argument></command></pipeline></sequence>"), 
("A='~'", "<sequence nrchild='1'><pipeline nrchild='1'><command><affectation>A=<argument>~</argument></affectation></command></pipeline></sequence>"), 
("'\\a'", "<sequence nrchild='1'><pipeline nrchild='1'><command><argument>\\a</argument></command></pipeline></sequence>"),
("a b <c", "<sequence nrchild='1'><pipeline nrchild='1'><command><argument>a</argument><argument>b</argument><fildes><direction>&lt;</direction><where><argument>c</argument></where></fildes></command></pipeline></sequence>"),
("a <c b", "<sequence nrchild='1'><pipeline nrchild='1'><command><argument>a</argument><argument>b</argument><fildes><direction>&lt;</direction><where><argument>c</argument></where></fildes></command></pipeline></sequence>"),
("a b <c >d", "<sequence nrchild='1'><pipeline nrchild='1'><command><argument>a</argument><argument>b</argument><fildes><direction>&gt;</direction><where><argument>d</argument></where></fildes><fildes><direction>&lt;</direction><where><argument>c</argument></where></fildes></command></pipeline></sequence>"),
("a <c b >d", "<sequence nrchild='1'><pipeline nrchild='1'><command><argument>a</argument><argument>b</argument><fildes><direction>&gt;</direction><where><argument>d</argument></where></fildes><fildes><direction>&lt;</direction><where><argument>c</argument></where></fildes></command></pipeline></sequence>"),
("a >d b <c", "<sequence nrchild='1'><pipeline nrchild='1'><command><argument>a</argument><argument>b</argument><fildes><direction>&gt;</direction><where><argument>d</argument></where></fildes><fildes><direction>&lt;</direction><where><argument>c</argument></where></fildes></command></pipeline></sequence>"),
("a >d '*' <c", "<sequence nrchild='1'><pipeline nrchild='1'><command><argument>a</argument><argument>*</argument><fildes><direction>&gt;</direction><where><argument>d</argument></where></fildes><fildes><direction>&lt;</direction><where><argument>c</argument></where></fildes></command></pipeline></sequence>"),
("sed <tp.c 's/\/\/.*//' >tp_.c", "<sequence nrchild='1'><pipeline nrchild='1'><command><argument>sed</argument><argument>s/\/\/.*//</argument><fildes><direction>&gt;</direction><where><argument>tp_.c</argument></where></fildes><fildes><direction>&lt;</direction><where><argument>tp.c</argument></where></fildes></command></pipeline></sequence>"),
("sed 's/\/\/.*//' <tp.c >tp_.c", "<sequence nrchild='1'><pipeline nrchild='1'><command><argument>sed</argument><argument>s/\/\/.*//</argument><fildes><direction>&gt;</direction><where><argument>tp_.c</argument></where></fildes><fildes><direction>&lt;</direction><where><argument>tp.c</argument></where></fildes></command></pipeline></sequence>"),
(">a b", "<sequence nrchild='1'><pipeline nrchild='1'><command><argument>b</argument><fildes><direction>&gt;</direction><where><argument>a</argument></where></fildes></command></pipeline></sequence>"),
(">a (b)", "<sequence nrchild='1'><pipeline nrchild='1'><subshell><sequence nrchild='1'><pipeline nrchild='1'><command><argument>b</argument></command></pipeline></sequence><fildes><direction>&gt;</direction><where><argument>a</argument></where></fildes></subshell></pipeline></sequence>"),
('echo $#', "<sequence nrchild='1'><pipeline nrchild='1'><command><argument>echo</argument><argument><variable double_quoted='0'>#</variable></argument></command></pipeline></sequence>"),
('echo $?', "<sequence nrchild='1'><pipeline nrchild='1'><command><argument>echo</argument><argument><variable double_quoted='0'>?</variable></argument></command></pipeline></sequence>"),
('echo $@', "<sequence nrchild='1'><pipeline nrchild='1'><command><argument>echo</argument><argument><variable double_quoted='0'>@</variable></argument></command></pipeline></sequence>"),
('echo $1', "<sequence nrchild='1'><pipeline nrchild='1'><command><argument>echo</argument><argument><variable double_quoted='0'>1</variable></argument></command></pipeline></sequence>"),
('echo $*', "<sequence nrchild='1'><pipeline nrchild='1'><command><argument>echo</argument><argument><variable double_quoted='0'>*</variable></argument></command></pipeline></sequence>"),
('echo "$/"', "<sequence nrchild='1'><pipeline nrchild='1'><command><argument>echo</argument><argument>$/</argument></command></pipeline></sequence>"),
('grep "="', "<sequence nrchild='1'><pipeline nrchild='1'><command><argument>grep</argument><argument>=</argument></command></pipeline></sequence>"),
# Do not work... it should
# ('"\'" \'\'', ""),
]:
        print "="*50, a
        c = str(sh(a))
        if c != b:
            print "Parse :", a
            print "Obtenu :"
            indent(c)
            print "Attendu :"
            indent(b)

if __name__ == "__main__":
    Sh.verbose =255 
    Sh.verbose =0 
    try:
        import profile
        profile.run('test()')
    except IOError:
        test()
    except ImportError:
        test()
