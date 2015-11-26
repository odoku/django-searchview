# -*- coding: utf-8 -*-

from django import forms

from searchview import SearchForm

from .models import Article


class ArticleSearchForm(SearchForm):
    hoge = forms.CharField(label='Hoge')

    class Meta:
        model = Article
        fields = (
            ('author__team', {'as': 'team'}),
            ('author__name', {'as': 'author_name'}),
            ('title', {'lookup': 'contains'}),
        )
        order_fields = ('author__team', 'author__name', 'title',)
        keyword_fields = ('author__team__name', 'author__name', 'title', 'body',)
