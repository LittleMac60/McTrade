from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('au/create/', views.au_create_search_results, name='au_create_search_results'),
    path('us/create/', views.us_create_search_results, name='us_create_search_results'),
    path('uk/create/', views.uk_create_search_results, name='uk_create_search_results'),
    path('au/delete/', views.au_delete_search_results, name='au_delete_search_results'),
    path('us/delete/', views.us_delete_search_results, name='us_delete_search_results'),
    path('uk/delete/', views.uk_delete_search_results, name='uk_delete_search_results'),
    path('au/delete/files', views.au_delete_search_results_files, name='au_delete_search_results_files'),
]
