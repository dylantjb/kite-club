"""BookClub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from blogs import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name = 'home'),
    path('about/', views.about, name = 'about'),
    path('sign_up/', views.sign_up, name = 'sign_up'),
    path('log_in/', views.log_in, name = 'log_in'),
    path('log_out/', views.log_out, name = 'log_out'),
    #club paths
    path('create_club/', views.create_club, name = 'create_club'),
    path('club/<int:club_id>', views.club, name = 'show_club'),
    path('join-request/<int:club_id>', views.join_request_club, name = 'join_request_club'),
    path('cancel-request/<int:club_id>', views.cancel_request, name = 'cancel_request'),
    path('user/<int:user_id>', views.profile, name = 'profile'),
    path('clubs/', views.club_list, name='club_list'),
    path('pending-users/<int:club_id>', views.pending_requests, name = 'pending_requests'),
    path('pending-users', views.all_pending_requests, name = 'all_pending_requests'),
    path('accept-request/<int:club_id>/<int:user_id>', views.admin_accept_request, name = 'admin_accept_request'),
    path('create_event/<int:club_id>', views.create_event, name='create_event'),
    #posts
    # path('new_post/', views.new_post, name='new_post'),
    #user profile
    # path("profile/", views.profile, name="profile"),

    path("accounts/account-details/", views.UpdateProfileView.as_view(), name="account_details"),
    path(
        "accounts/change-password/", views.ChangePasswordView.as_view(), name="change_password"
    ),
    # path("<username>/", views.profile, name = 'profile'),

]

