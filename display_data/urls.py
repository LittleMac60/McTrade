from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('stocks/view', views.stock_search_view, name='stock_search_view'),
    path('stocks/', views.stock_list, name='stock_list'),
    path('stocks/export/', views.export_stocks_csv, name='export_stocks_csv'),
    path('stocks/pivot/', views.stock_pivot_view, name='stock_pivot'),
    path('stocks/pivot/export/', views.export_stocks_pivot_csv, name='export_stocks_pivot_csv'),
]
