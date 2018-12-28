from django.conf.urls import url
#
from rest_framework.urlpatterns import format_suffix_patterns
#
from . import views

app_name = 'snippets'
urlpatterns = [
    url(r'^$', views.snippet_list),
    url(r'^(?P<pk>[0-9]+)/$', views.snippet_detail),
]

# 접미사(suffix)로 format형식 지정해주기.
# 해당 함수를 사용하면 api를 호출할 때, 포멧접미사를 붙여서 포맷을 지정할 수 있음
urlpatterns = format_suffix_patterns(urlpatterns)