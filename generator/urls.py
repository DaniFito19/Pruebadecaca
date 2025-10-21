from django.urls import path
from . import views

urlpatterns = [
    # La dirección raíz ('/') mostrará la vista 'home'
    path('', views.home, name='home'),
    # La dirección '/crear/raza/' mostrará la vista 'elegir_raza'
    path('crear/raza/', views.elegir_raza, name='elegir_raza'),
]