from django.shortcuts import get_object_or_404, render
from .models import Filme
from .forms import FilmeForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from usuarios.decorators import admin_required, user_required
from genero.models import Genero
from diretores.models import Diretor
from favoritos.models import ListaFavoritos

def index(request):
    """Página inicial acessível a todos os usuários"""
    generos = Genero.objects.prefetch_related('filmes').order_by('nome')
    diretores_destaque = Diretor.objects.all().order_by('nome')[:5]

    if request.user.is_authenticated:
        listas_usuario = ListaFavoritos.objects.filter(usuario=request.user)
        filmes_favoritos_ids = set()
        for lista in listas_usuario:
            filmes_favoritos_ids.update(lista.filmes.values_list('id', flat=True))
        
        from filmes.models import Filme
        filmes_favoritos = Filme.objects.filter(id__in=filmes_favoritos_ids)
    else:
        filmes_favoritos = []

    context = {
        'generos': generos,
        'diretores_destaque': diretores_destaque,
        'filmes_favoritos': filmes_favoritos
    }
    return render(request, 'filmes/index.html', context)


@admin_required
def adicionar_filme(request):
    """Adicionar filme - apenas administradores"""
    if request.method != 'POST':
        form = FilmeForm()
    
    else:
        form = FilmeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('index'))
    
    context =  {'form': form}
    return render (request, 'filmes/adicionar_filmes.html', context)


@admin_required
def editar_filme(request, id):
    """Editar filme - apenas administradores"""
    filme = get_object_or_404(Filme, pk=id)

    if request.method != 'POST':
        form = FilmeForm(instance = filme)
    else:
        form = FilmeForm(request.POST, instance=filme)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('index'))
         
    return render(request, 'filmes/edit_filmes.html', {'form': form, 'edit': filme})


@admin_required
def deletar_filme(request, id):
    """Deletar filme - apenas administradores"""
    filme= Filme.objects.get(pk=id)
    filme.delete()
    return HttpResponseRedirect(reverse('index'))
   

@user_required
def detalhar_filme(request, id):
    """Detalhar filme - usuários gerais e administradores"""
    filme = get_object_or_404(Filme, pk=id)
    user_is_admin = False
    if request.user.is_authenticated:
        user_is_admin = request.user.groups.filter(name='Administradores').exists()
    context = {
        'filme': filme,
        'user_is_admin': user_is_admin,
    }
    return render(request, 'filmes/detalhes_filme.html', context)

