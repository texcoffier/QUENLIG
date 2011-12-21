# -*- coding: latin-1 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2007-2011 Thierry EXCOFFIER, Universite Claude Bernard
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
import configuration
import questions
import re

def filter_student_answer(answer, state=None):
    answer = re.sub(' +', ' ', answer)
    answer = re.sub(' \n', '\n', answer)
    answer = re.sub('\n\n*', '\n', answer)
    return answer

questions.current_evaluate_answer = filter_student_answer

filename = os.path.join(configuration.session.dir, "nr_hosts")
try:
    f = open(filename, "r")
    nombre_de_postes = int(f.readlines()[0].strip())
except IOError:
    sys.stderr.write("""
You must create the file:
	%s
with the correct number of hosts inside in order to generate the good subject

""" % filename)
    sys.exit(1)

mots_de_passe = "'cisco', 'class', 'classe'"

effacer_password = """
Pour effacer le mot de passe sans effacer la configuration
il faut passer en mode ROMMON lors du démarrage et
taper les commandes suivantes&nbsp;:
<pre>
confreg 0x2142
reset
no

enable
copy startup-config running-config 

configure terminal
enable secret cisco
config-register 0x2102
exit
copy running-config startup-config

reload
no

</pre>
Remarques&nbsp;:
<ul>
<li> Faire un copié/collé de TOUTES les lignes ne fonctionnera pas.
<li> Un ligne vide veux dire que l'on répond Return à la question.
<li> Le mot de passe sera <tt>cisco</tt>
</ul>
"""

procedure_effacement = """<pre><b>enable</b> # S'il demande un mot de passe, essayez&nbsp;: """ +  mots_de_passe + """
<b>erase startup-config</b>
<b>y</b>       <em>LE 'y' N'APPARAÎT PAS ET L'ECRAN SE BLOQUE PENDANT 10 SECONDES</em>
<b>reload</b>
                        <em>Tapez return pour confirmer le redémarrage du routeur</em>
<b>no</b>                      <em>Pas le dialogue de configuration initiale</em>
<b>y</b>                       <em>Terminer l'auto install</em>
</pre>
"""

reinit = """Les mots de passes possibles : """ + mots_de_passe + """
    <p>
    La procédure de réinitialisation du CISCO :
    """ + procedure_effacement + """

<h2>Si vous NE trouvez PAS le mot de passe :</h2>
<p>
Pour effacer le mot de passe.
Il faut passer en mode ROMMON lors du démarrage et
taper les commandes suivantes&nbsp;:
<pre>
confreg 0x2142         # On dit au routeur de ne pas lire sa configuration
reset                  # Le routeur redémarre sans lire la configuration
no

enable                 # On passe "root" sur le routeur vierge
erase startup-config   # On efface la configuration

configure terminal
config-register 0x2102 # On dit au routeur de lire sa configuration
exit
reload                 # On redémarre proprement
no

</pre>
Remarques&nbsp;:
<ul>
<li> Faire un copié/collé de TOUTES les lignes ne fonctionnera pas.
<li> Un ligne vide veux dire que l'on répond Return à la question.
</ul>
        """

avant_de_partir = """Ceci n'est pas une question mais ce que vous devez
    faire avant de partir&nbsp:

    <ul>
    <li> Sauvegarder le résultat de la commande <tt>show running-config</tt>
    pour pouvoir vous en servir comme référence.
    Il est conseillé de l'annoter.
    <li>
    Vous devez rénitialiser le routeur avant de partir.
    Pour cela tapez les commandes&nbsp;:
    <pre>enable
erase startup-config
<em>Confirmez l'effacement</em>
<em>Quand le prompt revient et <b>pas avant</b>, éteignez le routeur</em>
</pre>
<p>
<li> Éteignez l'ordinateur avec la commande <tt>halt</tt> sous <tt>root</tt>.
<li> Éteignez l'écran.
<li> Ranger les cables.
</ul>
"""


conf = {
    "proxy_ip": "10.0.0.1",
    "proxy_port": "3128",
    "cours_ccna": "http://10.0.0.1/CCNA/",
    }

conf["proxy"] = "%(proxy_ip)s:%(proxy_port)s" % conf

##############################################################################
#
##############################################################################

