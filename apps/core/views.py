from django.shortcuts import render

# Create your views here.

def home(request):
   #template_name ='core/home.html'
    template_name ='accounts/user_login.html' #Quando abrir o sistema abrir primeiro na pagina de login
    context = {}
    return render(request, template_name, context)
