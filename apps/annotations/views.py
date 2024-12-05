from django.shortcuts import render, get_object_or_404, redirect
from .forms import AnnotationForm, CommentForm
from .models import Annotations, Comments
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from datetime import timedelta
from django.contrib import messages
import random
from django.db.models import Count
from datetime import timedelta


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
            negative_states = ['cansado', 'frustrado', 'confuso']
            if f.emotional_state in negative_states:
                recent_negative_annotations = Annotations.objects.filter(
                    user=request.user, 
                    emotional_state=f.emotional_state
                ).count()
                if recent_negative_annotations >= 3:
                    help_messages = [
                        "Lembre-se de tirar uma pausa para relaxar e respirar fundo.",
                        "Converse com alguém de confiança sobre como você está se sentindo.",
                        "Que tal anotar seus pensamentos para organizar suas ideias?",
                        "Pequenos passos podem ajudar a aliviar o cansaço ou a frustração.",
                        "Você está fazendo o seu melhor, e isso é o suficiente!",
                        "Se possível, tire um momento para cuidar de você mesmo."
                    ]
                    random_message = random.choice(help_messages)
                    messages.warning(request, random_message)
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
    if annotation.is_locked:
        return redirect('annotations:list_annotations')
    
    if request.method == 'POST':
        form = AnnotationForm(request.POST, instance=annotation)
        if form.is_valid():
            form.save()
            return redirect('annotations:list_annotations')
    form = AnnotationForm(instance=annotation)
    context['form'] = form
    return render(request, template_name, context)

@login_required(login_url='/contas/login/')
def list_annotations_admin(request, id_account):
    template_name = 'annotations/list_annotations.html'
    annotations = Annotations.objects.filter(user_id=id_account)
    context = {
        'annotations': annotations
    }
    return render(request, template_name, context)

@login_required(login_url='/contas/login/')
def add_annotation_comment(request, id_annotation):
    template_name = 'annotations/add_annotation_comment.html'
    annotation = get_object_or_404(Annotations, id=id_annotation)
    context = {
        'annotations': annotation
    }
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.user = request.user
            f.annotation = annotation
            f.save()
            annotation.is_locked = True
            annotation.save()
            form.save_m2m()
            return redirect('annotations:list_annotations_admin', id_account=annotation.user.id)
    form = CommentForm()
    context['form'] = form
    return render(request,template_name,context)

@login_required(login_url='/contas/login/')
def edit_annotation_comment(request, id_comment):
    template_name = 'annotations/add_annotation_comment.html'
    context ={}
    comment = get_object_or_404(Comments, id=id_comment, user=request.user)  
    
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('annotations:list_annotations_admin')
    form = CommentForm(instance=comment)
    context['form'] = form
    return render(request, template_name, context)

@login_required(login_url='/contas/login/')
def report_alerts(request):
    template_name = 'annotations/report_alerts.html'
    seven_days_ago = now() - timedelta(days=7)
    accounts = User.objects.all()
    user_emotional_states = []

    for account in accounts:
        # Recupera as anotações emocionais do usuário nos últimos 7 dias
        annotations = Annotations.objects.filter(
            user=account,
            emotional_state__in=['confuso', 'cansado'],
            datetime__gte=seven_days_ago
        ).order_by('datetime')

        # Verifica as ocorrências consecutivas de "confuso" ou "cansado"
        count = 0
        max_count = 0
        for annotation in annotations:
            if annotation.emotional_state in ['confuso', 'cansado']:
                count += 1
                max_count = max(max_count, count)
            else:
                count = 0

        # Determina a cor da linha com base no maior número de consecutivos
        if max_count >= 3:
            alert_level = 'red'
        elif 1 <= max_count <= 2:
            alert_level = 'yellow'
        else:
            alert_level = 'green'

        user_emotional_states.append({
            'user': account,
            'alert_level': alert_level
        })

    # Ordena a lista: vermelho > amarelo > verde
    user_emotional_states.sort(key=lambda x: {'red': 0, 'yellow': 1, 'green': 2}[x['alert_level']])

    context = {
        'user_emotional_states': user_emotional_states,
    }
    return render(request, template_name, context)

@login_required(login_url='/contas/login/')
def report_emotional_trends(request):
    template_name = 'annotations/report_emotional_trends.html'
    seven_days_ago = now() - timedelta(days=7)
    accounts = User.objects.all()

    user_emotional_trends = []
    overall_trends = {state: 0 for state, _ in Annotations.EMOTIONAL_STATE_CHOICE}

    for account in accounts:
        trends = {}
        for state, label in Annotations.EMOTIONAL_STATE_CHOICE:
            count = Annotations.objects.filter(
                user=account,
                emotional_state=state,
                datetime__gte=seven_days_ago
            ).count()
            trends[state] = count
            overall_trends[state] += count
        if any(trends.values()):
            most_frequent_state = max(trends, key=trends.get)
            user_emotional_trends.append({
                'user': account,
                'most_frequent_state': most_frequent_state,
                'frequency': trends[most_frequent_state],
            })

    context = {
        'user_emotional_trends': user_emotional_trends,
        'overall_trends': overall_trends,  # Certifique-se de passar isso!
    }
    return render(request, template_name, context)


