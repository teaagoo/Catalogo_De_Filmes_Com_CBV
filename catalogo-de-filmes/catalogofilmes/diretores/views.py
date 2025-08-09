from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from .models import Diretor
from .forms import DiretorForm
from usuarios.decorators import admin_required, user_required


@method_decorator(user_required, name='dispatch')
class ListaDiretoresView(ListView):
    model = Diretor
    template_name = 'diretores/lista_diretores.html'
    context_object_name = 'diretores'
    ordering = ['nome']


@method_decorator(user_required, name='dispatch')
class DetalharDiretorView(DetailView):
    model = Diretor
    template_name = 'diretores/detalhes_diretor.html'
    pk_url_kwarg = 'id'  # Aqui você fala que o parâmetro da URL é 'id'
    context_object_name = 'diretor'


@method_decorator(admin_required, name='dispatch')
class AdicionarDiretorView(CreateView):
    model = Diretor
    form_class = DiretorForm
    template_name = 'diretores/adicionar_diretor.html'
    success_url = reverse_lazy('diretores:lista_diretores')


@method_decorator(admin_required, name='dispatch')
class EditarDiretorView(UpdateView):
    model = Diretor
    form_class = DiretorForm
    template_name = 'diretores/editar_diretor.html'
    pk_url_kwarg = 'id'

    def get_success_url(self):
        return reverse_lazy('diretores:detalhar_diretor', kwargs={'id': self.object.id})


@method_decorator(admin_required, name='dispatch')
class DeletarDiretorView(DeleteView):
    model = Diretor
    template_name = 'diretores/deletar_diretor.html'  # Se quiser confirmação antes de deletar
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('diretores:lista_diretores')