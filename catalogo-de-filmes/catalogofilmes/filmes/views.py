from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from .models import Filme
from .forms import FilmeForm

# Mixins para controlar acesso (substituindo decorators)
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.shortcuts import redirect

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.groups.filter(name='Administradores').exists()

    def handle_no_permission(self):
        return redirect('login')


class UserRequiredMixin(LoginRequiredMixin):
    login_url = 'login'


class IndexView(TemplateView):
    template_name = 'filmes/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from genero.models import Genero
        from diretores.models import Diretor
        from favoritos.models import ListaFavoritos

        context['generos'] = Genero.objects.prefetch_related('filmes').order_by('nome')
        context['diretores_destaque'] = Diretor.objects.all().order_by('nome')[:5]

        if self.request.user.is_authenticated:
            listas_usuario = ListaFavoritos.objects.filter(usuario=self.request.user)
            filmes_favoritos_ids = set()
            for lista in listas_usuario:
                filmes_favoritos_ids.update(lista.filmes.values_list('id', flat=True))
            context['filmes_favoritos'] = Filme.objects.filter(id__in=filmes_favoritos_ids)
        else:
            context['filmes_favoritos'] = []
        return context


class FilmeCreateView(AdminRequiredMixin, CreateView):
    model = Filme
    form_class = FilmeForm
    template_name = 'filmes/adicionar_filmes.html'
    success_url = reverse_lazy('index')


class FilmeUpdateView(AdminRequiredMixin, UpdateView):
    model = Filme
    form_class = FilmeForm
    template_name = 'filmes/edit_filmes.html'
    success_url = reverse_lazy('index')
    pk_url_kwarg = 'id'


class FilmeDeleteView(AdminRequiredMixin, DeleteView):
    model = Filme
    template_name = 'filmes/confirmar_delete.html'  # cria esse template ou altera pra redirect direto
    success_url = reverse_lazy('index')
    pk_url_kwarg = 'id'


class FilmeDetailView(UserRequiredMixin, DetailView):
    model = Filme
    template_name = 'filmes/detalhes_filme.html'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_is_admin'] = self.request.user.groups.filter(name='Administradores').exists() if self.request.user.is_authenticated else False
        return context
