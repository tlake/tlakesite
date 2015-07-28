from django.conf.urls import patterns, include, url
from django.contrib import admin
from app_home.views import ComingSoonView


urlpatterns = patterns(
    # Examples:
    # url(r'^$', 'tlake_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    '',
    url(r'^$', include('app_home.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^comingsoon/', ComingSoonView.as_view(), name='app_home-comingsoon'),
    url(r'^blog/', include('app_blog.urls')),
    url(r'^projects/', include('app_projects.urls')),

)