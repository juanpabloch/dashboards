from django.urls import path, include
from .views import index_view, admin_index, dashboard_create, dashboard_delete
from django.contrib.auth.views import LogoutView, LoginView

urlpatterns = [
    path('', index_view, name='index'),
    path('admin/', admin_index, name='admin_index'),
    path('accounts/', include('allauth.urls')),
    path('accounts/login/', LoginView.as_view(template_name="account/login.html"), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    
    path('admin/dashboard/create/', dashboard_create, name='dashboard_create'),
    path("admin/dashboard/delete/<int:dashboard_id>/", dashboard_delete, name="dashboard_delete"),
]