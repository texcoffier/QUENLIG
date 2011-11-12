#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2007-2008 Thierry EXCOFFIER, Universite Claude Bernard
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

"""
Management of plugins and plugin attributes.

Presently, end-user defined attributes are possible
with the core of the attribute class.
But they are not fully implemented (users can't change the values)

"""

import utilities
import configuration
import os

plugin_dir = 'Plugins'

class Attribute:
    attributes = {}
    
    def __init__(self, name, default=None, css_name=None, selector=None):
        self.name = name
        self.default = default
        self.attributes[name] = self

    def css(self, name, value):
        return ''

class AttributeCSS(Attribute):

    selector = ""

    def __init__(self, name, default=None, css_name=None, selector=None):
        Attribute.__init__(self, name, default=default)
        if css_name:
            self.css_name = css_name
        else:
            self.css_name = name.replace('_','-')
        if selector:
            self.selector = selector

    def generate_css(self, name, selector, attribute, value, div='DIV.'):
        if attribute == 'content':
            value = '"' + value + '"'
        return div + name + selector + '{ %s: %s ; }' % (
            attribute, value)

    def css(self, name, value):
        if value == None:
            return ''
        if isinstance(value, dict):
            s = []
            for k, v in value.items():
                if k.startswith('//'):
                    s.append(self.generate_css('heart_content .' + name,
                                               self.selector % k[2:],
                                               self.css_name, v))
                else:
                    s.append(self.generate_css(name,
                                               self.selector % k,
                                               self.css_name, v))
            return '\n'.join(s)
        return self.generate_css(name, self.selector, self.css_name, value)


Attribute('javascript'      , '')
Attribute('css_attributes'  , ()              )
Attribute('execute'         , lambda state, plugin, argument: None)
Attribute('acls'            , {})
Attribute('permanent_acl'   , False)
Attribute('sort_column'     , 1)
Attribute('priority_display', 0)
Attribute('priority_execute', 0)
Attribute('priority_display_int')
Attribute('priority_execute_int')
Attribute('boxed')
Attribute('content_is_title')
Attribute('horizontal')
Attribute('tip_preformated')
Attribute('container')
Attribute('link')
Attribute('link_to_self')
Attribute('prototype')
AttributeCSS('width')
AttributeCSS('color', selector='>A')
AttributeCSS('font_size')
AttributeCSS('text_align')
AttributeCSS('title_background',
             css_name='background',selector='>A>EM.box_title')
AttributeCSS('background', selector='>TABLE>TBODY>TR>TD')
AttributeCSS('before',
             css_name='content', selector='>A:first-child.content:before')
AttributeCSS('after' ,
             css_name='content', selector='>A:first-child.content:after')
AttributeCSS('tip'   ,
             css_name='content', selector='>A:first-child.content> SPAN:before')
AttributeCSS('title' ,
             css_name='content',
             selector='>A:first-child.content>.box_title:before' )
AttributeCSS('translations',
             css_name='content', selector=' .%s:before')


class Plugin:
    plugins_dict = {}
    
    def __init__(self, plugin):
        self.plugin = plugin
        self.css_name = plugin.__name__.split('.')[-2]
        self.dir_name = os.path.join(plugin_dir, self.css_name)
        self.value = None
        self.lang = {}
        self.students = {}
        self.prototype = self.plugin.__dict__.get('prototype')

        self.plugins_dict[self.css_name] = self

    def __getitem__(self, (lang, attribute)):
        """Get an attribute from (in the order) :
        * The language dependent file (Plugins/plugin_name/fr.py for example)
        * The plugin itself (Plugins/plugin_name/plugin_name.py)
        * The default values
        """

        if lang not in self.lang: # Not yet loaded module
            for a_lang in lang: # Search the language
                module_name = os.path.join(self.dir_name, a_lang)
                try:
                    self.lang[lang] = utilities.load_module(module_name)
                    break
                except ImportError:
                    pass

        try: # Get the localized value
            return self.lang[lang].__dict__[attribute]
        except KeyError:
            pass

        try: # Get the default defined in the plugin file
            return self.plugin.__dict__[attribute]
        except KeyError:
            pass

        if self.prototype:
            return self.plugins_dict[self.prototype][(lang, attribute)]

        return Attribute.attributes[attribute].default

def init():
    for plugin in utilities.load_directory(plugin_dir, py=False).values():
        Plugin(plugin)

