from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Movie, Genre
from .permissions import IsSuperUserOrReadOnly
from .serializers import MovieSerializer, GenreSerializer


class MoviesViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = (IsSuperUserOrReadOnly,)

    @action(detail=False, methods=['get'])
    def year_release(self, request):
        year = request.query_params.get('year')

        if not year:
            return Response({"error": "year query parameter is required"}, status=400)

        movies = Movie.objects.filter(release_date__year=year)

        if not movies.exists():
            return Response({"error": "no movies found for this year"}, status=404)

        serializer = self.get_serializer(movies, many=True)

        return Response(serializer.data)



class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    @action(detail=True, methods=['get'])
    def movies(self, request, pk):
        movies = Movie.objects.filter(genre=pk)

        if not movies.exists():
            return Response({"error": "no movies found for this genre"}, status=404)


        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)
