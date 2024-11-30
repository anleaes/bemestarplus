from django.urls import path
from . import views

app_name = 'prescriptions'

urlpatterns = [
    path('', views.list_prescriptions, name='list_prescriptions'),
     path('admin/<int:id_account>/', views.list_prescriptions_admin, name='list_prescriptions_admin'), 
    path('adicionar/', views.add_prescription, name='add_prescription'),
    path('editar/<int:id_prescription>/', views.edit_prescription, name='edit_prescription'),
    path('excluir/<int:id_prescription>/', views.delete_prescription, name='delete_prescription'),
]
