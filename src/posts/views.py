from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from .forms import PostForm
from .models import Post

# Create your views here.
def  post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request,"Post successful created")
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.error(request,"Post not created")
        #return the form just created
        # add a message that say the object "form" was created
    context = {
        "form": form,
    }

    return render(request, "post_form.html",context)

def  post_list(request):
    queryset = Post.objects.all()
    context={
         "object_list":queryset,
               "title":"List"
    }
    # if request.user.is_authenticated():
    #         context={
    #                 "title":"My user List"
    #         }
    # else:
    #     context={
    #     "title":"List"
    #     }
    return render(request,"base.html",context)

def  post_detail(request, id):
    # instance = Post.objects.get(id=1)
    instance = get_object_or_404(Post, id=id)
    context={
    "title": instance.title,
    "instance": instance,
    }

    return render(request,"post_detail.html",context)


def  post_update(request, id=None):
    # instance = Post.objects.get(id=1)
    instance = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, instance = instance )
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request,"Post successful saved")
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.error(request,"Post not saved, check data validity")
        # add a message that say the object "form" was edited

    context={
    "title": instance.title,
    "instance": instance,
    "form":form,
    }

    return render(request,"post_form.html",context)

def  post_delete(request):
    instance = get_object_or_404(Post, id=id)
    instance.delete()
    messages.success(request,"Post successful deleted")
    return redirect("posts:list")
