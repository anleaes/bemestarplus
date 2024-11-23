from django.shortcuts import render, get_object_or_404, redirect
from .forms import AnnotationForm
from .models import Annotations
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='/contas/login/')
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

@login_required(login_url='/contas/login/')
def list_annotations(request):
    template_name = 'annotations/list_annotations.html'
    annotations = Annotations.objects.filter(user=request.user)
    context = {
        'annotations': annotations
    }
    return render(request, template_name, context)

@login_required(login_url='/contas/login/')
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
