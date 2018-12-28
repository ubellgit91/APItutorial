from django.conf.urls import url
from . import views

app_name = 'snippets'
urlpatterns = [
    url(r'^$', views.snippet_list),
    url(r'^(?P<pk>[0-9]+)/$', views.snippet_detail),
]