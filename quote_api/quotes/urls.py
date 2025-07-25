from django.urls import path
from . import views

urlpatterns = [
    path('quote/', views.get_random_quote, name='random_quote'),
]