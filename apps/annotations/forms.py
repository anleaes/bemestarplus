from django import forms
from .models import Annotations, Comments

class AnnotationForm(forms.ModelForm):

    class Meta:
        model = Annotations
        exclude = ('user', 'datetime')

class CommentForm(forms.ModelForm): 
    
    class Meta: 
        model = Comments 
        fields = ['comment'] 
        widgets = { 
            'comment': forms.Textarea(attrs={'rows': 3, 'cols': 40}),            
        }