from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import LoginView,LogoutView
from django.urls import path, include
from django.views.generic import TemplateView

from accounts.views import UserRegistrationView
from links.views import (
    HomeView,
    NewSubmissionView,
    SubmissionDetailView,
    NewCommentView,
    NewCommentReplyView,
    UpvoteSubmissionView,
    RemoveUpvoteSubmissionView,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', HomeView.as_view(), name='home'),

    path('login/', LoginView.as_view(template_name = 'login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page = '/login/'), name='logout'),
    path('register/', UserRegistrationView.as_view(), name='user-registration'),

    path('new-submission/', NewSubmissionView.as_view(), name='new-submission'),
    path('submission/<int:pk>/', SubmissionDetailView.as_view(), name='submission-detail'),
    path('new-comment/', NewCommentView.as_view(), name='new-comment'),
    path('new-comment-reply/', NewCommentReplyView.as_view(), name='new-comment-reply'),
    path('upvote/<int:pk>/', UpvoteSubmissionView.as_view(), name='upvote-submission'),
    path('upvote/<int:pk>/remove/', RemoveUpvoteSubmissionView.as_view(), name='remove-upvote'),
]