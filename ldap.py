import os, sys, json

appdir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(appdir + '/lib')

from ldap3 import Server, Connection, ALL, ALL_ATTRIBUTES, SUBTREE

class LDAPAuth():
    def __init__(self, hostname, port):
        self._server = Server(hostname, get_info=ALL) 

    def authenticate(self, dn, password):
        conn = Connection(self._server, dn, password)
        state = conn.bind()
        if state:
            conn.search(search_base=dn, search_filter='(objectClass=inetOrgPerson)', search_scope=SUBTREE, attributes=ALL_ATTRIBUTES)
            return LDAPUser(conn.response)
        else:
            return None

class LDAPUser():
    #[{'raw_dn': b'cn=dave,ou=splunk,ou=users,ou=dom,dc=example,dc=org', 'dn': 'cn=dave,ou=splunk,ou=users,ou=dom,dc=example,dc=org', 'raw_attributes': {'gidNumber': [b'500'], 'givenName': [b'David'], 'homeDirectory': [b'/home/users/dme'], 'loginShell': [b'/bin/sh'], 'objectClass': [b'inetOrgPerson', b'posixAccount', b'top'], 'sn': [b'Meyer'], 'uid': [b'dme'], 'uidNumber': [b'1000'], 'cn': [b'dave'], 'userPassword': [b'{SSHA}3z3Mx6P2TTa/BWC5BDnuO3pFI1TUuNg8']}, 'attributes': {'gidNumber': 500, 'givenName': ['David'], 'homeDirectory': '/home/users/dme', 'loginShell': '/bin/sh', 'objectClass': ['inetOrgPerson', 'posixAccount', 'top'], 'sn': ['Meyer'], 'uid': ['dme'], 'uidNumber': 1000, 'cn': ['dave'], 'userPassword': [b'{SSHA}3z3Mx6P2TTa/BWC5BDnuO3pFI1TUuNg8']}, 'type': 'searchResEntry'}]
    def __init__(self, ldap_resp):
        self._userinfo = ldap_resp[0]

    @property
    def uid(self):
        return elf._userinfo['raw_attributes']['uid'][0].decode("utf-8")

    @property
    def sn(self):
        return self._userinfo['raw_attributes']['sn'][0].decode("utf-8")

    @property
    def givenName(self):
        return self._userinfo['raw_attributes']['givenName'][0].decode("utf-8")

