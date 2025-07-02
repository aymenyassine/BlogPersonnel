from django import forms
from .models import Ticket  

from django import forms
from .models import Ticket

class TicketResponseForm(forms.ModelForm):
    mark_as_resolved = forms.BooleanField(
        required=False,
        label="Marquer comme résolu",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = Ticket
        fields = ['response', 'mark_as_resolved', 'status']
        widgets = {
            'response': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def save(self, commit=True):
        ticket = super().save(commit=False)
        if self.cleaned_data.get('mark_as_resolved'):
            ticket.status = 'Résolu'
        if commit:
            ticket.save()
        return ticket
