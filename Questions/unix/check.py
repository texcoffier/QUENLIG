#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2005-2011 Thierry EXCOFFIER, Universite Claude Bernard
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
import utilities
from shellParser import parse, parse_only_not_commented, parse_error
from questions import Test, TestUnary, no_parse


class TestShell(Test):
    def __init__(self, *a, **b):
        try:
            b['replace'] = b['dumb_replace']
            del b['dumb_replace']
        except KeyError:
            pass
        
        Test.__init__(self, *a, **b)

    def answer_processing(self, answer):
        return parse(answer, self.replacement) # (uncommented,commented)


def shellparse(test, state):
    if not test.parsed_strings:
        test.parsed_strings = tuple(utilities.rewrite_string(
            test.strings, parser = parse_only_not_commented))
    return test.parsed_strings

class TestShellParsed(TestShell):
    parsed_strings = None
    
    def __init__(self, *a, **b):
        b['parse_strings'] = shellparse
        TestShell.__init__(self, *a, **b)


class Shell(TestUnary):
    def __call__(self, student_answer, state=None, parser=no_parse):
        parsed, comment = parse(student_answer)
        return self.children[0](
            parsed, state,
            lambda string, state, test: parser(parse_only_not_commented(string), state, test))[0], ''

class shell_good(TestShellParsed):
    html_class = "test_shell test_good test_is"
    def test(self, student_answer, string):
        if student_answer[1] == '':
            return False, parse_error
        if string == student_answer[1]:
                return True, self.comment + student_answer[1]
class shell_bad(TestShellParsed):
    html_class = "test_shell test_bad test_is"
    def test(self, student_answer, string):
        if student_answer[1] == '':
            return False, parse_error
        if string == student_answer[1]:
                return False, self.comment + student_answer[1]
            
class shell_require(TestShell):
    html_class = "test_shell test_bad test_require"
    def test(self, student_answer, string):
        if student_answer[1] == '':
            return False, parse_error
        if string not in student_answer[1]:
                return False, self.comment + student_answer[1]
class shell_reject(TestShell):
    html_class = "test_shell test_bad test_reject"
    def test(self, student_answer, string):
        if student_answer[1] == '':
            return False, parse_error
        if string in student_answer[1]:
                return False, self.comment + student_answer[1]
            
class Shell_display(TestShell):
    html_class = "test_shell test_unknown"
    def test(self, student_answer, string):
        return None, student_answer[1]

shell_display = Shell_display()
