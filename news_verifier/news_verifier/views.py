# news_verifier/views.py
from django.shortcuts import render
from .utils import fetch_news

def news_view(request):
    articles = fetch_news()
    return render(request, 'news_view.html', {'articles': articles})
