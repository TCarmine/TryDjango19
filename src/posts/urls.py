from django.conf.urls import url
from django.contrib import admin

from .views import (
post_list,
post_create,
post_detail,
post_update,
post_delete,
# search,
)

# ^ beginning string,$ end string, so a URL string need to be
# exactly matched if between those 2
urlpatterns = [
    url(r'^$', post_list, name='list'),
    # url(r'^results/$', search, name="search"),
    url(r'^create/$',  "posts.views.post_create"),
    #url(r'^(?P<slug>\d+)/$', post_detail, name='detail'),
    url(r'^(?P<slug>[\w-]+)/$', post_detail, name='detail'),
    url(r'^(?P<slug>[\w-]+)/edit/$', post_update, name='update'),
    url(r'^(?P<id>\d+)/delete/$', post_delete, name='delete'),
]
