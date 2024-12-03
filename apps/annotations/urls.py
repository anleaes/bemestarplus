from django.urls import path
from . import views

app_name = 'annotations'

urlpatterns = [
    path('', views.list_annotations, name='list_annotations'),
    path('admin/<int:id_account>/', views.list_annotations_admin, name='list_annotations_admin'),    
    path('adicionar/', views.add_annotation, name='add_annotation'),
    path('editar/<int:id_annotation>/', views.edit_annotation, name='edit_annotation'),
    path('admin/<int:id_annotation>/comentario/', views.add_annotation_comment, name='add_annotation_comment'),
    path('admin/<int:id_annotation>/comentario/editar', views.add_annotation_comment, name='edit_annotation_comment'),
    path('relatorio-alertas/', views.report_alerts, name='report_alerts'),
    path('relatorio-emocional/', views.report_emotional_trends, name='report_emotional_trends'),    
]