class IP:
    def __init__(self, ip):
        if ip == None:
            self.ip = None
            return
        try:
            m = int(ip)
            m = int("1"*m + "0"*(32-m), 2)
            self.bytes = []
            while m:
                self.bytes = [m % 256] + self.bytes
                m /= 256
            self.ip = '.'.join( [str(i) for i in self.bytes] )
            return
        except ValueError:
            pass
        if ' ' in ip:
            raise ValueError("Une adresse IP ne contient pas d'espace")

        self.ip = ip
        self.bytes = ip.split('.')
        if len(self.bytes) != 4 :
            raise ValueError("""Une adresse IP est composée de 4 nombres
            séparés par des points (.).""")
        try:
            self.bytes = [int(i) for i in self.bytes]
        except ValueError:
            raise ValueError("Les nombres entre les points sont en décimal")

        for i in self.bytes:
            if i<0 or i>255:
                raise ValueError("Les nombres sont entre 0 et 255 inclus.")

    def nr_bits_netmask(self):
        "Number of bits set to 1 on the left (netmask)"
        if self.ip == None:
            return None
        nr = 0
        done = False
        for i in self.bytes:
            if done:
                if i:
                    raise ValueError("Not a netmask")
                continue
            while i & 128:
                nr += 1
                i *= 2
            if nr % 8:
                done = True
        return nr

    def __and__(self, ip):
        if self.ip == None:
            return IP(ip.ip)
        if ip.ip == None:
            return IP(self.ip)
        return IP('.'.join([str(a & b) for a,b in zip(self.bytes, ip.bytes)]))

    def __or__(self, ip):
        if self.ip == None:
            return IP(ip.ip)
        if ip.ip == None:
            return IP(self.ip)
        return IP('.'.join([str(a | b) for a,b in zip(self.bytes, ip.bytes)]))

    def __invert__(self):
        if self.ip == None:
            return self
        return IP('.'.join([str(256 + ~ a) for a in self.bytes]))

    def __eq__(self, ip):
        return self.ip == ip.ip
        
    def __ne__(self, ip):
        return self.ip != ip.ip
        
    def __str__(self):
        return self.ip

    def __nonzero__(self):
        if self.ip:
            return 1
        else:
            return 0

##############################################################################
#
##############################################################################

def dce_dte(v):
    if v == "DCE":
        return "DTE"
    elif v == "DTE":
        return "DCE"
    elif v == None:
        return None
    else:
        raise ValueError("Problème with DCT/DTE")

class Port:
    def __init__(self, host, ip=None, type=None, key=None):
        self.host = host
        self.ip = IP(ip)
        self.type = type
        self.key = key
        if type == 'DCE':
            self.clock = 'clock rate 56000'
        else:
            self.clock = ''

##############################################################################
#
##############################################################################

class Link:
    def __init__(self, mask=None, port=None, remote_port=None, add_link=True,
                 label=None, hide_port=False, weight=None, length=None):
        self.mask = IP(mask)
        self.nr_bits_netmask = self.mask.nr_bits_netmask()
        self.port = port
        self.remote_port = remote_port
        self.label = label
        self.hide_port = hide_port
        self.weight = weight
        self.length = length
        self.broadcast = self.port.ip | ~ self.mask
        if remote_port and port.type:
            remote_port.type = dce_dte(port.type)
        if self.mask:
            self.network = self.mask & self.port.ip
            self.network_plus_bits = str(self.network) + '/' + \
                                     str(self.mask.nr_bits_netmask())

        if add_link:
            self.inverted = False
            self.port.host.add_link(self)
            if self.remote_port:
                self.invert = self.revert()
                self.invert.invert = self
                self.remote_port.host.add_link(self.invert)
                if self.mask and self.port.ip and self.remote_port.ip and self.invert.network != self.network:
                    raise ValueError("""Link ends are not in the same net:
                    %s (%s) and %s (%s)""" % (self.network, self.mask,
                                            self.invert.network, self.invert.mask))
        else:
            self.inverted = True

    def revert(self):
        return self.__class__(self.mask.ip,
                              self.remote_port, self.port,
                              add_link=False, label=self.label,
                              hide_port=self.hide_port,
                              weight=self.weight, length=self.length)

    def dot_label(self, showip):
        if self.mask and showip:
            return ',label="%s"' % self.mask
        if self.label:
            return ',label="%s"' % self.label
        return ""

    def tail(self, showip):
        label = self.port.key
        if not showip:
            return label
        if self.port.type:
            label += ' ' + self.port.type
        if self.port.ip:
            label += '\\n' + str(self.port.ip)
        return label

    def dot_option(self):
        return ""

    def head(self, showip):
        return self.invert.tail(showip)

    def from_to(self):
        return '%s -> %s' % ( self.port.host.port_name(),
            self.remote_port.host.port_name() )

    def dot(self, showip):
        s = '%s [fontcolor="#444444",style=%s%s%s'%(
                self.from_to(),
                self.dot_style,
                self.dot_label(showip),
                self.dot_option(),
                )
        if self.weight:
            s += ',weight="%g"' % self.weight
        if self.length:
            s += ',len="%g"' % self.length
       
        if not self.hide_port:
            s += ',taillabel="%s",headlabel="%s"'%(
                self.tail(showip), self.head(showip),
                )

        return s + '];\n'
            
    def port_str(self, port):
        s = str(port.ip) + '/' + str(self.mask.nr_bits_netmask())
        if port.type:
            s += ' ' + port.type
        return s
    def port_ip(self):
        return self.port_str(self.port)
    def remote_port_ip(self):
        return self.port_str(self.remote_port)

