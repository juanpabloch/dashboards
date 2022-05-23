from dataclasses import fields
from django import forms
from .models import Dashboard


class BannForm(forms.Form):
    ban_reason = forms.CharField(max_length=100)
    

class DashboardForm(forms.ModelForm):
    class Meta:
        model = Dashboard
        fields = ['name', 'url', 'iframe']
