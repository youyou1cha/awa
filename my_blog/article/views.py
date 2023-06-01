from django.shortcuts import render,redirect
import markdown
# Create your views here.

from django.http import HttpResponse
from .models import ArticlePost
from .forms import ArticlePostForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# 试图函数
def article_list(request):
    articles = ArticlePost.objects.all()
    # context = {'articles': articles}
    # return render(request, 'article/list.html', context)

    paginator = paginator(article_list,1)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    context = {'articles':articles}
    # context = {'articles'}
    return render(request,'article/list.html',context)


def article_detail(request, id):
    article = ArticlePost.objects.get(id=id)
    # context = {'article': article}
    # return render(request, 'article/detail.html', context)

    #  markdown语法
    article.total_views += 1
    article.save(update_fields=['total_views'])
    article.body = markdown.markdown(article.body,
                                     extensions=[
                                         #
                                         'markdown.extensions.extra',
                                         'markdown.extensions.codehilite',
                                     ]                 
                                     )
    context = {'article':article}
    return render(request,'article/detail.html',context)
@login_required(login_url='/userprofile/logine/')
def article_create(request):
    if request.method == 'POST':
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            new_article = article_post_form.save(commit=False)
            new_article.author = User.objects.get(id=1)
            new_article.save()
            return redirect("article:article_list")
        else:
            return HttpResponse("表单内容有错误，请重新填写。")
    else:
        article_post_form = ArticlePostForm()
        context = {'article_post_form':article_post_form}
        return render(request,'article/create.html',context)

def article_delete(request,id):
    article = ArticlePost.objects.get(id=id)
    article.delete()
    return redirect("article:article_list")

def article_update(request,id):
    article = ArticlePost.objects.get(id=id)
    if request.method == "POST":
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            article.title = request.POST['title']
            article.body = request.POST['body']
            article.save()
            return redirect("article:article_detail",id=id)
        else:
            return HttpResponse("表单内容有误 请重新登录")
    else:
        article_post_form = ArticlePostForm()
        context = {"article":article,'article_post_form':article_post_form}
        return render(request,'article/update.html',context)