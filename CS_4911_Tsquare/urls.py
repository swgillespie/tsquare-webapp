from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
   
    # Examples:
    url(r'^$','tsquare.views.index'),
    url(r'^tlogin/$', 'tsquare.views.tlogin'),
    url(r'^tlogout/$','tsquare.views.tlogout'),
    url(r'^home/$','tsquare.views.home'),
    url(r'^assignments/$','tsquare.views.assignments'),
    url(r'^profile/$','tsquare.views.profile'),
    url(r'^setup_profile/$','tsquare.views.setup_profile'), 
    url(r'^github/repos/select/$','tsquare.views.select_github_repos'),
    url(r'^github_login/$','tsquare.views.github_login'),
    url(r'^github_login_exchange/$','tsquare.views.github_login_exchange'),
    # url(r'^CS_4911_Tsquare/', include('CS_4911_Tsquare.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
