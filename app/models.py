from django.db import models

from django.contrib.auth.models import User
import uuid
# Create your models here.

class Genre(models.TextChoices):
    ACTION = "action", "Action"
    COMEDY = "comedy", "Comedy"
    DRAMA = "drama", "Drama"
    HORROR = "horror", "Horror"
    ROMANCE = "romance", "Romance"
    THRILLER = "thriller", "Thriller"


class Movie(models.Model):
    uu_id = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    genre = models.CharField(max_length=20,choices=Genre.choices)
    image_card = models.ImageField(upload_to='movie/cards/')
    image_cover = models.ImageField(upload_to='movie/covers/')
    video = models.FileField(upload_to='movie/videos/')
    release_date = models.DateField()
    length = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Movielist(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'movie')

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"