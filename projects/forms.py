from django import forms
from .models import Proyecto, Repositorio, Etiqueta, Imagen
from django.http import HttpResponse

class ProjectForm(forms.ModelForm):
    tag_uno = forms.CharField()
    tag_dos = forms.CharField(help_text='Segunda especie')
    tag_tres = forms.CharField(help_text='Tercera especie')

    class Meta:
        model = Proyecto
        fields = ['titulo','contenido','tag_uno','tag_dos','tag_tres']
        widgets = {
            'titulo': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Titulo'}),
            'contenido': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Contenido', 'rows':3}),
            'tag_uno': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Primera especie'}),
        }

        labels = {
            'titulo':'', 'contenido':'','tag_uno':'','tag_dos':'','tag_tres':''
        }

class BancoImageForm(forms.ModelForm):
    class Meta:
        model = Repositorio
        fields = ['Etiqueta','repositorio']
        widgets = {
            'repositorio':forms.ClearableFileInput(attrs={'class':'form-control', 'multiple':True})
        }
        labels = {
            'Etiqueta':''
        }
        

class ImageForm(forms.ModelForm):
    class Meta:
        model = Imagen
        fields=['imagen']
        widgets = {
            'imagen':forms.ClearableFileInput(attrs={'class':'form-control'})
        }