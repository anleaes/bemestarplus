from django.shortcuts import render, get_object_or_404, redirect
from .forms import AnnotationForm
from .models import Annotations

# Create your views here.

def add_annotation(request):
    template_name = 'annotations/add_annotation.html'
    context = {}
    if request.method == 'POST':
        form = AnnotationForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.user = request.user
            f.save()
            form.save_m2m()
            return redirect('annotations:list_annotations')
    form = AnnotationForm()
    context['form'] = form
    return render(request, template_name, context)

def list_annotations(request):
    template_name = 'annotations/list_annotations.html'
    annotations = Annotations.objects.filter(user=request.user)
    context = {
        'annotations': annotations
    }
    return render(request, template_name, context)

def edit_annotation(request, id_annotation):
    template_name = 'annotations/add_annotation.html'
    context ={}
    annotation = get_object_or_404(Annotations, id=id_annotation, user=request.user)
    if request.method == 'POST':
        form = AnnotationForm(request.POST, instance=annotation)
        if form.is_valid():
            form.save()
            return redirect('annotations:list_annotations')
    form = AnnotationForm(instance=annotation)
    context['form'] = form
    return render(request, template_name, context)

#adicionado por PedroQ o a busca de comentários.
def search_annotations(request):
    template_name = 'annotations/list_annotations.html'
    query = request.GET.get('query', '')  # Obtém a query ou string vazia por padrão
    
    # Verifica se o usuário logado é admin
    if request.user.is_superuser:
        # Admin pode buscar anotações de qualquer usuário
        annotations = Annotations.objects.filter(
            user__username__icontains=query
        )
    else:
        # Usuários não administradores só podem ver suas próprias anotações
        annotations = Annotations.objects.filter(
            user=request.user,
            user__username__icontains=query
        )
    
    context = {
        'annotations': annotations
    }

    return render(request, template_name, context)