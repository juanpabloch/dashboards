from multiprocessing import context
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .selectors import thank_auth
from .models import User, Dashboard

from allauth.socialaccount.signals import pre_social_login
from allauth.exceptions import ImmediateHttpResponse
from django.dispatch import receiver

# formularios
from .forms import BannForm, DashboardForm, DashboardSelectForm



# Create your views here.
@receiver(pre_social_login)
def check_user(request, sociallogin, **kwargs):
    socialemail = sociallogin.user.email
    user = User.objects.filter(email=socialemail)
    if user:
        if user[0].banned:
            raise ImmediateHttpResponse(redirect('banned'))
        if user[0].delete:
            raise ImmediateHttpResponse(redirect('banned'))


@login_required(login_url='accounts/login')
def index_view(request):
    admin = thank_auth.is_staff(request)
    if admin:
        return redirect('admin_dashboard_view')
    user = User.objects.filter(id=request.user.id)[0]
    user_dash = Dashboard.objects.filter(users__id=user.id).filter(active=1)
    print("USER: ", user_dash)
    context = {
        'user': user,
        'dashboards': user_dash
    }
    return render(request, 'index.html', context)


def admin_redirect(request):
    admin = thank_auth.is_staff(request)
    if not admin:
        return redirect('login')
    return redirect('admin_dashboard_view')


def admin_dashboard_view(request):
    admin = thank_auth.is_staff(request)
    if not admin:
        return redirect('login')
    
    dashboard = Dashboard.objects.all()
    context = {
        "dashboards": dashboard,
        "new_dash_form": DashboardForm()
    }
    return render(request, 'admin/index.html', context)


def dashboard_create(request):
    admin = thank_auth.is_staff(request)
    if not admin:
        return redirect('login')
    
    if request.method == "POST":
        form = DashboardForm(request.POST)
        if form.is_valid():
            dash = request.POST
            dashboard = Dashboard.objects.create(
                name = dash["name"],
                url = dash["url"],
                iframe = dash["iframe"]
            )
            if dashboard:
                return redirect('admin_dashboard_view')
        

def dashboard_delete(request, dashboard_id):
    admin = thank_auth.is_staff(request)
    if not admin:
        return redirect('login')
    
    dashboard = Dashboard.objects.get(id=dashboard_id).delete()
    if dashboard:
        return redirect('admin_dashboard_view')
    return redirect('admin_dashboard_view')
    
    
def dashboard_deactivate(request, dashboard_id):
    admin = thank_auth.is_staff(request)
    if not admin:
        return redirect('login')
    
    dashboard = Dashboard.objects.filter(id=dashboard_id).update(active=0)
    if dashboard:
        return redirect('admin_dashboard_view')
   

def dashboard_activate(request, dashboard_id):
    admin = thank_auth.is_staff(request)
    if not admin:
        return redirect('login')
    
    dashboard = Dashboard.objects.filter(id=dashboard_id).update(active=1)
    if dashboard:
        return redirect('admin_dashboard_view')    
    

def dashboard_edit(request, dashboard_id):
    admin = thank_auth.is_staff(request)
    if not admin:
        return redirect('login')
    
    dashboard = Dashboard.objects.filter(id=dashboard_id)
    
    if request.method == "POST":
        form = DashboardForm(request.POST)
        if form.is_valid():
            dash = request.POST
            dashboard.update(
                name = dash["name"],
                url = dash["url"],
                iframe = dash["iframe"]
            )
            if dashboard:
                return redirect('admin_dashboard_view')
            
    dashboard_form = {
        "name": dashboard[0].name,
        "url": dashboard[0].url,
        "iframe": dashboard[0].iframe
    }
    form = DashboardForm(dashboard_form)
    context = {
        'dashboard': dashboard[0],
        'form': form
    }
    
    return render(request, 'admin/dashboard_edit.html', context)

# USER
def admin_user_view(request):
    admin = thank_auth.is_staff(request)
    if not admin:
        return redirect('login')
    
    users = User.objects.all()
    dashboards = Dashboard.objects.all().values("id", "name")
    form = DashboardSelectForm()
    context = {
        "users": users,
        "dashboards": dashboards,
        "ban_form": BannForm(),
        "dashboard_select_form": form
    }
    return render(request, 'admin/users.html', context)
    


def user_activate(request, user_id):
    admin = thank_auth.is_staff(request)
    if not admin:
        return redirect('login')
    if request.method == "POST":
        user = User.objects.filter(id=user_id)[0]
        user.is_active = 1
        user.banned = 0
        user.save()
        if user:
            dash_list = request.POST.getlist('dashboard_select')
            dashboards = Dashboard.objects.filter(id__in=dash_list)
            for dash in dashboards:
                dash.users.add(user.id)
    
            return redirect('admin_user_view') 
        else:
            print("error al activar usuario")


def user_banned(request, user_id):
    admin = thank_auth.is_staff(request)
    if not admin:
        return redirect('login')
    if request.method == "POST":
        form = BannForm(request.POST)
        if form.is_valid():
            user = User.objects.filter(id=user_id).update(is_active=0, banned=1, ban_reason=request.POST["ban_reason"])
            if user:
                return redirect('admin_user_view')
    return redirect('admin_user_view')
        

def user_delete(request, user_id):
    admin = thank_auth.is_staff(request)
    if not admin:
        return redirect('login')
    if request.method == "POST":
        user = User.objects.filter(id=user_id).update(is_active=0, banned=0, delete=1)
        if user:
            return redirect('admin_user_view')
    return redirect('admin_user_view')


def user_edit(request, user_id):
    user = User.objects.filter(id=user_id)[0]
    user.dashboards.clear()
    if request.method == "POST":
        dash_list = request.POST.getlist('dashboards')
        dashboards = Dashboard.objects.filter(id__in=dash_list)
        for dash in dashboards:
            dash.users.add(user.id)
                
    return redirect('admin_user_view')
    
    
def banned_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    return render(request, 'account/banned.html')
    
    
# def prueba(request):
#     form = DashBoarsFormSelect
#     context = {
#         "form": form
#     }
#     return render(request, 'pruebas.html', context)
