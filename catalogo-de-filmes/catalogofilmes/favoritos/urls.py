from django.urls import path
from . import views

app_name = 'favoritos'

urlpatterns = [
    path('', views.MinhasListasView.as_view(), name='minhas_listas'),
    path('criar/', views.CriarListaView.as_view(), name='criar_lista'),
    path('<int:lista_id>/', views.DetalhesListaView.as_view(), name='detalhes_lista'),
    path('<int:lista_id>/editar/', views.EditarListaView.as_view(), name='editar_lista'),
    path('<int:lista_id>/deletar/', views.DeletarListaView.as_view(), name='deletar_lista'),
    path('adicionar/<int:filme_id>/', views.AdicionarAosFavoritosView.as_view(), name='adicionar_aos_favoritos'),
]