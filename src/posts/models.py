from __future__ import unicode_literals

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
#in order to take an action before the model is saved
from django.db.models.signals import pre_save
#this in oder to put a default in DateField
from django.utils import timezone
from django.utils.timezone import now
from django.utils.text import slugify


class PostManager(models.Manager):
    def active(self,*args,**kwargs):
        return super(PostManager,self).filter(draft=False).filter(publish__lte=timezone.now())


def upload_location( instance, filename):
    return "%s/%s" %(instance.id,filename)

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    title = models.CharField(max_length=120)
    #once introduced the db need to be recreated
    slug = models.SlugField(unique = True)
    image = models.ImageField(upload_to=upload_location,
            null=True, blank=True,
            width_field="width_field",
            height_field="height_field" )
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField()
    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False, auto_now_add=False, default=now)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField (auto_now=False, auto_now_add=True)

    objects = PostManager()

    #Python 2.7
    def __unicode__(self):
        return self.title
    #Python 3.4
    #def __str__(self):
    #   return self.title

    #for better serving url
    def get_absolute_url(self):
        # return "/posts/%s/" %(self.id)
         return reverse("posts:detail", kwargs={"slug": self.slug})

    #adding ordering directly in the model
    class Meta:
        ordering = ["-timestamp","-updated"]

def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug ="%s-%s" %(slug, qs.first().id)
        #return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_post_receiver(sender, instance, *args,**kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_post_receiver, sender=Post)
