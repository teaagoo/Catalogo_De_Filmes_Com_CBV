from django.urls import path
from .views import GeneroListView, GeneroCreateView, GeneroUpdateView, GeneroDeleteView

app_name = 'genero'

urlpatterns = [
    path('', GeneroListView.as_view(), name='listar_generos'),
    path('novo/', GeneroCreateView.as_view(), name='criar_genero'),
    path('editar/<int:pk>/', GeneroUpdateView.as_view(), name='editar_genero'),
    path('deletar/<int:pk>/', GeneroDeleteView.as_view(), name='deletar_genero'),
]