from django import forms
from .models import Cliente, Local


class ClienteForm(forms.ModelForm):
    """Form para criar/editar Cliente"""
    
    class Meta:
        model = Cliente
        fields = ['nome', 'email', 'telefone', 'morada']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome completo do cliente'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@exemplo.com'
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+351 912 345 678'
            }),
            'morada': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Morada completa'
            }),
        }
        labels = {
            'nome': 'Nome Completo',
            'email': 'E-mail',
            'telefone': 'Telefone',
            'morada': 'Morada',
        }
    
    def clean_email(self):
        """Validar email único"""
        email = self.cleaned_data.get('email')
        if email:
            # Se está editando, excluir o próprio objeto da verificação
            if self.instance.pk:
                if Cliente.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
                    raise forms.ValidationError('Este email já está em uso.')
            else:
                if Cliente.objects.filter(email=email).exists():
                    raise forms.ValidationError('Este email já está em uso.')
        return email
    
    def clean_telefone(self):
        """Validar formato do telefone"""
        telefone = self.cleaned_data.get('telefone')
        if telefone:
            # Remover espaços e caracteres especiais para validação
            telefone_limpo = ''.join(filter(str.isdigit, telefone))
            if len(telefone_limpo) < 9:
                raise forms.ValidationError('Telefone deve ter pelo menos 9 dígitos.')
        return telefone


class LocalForm(forms.ModelForm):
    """Form para criar/editar Local"""
    
    class Meta:
        model = Local
        fields = ['nome', 'morada', 'capacidade', 'contacto']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome do local/venue'
            }),
            'morada': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Morada completa do local'
            }),
            'capacidade': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de lugares',
                'min': 1
            }),
            'contacto': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Telefone ou email de contacto'
            }),
        }
        labels = {
            'nome': 'Nome do Local',
            'morada': 'Morada',
            'capacidade': 'Capacidade (lugares)',
            'contacto': 'Contacto',
        }
    
    def clean_capacidade(self):
        """Validar capacidade"""
        capacidade = self.cleaned_data.get('capacidade')
        if capacidade is not None and capacidade <= 0:
            raise forms.ValidationError('A capacidade deve ser maior que zero.')
        if capacidade is not None and capacidade > 100000:
            raise forms.ValidationError('A capacidade parece excessivamente grande. Verifique o valor.')
        return capacidade
    
    def clean_nome(self):
        """Validar nome único"""
        nome = self.cleaned_data.get('nome')
        if nome:
            # Se está editando, excluir o próprio objeto da verificação
            if self.instance.pk:
                if Local.objects.filter(nome__iexact=nome).exclude(pk=self.instance.pk).exists():
                    raise forms.ValidationError('Já existe um local com este nome.')
            else:
                if Local.objects.filter(nome__iexact=nome).exists():
                    raise forms.ValidationError('Já existe um local com este nome.')
        return nome