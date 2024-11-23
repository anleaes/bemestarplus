from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('novo-usuario/',views.add_user, name='add_user'),
    path('login/',views.user_login, name='user_login'),
    path('sair/',views.user_logout, name='user_logout'),
    path('alterar-senha/',views.user_change_password, name='user_change_password'),
    path('alterar-usuario/<username>/',views.user_change_information, name='user_change_information'),
    path('',views.list_accounts, name='list_accounts'),
    path('editar/<int:id_account>/', views.edit_account, name='edit_account'),
    path('buscar/', views.search_accounts, name='search_accounts'),       
]