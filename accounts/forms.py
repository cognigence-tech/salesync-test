# accounts/forms.py

from django import forms
from .models import Connection, Application


class ConnectionForm(forms.ModelForm):

    class Meta:
        model = Connection
        fields = ['sender',
                  'receiver']  # Specify the fields you want in the form

    def __init__(self, *args, **kwargs):
        country = kwargs.pop('country', None)  # Get country from kwargs
        super().__init__(*args, **kwargs)

        if country:
            # Filter applications based on the provided country
            self.fields['sender'].queryset = Application.objects.filter(
                country=country, role=Application.SENDER)
            self.fields['receiver'].queryset = Application.objects.filter(
                country=country, role=Application.RECEIVER)
