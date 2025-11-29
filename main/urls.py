# main/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('about/', views.about, name='about'),
    path('solutions/', views.solutions, name='solutions'),
    path('portfolio/', views.portfolio_view, name='portfolio'),
    path('portfolio/<slug:slug>/', views.portfolio_detail_view, name='portfolio_detail'),
    path('contact/', views.contact_view, name='contact'),
]