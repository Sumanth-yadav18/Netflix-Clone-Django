from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),

    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('signup/', views.signup, name='signup'),

    path('movie/<uuid:movie_id>/',views.movie,name='movie'),
    path('my_list/',views.my_list,name='my_list'),
    path('search/',views.search,name='search'),
    path('genre/<str:genre_name>/',views.genre,name='genre'),
    path('add_to_list/',views.add_to_list,name='add_to_list'),
    path('remove_from_list/', views.remove_from_list, name='remove_from_list'),

]