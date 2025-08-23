from rest_framework import viewsets
from .models import Movie
from .permissions import IsSuperUserOrReadOnly
from .serializers import MovieSerializer


class MoviesViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = (IsSuperUserOrReadOnly,)
