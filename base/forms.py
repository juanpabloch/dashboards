from dataclasses import fields
from pyexpat import model
from django import forms
from .models import Dashboard

class BannForm(forms.Form):
    ban_reason = forms.CharField(max_length=100)
    

class DashboardForm(forms.ModelForm):
    class Meta:
        model = Dashboard
        fields = ['name', 'url', 'iframe']
        

class DashboardSelectForm(forms.Form):
    dashboards_list = Dashboard.objects.all().values_list("id", "name")
    dashboards = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=dashboards_list)
    
    

    
    