from django.urls import path
from .views import MovieViewSet, MovieDescriptionViewSet

urlpatterns = [
    path('movie_suggestions', MovieViewSet.as_view({
        'post': 'request_recommendations',
    })),
    path('movie_descriptions', MovieDescriptionViewSet.as_view({
        'post': 'request_movie_descriptions',
    }))
]
