# -*- coding: utf-8 -*-

from searchview import SearchView

from .models import Article


class IndexView(SearchView):
    model = Article
    fields = ('author', 'title', 'body')
    keyword_fields = ('body',)
    order_fields = ('author', 'title')


index = IndexView.as_view()
