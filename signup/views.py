from django.contrib import messages
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import activate_account_form, account_register_form
from .models import Token 

# Create your views here.

def activate_account(request):
    if request.method == 'POST':
        form = activate_account_form(request.POST)
        if form.is_valid():
            site = get_current_site(request)
            user = form.save( request.is_secure(), site.domain)
            return HttpResponseRedirect(reverse('signup.views.activation_email_sent'))
    else:
        form = activate_account_form()
    return render(request, 'signup/activate_account.html', {
        'form': form,
    })

def activation_email_sent(request):
    return render(request, 'signup/activate_account_email_sent.html')

def account_activate_confirm(request, token):
    try:
        token = Token.objects.get(token=token)
    except Token.DoesNotExist:
        messages.error(request, "Unknown Account Activation URL")
        return HttpResponseRedirect(reverse('signup.views.activate_account'))
    person = token.person
    if request.method == 'POST':
        form = account_register_form(request.POST)
        if form.is_valid():
            user = form.save()
            user.backend = 'accounts.backends.PS1Backend'
            login(request, user)
            return HttpResponseRedirect(reverse('accounts.views.set_password'))
    else:
        data = {}
        data['first_name'] = person.first_name
        data['last_name'] = person.last_name
        data['preferred_email'] = person.email
        data['token'] = token.token
        form = account_register_form(initial=data)
    return render(request, 'signup/account_register.html', {
        'form': form,
    })
