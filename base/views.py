from unicodedata import name
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .selectors import thank_auth
from .models import User, Dashboard

# Create your views here.
@login_required(login_url='accounts/login')
def index_view(request):
    admin = thank_auth.is_staff(request)
    if admin:
        return redirect('admin_index')
    return render(request, 'index.html')


def admin_index(request):
    admin = thank_auth.is_staff(request)
    if not admin:
        return redirect('login')
    
    # users
    users = User.objects.all()
    dashboard = Dashboard.objects.all()
    context = {
        "users": users,
        "dashboards": dashboard
    }
    return render(request, 'admin/index.html', context)


def dashboard_create(request):
    admin = thank_auth.is_staff(request)
    if not admin:
        return redirect('login')
    
    dash = request.POST
    if request.method == "POST":
        dashboard = Dashboard.objects.create(
            name = dash["name"],
            url = dash["url"],
            iframe = dash["iframe"]
        )
        if dashboard:
            return redirect('admin_index')
        

def dashboard_delete(request, dashboard_id):
    admin = thank_auth.is_staff(request)
    if not admin:
        return redirect('login')
    
    dashboard = Dashboard.objects.get(id=dashboard_id).delete()
    if dashboard:
        return redirect('admin_index')
    