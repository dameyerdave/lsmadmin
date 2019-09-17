import os, sys

appdir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(appdir + '/lib')

import cherrypy
from ldap import LDAPAuth, LDAPUser

class LSMAdmin(object):
    @cherrypy.expose
    def index(self):
        return "Hello World!"

@cherrypy.expose
class LSMAdminLogon(object):
    def GET(self):
        return """
            <html><head></head><body>
            <form method="post" action="logon">
                <input type="text" name="user"/>
                <input type="password" name="password" />
                <button type="submit">Login</button>
            </form>
            </body></html>
        """

    def POST(self, user, password):
        print(user, password)
        ldapauth = LDAPAuth('ldap', 389)
        ldapuser = ldapauth.authenticate('cn=' + user + ',ou=splunk,ou=users,ou=dom,dc=example,dc=org', password)
        return "Hello " + ldapuser.givenName

if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/logon': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/html')],
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './static'
        }
    }
    app = LSMAdmin()
    app.logon = LSMAdminLogon()
    cherrypy.quickstart(app, '/', conf)
