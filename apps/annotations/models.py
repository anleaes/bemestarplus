from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Annotations(models.Model):
    #Lista de opções de como foi o dia
    DAY_STATE_CHOICE = [
        ('muito_bom', 'Muito bom'),
        ('bom', 'Bom'),
        ('normal', 'Normal'),
        ('mal', 'Mal'),
        ('muito_mal', 'Muito mal'),
    ]
    EMOTIONAL_STATE_CHOICE = [
        ('animado', 'Animado'),
        ('calmo', 'Calmo'),
        ('frustrado', 'Frustrado'),
        ('confuso', 'Confuso'),
        ('cansado', 'Cansado'),

    ]
    datetime = models.DateTimeField(auto_now_add=True)   
    description = models.TextField('Descricao', max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    day_state = models.CharField('Estado do dia', max_length=20, choices=DAY_STATE_CHOICE, default='normal')
    emotional_state = models.CharField('Estado emocional', max_length=20, choices=EMOTIONAL_STATE_CHOICE, default="")
    is_locked = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Anotação'
        verbose_name_plural = 'Anotações'
        ordering =['datetime']

    def __str__(self):
        return self.description
    
class Comments(models.Model):
    STATUS_CHOICES = [
        (False, 'Em análise'),
        (True, 'Respondido'),
    ]
    annotation = models.ForeignKey(Annotations, related_name='comments', on_delete=models.CASCADE) 
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    comment = models.TextField() 
    created_at = models.DateTimeField(auto_now_add=True) 
    status = models.BooleanField(choices=STATUS_CHOICES, default=False)
         
    def __str__(self): 
        return self.comment