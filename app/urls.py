# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from app import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('profile/<int:uid>', views.profile, name='profile'),
    path('rule/<str:v>', views.rule, name='rules'),
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
