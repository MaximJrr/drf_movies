from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    description = models.TextField(null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)
    budget = models.IntegerField(null=True, blank=True)
    age_restriction = models.IntegerField(null=True, blank=True)
    genre = models.ForeignKey("Genre", on_delete=models.SET_NULL, null=True)
    actors = models.ManyToManyField("Actor", related_name="movies")
    director = models.ForeignKey("Director", on_delete=models.SET_NULL, null=True,  related_name="movies")

    def __str__(self):
        return self.title


class Genre(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Review(models.Model):
    comment = models.TextField()
    rating = models.DecimalField(max_digits=2, decimal_places=1, validators=[MinValueValidator(0.0), MaxValueValidator(10.0)])
    created_at = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey("Movie", on_delete=models.CASCADE)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)

    def __str__(self):
        return f"Review by {self.user} on {self.movie} - {self.rating}/10"


class Actor(models.Model):
    name = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Actor - {self.name}"


class Director(models.Model):
    name = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Director - {self.name}"
