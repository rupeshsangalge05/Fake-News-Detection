from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
import requests
from bs4 import BeautifulSoup
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.hashers import make_password



def signup(request):
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.')
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already registered.')
            return redirect('signup')

        # Create the user
        user = User(username=username, email=email, password1=make_password(password1))
        user.save()

        messages.success(request, 'Account created successfully!')
        return redirect('login')
    
    return render(request, 'signup.html')


def user_login(request):
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'You are now logged in!')
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')
    
    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')

# Your NewsAPI key (replace 'your_newsapi_key_here' with your actual key)
NEWS_API_KEY = 'your_newsapi_key_here'


def fetch_news():
    """
    Fetches the latest news articles from the NewsAPI.
    """
    url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        articles = data.get('articles', [])
        return articles
    else:
        return []



def verify_news(news_query):
    """
    Simulates verifying a news article by performing a Google search.
    """
    search_url = f"https://www.google.com/search?q={news_query.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all the snippets and titles in the search results
    results = [g.get_text() for g in soup.find_all('div', class_='BNeawe s3v9rd AP7Wnd')]

    # Simple logic to determine if the news is real or fake based on search results
    if any(keyword in result.lower() for keyword in ["verified", "reliable", "fact-check", "news", "source"] for result in results):
        verdict = "Real"
    else:
        verdict = "Fake"
    
    return verdict, results



def index(request):
    return render(request, 'index.html')




def about(request):
    return render(request, 'about.html')



def check_news(request):
    if request.method == 'POST':
        news_query = request.POST.get('news', '')
        if news_query:
            verdict, results = verify_news(news_query)
            return render(request, 'result.html', {
                'news_query': news_query,
                'verdict': verdict,
                'results': results
            })
        else:
            return redirect(reverse('check_news'))
    
    return render(request, 'check_news.html')




def contact(request):
    if request.method == 'POST':
        # Handle contact form submission here
        return render(request, 'contact.html', {
            'message': "Thank you for your message. We'll get back to you soon."
        })

    return render(request, 'contact.html')

