from ldap3 import Connection, LEVEL, Server, Tls, LDAPBindError
from ldap3.utils.conv import escape_bytes
from django.contrib.auth.models import User, BaseUserManager
from django.conf import settings
from django.views.decorators.debug import sensitive_variables
import base64
import accounts.models
import uuid
from pprint import pprint


def get_ldap_connection( binddn=settings.AD_BINDDN, password=settings.AD_BINDDN_PASSWORD):
    tls = Tls()
    server = Server(settings.AD_URL, tls=tls)
    connection = Connection(server, user=binddn, password=password, auto_bind=True)
    return connection

class PS1Backend(object):

    @sensitive_variables('password')
    def authenticate(self, username=None, password=None, **kwargs):
        if len(password) == 0:
            return None

        user = None
        binddn = "{0}@{1}".format(username, settings.AD_DOMAIN)

        try:
            get_ldap_connection( binddn, password )
        except LDAPBindError:
            return None

        with get_ldap_connection() as c:
            filter_string ='(sAMAccountName={0})'.format(username)
            x = c.search(
                search_base=settings.AD_BASEDN,
                search_filter=filter_string,
                search_scope=LEVEL,
                attributes = ['objectGUID']
            )
            object_guid = c.response[0]['attributes']['objectGUID'][0]
            guid = uuid.UUID(bytes_le=object_guid)
            user = self.get_user(str(guid))
            user._expire_ldap_data()
            return user

    def get_user(self, user_id):
        from .models import PS1User
        """
        Get's The user object and attached ldap_user data.
        Will create the database entry if required.

        Keyword arguments:
        user_id -- a string or UUID object of samba4 objectGUID of a user.
        """
        try:
            guid = uuid.UUID(str(user_id))
        except ValueError:
            # Happens when we get passed an invalid or outdated user_id
            return None
        try:
            user = PS1User.objects.get(object_guid=str(guid))
        except PS1User.DoesNotExist:
            filter_string = '(objectGUID={})'.format(escape_bytes(guid.bytes_le))
            with get_ldap_connection() as c:
                c.search(settings.AD_BASEDN, filter_string, LEVEL)
                user_dn = c.response[0]['dn']
            user = PS1User(object_guid=str(guid))
            user.save()
        return user

    def get_group_permissions(self, user_obj, obj=None):
        raise NotImplementedError

    def get_all_permissions(self, user_obj, obj=None):
        raise NotImplementedError

    def has_perm(self, user_obj, perm, obj=None):
        raise NotImplementedError

    def has_module_perms(self, user_obj, app_label):
        raise NotImplementedError

