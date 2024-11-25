from django.urls import path
from . import views

app_name = 'annotations'

urlpatterns = [
    path('', views.list_annotations, name='list_annotations'),
    path('admin/<int:id_account>/', views.list_annotations_admin, name='list_annotations_admin'),    
    path('adicionar/', views.add_annotation, name='add_annotation'),
    path('editar/<int:id_annotation>/', views.edit_annotation, name='edit_annotation'),      
]