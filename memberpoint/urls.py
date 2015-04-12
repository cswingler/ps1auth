from django.conf.urls import patterns, include, url
from .views import MemberPointFormView
from .forms import GrantMemberPointForm, ConsumeMemberPointForm

urlpatterns = patterns('memberpoint.views',
    url(r'list/(?P<user_id>.+)$', 'list', name='memberpoint-list'),
    url(r'grant/(?P<user_id>.+)$',
        MemberPointFormView.as_view(
            form_class = GrantMemberPointForm,
            title = 'Add Member Point',
        ), name='memberpoint-grant'),
    url(r'consume/(?P<user_id>.+)$',
        MemberPointFormView.as_view(
            form_class=ConsumeMemberPointForm,
            title = 'Consume Member Point',
        ), name='memberpoint-consume'),
)
