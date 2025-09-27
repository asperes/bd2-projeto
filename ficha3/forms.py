from django import forms
from .models import Fatura, Bilhete, FaturasItem

class BilheteForm(forms.ModelForm):
    class Meta:
        model = Bilhete
        fields = ['sessao', 'cliente', 'tipo', 'lugar']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'border border-gray-300 rounded-md px-3 py-2'}),
            'lugar': forms.TextInput(attrs={'class': 'border border-gray-300 rounded-md px-3 py-2', 'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['lugar'].initial = 'Geral'

class BilheteMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.display_label()

class FaturaWithBilhetesForm(forms.ModelForm):
    bilhetes = BilheteMultipleChoiceField(
        queryset=Bilhete.objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Fatura
        fields = ['cliente', 'estado']
        widgets = {
            'estado': forms.Select(attrs={'class': 'border border-gray-300 rounded-md px-3 py-2'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Determine cliente from data, initial, or instance
        cliente_id = None
        if 'cliente' in self.data:
            try:
                cliente_id = int(self.data.get('cliente'))
            except (ValueError, TypeError):
                pass
        elif 'cliente' in self.initial:
            try:
                cliente_id = int(self.initial.get('cliente'))
            except (ValueError, TypeError):
                pass
        elif self.instance and self.instance.cliente_id:
            cliente_id = self.instance.cliente_id
        if cliente_id:
            self.fields['bilhetes'].queryset = Bilhete.objects.filter(
                cliente_id=cliente_id,
                fatura_item__isnull=True
            )
        else:
            self.fields['bilhetes'].queryset = Bilhete.objects.none()

    def clean_bilhetes(self):
        bilhetes = self.cleaned_data.get('bilhetes')
        if not bilhetes or len(bilhetes) == 0:
            raise forms.ValidationError('Selecione pelo menos um bilhete para a fatura.')
        return bilhetes