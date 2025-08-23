from django.contrib import admin

from .models import Movie, Review, Genre, Actor, Director

admin.site.register(Movie)
admin.site.register(Review)
admin.site.register(Genre)
admin.site.register(Actor)
admin.site.register(Director)
