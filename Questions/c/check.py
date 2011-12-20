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

from questions import *
import os
import subprocess
import utilities

navigation = """<p>Quelques commandes pour naviguer dans les fichiers :
<ul>
<li> <tt>pwd</tt> permet de voir le nom du répertoire ou vous êtes.
<li> <tt>cd</tt> permet de changer de répertoire.
<li> <tt>ls</tt> liste le contenu du répertoire.
<li> <tt>mkdir</tt> permet de créer un répertoire.
</ul>
"""

class C_stdout(TestUnary):
    """This modifier has not canonizer because:
      * We don't want to write the answer in the source.
      * The teacher answer will be compiled each time (long time to load)

      Examples:
         # Good answer if the student program write 'Hello world !'
         Good(C_stdout(Uppercase(Start('HELLO WORLD'))))
         #
         Good(C_stdout(Start('HELLO WORLD'),
                       c_input = "Text put in the process stdin",
                       c_args = ('arg1', 'arg2', 'arg3'),
                      ))
    """
    
    def __init__(self, *args, **keys):
        self.c_input = keys.get('c_input', '')
        self.c_args = list(keys.get('c_args', ()))
        TestExpression.__init__(self, *args)

    def __call__(self, student_answer, state=None):

        utilities.write('xxx.c', student_answer + '\n')
        error = os.system("gcc -Wall xxx.c 2>xxx.errors")
        error_text = utilities.read('xxx.errors')
        if error:
            return False, '<pre>' + error_text + '</pre>'
   
        f = subprocess.Popen(
            ["./a.out"] + self.c_args,
            stdin = subprocess.PIPE,
            stdout = subprocess.PIPE,            
            )
        result = f.communicate(self.c_input)

        ok, comment = self.children[0](result[0], state)

        if error_text != '':
            message = 'Message du compilateur : <pre>'+error_text+'</pre><hr>'
        else:
            message = ''

        return (ok, message +
                'Ce que ce programme affiche : <pre>' + result[0] + '</pre>' +
                comment)


