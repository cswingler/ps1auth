from django.contrib.auth import get_user_model
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView
from .models import MemberPoint
from .forms import GrantMemberPointForm
from accounts.models import PS1User
import reversion

@login_required
def list(request, user_id):
    target_user = PS1User.objects.get(object_guid=user_id)
    context = {}
    context['target_user'] = target_user
    context['points'] = target_user.memberpoint_set.all()
    return render(request, 'memberpoint/list.html', context)

class MemberPointFormView(FormView):
    template_name = 'memberpoint/form.html'
    form_class = None
    title = None
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(MemberPointFormView, self).get_context_data(**kwargs)
        context['title'] = self.title
        context['points'] = self.owner.memberpoint_set.valid()
        context['owner'] = self.owner
        return context

    def get(self, request, user_id):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        form.owner = get_user_model().objects.get(pk=user_id)
        #form.fields['owner'].initial = user_id
        self.owner = get_user_model().objects.get(pk=user_id)
        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def post(self, request, user_id):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        self.owner = get_user_model().objects.get(pk=user_id)
        form.owner = self.owner
        if form.is_valid():
            with transaction.atomic(), reversion.create_revision():
                form.save()
                messages.success(request, form.success_message)
                reversion.set_user(request.user)
            return HttpResponseRedirect(request.get_full_path())
        else:
            return self.form_invalid(form)

    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kwargs):
        return super(MemberPointFormView, self).dispatch(*args, **kwargs)
