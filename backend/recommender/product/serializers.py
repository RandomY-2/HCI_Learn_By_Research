from rest_framework import serializers
from .models import Movie, MovieDescription

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

class MovieDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieDescription
        fields = '__all__'

