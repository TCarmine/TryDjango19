from django.conf.urls import url
from django.contrib import admin

from .views import (
post_list,
post_create,
post_detail,
post_update,
post_delete,
)

# ^ beginning string,$ end string, so a URL string need to be
# exactly matched if between those 2
urlpatterns = [
    url(r'^$',        "posts.views.post_list"),
    url(r'^create/$',  "posts.views.post_create"),
    url(r'^(?P<id>\d+)/$', post_detail, name='detail'),
    url(r'^update/$', "posts.views.post_update"),
    url(r'^delete/$', "posts.views.post_delete"),
]
