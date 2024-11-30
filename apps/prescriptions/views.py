from django.shortcuts import render, get_object_or_404, redirect
from .forms import PrescriptionForm
from .models import Prescription
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='/contas/login/')
def add_prescription(request):
    template_name = 'prescriptions/add_prescription.html'
    context = {}
    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.user = request.user
            f.save()
            form.save_m2m()
            return redirect('prescriptions:list_prescriptions')
    form = PrescriptionForm()
    context['form'] = form
    return render(request, template_name, context)

@login_required(login_url='/contas/login/')
def list_prescriptions(request):
    template_name = 'prescriptions/list_prescriptions.html'
    prescriptions = Prescription.objects.filter(user=request.user)
    context = {
        'prescriptions': prescriptions
    }
    return render(request, template_name, context)

@login_required(login_url='/contas/login/')
def edit_prescription(request, id_prescription):
    template_name = 'prescriptions/add_prescription.html'
    context ={}
    prescription = get_object_or_404(Prescription, id=id_prescription, user=request.user)
    if request.method == 'POST':
        form = PrescriptionForm(request.POST, instance=prescription)
        if form.is_valid():
            form.save()
            return redirect('prescriptions:list_prescriptions')
    form = PrescriptionForm(instance=prescription)
    context['form'] = form
    return render(request, template_name, context)

@login_required(login_url='/contas/login/')
def delete_prescription(request, id_prescription):
    prescription = Prescription.objects.get(id=id_prescription)
    if prescription.user == request.user:
        prescription.delete()
    else:
        return redirect('core:home')
    return redirect('prescriptions:list_prescriptions')

@login_required(login_url='/contas/login/')
def list_prescriptions_admin(request, id_account):
    template_name = 'prescriptions/list_prescriptions.html'
    prescriptions = Prescription.objects.filter(user_id=id_account)
    context = {
        'prescriptions': prescriptions
    }
    return render(request, template_name, context)