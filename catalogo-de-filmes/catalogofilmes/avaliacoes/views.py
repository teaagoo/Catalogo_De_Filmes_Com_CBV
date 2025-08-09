from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Avaliacao
from .forms import AvaliacaoForm
from filmes.models import Filme

class AvaliacaoOwnerMixin(UserPassesTestMixin):
    def test_func(self):
        avaliacao = self.get_object()
        return avaliacao.usuario == self.request.user

    def handle_no_permission(self):
        filme_id = self.get_object().filme.id
        return redirect('detalhes_filme', id=filme_id)


class AdicionarAvaliacaoView(LoginRequiredMixin, CreateView):
    model = Avaliacao
    form_class = AvaliacaoForm
    template_name = 'avaliacoes/adicionar_avaliacao.html'

    def dispatch(self, request, *args, **kwargs):
        self.filme = get_object_or_404(Filme, pk=kwargs['filme_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        form.instance.filme = self.filme
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['filme'] = self.filme
        return ctx

    def get_success_url(self):
        return reverse('detalhes_filme', kwargs={'id': self.filme.id})


class EditarAvaliacaoView(LoginRequiredMixin, AvaliacaoOwnerMixin, UpdateView):
    model = Avaliacao
    form_class = AvaliacaoForm
    template_name = 'avaliacoes/editar_avaliacao.html'
    pk_url_kwarg = 'avaliacao_id'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['filme'] = self.object.filme
        ctx['editar'] = True
        return ctx

    def get_success_url(self):
        return reverse('detalhes_filme', kwargs={'id': self.object.filme.id})


class DeletarAvaliacaoView(LoginRequiredMixin, AvaliacaoOwnerMixin, DeleteView):
    model = Avaliacao
    template_name = 'avaliacoes/deletar_avaliacao.html'  # Se quiser tela de confirmação
    pk_url_kwarg = 'avaliacao_id'

    def get_success_url(self):
        return reverse('detalhes_filme', kwargs={'id': self.object.filme.id})