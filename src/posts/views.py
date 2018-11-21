from urllib import quote_plus
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect, Http404
from django.db.models import Q

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.utils import timezone
from .forms import PostForm
from .models import Post

# Create your views here.
def  post_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Post successful created")
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "form": form,
    }

    return render(request, "post_form.html", context)

def  post_list(request):
    today = timezone.now().date()
    # Post.objects.filter(publish__lte=timezone.now())
    #.filter(draft=False) show only posts that are been created after have add draft
    queryset_list = Post.objects.active() #.order_by("-timestamp")
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Post.objects.all()
    # this is for the search posts

    query = request.GET.get("q")
    if query:
        queryset_list = Post.objects.filter(Q(title__icontains=query))

    # pagination
    paginator = Paginator(queryset_list, 5) # Show 5 contacts per page
    page_request = "page"
    page = request.GET.get(page_request)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    context={
         "object_list":queryset,
         "title":"List",
         "page_request":page_request,
         "today":today,
    }
    template = "post_list.html"
    # if request.user.is_authenticated():
    #         context={
    #                 "title":"My user List"
    #         }
    # else:
    #     context={
    #     "title":"List"
    #     }
    return render(request, template, context)


def  post_detail(request, slug=None):
    # instance = Post.objects.get(id=1)
    instance = get_object_or_404(Post, slug=slug)
    if instance.publish >timezone.now().date() or instance.draft:
        if not request.user.is_staff or not request.user.is_superuser:
           raise Http404
    share_string = quote_plus(instance.content)
    context={
    "title": instance.title,
    "instance": instance,
    "share_string": share_string,
    }

    return render(request,"post_detail.html",context)


def  post_update(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser or not request.user.is_authenticated():
        raise Http404
    # instance = Post.objects.get(id=1)
    instance = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None,request.FILES or None, instance = instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request,"<a href='#'>Post</a> Saved", extra_tags='html_safe')
        return HttpResponseRedirect(instance.get_absolute_url())

    context={
        "title": instance.title,
        "instance": instance,
        "form":form,
    }

    return render(request,"post_form.html", context)

def  post_delete(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    instance.delete()
    messages.success(request,"Post successful deleted")
    return redirect("posts:list")

# def search(request):
#    template = "post_list.html"
#    query = request.GET.get("q")
#    results = Post.objects.filter(Q(title__icontains=query)| Q(content__contains=query))
#    #pages = pagination(request, results, num=1)
#    paginator = Paginator(results, 5)
#    page_request = "page"
#    page = request.GET.get(page_request)
#    try:
#        queryset = paginator.page(page)
#    except PageNotAnInteger:
#        # If page is not an integer, deliver first page.
#        queryset = paginator.page(1)
#    except EmptyPage:
#        # If page is out of range (e.g. 9999), deliver last page of results.
#        queryset = paginator.page(paginator.num_pages)
#
#    context = {
#        "page_request":page_request,
#    }
#    return render(request,template, context)
