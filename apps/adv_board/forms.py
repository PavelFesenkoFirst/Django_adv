from django import forms

from apps.adv_board.models import Advertisement

class AdverisementModelForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea({'cols': 125, 'row': 5}))
    class Meta:
        model = Advertisement
        fields = ('title', 'id_category', 'description', 'price', 'image')