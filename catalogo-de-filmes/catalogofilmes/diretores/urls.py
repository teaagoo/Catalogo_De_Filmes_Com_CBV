from django.urls import path
from .views import (
    ListaDiretoresView, 
    DetalharDiretorView, 
    AdicionarDiretorView, 
    EditarDiretorView, 
    DeletarDiretorView
)

app_name = 'diretores'

urlpatterns = [
    path('', ListaDiretoresView.as_view(), name='lista_diretores'),
    path('adicionar/', AdicionarDiretorView.as_view(), name='adicionar_diretor'),
    path('<int:id>/', DetalharDiretorView.as_view(), name='detalhar_diretor'),
    path('<int:id>/editar/', EditarDiretorView.as_view(), name='editar_diretor'),
    path('<int:id>/deletar/', DeletarDiretorView.as_view(), name='deletar_diretor'),
]