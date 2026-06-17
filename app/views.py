from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from .models import Movie, Movielist
import re
from django.contrib import messages

# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return redirect('app:login')

    movies = Movie.objects.all()
    return render(request, 'app/index.html', {'movies': movies})

from django.contrib import messages

def login_user(request):
    if request.method == "POST":

        # LOGIN
        if "login" in request.POST:
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('app:index')
            else:
                messages.error(request, "❌ Wrong username or password")

        # FORGOT PASSWORD 
        elif "reset" in request.POST:
            email = request.POST.get("email", "").strip().lower()

            try:
                user = User.objects.get(email=email)
                request.session["reset_user"] = user.username
                messages.success(request, "Now set your new password below")
            except User.DoesNotExist:
                messages.error(request, "Email not found")
                request.session.pop("reset_user", None)

        # UPDATE PASSWORD
        elif "update_password" in request.POST:
            username = request.session.get("reset_user")
            new_password = request.POST.get("new_password")

            if username and new_password:
                user = User.objects.get(username=username)
                user.set_password(new_password)
                user.save()

                request.session.pop("reset_user", None)

                messages.success(request, "Password updated successfully")

    return render(request, 'app/login.html')

def logout_user(request):
    logout(request)
    return redirect('app:login')

def signup(request):
    if request.method == "POST":

        username = request.POST.get('username').strip()
        email = request.POST.get('email').strip().lower()
        password = request.POST.get('password').strip()

        # 🚨 MUST BE HERE (BEFORE USING IT)
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        if not username or not email or not password:
            messages.error(request, "All fields are required")
            return redirect('app:signup')

        if not re.fullmatch(email_pattern, email):
            messages.error(request, "Invalid email format")
            return redirect('app:signup')

        domain = email.split("@")[-1]

        valid_tlds = ["com", "in", "org", "net", "edu", "co", "io", "ai"]

        if domain.split(".")[-1] not in valid_tlds:
            messages.error(request, "Invalid email domain")
            return redirect('app:signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('app:signup')

        if User.objects.filter(email__iexact=email).exists():
            messages.error(request, "Email already exists")
            return redirect('app:signup')

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(request, "Account created successfully")
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

def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email").strip().lower()

        try:
            user = User.objects.get(email=email)
            return redirect('app:reset_password', username=user.username)
        except User.DoesNotExist:
            messages.error(request, "No account found with this email")
            return redirect('app:forgot_password')

    return render(request, "app/forgot_password.html")

def reset_password(request, username):
    user = User.objects.get(username=username)

    if request.method == "POST":
        password = request.POST.get("password")

        if len(password) < 6:
            messages.error(request, "Password too short")
            return redirect('app:reset_password', username=username)

        user.set_password(password)
        user.save()

        messages.success(request, "Password updated successfully")
        return redirect('app:login')

    return render(request, "app/reset_password.html", {"username": username})