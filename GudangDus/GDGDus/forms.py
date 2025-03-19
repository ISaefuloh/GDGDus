from django import forms
from .models import TransaksiMasuk, TransaksiKeluar, Merek, MasterDus, Dus


class MerekForm(forms.ModelForm):
    class Meta:
        model = Merek
        fields = ['nama']
        widgets = {
            'nama': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Merek'})
        }

class MasterDusForm(forms.ModelForm):
    class Meta:
        model = MasterDus
        fields = ['tipe', 'merek']
        widgets = {
            'tipe': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tipe Dus'}),
            'merek': forms.Select(attrs={'class': 'form-control'})
        }

class DusForm(forms.ModelForm):
    class Meta:
        model = Dus
        fields = ['tipe']
        widgets = {
            'tipe': forms.Select(attrs={'class': 'form-control'})
        }


class TransaksiMasukForm(forms.ModelForm):
    class Meta:
        model = TransaksiMasuk
        fields = ['tipe', 'jumlah_masuk']
        widgets = {
            'tipe': forms.Select(attrs={'class': 'form-control'}),
            'jumlah_masuk': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }

class TransaksiKeluarForm(forms.ModelForm):
    class Meta:
        model = TransaksiKeluar
        fields = ['tipe', 'jumlah_keluar']
        widgets = {
            'tipe': forms.Select(attrs={'class': 'form-control'}),
            'jumlah_keluar': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }
