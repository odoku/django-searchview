# -*- coding: utf-8 -*-

from django.conf.urls import url


urlpatterns = [
    url(r'^$', 'testapp.articles.views.index', name='index'),
]
