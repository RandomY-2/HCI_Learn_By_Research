from django.db import models
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from bs4 import BeautifulSoup
import requests
import time
import os

