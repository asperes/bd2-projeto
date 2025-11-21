from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User
import json


 
class CriarUtilizador(UserCreationForm):    #UserCreationForm pois ja tem alguns campos com a validacao automatica
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Email'
        })
    )

    class Meta:
        model = User
        fields = ['username','email','first_name','last_name','password1','password2']
        labels = {
            'username': 'Nome de Utilizador',
            'email': 'Email',
            'first_name': 'Primeiro Nome',
            'last_name': 'Último Nome',
            'password1': 'Palavra-passe',
            'password2': 'Confirmação da Palavra-passe'
        }
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Username'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Nome'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Apelido'
            }),
        }
    def __init__(self, *args, **kwargs):    #os campos da pass tem que ser feitos pelo metodo init porque o usercreationform já tem widgets defenidos para estes campos 
        super().__init__(*args, **kwargs)   
        self.fields['password1'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Senha'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Confirmar senha'
        })

# class LoginForm(forms.Form):
#     username = forms.CharField(label='Username', max_length=50)
#     password = forms.CharField(label='Password', widget=forms.PasswordInput)


class EditarPerfilForm(forms.ModelForm):
    pass
    class Meta:
        model = User
        fields = ['username', 'bio','profile_picture_url','date_of_birth','location']
        labels = {
            'username': 'Nome de Utilizador',
            'bio': 'Biografia',
            'profile_picture_url': 'URL da Foto de Perfil',
            'date_of_birth': 'Data de Nascimento',
            'location': 'Localização'
        }
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Username'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Bio',
                'rows': 4
            }),
            'profile_picture_url': forms.URLInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'URL da foto de perfil'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Data de nascimento',
                'type': 'date'
            }),
            'location': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Localização'
            }),
        }




    


