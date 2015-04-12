from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import password_reset_complete
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
from django.template.loader import get_template
from django.template.response import TemplateResponse
from django.views.decorators.debug import sensitive_variables, sensitive_post_parameters

from .tokens import default_token_generator
from .forms import SetPasswordForm
from .backends import PS1Backend, get_ldap_connection
from .models import Token

def hello_world(request):
    t = get_template("hello_world.html")
    context = RequestContext(request)
    html = t.render(context)
    return HttpResponse(html)

@sensitive_post_parameters('password')
def login(request):
    if request.method == 'POST':
        form = AutenticationForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    #Redirect to a success page.
                else:
                    pass
                    #return a 'disabled account' error message
            else:
                pass
                #return an 'invalid login' error message

@login_required()
def access_page(request):
    data = {}
    return render( request, "access_page.html", data )

@login_required()
def set_password(request):
    if request.method == 'POST':
        form = SetPasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('member_management.views.member_list'))
    else:
        form = SetPasswordForm(request.user)
    context = {
            'user': request.user,
            'form': form,
    }
    return render(
            request,
            'registration/password_reset_confirm.html',
            context)

def password_reset_confirm(request, uid=None, token=None,
                           template_name='registration/password_reset_confirm.html',
                           token_generator=default_token_generator,
                           set_password_form=SetPasswordForm,
                           post_reset_redirect=None,
                           current_app=None, extra_context=None):
    """
    View that checks the hash in a password reset link and presents a
    form for entering a new password.
    ripped from https://github.com/django/django/blob/d51b7794bfd1ddfd92f71f71d07daf931421c5f7/django/contrib/auth/views.py#L185-L229
    """
    UserModel = get_user_model()
    assert uid is not None and token is not None # checked by URLconf
    if post_reset_redirect is None:
        post_reset_redirect = reverse('django.contrib.auth.views.password_reset_complete')
    else:
        post_reset_redirect = resolve_url(post_reset_redirect)
    try:
        uid = uid
        user = UserModel._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        validlink = True
        if request.method == 'POST':
            form = set_password_form(user, request.POST)
            if form.is_valid():
                form.save()
                token_object = Token.objects.get(key=token)
                token_object.delete()
                # HEFTODO I really could just log the user in here.
                # HEFTODO It would be smart to delete all the users tokens.
                return HttpResponseRedirect(post_reset_redirect)
        else:
            form = set_password_form(None)
    else:
        validlink = False
        form = None
    context = {
        'user': PS1Backend().get_user(uid),
        'form': form,
        'validlink': validlink,
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)

import uuid
from zoho_integration.models import Contact
from accounts.models import PS1User
@login_required()
def audits(request):
    l = get_ldap_connection()
    filter_string ='(ObjectClass=Person)'
    #sAMAccountName userAccountControl pwdLastSet
    users_result = l.search_ext_s(settings.AD_BASEDN ,ldap.SCOPE_ONELEVEL, filterstr=filter_string)
    users = []
    for user_result in users_result:
        guid = str( uuid.UUID( bytes_le=( user_result[1]['objectGUID'][0] ) ) )
        try:
            account = PS1User.objects.get(object_guid=guid)
            try:
                contact = account.contact
            except Contact.DoesNotExist:
                contact = None
        except PS1User.DoesNotExist:
            account = None
            contact = None

        end_date = None
        if contact:
            end_date = contact.membership_end_date

        user = {
            'name':       user_result[1]['sAMAccountName'][0],
            'enabled':    (int(user_result[1]['userAccountControl'][0]) & 2) != 2,
            'pwdLastSet': win32_filetime(user_result[1]['pwdLastSet'][0]),
            'contact':  contact,
            'account': account,
            'guid': str(guid),
            'end_date': end_date,
        }
        users.append(user)

    data = {}
    data["debug"] = True
    data["users"] = users
    data['payers'] = paypal_payers()
    return render( request, "audits.html", data )


from datetime import datetime, timedelta

def win32_filetime(filetime_timestamp):
    microseconds = int(filetime_timestamp) / 10.
    return datetime(1601,1,1) + timedelta(microseconds=microseconds)

