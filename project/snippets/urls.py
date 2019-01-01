from django.conf.urls import url
from . import views

app_name = 'snippets'
urlpatterns = [
    url(r'^$', views.snippet_list),
    url(r'^(?P<pk>[0-9]+)/$', views.snippet_detail),
    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
    url(r'^api-auth/',  include('rest_framework.urls', namespace='rest_framework')), # namespace값은 고정임.
]

# 접미사(suffix)로 format형식 지정해주기.
# 해당 함수를 사용하면 api를 호출할 때, 포멧접미사를 붙여서 포맷을 지정할 수 있음
urlpatterns = format_suffix_patterns(urlpatterns)