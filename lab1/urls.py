from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^$', views.url_list, name='url_list'),
    url(r'^url/(?P<pk>\d+)/$', views.url_detail, name='url_detail'),
    url(r'^delete/(?P<pk>\d+)$', views.url_delete, ),
    url(r'^accounts/login/$', views.auth_views.login, name="login"),
    url(r'^accounts/logout/$', views.logout_view, name="logout"),
    url(r'^api/urls/$', views.url_api),
    url(r'^api/urls/(?P<pk>[0-9]+)$', views.detail_url_api)
]

urlpatterns = format_suffix_patterns(urlpatterns)
