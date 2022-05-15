from django.urls import path, include
from .views import index_view
from django.contrib.auth.views import LogoutView, LoginView

urlpatterns = [
    path('', index_view, name='index'),
    path('accounts/', include('allauth.urls')),
    path('accounts/login/', LoginView.as_view(template_name="account/login.html"), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
]