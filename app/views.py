from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect, get_object_or_404
from .models import Movie, Movielist

# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return redirect('app:login')

    movies = Movie.objects.all()
    return render(request, 'app/index.html', {'movies': movies})

from django.contrib import messages

def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('app:index')
        else:
            messages.error(request, "❌ Wrong username or password")

    return render(request, 'app/login.html')

def logout_user(request):
    logout(request)
    return redirect('app:login')

def signup(request):
    if request.method == "POST":

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():

            User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            return redirect('app:login')

    return render(request, 'app/signup.html')


def movie(request, movie_id):
    movie = Movie.objects.get(uu_id=movie_id)

    return render(request,'app/movie.html',{'movie': movie})


def my_list(request):

    if not request.user.is_authenticated:
        return redirect('app:login')

    movies = Movielist.objects.filter(user=request.user)

    return render(request, 'app/my_list.html', {'movies': movies})

def search(request):

    query = request.GET.get('q')

    movies = Movie.objects.filter(title__icontains=query)
    
    return render(request,'app/search.html',
        {
            'movies': movies,
            'query': query
        }
    )


def genre(request, genre_name):

    movies = Movie.objects.filter(genre=genre_name)

    return render(request,'app/genre.html',
        {
            'movies': movies,
            'genre': genre_name
        }
    )


def add_to_list(request):
    if request.method == "POST":

        movie_id = request.POST.get('movie_id')

        # direct UUID safe handling
        movie = get_object_or_404(Movie, uu_id=movie_id)

        obj, created = Movielist.objects.get_or_create(user=request.user,movie=movie)

        if created:
            return JsonResponse({"message": "Added to My List"})
        else:
            return JsonResponse({"message": "Already in My List"})

def remove_from_list(request):
    if request.method == "POST":

        movie_id = request.POST.get('movie_id')
        movie = get_object_or_404(Movie, uu_id=movie_id)

        Movielist.objects.filter(user=request.user,movie=movie).delete()
        return redirect('app:my_list')
  