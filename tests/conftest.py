# -*- coding: utf-8 -*-

from django_webtest import DjangoTestApp, WebTestMixin
import pytest

from testapp.articles.factories import AuthorFactory, ArticleFactory, TeamFactory


@pytest.fixture(scope='function')
def app(request):
    wtm = WebTestMixin()
    wtm._patch_settings()
    wtm._disable_csrf_checks()
    request.addfinalizer(wtm._unpatch_settings)
    return DjangoTestApp()


@pytest.fixture(scope='function')
def data(request):
    teams = [
        TeamFactory()
        for x in range(0, 2)
    ]
    authors = [
        AuthorFactory(team=team)
        for team in teams
        for x in range(0, 5)
    ]
    articles = [
        ArticleFactory(author=author)
        for author in authors
        for x in range(0, 10)
    ]
    return {
        'teams': teams,
        'authors': authors,
        'articles': articles,
    }
