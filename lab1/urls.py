from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.url_list, name='url_list'),
    url(r'^url/(?P<pk>\d+)/$', views.url_detail, name='url_detail'),
    url(r'^delete/(?P<pk>\d+)$', views.url_delete, ),
]
