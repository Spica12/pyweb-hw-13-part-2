from django.urls import path

from . import seed, seed_mongo, views

app_name = 'quoteapp'

urlpatterns = [
    path('', views.main, name='main'),
    path('tag/', views.tag, name='tag'),
    path('quote/', views.quote, name='quote'),
    path('author/', views.author, name='author'),
    path('detail/<author_fullanme>', views.detail, name='detail'),
    path('find_quotes_by_tag/<tag>', views.find_quotes_by_tag, name='find_quotes_by_tag'),
    path('delete_all_quotes/', views.delete_all_quotes, name='delete_all_quotes'),
    path('delete_all_authors/', views.delete_all_authors, name='delete_all_authors'),
    path('delete_all_tags/', views.delete_all_tags, name='delete_all_tags'),
    path('seed_authors/', seed.seed_authors, name='seed_authors'),
    path('seed_quotes/', seed.seed_quotes, name='seed_quotes'),
    path('seed_authors_mongo/', seed_mongo.seed_authors, name='seed_authors_mongo'),
    path('seed_quotes_mongo/', seed_mongo.seed_quotes, name='seed_quotes_mongo'),

]
