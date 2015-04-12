from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse
from django.views.generic import RedirectView
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'auth.views.home', name='home'),
    url(r'^$', RedirectView.as_view(permanent=False, url='/mm/member_list')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ckeditor/', include('ckeditor.urls')),
    url(r'^memberpoints/', include('memberpoint.urls')),
    url(r'^mm/', include('member_management.urls')),
    #url(r'^pp/', include('paypal_integration.urls')),
    url(r'^rfid/', include('rfid.urls')),
    url(r'^signup/', include('signup.urls')),
)

# Cool URIs don't change
urlpatterns += patterns('',
    url(r'^zinc/member_list$', RedirectView.as_view(permanent=False, url='/mm/member_list')),
    url(r'^zinc/activate/$', RedirectView.as_view(permanent=False, url='/signup/activate')),
)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()

