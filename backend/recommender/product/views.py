from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Movie, MovieDescription
from .serializers import MovieSerializer, MovieDescriptionSerializer

from django.core import serializers
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from bs4 import BeautifulSoup
import requests
import time
import os

movie_data = pd.read_csv('movie_dataset.csv')
features = ['keywords', 'cast', 'genres', 'director']

for feature in features:
  movie_data[feature] = movie_data[feature].fillna('')

movie_data['combine_sentence'] = movie_data['keywords'] + ' ' + movie_data['cast'] + ' ' + movie_data['genres'] + ' ' + movie_data['director']

cv = CountVectorizer()
count_matrix = cv.fit_transform(movie_data['combine_sentence'])

cosine_sim = cosine_similarity(count_matrix)

def get_title_from_index(df, index):
	return df[df.index == index]["title"].values[0]

def get_index_from_title(df, title):
	return df[df.title.str.lower() == title]["index"].values[0]

def get_zhihu_urls(movie):
    response = requests.get('https://www.google.com/search?q=' + movie + '+site%3Azhihu.com&oq=' + movie + '+site%3Azhihu.com&aqs=chrome..69i57.6845j0j7&sourceid=chrome&ie=UTF-8').text
    soup = BeautifulSoup(response, 'lxml')

    zhihu_urls = []
    for a in soup.find_all('a', href=True):
        if ('zhihu.com/question/' in a['href']) and \
           ('img' not in a['href']) and \
           ('answer' not in a['href']):
            zhihu_url = a['href'][7:].partition('&sa')[0]
            zhihu_urls.append(zhihu_url)

    return zhihu_urls

def get_zhihu_question_answers(zhihu_question_id, answer_list):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    }

    answer_api = 'https://www.zhihu.com/api/v4/questions/' + zhihu_question_id + '/answers?include=content&limit=5&offset=5&platform=desktop&sort_by=default'

    response = requests.get(answer_api, headers=headers)

    if len(response.json()['data']) == 0:
        return

    for answer in response.json()['data']:
        answer_list.append(answer['content'])


class MovieViewSet(viewsets.ViewSet):
    # get recommended movies
    def request_recommendations(self, request):
        input_movie_name = request.data['movie'].lower()
        movie_index = get_index_from_title(movie_data, input_movie_name)

        similar_movies = list(enumerate(cosine_sim[movie_index]))
        sorted_list = sorted(similar_movies, key=lambda x: x[1], reverse=True)

        i = 0
        movie_recommendations = []
        for movie in sorted_list:
            if get_title_from_index(movie_data, movie[0]).lower() != input_movie_name:
                movie_recommendations.append(get_title_from_index(movie_data, movie[0]))
            i = i + 1
            if i > 10:
                break

        response = {}
        response['recommended_movies'] = movie_recommendations
        return Response(response)


class MovieDescriptionViewSet(viewsets.ViewSet):
    # get movie descriptions
    def request_movie_descriptions(self, request):
        input_movie_name = request.data['movie']
        zhihu_urls = get_zhihu_urls(input_movie_name)

        answer_list = []
        for url in zhihu_urls:
            qid = url.partition('/question/')[2]
            get_zhihu_question_answers(qid, answer_list)

        response = {}
        response['movie_descriptions'] = answer_list
        return Response(response)
