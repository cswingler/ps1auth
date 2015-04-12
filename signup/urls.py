from django.conf.urls import patterns, include, url

urlpatterns = patterns('signup.views',
    url(r'activate/$', 'activate_account', {}),
    url(r'activate/email_sent$', 'activation_email_sent', {}),
    url(r'activate/confirm/(?P<token>.*)$', 'account_activate_confirm', {}),
)