class SerialLink(Link):
    name = "S"
    dot_style = "solid"
    legend = "Liaison Série"

class EthLink(Link):
    dot_style = "bold"
    name = "E"
    legend = "Liaison Ethernet"

class ConsoleLink(Link):
    dot_style = "dashed"
    name = "C"
    legend = "Liaison Console"
    def dot_option(self):
        return ',weight="1"'

class CloudLink(Link):
    name = "V"
    dot_style = "dotted"
    legend = "Réseau logique"

    def dot(self, showip):
        return  '%s [ style=%s%s%s];\n' % (
            self.from_to(),
            self.dot_style, self.dot_label(showip), self.dot_option(),
            )

##############################################################################
#
##############################################################################

class Node:
    default_nr_interfaces = None
    nr = 0
    dot_shape_file = None
    dot_shape_file_ratio = None
    interfaces_name = {'C0': 'ttyS0', 'E0': 'eth0', 'E1': 'eth1', 'E2': 'eth2', 'E3': 'eth3'}

    def __init__(self, name, ip=None, nr_interfaces=None,label=None,
                 pos=None):
        if nr_interfaces == None:
            nr_interfaces = Host.default_nr_interfaces
        if ip:
            ip = IP(ip)
        self.ip = ip
        self.name = name
        self.pos = pos
        self.nr_interfaces = nr_interfaces
        self.interfaces = {}
        self.dot_name = 'n' + name.replace('.','_').replace('/','_')
        if label:
            self.name = label

    def inflate(self, nodes):
        n = list(nodes)
        for i in nodes:
            if i.done:
                continue
            i.done = True
            for j in i.interfaces.values():
                if isinstance(j, ConsoleLink):
                    continue
                h = j.remote_port.host
                if h not in n:
                    n.append(h)
                    h.distance = 1000000
                    h.distance_routeur = 1000000
                    h.done = False

                if h.distance > i.distance + 1:
                    h.distance = i.distance + 1
                    h.min_path = i.min_path + [j]

                if isinstance(h, Cisco):
                    increment = 1
                else:
                    increment = 0

                if h.distance_routeur > i.distance_routeur + increment:
                    h.distance_routeur = i.distance_routeur + increment
                    h.min_path_routeur = i.min_path + [j]
        return n

    def inflate_init(self):
        for h in self.network.hosts.values():
            h.done = False
        self.distance = 0
        self.distance_routeur = 0
        self.min_path = []
        self.min_path_routeur = []
        

    def distance_to(self, node):
        n = (self,)
        i = 0
        self.inflate_init()
        while True:
            if node in n:
                return i
            nn = self.inflate(n)
            if len(nn) == len(n):
                return None
            i += 1
            n = nn

    def connected(self, node):
        return self.distance_to(node) != None

    def inflate_max(self):
        n = [self]
        self.inflate_init()
        while True:
            m = self.inflate(n)
            if len(m) == len(n):
                break
            n = m
        return n

    def distance_max(self):
        return max([h.distance for h in self.inflate_max()])

    def distance_max_routeur(self):
        return max([h.distance_routeur for h in self.inflate_max()])

    def farest_nodes(self):
        m = self.distance_max()
        distance_max = max([h.distance for h in m])
        return [h for h in m if h.distance == distance_max]

    def ratio(self, dirname):
        if self.dot_shape_file_ratio == None:
            f = os.popen('identify -format "%w %h" ' + \
                         os.path.join(dirname, 'HTML', self.dot_shape_file),
                         "r")
            try:
                w, h = [int(x) for x in f.read()[:-1].split(' ')[0:2]]
            except:
                w, h = (1,1)

            f.close()
            self.dot_shape_file_ratio = w / float(h)
        return self.dot_shape_file_ratio


    def add_link(self, link):
        if link.port.key:
            if link.port.key in self.interfaces:
                raise ValueError("Interface yet used")
        else:
            for i in range(9): # Search free number
                interface_name = link.name + str(i)
                if interface_name not in self.interfaces:
                    link.port.key = interface_name
                    break

        link.port.name = self.interfaces_name.get(link.port.key, link.port.key)
        link.port.name_without_space = link.port.name.replace(' ','')
        self.interfaces[link.port.key] = link
        self.__dict__[link.port.key] = link

    def dot(self, zoom, dirname):
        if self.pos:
            s = 'pin=true,pos="%g,%g",' % (self.pos[0], self.pos[1])
        else:
            s = ''
        if self.dot_shape_file:
            return '%s [%slabel=<<TABLE BORDER="0" CELLBORDER="0" CELLPADDING="0" CELLSPACING="0"><TR><TD BORDER="0" PORT="0" HEIGHT="%d" WIDTH="%d" FIXEDSIZE="true"><IMG SRC="%s"/></TD></TR><TR><TD BORDER="0" BGCOLOR="#EEEEEE80">%s</TD></TR></TABLE>>,shape=none];\n' % (
        self.dot_name,
        s,
        # zoom/self.ratio(dirname)/100., zoom/100.,
        int(zoom/self.ratio(dirname)), int(zoom),
        self.dot_shape_file,
        self.name)
        else:
            return '%s [%slabel="%s",shape=%s ] ;\n' % (
                self.dot_name, s, self.name, self.dot_shape)

    def port_name(self):
        return self.dot_name + ':0'
    
    def filter(self, name, connected=True):
        if connected:
            for link in self.interfaces.values():
                if link.name == name:
                    yield link
        else:
            for iname in self.interfaces_name:
                if iname[0] == name:
                    yield iname

    def __str__(self):
        return self.name + '(' + self.__class__.__name__ + ')'
                    
