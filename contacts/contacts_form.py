from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('__all__')
        labels = {
            'first_name': "first name",
            'last_name': "last name",
            'contact_url': 'contact url',
            'phone_number': "phone number"
        }
