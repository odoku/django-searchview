# -*- coding: utf-8 -*-

from collections import OrderedDict

from django import forms
from django.core.exceptions import NON_FIELD_ERRORS
from django.utils import six

from searchview.forms import searchform_factory, SearchFormOptions
from searchview.forms import get_form_field, get_model_field

from testapp.articles.forms import ArticleSearchForm
from testapp.articles.models import Author, Article


class TestGetModelField(object):
    def test_get_field(self):
        field = get_model_field(Article, 'title')
        assert field.name == 'title'
        assert field == Article._meta.get_field('title')

    def test_get_related_field(self):
        field = get_model_field(Article, 'author__name')
        assert field.name == 'name'
        assert field == Author._meta.get_field('name')


class TestGetFormField(object):
    def test_get_field(self):
        field = get_form_field(Article, 'title')
        assert isinstance(field, forms.CharField)

    def test_get_related_field(self):
        field = get_form_field(Article, 'author__name')
        assert isinstance(field, forms.CharField)

    def test_get_with_widget(self):
        field = get_form_field(Article, 'title', widget=forms.Textarea)
        assert isinstance(field.widget, forms.Textarea)

    def test_get_with_label(self):
        field = get_form_field(Article, 'title', label='foo')
        assert field.label == 'foo'

    def test_get_with_help_text(self):
        field = get_form_field(Article, 'title', help_text='foo')
        assert field.help_text == 'foo'


class TestSearchFormOptions(object):
    def test_create_instance(self):
        class Meta:
            model = Article
            fields = (
                'author__team__name',
                'author__name',
                'title',
            )
            order_fields = ('author__team', 'author__name', 'title',)
            order_field_name = 'sort_condition'
            keyword_fields = ('author__team__name', 'author__name', 'title', 'body',)
            keyword_field_name = 'keyword_text'
            widgets = {
                'author__team__name': forms.Textarea,
                'author__name': forms.Textarea,
                'title': forms.Textarea,
            }
            labels = {
                'author__team__name': 'team name',
                'author__name': 'author name',
                'title': 'article title',
            }
            help_texts = {
                'author__team__name': 'team name help text',
                'author__name': 'author name help text',
                'title': 'article title help text',
            }
            error_messages = {
                NON_FIELD_ERRORS: {
                    'unique_together': "%(model_name)s's %(field_labels)s are not unique.",
                }
            }

        options = SearchFormOptions(Meta)
        assert options
        assert isinstance(options.fields, OrderedDict)
        assert options.order_fields == Meta.order_fields
        assert options.order_field_name == Meta.order_field_name
        assert options.keyword_fields == Meta.keyword_fields
        assert options.keyword_field_name == Meta.keyword_field_name
        assert options.widgets == Meta.widgets
        assert options.labels == Meta.labels
        assert options.help_texts == Meta.help_texts
        assert options.error_messages == Meta.error_messages
        assert isinstance(options.lookups, dict)
        assert isinstance(options.aliases, dict)

        for field, opts in six.iteritems(options.fields):
            assert isinstance(field, six.string_types)
            assert isinstance(opts, dict)
            assert opts['lookup'] is None
            assert opts['as'] is None
            assert options.lookups[field] == opts['lookup']
            assert options.aliases[field] == opts['as']

    def test_get_aliase(self):
        class Meta:
            model = Article
            fields = (
                ('author__team__name', {'as': 'team_name'}),
                'title',
            )

        options = SearchFormOptions(Meta)
        assert options.get_aliase('author__team__name') == 'team_name'
        assert options.get_aliase('title') == 'title'

    def test_get_lookup(self):
        class Meta:
            model = Article
            fields = (
                ('author__team__name', {'lookup': 'contain'}),
                'title',
            )

        options = SearchFormOptions(Meta)
        assert options.get_lookup('author__team__name') == 'contain'
        assert options.get_lookup('title') == ''


class TestSearchForm(object):
    def test_create_instance(self):
        form = ArticleSearchForm()
        assert form

        assert isinstance(form._meta, SearchFormOptions)

        assert 'author__team' in form._meta.fields
        assert 'author__name' in form._meta.fields
        assert 'title' in form._meta.fields

        assert 'author__team' in form._meta.order_fields
        assert 'author__name' in form._meta.order_fields
        assert 'title' in form._meta.order_fields

        assert 'author__team__name' in form._meta.keyword_fields
        assert 'author__name' in form._meta.keyword_fields
        assert 'title' in form._meta.keyword_fields
        assert 'body' in form._meta.keyword_fields

        assert 'team' in form.fields
        assert 'author_name' in form.fields
        assert 'title' in form.fields
        assert form._meta.keyword_field_name in form.fields
        assert form._meta.order_field_name in form.fields
        assert 'hoge' in form.fields


class TestSearchFormFactory(object):
    def test_create(self):
        model = Article
        fields = (
            ('author__team', {'as': 'team'}),
            ('author__name', {'as': 'author_name'}),
            ('title', {'lookup': 'contains'}),
        )
        order_fields = ('author__team', 'author__name', 'title',)
        order_field_name = 'sort_condition'
        keyword_fields = ('author__team__name', 'author__name', 'title', 'body',)
        keyword_field_name = 'keyword_text'
        widgets = {
            'author__name': forms.Textarea,
            'title': forms.Textarea,
        }
        labels = {
            'author__team': 'team',
            'author__name': 'author name',
            'title': 'article title',
        }
        help_texts = {
            'author__team': 'team help text',
            'author__name': 'author name help text',
            'title': 'article title help text',
        }
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "%(model_name)s's %(field_labels)s are not unique.",
            }
        }
        form_class = searchform_factory(
            model, fields,
            keyword_fields=keyword_fields, keyword_field_name=keyword_field_name,
            order_fields=order_fields, order_field_name=order_field_name,
            widgets=widgets, labels=labels,
            help_texts=help_texts, error_messages=error_messages
        )
        assert form_class
        form = form_class()

        assert isinstance(form._meta, SearchFormOptions)

        assert 'author__team' in form._meta.fields
        assert 'author__name' in form._meta.fields
        assert 'title' in form._meta.fields

        assert 'author__team' in form._meta.order_fields
        assert 'author__name' in form._meta.order_fields
        assert 'title' in form._meta.order_fields

        assert 'author__team__name' in form._meta.keyword_fields
        assert 'author__name' in form._meta.keyword_fields
        assert 'title' in form._meta.keyword_fields
        assert 'body' in form._meta.keyword_fields

        assert 'team' in form.fields
        assert 'author_name' in form.fields
        assert 'title' in form.fields
        assert form._meta.keyword_field_name in form.fields
        assert form._meta.order_field_name in form.fields