class Host(Node):
    dot_shape = "ellipse"
    dot_shape_file = "icon-pc.png"

class Cisco(Node):
    dot_shape = "rectangle"
    dot_shape_file = "icon-routeur.png"

class Cisco1800(Cisco):
    names = ('1800', '1841')
    interfaces_name = {'C0': 'console',
                       'S0': 'serial 0/0/0', 'S1': 'serial 0/0/1',
                       'E0': 'fastethernet 0/0', 'E1': 'fastethernet 0/1'}
    ram = 1024*128
    nvram = 191
    flash = 31360
    conf_register = '0x2102'
    conf_register2 = '0x2142'
    interrupteur_on_off = True
    version_bootstrap="12.3(8r)"
    version_IOS="12.4(1c)"

class Cisco1700(Cisco):
    names = ('1700', '1721')
    interfaces_name = {'C0': 'console',
                       'S0': 'serial 0', 'S1': 'serial 1',
                       'E0': 'fastethernet 0'}
    ram = 1024*64
    nvram = 32
    flash = 32768
    conf_register = '0x2102'
    conf_register2 = '0x2142'
    interrupteur_on_off = True
    version_bootstrap="12.2(7r)"
    version_IOS="12.2(11)"

class Cloud(Node):
    dot_shape = "none"
    dot_shape_file = "icon-nuage.png"

class Switch(Node):
    dot_shape = "box"
    dot_shape_file = "icon-switch.png"


