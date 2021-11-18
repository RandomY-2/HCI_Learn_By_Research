from django.db import models

class Movie(models.Model):
    movie_name = models.CharField(max_length=200)

class MovieDescription(models.Model):
    movie_description = models.CharField(max_length=200)


