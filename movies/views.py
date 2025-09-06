from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Movie, Genre, Review
from .permissions import IsSuperUserOrReadOnly, IsOwnerOrAdmin
from rest_framework.permissions import IsAuthenticated
from .serializers import MovieSerializer, GenreSerializer, ReviewSerializer


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

    @action(detail=False, methods=['get'])
    def age_restriction(self, request):
        age = request.query_params.get('age')

        if not age:
            return Response({"error": "age query parameter is required"}, status=400)

        movies = Movie.objects.filter(age_restriction=age)

        if not movies.exists():
            return Response({"error": "no movies found for this age"}, status=404)

        serializer = self.get_serializer(movies, many=True)

        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        movie = self.get_object()
        reviews = Review.objects.filter(movie=movie)
        serializer = ReviewSerializer(reviews, many=True)

        return Response(serializer.data)

    @extend_schema(
        request=ReviewSerializer,
        responses=ReviewSerializer,
    )
    @action(detail=True, methods=['post'])
    def add_review(self, request, pk=None):
        movie = self.get_object()
        serializer = ReviewSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save(user=request.user, movie=movie)
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)


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


class ReviewsViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrAdmin)

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)