class Table(Node):
    dot_shape = "none"

    def dot(self, zoom, dirname):
        s = self.network.html(self.from_node)
        s = s.replace("<td>", '<td port="0">', 1)
        s = s.replace("<table>",
                      '<table cellpadding="0" cellspacing="0" cellborder="1" border="0">')
        
        return 'n%s [ shape=none,label=<%s> ] ;\n' % (self.name, s)
        

class Dot(Node):
    dot_shape = "none"
    dot_shape = "point"

    def port_name(self):
        return self.dot_name

    
##############################################################################
#
##############################################################################

class Network:
    def __init__(self, dirname, display_eth1=False):
        self.dirname = dirname
        self.hosts = {}
        Network.hosts = self.hosts # XXX Horrible XXX
        self.cache_nr_networks = None
        self.display_eth1 = display_eth1
    
    
    def append(self, hosts):
        for h in hosts:
            h.network = self
            if h.ip:
                self.hosts[str(h.ip)] = h
            else:
                self.hosts[len(self.hosts)] = h

    def remove(self, host):
        # Should remove links
        for k, h in self.hosts.items():
            if h == host:
                del self.hosts[k]
                return

    def nr_networks(self):
        if self.cache_nr_networks:
            return self.cache_nr_networks
        d = {}
        for h in self.hosts.values():
            for link in h.interfaces.values():
                if link.mask and link.port.ip:
                    d["%s/%d" % (str(link.network),
                                 link.mask.nr_bits_netmask()) ] = True
        self.cache_nr_networks = len(d)
        return self.cache_nr_networks
        

    def generate_clouds(self):
        # Do nothing if they exist
        for h in self.hosts.values():
            if isinstance(h, Cloud):
                return
        # compute network list and create link
        for h in self.hosts.values():
            for link in h.interfaces.values():
                if link.mask and link.port.ip:
                    n = "%s/%d" % (str(link.network),
                                   link.mask.nr_bits_netmask())
                    if n not in self.hosts.keys():
                        self.hosts[n] = Cloud(n)
                        self.hosts[n].network = self
                    CloudLink(port=Port(h), remote_port=Port(self.hosts[n]))

    def dot(self, filename, network_nodes=False, showip=False,
            start='x',table=True,zoom=20,legend=True,label_distance=1,
            from_node=None):

        f = open(os.path.join(self.dirname, 'HTML', filename) + '.dot', "w")
        label_distance = ',labeldistance="%g"' % label_distance
        if showip:
            font1 = 9
            font2 = 7
        else:
            font1 = 7
            font2 = 6
        font_size = "%d,%d" % (font1, font2)
        if network_nodes:
            self.generate_clouds()

        f.write("""
        digraph "Reseau" {
        charset="latin1";
        node[fontsize="%s"];
        edge[arrowhead=none,labelfontsize="%s", fontsize="%s", labelangle="30"%s];

        graph[outputorder="edgesfirst",page="11.69,8.26",maxiter="10000",charset="Latin1",start=%d];
        
        """ % (font_size, font_size,font_size,  label_distance, start))

        if table:
            t = Table('table')
            t.from_node = from_node
            self.append([t])

        if legend:
            links_type = []
            t = Dot('dot', label=' ')
            self.append([t])
            for h in self.hosts.values():
                for link in h.interfaces.values():
                    if link.__class__ not in links_type:
                        links_type.append(link.__class__)
                        d = Dot('v' + link.__class__.__name__, label=' ')
                        self.append([d])
                        link.__class__(port=Port(t), remote_port=Port(d),
                                       label=link.legend, hide_port=True)



        for h in self.hosts.values():
            if not isinstance(h, Table) \
               and not isinstance(h, Dot) \
                   and from_node and not h.connected(from_node):
                continue
            f.write(h.dot(zoom, self.dirname))
            for link in h.interfaces.values():
                if not link.inverted and link.remote_port:
                    f.write(link.dot(showip))

        if table:
            self.remove(t)

                
        f.write("}\n")                
        f.close()
        os.system("""
cd %s
neato -oxxx.svg -Tsvg %s.dot
sed <xxx.svg -e 's/font-size:%d\.[0-9]*pt/font-size:4.2pt/g' \\
            -e 's/font-size:%d.[0-9]*pt/font-size:4.0pt/g' \\
            -e 's/font-size:20.[0-9]*pt/font-size:10.0pt/g' \\
            >%s.svg
make %s.png
mv %s.svg %s.png %s

""" % (os.path.join(self.dirname, 'HTML'), filename, font1, font2,
       filename, filename, filename, filename,
       os.path.join('..','..','..',configuration.session.dir,'HTML')))
        
    def hosts_list(self):
        s = []
        for h in self.hosts.values():
            for link in h.interfaces.values():
                if link.mask and link.port.ip:
                    s.append(str(link.port.ip) + ' ' +
                                h.name + link.port.key)
        print '\n'.join(s)

    def html(self, from_node):
        hosts = self.hosts.values()
        hosts.sort(lambda x,y: cmp(x.name, y.name))
        if self.display_eth1:
            x = '<td>Host eth1</td>'
        else:
            x = ''
        s = ['<table>',
            "<tr><td>Host</td><td>Host eth0</td>",
             x,
             "<td>Cisco</td><td>Cisco eth0</td><td>Cisco serial 0</td>",
             "<td>Cisco serial 1</td></tr>"
             ]
        for h in hosts:
            if not isinstance(h, Host):
                continue
            if from_node and not h.connected(from_node):
                continue
            s.append("<tr>")
            if 'E0' in h.C0.remote_port.host.interfaces:
                e0 = h.C0.remote_port.host.E0.port_ip()
            else:
                e0 = ''
            if 'S0' in h.C0.remote_port.host.interfaces:
                s0 = h.C0.remote_port.host.S0.port_ip()
            else:
                s0 = ''
            if 'S1' in h.C0.remote_port.host.interfaces:
                s1 = h.C0.remote_port.host.S1.port_ip()
            else:
                s1 = ''
            x = [h.name, h.E0.port_ip()]
            if self.display_eth1:
                x.append( h.E1.port_ip() )
            x += [h.C0.remote_port.host.name, e0, s0, s1]
            for v in x:
                s.append("<td>%s</td>" % v)
            s.append("</tr>")
        s.append('</table>')
        return ''.join(s)


