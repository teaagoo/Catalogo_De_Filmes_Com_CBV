from django.urls import path
from .views import AdicionarAvaliacaoView, EditarAvaliacaoView, DeletarAvaliacaoView

urlpatterns = [
    path('filme/<int:filme_id>/avaliar/', AdicionarAvaliacaoView.as_view(), name='adicionar_avaliacao'),
    path('avaliacao/<int:avaliacao_id>/editar/', EditarAvaliacaoView.as_view(), name='editar_avaliacao'),
    path('avaliacao/<int:avaliacao_id>/deletar/', DeletarAvaliacaoView.as_view(), name='deletar_avaliacao'),
]