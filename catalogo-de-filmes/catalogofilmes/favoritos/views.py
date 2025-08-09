from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages

from .models import ListaFavoritos
from .forms import ListaFavoritosForm
from filmes.models import Filme


class MinhasListasView(LoginRequiredMixin, ListView):
    model = ListaFavoritos
    template_name = 'favoritos/minhas_listas.html'
    context_object_name = 'listas'

    def get_queryset(self):
        return ListaFavoritos.objects.filter(usuario=self.request.user).order_by('nome')


class CriarListaView(LoginRequiredMixin, CreateView):
    model = ListaFavoritos
    form_class = ListaFavoritosForm
    template_name = 'favoritos/criar_lista.html'

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('favoritos:detalhes_lista', kwargs={'lista_id': self.object.id})


class DetalhesListaView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = ListaFavoritos
    template_name = 'favoritos/detalhes_lista.html'
    pk_url_kwarg = 'lista_id'
    context_object_name = 'lista'

    def test_func(self):
        lista = self.get_object()
        return lista.usuario == self.request.user

    def handle_no_permission(self):
        return redirect('favoritos:minhas_listas')


class EditarListaView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ListaFavoritos
    form_class = ListaFavoritosForm
    template_name = 'favoritos/editar_lista.html'
    pk_url_kwarg = 'lista_id'

    def test_func(self):
        lista = self.get_object()
        return lista.usuario == self.request.user

    def handle_no_permission(self):
        return redirect('favoritos:minhas_listas')

    def get_success_url(self):
        return reverse_lazy('favoritos:detalhes_lista', kwargs={'lista_id': self.object.id})


class DeletarListaView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ListaFavoritos
    template_name = 'favoritos/confirmar_delete_lista.html'
    pk_url_kwarg = 'lista_id'
    success_url = reverse_lazy('favoritos:minhas_listas')

    def test_func(self):
        lista = self.get_object()
        return lista.usuario == self.request.user

    def handle_no_permission(self):
        return redirect('favoritos:minhas_listas')


class AdicionarAosFavoritosView(LoginRequiredMixin, View):
    def post(self, request, filme_id):
        filme = get_object_or_404(Filme, id=filme_id)
        listas_usuario = ListaFavoritos.objects.filter(usuario=request.user)

        lista_id = request.POST.get('lista_id')
        lista = get_object_or_404(ListaFavoritos, id=lista_id, usuario=request.user)

        if filme in lista.filmes.all():
            return JsonResponse({
                'success': False,
                'message': f'O filme "{filme.titulo}" já está na lista "{lista.nome}"!'
            })
        else:
            lista.filmes.add(filme)
            return JsonResponse({
                'success': True,
                'message': f'Filme "{filme.titulo}" adicionado à lista "{lista.nome}" com sucesso!'
            })

    def get(self, request, filme_id):
        filme = get_object_or_404(Filme, id=filme_id)
        listas_usuario = ListaFavoritos.objects.filter(usuario=request.user)

        if listas_usuario.count() == 0:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': 'Você precisa criar uma lista de favoritos primeiro.',
                    'redirect_criar_lista': True
                })
            else:
                messages.info(request, 'Você precisa criar uma lista de favoritos primeiro.')
                return redirect('favoritos:criar_lista')

        elif listas_usuario.count() == 1:
            lista = listas_usuario.first()
            if filme in lista.filmes.all():
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False,
                        'message': f'O filme "{filme.titulo}" já está na sua lista de favoritos!'
                    })
                else:
                    messages.warning(request, f'O filme "{filme.titulo}" já está na sua lista de favoritos!')
                    return redirect('detalhes_filme', id=filme.id)
            else:
                lista.filmes.add(filme)
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': True,
                        'message': f'Filme "{filme.titulo}" adicionado aos favoritos!'
                    })
                else:
                    messages.success(request, f'Filme "{filme.titulo}" adicionado aos favoritos!')
                    return redirect('detalhes_filme', id=filme.id)

        else:
            listas_data = [{
                'id': lista.id,
                'nome': lista.nome,
                'total_filmes': lista.filmes.count(),
                'filme_ja_na_lista': filme in lista.filmes.all()
            } for lista in listas_usuario]

            return JsonResponse({
                'listas': listas_data,
                'filme_titulo': filme.titulo
            })