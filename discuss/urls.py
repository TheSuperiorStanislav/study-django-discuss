from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import LoginView,LogoutView
from django.urls import path, include
from django.views.generic import TemplateView

from accounts.views import UserRegistrationView
from links.views import (
    NewSubmissionView,
    SubmissionDetailView
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', TemplateView.as_view(template_name = 'home.html'), name='home'),

    path('login/', LoginView.as_view(template_name = 'login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page = '/login/'), name='logout'),
    path('register/', UserRegistrationView.as_view(), name='user-registration'),

    path('new-submission/', NewSubmissionView.as_view(), name='new-submission'),
    path('submission/<int:pk>/', SubmissionDetailView.as_view(), name='submission-detail'),
]