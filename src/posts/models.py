from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=120)
    content = models.TextField()
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField (auto_now=False, auto_now_add=True)

    #Python 2.7
    def __unicode__(self):
        return self.title
    #Python 3.4
    #def __str__(self):
    #   return self.title

    #for better serving url
    def get_absolute_url(self):
        # return "/posts/%s/" %(self.id)
         return reverse("posts:detail", kwargs={"id": self.id})
