from dataclasses import fields
from django import forms
from .models import Dashboard, EmailsDomains


class BannForm(forms.Form):
    ban_reason = forms.CharField(max_length=100)
    

class DashboardForm(forms.ModelForm):
    class Meta:
        model = Dashboard
        fields = ['name', 'url']


class DomainsForm(forms.ModelForm):
    class Meta:
        model = EmailsDomains
        fields = ['name', 'domain']