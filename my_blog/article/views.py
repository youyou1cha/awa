from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from .models import ArticlePost


# 试图函数
def article_list(request):
    articles = ArticlePost.objects.all()
    print(articles)
    context = {'articles': articles}
    return render(request, 'article/list.html', context)


def article_detail(request, id):
    article = ArticlePost.objects.get(id=id)
    context = {'article': article}
    return render(request, 'article/detail.html', context)
