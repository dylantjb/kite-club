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
    path('club/<int:club_id>', views.club, name = 'show_club'),
    path('club/<int:club_id>/settings', views.UpdateClubView.as_view(), name='club_settings'),
    path('clubs/', views.club_list, name='club_list'),
    path('create_club/', views.create_club, name = 'create_club'),
    path('join-request/<int:club_id>', views.join_request_club, name = 'join_request_club'),
    path('cancel-request/<int:club_id>', views.cancel_request, name = 'cancel_request'),
    path('user/<int:user_id>', views.profile, name = 'profile'),
    path('pending-users/<int:club_id>', views.pending_requests, name = 'pending_requests'),
    path('pending-users', views.all_pending_requests, name = 'all_pending_requests'),
    path('accept-request/<int:club_id>/<int:user_id>', views.admin_accept_request, name = 'admin_accept_request'),
    # club actions
    path('club/<int:club_id>/promote_admin/<int:user_id>/', views.promote_admin, name='promote_admin'),
    path('club/<int:club_id>/promote_user/<int:user_id>/', views.promote_user, name='promote_user'),
    path('club/<int:club_id>/demote_admin/<int:user_id>/', views.demote_admin, name='demote_admin'),
    path('club/<int:club_id>/kick_user/<int:user_id>/', views.kick_user, name='kick_user'),
    path('club/<int:club_id>/delete_club', views.delete_club, name='delete_club'),

    #events
    path('create_event/<int:club_id>', views.create_event, name='create_event'),
    path('attend_event/<int:event_id>', views.attend_event, name='attend_events'),
    # path('unattend_event/<int:event_id>', views.unattend_event, name='unattend_events'),
    #posts
    # path('new_post/', views.new_post, name='new_post'),
    #user profile
    # path("profile/", views.profile, name="profile"),

    path("accounts/account-details/", views.UpdateProfileView.as_view(), name="account_details"),
    path(
        "accounts/change-password/", views.ChangePasswordView.as_view(), name="change_password"
    ),
    path("accounts/account-details/delete", views.delete_user, name="delete_user"),
    # path("<username>/", views.profile, name = 'profile'),
    #BOOKS
    path("featured_book/<int:club_id>", views.featured_book, name="featured_book"),
    # path("book_list/<int:club_id>", views.book_list, name="book_list"),
   
    # path("book_choice/<int:club_id>/<int:book_id>", views.book_choice, name="book_choice")
]

