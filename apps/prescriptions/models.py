from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Prescription(models.Model):
    diagnoses = models.TextField('Diagnostico', max_length=250)
    prescription = models.TextField('Prescicao de medicamento', max_length=200)
    is_active = models.BooleanField('Status', default=False)
    date_prescription = models.DateField('Data da prescricao', auto_now=False, auto_now_add=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    class Meta:
        verbose_name = 'Prescricao'
        verbose_name_plural = 'Prescricao'
        ordering =['id']

    def __str__(self):
        return self.diagnoses