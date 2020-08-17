from django import forms

from apps.contacts.models import ContactUs


class ContactUsModelForm(forms.ModelForm):

    message = forms.CharField(widget=forms.Textarea({'cols': 50, 'rows': 2}))

    class Meta:
        model = ContactUs
        fields = ('subject', 'message')