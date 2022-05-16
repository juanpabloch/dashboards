from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .selectors import thank_auth
from .models import User

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
    context = {
        "users": users
    }
    return render(request, 'admin/index.html', context)