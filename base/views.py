from multiprocessing import context
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .selectors import thank_auth, iframe_converter
from .models import User, Dashboard, EmailsDomains

from allauth.socialaccount.signals import pre_social_login
from allauth.exceptions import ImmediateHttpResponse
from django.dispatch import receiver

from django.http import JsonResponse

# formularios
from .forms import BannForm, DashboardForm, DomainsForm

# TODO: traer lista de dominios desde la base de datos
# Create your views here.
@receiver(pre_social_login)
def check_user(request, sociallogin, **kwargs):
    DOMAIN_LIST = EmailsDomains.objects.all().values_list('domain', flat=True)
    socialemail = sociallogin.user.email
    domain = socialemail.split('@')[1]
    
    if not domain in DOMAIN_LIST:
        raise ImmediateHttpResponse(redirect('forbidden'))
    
    user = User.objects.filter(email=socialemail).first()
    if user:
        if user.banned or user.delete:
            raise ImmediateHttpResponse(redirect('banned'))


@login_required(login_url='accounts/login')
def index_view(request):
    admin = thank_auth.is_staff(request)
    if admin:
        return redirect('admin_index')
    
    user = User.objects.filter(id=request.user.id)[0]
    user_dash = Dashboard.objects.filter(users__id=user.id).filter(active=1)
    if len(user_dash) == 1:
        context = {
            "iframe":user_dash[0].iframe
        }
        return render(request, 'dashboard.html', context)
    context = {
        'user': user,
        'dashboards': user_dash
    }
    return render(request, 'index.html', context)


@login_required(login_url='accounts/login')
def admin_index(request):
    admin = thank_auth.is_staff(request)
    if not admin:
        return redirect('login')
    return render(request, 'admin/index.html')


def admin_dashboard_view(request):
    admin = thank_auth.is_staff(request)
    if not admin:
        return redirect('login')
    
    dashboard = Dashboard.objects.all()
    context = {
        "dashboards": dashboard,
        "new_dash_form": DashboardForm()
    }
    return render(request, 'admin/dashboards.html', context)


def dashboard_create(request):
    admin = thank_auth.is_staff(request)
    if not admin:
        return redirect('login')
    
    if request.method == "POST":
        form = DashboardForm(request.POST)
        if form.is_valid():
            dash = request.POST
            iframe = iframe_converter.converter(dash["url"])
            dashboard = Dashboard.objects.create(
                name = dash["name"],
                url = dash["url"],
                iframe = iframe
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
    
    if request.method == "POST":
        form = DashboardForm(request.POST)
        if form.is_valid():
            dash = request.POST
            iframe = iframe_converter.converter(dash["url"])
            dashboard = Dashboard.objects.filter(id=dashboard_id).update(
                name = dash["name"],
                url = dash["url"],
                iframe = iframe
            )
            if dashboard:
                print("OK")
        return redirect('admin_dashboard_view')
            

# USER
def admin_user_view(request):
    admin = thank_auth.is_staff(request)
    if not admin:
        return redirect('login')
    
    users = User.objects.all()
    dashboards = Dashboard.objects.all().values("id", "name")
    context = {
        "users": users,
        "dashboards": dashboards,
        "ban_form": BannForm(),
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
            dash_list = request.POST.getlist('dashboards[]')
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
        dash_list = request.POST.getlist('dashboards[]')
        dashboards = Dashboard.objects.filter(id__in=dash_list)
        for dash in dashboards:
            dash.users.add(user.id)
                
    return redirect('admin_user_view')
    

# Domain
def admin_domain_view(request):
    domains = EmailsDomains.objects.all()
    context = {
        "domains": domains,
        "new_domain_form": DomainsForm()
    }
    return render(request, 'admin/domains.html',context) 
    

def domain_create(request):
    admin = thank_auth.is_staff(request)
    if not admin:
        return redirect('login')
    
    if request.method == "POST":
        form = DomainsForm(request.POST)
        if form.is_valid():
            dom = request.POST
            
            domain = EmailsDomains.objects.create(
                name = dom["name"],
                domain = dom["domain"]
            )
            if domain:
                return redirect('admin_domain_view') 
 

def domain_delete(request, domain_id):
    admin = thank_auth.is_staff(request)
    if not admin:
        return redirect('login')
    
    domain = EmailsDomains.objects.filter(id=domain_id).first()
    if domain:
        domain.delete()
        return redirect('admin_domain_view')
        
    return redirect('admin_domain_view')   
    
    
def domain_edit(request, domain_id):
    if request.method == "POST": 
        form = DomainsForm(request.POST)
        if form.is_valid():
            domain = EmailsDomains.objects.filter(id=domain_id).update(name=request.POST["name"], domain=request.POST["domain"])
            if domain:
                print("OK")
    return redirect('admin_domain_view')
    
    
def dashboard_view(request):
    iframe = request.GET.get('iframe')
    if iframe or iframe != '':
        dash = f'https://{iframe}'
        print("dash_iframe: ", dash)
        return render(request, 'dashboard.html', {"iframe":dash})
    else:
        return redirect('index')
    
    
def banned_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    return render(request, 'account/banned.html')


def forbidden_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    return render(request, 'account/forbidden.html')


# def get_domains(request, domain_id):
#     domain = EmailsDomains.objects.filter(id=domain_id).first()
#     data = {
#         "name": domain.name,
#         "domain": domain.domain
#     }
#     return JsonResponse(data)