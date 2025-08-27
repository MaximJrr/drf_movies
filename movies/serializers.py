from rest_framework import serializers

from movies.models import Movie, Genre, Review


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

    def validate_age_restriction(self, value):
        if value < 0 or value > 18:
            raise serializers.ValidationError("please specify age restriction from 0 to 18")


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Review
        fields = '__all__'
