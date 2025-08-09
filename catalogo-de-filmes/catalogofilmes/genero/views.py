from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Genero
from .forms import GeneroForm

class GeneroListView(ListView):
    model = Genero
    template_name = 'genero/listar.html'
    context_object_name = 'generos'

class GeneroCreateView(CreateView):
    model = Genero
    form_class = GeneroForm
    template_name = 'genero/form.html'
    success_url = reverse_lazy('genero:listar_generos')

class GeneroUpdateView(UpdateView):
    model = Genero
    form_class = GeneroForm
    template_name = 'genero/form.html'
    success_url = reverse_lazy('genero:listar_generos')

class GeneroDeleteView(DeleteView):
    model = Genero
    template_name = 'genero/confirmar_delete.html'
    success_url = reverse_lazy('genero:listar_generos')