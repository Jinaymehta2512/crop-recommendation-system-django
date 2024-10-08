from django.urls import path
from .views import *

urlpatterns = [
    path('recommend/', recommend_crop, name='recommend_crop'),
    path('prediction/', crop_recommendation_page, name='crop_recommendation_page'),
]
