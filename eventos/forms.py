from django import forms
from .models import Events


class CriarEvento(forms.ModelForm):
    class Meta:
        model = Events
        fields = ['title', 'description', 'location_name', 'location_address', 'start_datetime', 'end_datetime','max_attendees','is_public','cover_image_url', 'category']
        labels = {
            'title': 'Título',
            'description': 'Descrição',
            'location_name': 'Nome do Local',
            'location_address': 'Endereço',
            'start_datetime': 'Data de Início',
            'end_datetime': 'Data de Fim',
            'max_attendees': 'Máximo de Participantes',
            'is_public': 'Público',
            'cover_image_url': 'Imagem de Capa',
            'category': 'Categoria'
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Título do Evento'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Descrição do Evento',
                'rows': 4
            }),
            'location_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Nome do Local'
            }),
            'location_address': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Endereço do Local'
            }),
            'start_datetime': forms.DateTimeInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Data e Hora de Início',
                'type': 'datetime-local'
            }),
            'end_datetime': forms.DateTimeInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Data e Hora de Fim',
                'type': 'datetime-local'
            }),
            'max_attendees': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Número Máximo de Participantes'
            }),
            'is_public': forms.CheckboxInput(attrs={
                'class': 'form-checkbox h-5 w-5 text-blue-600'
            }),
            'cover_image_url': forms.URLInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'URL da Imagem de Capa'
            }),
            'category': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Categoria'
            })
        }

# class EditarEvento(forms.ModelForm):

#     class Meta:
#         model = Events
#         fields = ['username', 'bio','profile_picture_url','date_of_birth','location']
#         widgets = {
#             'username': forms.TextInput(attrs={
#                 'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
#                 'placeholder': 'Username'
#             }),
#             'bio': forms.Textarea(attrs={
#                 'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
#                 'placeholder': 'Bio',
#                 'rows': 4
#             }),
#             'profile_picture_url': forms.URLInput(attrs={
#                 'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
#                 'placeholder': 'URL da foto de perfil'
#             }),
#             'date_of_birth': forms.DateInput(attrs={
#                 'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
#                 'placeholder': 'Data de nascimento',
#                 'type': 'date'
#             }),
#             'location': forms.TextInput(attrs={
#                 'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
#                 'placeholder': 'Localização'
#             }),
#         }