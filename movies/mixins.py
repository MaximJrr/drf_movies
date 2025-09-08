from rest_framework.decorators import action
from rest_framework.response import Response

from movies.serializers import MovieShortSerializer


class RelatedMoviesMixin:
    @action(detail=True, methods=['get'])
    def movies(self, request, pk):
        instance = self.get_object()
        movies = instance.movies.all()

        if not movies.exists():
            return Response([], status=200)

        serializer = MovieShortSerializer(movies, many=True)

        return Response(serializer.data)