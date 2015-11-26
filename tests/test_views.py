# -*- coding: utf-8 -*-

import pytest

from django.core.urlresolvers import reverse

from testapp.articles.models import Article


@pytest.mark.django_db
class TestArticleSearchView(object):
    def test_access(self, app, data):
        response = app.get(reverse('articles:index'))
        assert response.status_code == 200
        assert len(response.context['object_list']) == len(data['articles'])

    def test_search_author(self, app, data):
        response = app.get(reverse('articles:index'), {
            'author': data['authors'][2].pk,
        })
        assert response.status_code == 200

        articles = Article.objects.filter(author=data['authors'][2])
        assert len(response.context['object_list']) == articles.count()

    def test_search_title(self, app, data):
        article = data['articles'][10]
        response = app.get(reverse('articles:index'), {
            'title': article.title,
        })
        assert response.status_code == 200

        assert len(response.context['object_list']) == 1
        assert response.context['object_list'][0].title == article.title

    def test_search_keyword(self, app, data):
        keyword = 'abc'
        response = app.get(reverse('articles:index'), {
            'keyword': keyword,
        })
        assert response.status_code == 200

        articles = Article.objects.filter(body__contains=keyword)
        assert len(response.context['object_list']) == articles.count()

    def test_order_author_asc(self, app, data):
        response = app.get(reverse('articles:index'), {
            'order': 'author',
        })
        assert response.status_code == 200

        articles = Article.objects.order_by('author')
        assert len(response.context['object_list']) == articles.count()

        for a, b in zip(response.context['object_list'], articles):
            assert a.author_id == b.author_id

    def test_order_author_desc(self, app, data):
        response = app.get(reverse('articles:index'), {
            'order': '-author',
        })
        assert response.status_code == 200

        articles = Article.objects.order_by('-author')
        assert len(response.context['object_list']) == len(articles)

        for a, b in zip(response.context['object_list'], articles):
            assert a.author_id == b.author_id
