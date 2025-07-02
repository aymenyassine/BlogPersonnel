from django import forms
from .models import Post, Comment, Signaler

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'category']
        labels = {
            'title': "Titre de l'article",
            'content': "Contenu",
            'image': "Image",
            'category': "Catégorie",
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le titre'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Rédigez votre contenu ici...'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': "Commentaire",
        }
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ajoutez un commentaire...'}),
        }

class SignalForm(forms.ModelForm):
    class Meta:
        model = Signaler
        fields = ['objet', 'description']
        labels = {
            'objet': "Objet du signalement",
            'description': "Description",
        }
        widgets = {
            'objet': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sujet du signalement'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Expliquez votre signalement...'}),
        }
