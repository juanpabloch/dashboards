from django.urls import path, include
from .views import (
    index_view,  
    admin_redirect,
    admin_user_view,
    admin_dashboard_view,
    dashboard_edit,
    dashboard_create, 
    dashboard_delete, 
    dashboard_deactivate,
    dashboard_activate,
    user_activate,
    user_banned,
    user_edit,
    user_delete,
    banned_view,
    pruebas
)
from django.contrib.auth.views import LogoutView, LoginView

urlpatterns = [
    path('', index_view, name='index'),
    path('admin/', admin_redirect),
    path('accounts/', include('allauth.urls')),
    path('accounts/login/', LoginView.as_view(template_name="account/login.html"), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('accounts/banned/', banned_view, name='banned'),
    
    path('admin/dashboards/', admin_dashboard_view, name='admin_dashboard_view'),
    path('admin/dashboards/create/', dashboard_create, name='dashboard_create'),
    path('admin/dashboards/edit/<int:dashboard_id>/', dashboard_edit, name='dashboard_edit'),
    path("admin/dashboards/activate/<int:dashboard_id>/", dashboard_activate, name="dashboard_activate"),
    path("admin/dashboards/delete/<int:dashboard_id>/", dashboard_delete, name="dashboard_delete"),
    path("admin/dashboards/deactivate/<int:dashboard_id>/", dashboard_deactivate, name="dashboard_deactivate"),
    
    path("admin/user/", admin_user_view, name="admin_user_view"),
    path("admin/user/activate/<int:user_id>/", user_activate, name="user_activate"),
    path("admin/user/edit/<int:user_id>/", user_edit, name="user_edit"),
    path("admin/user/delete/<int:user_id>/", user_delete, name="user_delete"),
    path("admin/user/banned/<int:user_id>/", user_banned, name="user_banned"),
    
    path('pruebas/', pruebas, name='pruebas')
]