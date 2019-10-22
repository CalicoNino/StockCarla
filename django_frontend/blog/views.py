from django.shortcuts import render
from django.http import HttpResponse

posts = [
    {
        'author': 'elninokr',
        'title': 'Blog Post 1',
        'content': 'First Post',
        'date_posted': 'October 22nd 2019'
    }
]

def home(request):
    context = { 'posts': posts, 'title': 'blog'}
    return render(request, 'blog/home.html', context)
    # return HttpResponse('<h1> Blog Home <h1>')

def about(request):
    context = { 'title': 'About' }
    return render(request, 'blog/about.html', context)
    # return HttpResponse('<h1> Blog about <h1>')
