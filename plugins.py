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
import cgi

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

    def doc_html_item(self, item):
        v = self[('en','fr'), item]
        if isinstance(v, str):
            return cgi.escape(v)
        if isinstance(v, int):
            return str(v)
        if v is None:
            return ''
        return cgi.escape(repr(v))

    def priority_html(self, value, name):
        if value == '0':
            value = ''
        else:
            if not value[-1].isdigit():
                value = '<a href="#%s">' % value.strip('-') + value + '</a>'
            value = name + '=' + value
        return value

    def display_dicts(self, name, d1, d2):
        s = '<table class="attr"><caption><b>' + name + '</caption>'
        s += '<tr><th>CSS selector<th>English<th>French</tr>'
        for k in sorted(set(d1.keys() + d2.keys())):
            v1 = cgi.escape(d1.get(k, '???'))
            v2 = cgi.escape(d2.get(k, '???'))
            if v1 != v2:
                s += '<tr><td>%s<td>%s<td>%s</tr>' % (cgi.escape(k), v1, v2)
            else:
                s += '<tr><td>%s<td colspan="2">%s</tr>' % (cgi.escape(k), v1)
        return s + '</table>'

    def doc_html(self):

        # Boxed attribute can be computed
        if ((self.doc_html_item('boxed') != '')
            != ( self.doc_html_item('title') != ''
                 or self.doc_html_item('content_is_title') != '' )):
            print self.css_name, '===BOXED=====', self.doc_html_item('title')

        if ('\\A' in self.doc_html_item('tip')) != (self.doc_html_item('tip_preformated') == 'True'):
            print self.css_name, '===PREFORMATED=====', self.doc_html_item('title')

        
        boolean = ('link_to_self',  'boxed', 'permanent_acl',
                   'content_is_title', 'horizontal', 'tip_preformated')
        required = ('acls', 'container', 'execute', 'priority_execute',
                    'priority_display', 'before', 'font_size', 'color',
                    'text_align', 'after', 'background',
                    'title_background') + boolean
        
        acls = []
        for k, v in self[('en','fr'), 'acls'].items():
            if v == ('executable',):
                acls.append(k)
            elif v == ('!executable',):
                acls.append('!'+k)
            else:
                acls.append(k + ':' + repr(v))

        title_background = self.doc_html_item('title_background')
        if title_background:
            more = 'background:' + title_background
        else:
            more = ''
        s = ['<div class="title"><a name="%s"><b style="%s">' % (
                self.css_name, more)
             + self.css_name + '</b></a> [' + ','.join(acls) + '] ']
        pe = self.priority_html(self.doc_html_item('priority_execute'),
                                'execute')
        pd = self.priority_html(self.doc_html_item('priority_display'),
                                'display')
        if pe and pd:
            s.append(pe + ', ' + pd + ' ')
        elif pe or pd:
            s.append(pe + pd + ' ')
        v = []
        for b in boolean:
            if self.doc_html_item(b) == 'True':
                v.append(b)
        if v:
            s.append('<span class="bool">' + ', '.join(v)
                     + '</span>')
        s.append('</div>')
        font_size = self.doc_html_item('font_size')
        color = self.doc_html_item('color')
        text_align = self.doc_html_item('text_align')
        before = self.doc_html_item('before')
        after = self.doc_html_item('after')
        background = self.doc_html_item('background')
        if font_size or color or before or text_align or after or background:
            v = '<div class="style" style="'
            if color:
                v += 'color:' + color + ';'
                after += ' color:' + color
            if font_size:
                v += 'font-size:' + font_size + ';'
                after += ' size:' + font_size
            if text_align:
                v += 'text-align:' + text_align + ';'
                after += ' align:' + text_align
            if background:
                v += 'background:' + background + ';'
                after += ' background:' + background
            v += '">' + before + ' ????? ' + after + '</div>'
            s.append(v)
            
        for attr in Attribute.attributes.values():
            if attr.name in required:
                continue
            attr_value = self[('en', 'fr'), attr.name]
            if attr_value == attr.default:
                continue
            if isinstance(attr_value, dict):
                s.append(self.display_dicts(attr.name, attr_value,
                                            self[('fr',), attr.name]))
            elif isinstance(attr_value, tuple) or isinstance(attr_value, list):
                d1 = {}
                for v in attr_value:
                    v = v.split('{', 1)
                    d1[v[0].strip()] = v[1].strip('} ')
                d2 = {}
                for v in self[('fr',), attr.name]:
                    v = v.split('{', 1)
                    d2[v[0].strip()] = v[1].strip('} ')
                s.append(self.display_dicts(attr.name, d1, d2))
            else:
                fr = self[('fr',), attr.name]
                def value_html(x):
                    v = '<td'
                    x = str(x).replace('\\A','\n')
                    if '\n' in x:
                        v += ' class="pre"'
                    return v + '>' + x + '</td>'
                
                s.append('<table class="attr"><tr><th>'
                      + attr.name + value_html(attr_value))
                if fr != attr_value:
                    s.append(value_html(fr))
                s.append('</tr></table>')
        return ''.join(s)
    
def init():
    for plugin in utilities.load_directory(plugin_dir, py=False).values():
        Plugin(plugin)

