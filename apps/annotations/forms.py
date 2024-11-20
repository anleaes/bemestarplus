from django import forms
from .models import Annotations

class AnnotationForm(forms.ModelForm):

    class Meta:
        model = Annotations
        exclude = ('user', 'datetime')