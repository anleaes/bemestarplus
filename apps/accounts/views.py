from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from .forms import UserForm, UserChangeInformationForm, UserFormEdit
from annotations.models import Annotations

# Create your views here.

def user_login(request):
    template_name = 'accounts/user_login.html'
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(request.GET.get('next', 'annotations:list_annotations'))
            #return redirect(request.GET.get('next', '/'))
        else:
            return redirect('accounts:user_login')
    return render(request, template_name, {})

@login_required(login_url='/contas/login/')
def add_user(request):
    template_name = 'accounts/add_user.html'
    context = {}
    if request.method =='POST':
        form = UserForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.set_password(f.password)
            f.save()
            return redirect('accounts:list_accounts')
        else:
            return redirect('accounts:add_user')
    form = UserForm()
    context['form'] = form
    return render(request, template_name, context) 

@login_required(login_url='/contas/login/')
def user_logout(request):
    logout(request)
    return redirect('accounts:user_login')

@login_required(login_url='/contas/login/')
def user_change_password(request):
    template_name = 'accounts/user_change_password.html'
    context = {}
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
        else:
            return redirect('accounts:user_login')
    form = PasswordChangeForm(user=request.user)
    context['form'] = form
    return render(request, template_name, context)

@login_required(login_url='/contas/login/')
def user_change_information(request, username):
    template_name = 'accounts/user_change_information.html'
    context = {}
    user = User.objects.get(username=username)
    if request.method == 'POST':
        form = UserChangeInformationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
    form = UserChangeInformationForm(instance=user)
    context['form'] = form
    return render(request, template_name, context)

@login_required(login_url='/contas/login/')
def list_accounts(request):
    template_name = 'accounts/list_accounts.html'
    account = User.objects.order_by('id').all()  # Recupera todos os usuários
    #annotation = Annotations.objects.all()  # Recupera todos os usuários
    context = {
        'accounts': account,
        #'annotations': annotation,
    }
    return render(request, template_name, context)

@login_required(login_url='/contas/login/')
def search_accounts(request):    
    template_name = 'accounts/list_accounts.html'
    query = request.GET.get('query')     
    account = User.objects.filter(first_name__icontains=query)
    annotation = Annotations.objects.all()
    context = {
        'accounts': account,
        'annotations': annotation,
    }
    return render(request,template_name, context)

@login_required(login_url='/contas/login/')
def edit_account(request, id_account):
    template_name = 'accounts/add_user.html'
    context ={}
    account = get_object_or_404(User, id=id_account)
    if request.method == 'POST':
        form = UserFormEdit(request.POST, instance=account)
        if form.is_valid():
            form.save()
            return redirect('accounts:list_accounts')
    form = UserFormEdit(instance=account)
    context['form'] = form
    return render(request, template_name, context)