from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('au/mom/', views.au_mom_dashboard, name='au_mom_dashboard'),
]