from django.conf.urls import url
from django.contrib import admin

from . import views

# ^ beginning string,$ end string, so a URL string need to be
# exactly matched if between those 2
urlpatterns = [
    url(r'^$',        "posts.views.post_list"),
    url(r'^create/$',  "posts.views.post_create"),
    url(r'^detail/$',  "posts.views.post_detail"),
    url(r'^update/$', "posts.views.post_update"),
    url(r'^delete/$', "posts.views.post_delete"),
]
