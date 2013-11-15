from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
   
    # Examples:
    url(r'^$','tsquare-web.views.tlogin'),
    url(r'^tlogin/$', 'tsquare-web.views.tlogin'),
    url(r'^tlogout/$','tsquare-web.views.tlogout'),
    url(r'^home/$','tsquare-web.views.home'),
    url(r'^services/$','tsquare-web.views.external_services'),
    url(r'^sites/$','tsquare-web.views.sites'),
    url(r'^github/repos/select/$','tsquare-web.views.select_github_repos'),
    url(r'^github_login/$','tsquare-web.views.github_login'),
    url(r'^github_login_exchange/$','tsquare-web.views.github_login_exchange'),
    url(r'^google_login/$','tsquare-web.views.google_login'),
    url(r'^google_login_exchange/$','tsquare-web.views.google_login_exchange'),
    url(r'^gdrive_select/$','tsquare-web.views.gdrive_select'),
    url(r'^assignments/$','tsquare-web.views.assignments'),
    url(r'^assignment_detail','tsquare-web.views.assignment_detail'),
    url(r'^profile','tsquare-web.views.profile'),
    url(r'^gradebook','tsquare-web.views.gradebook'),
    url(r'^resources','tsquare-web.views.resources'),
    url(r'^course_info','tsquare-web.views.course_info'),
    url(r'^announcements','tsquare-web.views.announcements'),
    url(r'^wiki','tsquare-web.views.wiki'),
    url(r'^help','tsquare-web.views.help'),
    # url(r'^CS_4911_Tsquare/', include('CS_4911_Tsquare.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
