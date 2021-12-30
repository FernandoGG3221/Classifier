from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile

class FormUserWithEmail(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Requerido, 200 carácteres como máximo y debe ser válido')
    first_name = forms.CharField(required=True, help_text='Escribe tu nombre, Requerido')
    last_name = forms.CharField(required=True, help_text='Escribe tus apellidos, Requerido')

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('El email ya está registrado, prueba con otro.')
        return email

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar','bio','link','name','name2','name3','institute','address']
        widgets = {
            'avatar':forms.ClearableFileInput(attrs={'class':'form-control-file mt-3'}),
            'bio':forms.Textarea(attrs={'class':'form-control mt-3','rows':3,'placeholder':'Biografia'}),
            'link':forms.URLInput(attrs={'class':'form-control mt-3','placeholder':'Enlace'}),
            'name' : forms.TextInput(attrs={'class':'form-control mt-3','placeholder':'Nombre'}),
            'name2' : forms.TextInput(attrs={'class':'form-control mt-3','placeholder':'Apellido Paterno'}),
            'name3' : forms.TextInput(attrs={'class':'form-control mt-3','placeholder':'Apellido Materno'}),
            'institute' : forms.TextInput(attrs={'class':'form-control mt-3','placeholder':'Dependencia ó Instituto'}),
            'address' : forms.TextInput(attrs={'class':'form-control mt-3','placeholder':'Dirección de la dependencia o instituto'}),
        }

class EmailForm(forms.ModelForm):
    email = forms.EmailField(required=True, help_text='Requerido, 254 caracteres como máximo y debe ser válido')

    class Meta:
        model = User
        fields = ['email']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if 'email' in self.changed_data:
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError('El email ya está registrado, prueba con otro.')
        return email