##############################################################################
#
# TESTS
#
##############################################################################

# Do not  use this test
class HostTest(Test):
    html_class = 'test_string test_good test_is'

    def test(self, student_answer, string, state=None):
        if state == None:
            return None
        try:
            host = Network.hosts[state.client_ip]
        except KeyError:
            return False, """Cet ordinateur (%s) ne fait pas parti du TP
            changez de poste ou prévenez l'enseignant si c'est un bug.""" % \
             state.client_ip
        return self.test_host(student_answer, string, state, host)


# NEW STYLE TEST : THIS ONE MUST BE USED.
class HostReplace(TestUnary):
    """Replace {attribute_name} in the teacher defined answer
    by the value for the host used by the student.

    Example:
       Good(HostReplace(Equal('ifconfig eth0 {E0.ip} netmask {E0.mask}')))
       # The order is important :
       Good(HostReplace(UpperCase('hostname {name}')))
       # The following will not work because the {name} is uppercased
       # Good(UpperCase(HostReplace('hostname {name}')))
    """
    
    def canonize(self, student_answer, state=None):
        """Do not canonize the student answer, but the tests themselve"""
        if state:
            self.children[0].initialize(
                lambda string, a_state:host_substitute(
                    self.parser(string, a_state),
                    Network.hosts[a_state.client_ip]
                    ),
                state)
        if state is None:
            return "?"
        if state.client_ip not in Network.hosts:
            return False, """Cet ordinateur (%s) ne fait pas parti du TP
            changez de poste ou prévenez l'enseignant si c'est un bug.""" % \
             state.client_ip
        return student_answer
        

def host_substitute(string, host):
    items = string.split('{')
    new = items[0]
    for i in items[1:]:
        item = i.split('}')
        if len(item) != 2:
            new += '{' + i
        else:
            e = item[0].replace('[', '["').replace(']', '"]')
            new += str(eval('host.' + e)) + item[1]
    return new
    
    
# Should be a 'Test' method ?
def host(test, state):
    """
    Some possible replacement:
       {name}
       {E0.mask}
       {E0.port.ip}
       {E0.remote_port.ip}
       {E0.remote_port.host.name}
       {C0.remote_port.host.name}
       {C0.remote_port.host.E0.port.ip}
       {C0.remote_port.host.E1.port.ip}       
    """
    
    strings = test.strings

    if state == None:
        return strings
    s = []
    try:
        host = Network.hosts[state.client_ip] # XXX Horrible XXX
    except KeyError:
        return strings
    for string in strings:
        string = filter_student_answer(string)
        new = host_substitute(string, host)
        if test.uppercase:
            new = new.upper()
        s.append(new)
    return s

def replace_host(string):
    """Used as : question=replace_host('Your computer is {name}')"""
    s = string
    def replace_host_tmp(state):
        if state == None:
            return s
        try:
            host = Network.hosts[state.client_ip] # XXX Horrible XXX
        except KeyError:
            return s
        return host_substitute(s, host)
    return replace_host_tmp

class HostInterfaces(HostTest):
    def test_host(self, student_answer, string, state, host):
        if host.nr_interfaces == int(student_answer):
            return True
        if host.nr_interfaces < int(student_answer):
            return False, """Recomptez ou bien vérifiez si le convertisseur
            USB/ethernet est bien branché"""
        return (False,
                "Ne comptez pas les interfaces réseaux virtuels (lo, sit, ...)"
                )

class HostCiscoModele(HostTest):
    uppercase = True
    def test_host(self, student_answer, string, state, host):
        student_answer = student_answer.upper().strip(' CISCOSERIE')
        if student_answer in host.C0.remote_port.host.names :
            return True

class HostCiscoNrSerials(HostTest):
    def test_host(self, student_answer, string, state, host):
        if int(student_answer) == len(
            list(host.C0.remote_port.host.filter('S', connected=False))):
            return True

class HostCiscoNrEthernet(HostTest):
    def test_host(self, student_answer, string, state, host):
        if int(student_answer) == len(
            list(host.C0.remote_port.host.filter('E',connected=False))):
            return True

class HostCiscoOnOff(HostTest):
    def test_host(self, student_answer, string, state, host):
        return yesno(student_answer,
                     yes_is_good = host.C0.remote_port.host.interrupteur_on_off)

class NrInterfacesUsed(HostTest):
    def test_host(self, student_answer, string, state, host):
        if int(student_answer) == ( len(list(host.C0.remote_port.host.filter('E')))
            + len(list(host.C0.remote_port.host.filter('S'))) ):
            return True
        return False, "La liaison console n'est pas un interface réseau"

class MaxDistance(HostTest):
    def test_host(self, student_answer, string, state, host):
        if int(student_answer) == host.distance_max() - 1:
            return True
        return False, ""

class MaxDistanceRouteur(HostTest):
    def test_host(self, student_answer, string, state, host):
        if int(student_answer) \
               == host.C0.remote_port.host.distance_max_routeur() + 2:
            return True
        return False, ""

###############################################################################

class require_ip(Test):
    def test(self, student_answer, string):
        try:
            a = IP(student_answer)
        except ValueError, e:
            return False, str(e)


require_ping = require('ping',"On utilise la commande <tt>ping</tt>")

postes = (      
["10.57.19.233", 'A3',Cisco1700], # Not tuple In order to modify after
["10.57.18.10", 'B3',Cisco1800],
("10.57.30.150", 'C3',Cisco1700),
("10.57.30.152", 'D3',Cisco1800),
("10.56.145.237", 'E3',Cisco1700),
("10.57.30.155", 'F3',Cisco1800),
("10.57.30.159", 'G3',Cisco1700),
("10.57.18.238", 'H3',Cisco1800),
("10.57.30.151", 'I3',Cisco1700),
("10.57.18.242", 'J3',Cisco1800),
("10.57.30.162", 'K3',Cisco1700),
("10.57.18.250", 'L3',Cisco1800),
("10.57.30.156", 'M3',Cisco1700),
("10.57.30.165", 'N3',Cisco1800),
("10.57.30.164", 'O3',Cisco1700),
("10.57.30.160", 'P3',Cisco1800),
)

# When the system is debugged, the server change the IP address
# of the first student.

import socket

if socket.gethostname() == 'lirispaj':
    postes[0][0] = "134.214.142.30"
elif socket.gethostname() == 'pundit':
    postes[1][0] = "127.0.1.1"

