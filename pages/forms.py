from django import forms
from .models import PageModel

class PageForm(forms.ModelForm):

    class Meta:
        model = PageModel
        fields = ['title', 'content', 'order']
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Titulo'}),
            'content': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Contenido', 'rows':'3'}),
            'order': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Orden'}),
        }

        labels = {
            'title':'', 'order':'', 'content':''
        }