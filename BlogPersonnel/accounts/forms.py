from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import CustomUser

class FormUserregister(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'imageProfile',
            'imageCoverture',
        )
        labels = {
            'username': 'Nom d’utilisateur',
            'email': 'Adresse e-mail',
            'first_name': 'Prénom',
            'last_name': 'Nom',
            'bio': 'Biographie',
            'imageProfile': 'Image de profil',
            'imageCoverture': 'Image de couverture',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom d’utilisateur'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Adresse e-mail'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Parlez un peu de vous...', 'rows': 3}),
            'imageProfile': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'imageCoverture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Mot de passe'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirmez le mot de passe'
        })

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': "Nom d'utilisateur"
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': "Mot de passe"
        })
