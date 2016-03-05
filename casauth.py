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
import urllib.request, urllib.error, urllib.parse
import urllib.request, urllib.parse, urllib.error
from . import configuration

# To make casauth work we should not use a proxy
# It is done in 'main.py'

def redirect(serv, service):
    """Redirect user browser on the CAS login page for the given service"""
    print('Redirect web client to', service)
    serv.send_response(307)
    serv.send_header('Location', '%s/login?service=%s' % (
        configuration.CAS,service))
    serv.end_headers()

def get_name(ticket, service):
    """With the ticket and the service get the user name"""
    print('Get user name for service', service, 'and ticket', ticket)
    checkparams = "?service=" + service + "&ticket=" + ticket
    casdata = urllib.request.urlopen("%s/validate?service=%s&ticket=%s" % (
        configuration.CAS, service, urllib.parse.quote(ticket)
    ))
    
    test = casdata.readline().strip()
    if test == 'yes':
        return casdata.readline().strip().lower()               
    else:
        print('Cannot authenticate ticket', test)
        raise IOError("Can't authenticate ticket: " + test)

def logout_url():
    return configuration.CAS + "/logout"
    
