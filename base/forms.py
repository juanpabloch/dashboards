from django import forms
from .models import Dashboard
from django_select2 import forms as s2forms

class BannForm(forms.Form):
    ban_reason = forms.CharField(max_length=100)
    

class DashboardForm(forms.ModelForm):
    class Meta:
        model = Dashboard
        fields = ['name', 'url', 'iframe']
        

class DashboardSelectForm(forms.Form):
    dashboards_list = Dashboard.objects.all().values_list("id", "name")
    dashboards = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=dashboards_list)
    
   
class DashBoarsFormSelect(s2forms.ModelSelect2MultipleWidget):
    search_fields = [
        "name_icontains"
    ]
    
