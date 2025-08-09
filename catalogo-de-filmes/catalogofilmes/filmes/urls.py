from django.urls import path
from .views import IndexView, FilmeCreateView, FilmeUpdateView, FilmeDeleteView, FilmeDetailView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('adicionar/', FilmeCreateView.as_view(), name='adicionar_filme'),
    path('editar/<int:pk>/', FilmeUpdateView.as_view(), name='editar_filme'),
    path('deletar/<int:pk>/', FilmeDeleteView.as_view(), name='deletar_filme'),
    path('detalhes/<int:pk>/', FilmeDetailView.as_view(), name='detalhar_filme'),
]

