from django.shortcuts import render
from apps.blog.models import Article, Category, Tag
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404
from django.conf import settings

categories = Category.objects.all()  # get all Category objects
tags = Tag.objects.all() #get all Tag objects

# Create your views here.
def home(request):
    posts = Article.objects.all()  # get all Article objects
    paginator = Paginator(posts, settings.PAGE_NUM)  # the number of articles every page, PAGE_NUM is set in the settings.py
    page = request.GET.get('page') # get page parm in URL
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list =paginator.page(paginator.num_pages)

    return render(request, 'home.html', {'post_list': post_list, 'category_list': categories})

def detail(request, id):  # detail of article
    try:
        post = Article.objects.get(id = str(id))
        post.viewed()  # Update the count of viewed
        tags = post.tags.all()   #get all the tags of this article
        next_post = post.next_article()
        prev_post = post.prev_article()
    except Article.DoesNotExist:
        raise Http404

    return render(
        request, 'post.html',
        {
            'post': post,
            'tags': tags,
            'category_list': categories,
            'next_post': next_post,
            'prev_post': prev_post
        }
    )

def search_category(request, id):
    posts = Article.objects.filter(category_id = str(id))
    category = categories.get(id = str(id))
    paginator = Paginator(posts, settings.PAGE_NUM)
    try:
        page = request.GET.get('page')   # 获取URL中page参数的值
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)

    return render(request, 'category.html', {'post_list': post_list, 'category_list': categories, 'category': category})

def search_tag(request, tag):
    posts = Article.objects.filter(tags__name__contains=tag)
    paginator = Paginator(posts, settings.PAGE_NUM)
    try:
        page = request.GET.get('page')
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)

    return render(request, 'tag.html', {'post_list': post_list, 'category_list': categories, 'tag': tag})

def archives(request, year, month):
    posts = Article.objects.filter(pub_time__year=year, pub_time__month=month).order_by('-pub_time')
    paginator = Paginator(posts, settings.PAGE_NUM)
    try:
        page = request.GET.get('page')
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)

    return render(request, 'archive.html', {'post_list': post_list, 'category_list': categories, 'months': months, 'year_month': year+'年'+month+'月' })
