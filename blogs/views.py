
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.views.generic.edit import UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import redirect, render
from django.urls import reverse_lazy


from django.core.exceptions import ObjectDoesNotExist


from .forms import CreateClubForm, LogInForm, SignUpForm, UserForm, PostForm
from .models import Club, User, Post, books
from .helpers import login_prohibited, active_count

from random import randint


"""SETUP"""
def pending_requests_count(user):
    pending =[]
    clubs = Club.objects.filter(owner = user)
    for club in clubs:
        for p_member in club.pending_members.all():
            pending.append(p_member)
    return len(pending)

class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = form_class = UserForm
    template_name = "account_details.html"
    extra_context = {"nbar": "account"}

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        messages.add_message(
            self.request, messages.SUCCESS, "Your profile updated successfully!"
        )
        return reverse_lazy("home")



class ChangePasswordView(LoginRequiredMixin, SuccessMessageMixin, PasswordChangeView):
    template_name = "change_password.html"
    success_url = reverse_lazy("home")
    extra_context = {"nbar": "password"}

    def get_success_url(self):
        messages.add_message(
            self.request, messages.SUCCESS, "Your password changed successfully!"
        )
        return reverse_lazy("home")


def home(request):
    if request.user.is_authenticated:
        random_books = []
        clubs = Club.objects.all()
        count = books.objects.count()
        for i in range(0,2):
            random_books.append(books.objects.all()[randint(0, count - 1)])
        return render(request, 'feed.html', {'clubs': clubs, 'pending': pending_requests_count(request.user), 'random_books': random_books})
    return render(request, 'home.html', {'form': LogInForm()})

def about(request):
    return render(request, 'about.html')

@login_required
def profile(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except ObjectDoesNotExist:
        raise Http404
    return render(request, 'profile.html', {'user': user, 'pending': pending_requests_count(request.user)})

@login_prohibited
def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(form.cleaned_data['password_confirmation'])
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form})

@login_prohibited
def log_in(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username, password = password)
            if user is not None:
                login(request, user)
                return redirect('home')
            messages.add_message(request, messages.ERROR, "The credentials provided were invalid!")
    return render(request, 'log_in.html', {'form': LogInForm()})



@login_required
def log_out(request):
    logout(request)
    return redirect('home')

@login_required
def create_club(request):
    if request.method == 'POST':
        form = CreateClubForm(request.POST)
        if form.is_valid():
            club = form.save()
            messages.add_message(request, messages.SUCCESS, "Club created successfully.")
            club.admins.add(request.user)
            club.members.add(request.user)
            return redirect('show_club', club_id = club.id) # should take you to the newly created club's page - not implemented yet
        else:
            messages.add_message(request, messages.ERROR, "This club name is already taken, please choose another name.")
    else:
        form = CreateClubForm(initial = {'owner': request.user})
    return render(request, 'create_club.html', {'form': form, 'pending': pending_requests_count(request.user)})

@login_required
def club_list(request):
    clubs = Club.objects.all()
    return render(request, 'club_list.html', {'clubs': clubs, 'pending': pending_requests_count(request.user)})

@login_required
def joined_club_list(request, user_id):
    user = User.objects.get(id=user_id)
    clubs = Club.objects.filter(member_of = user)
    return render(request, 'club_list.html', {'clubs': clubs})

@login_required
def club(request, club_id):
    try:
        club = Club.objects.get(id=club_id)
        posts = Post.objects.filter(in_club = club)
    except ObjectDoesNotExist:
        return redirect('club_list')
    else:
        if request.method == 'POST':
            if request.user.is_authenticated:
                current_user = request.user
                form = PostForm(request.POST)
                if form.is_valid():
                    text = form.cleaned_data.get('text')
                    post = Post.objects.create(author=current_user, text=text, in_club=club)
                    return redirect('show_club', club_id)
                else:
                    return render(request, 'club_page.html', {'club': club, 'form': form, 'post': post})
            else:
                return redirect('log_in')
        form = PostForm()
        applied = False
        is_member = False
        active_users = active_count(club)
        if request.user in club.members.all():
            is_member = True
        if request.user in club.pending_members.all():
            applied = True
            return render(request, 'club_page.html', {'club': club, 'form': form, 'posts': posts, 'applied' : applied, 'is_member' : is_member, 'pending': pending_requests_count(request.user)})
        return render(request, 'club_page.html', {'club': club, 
                                                  'form': form, 
                                                  'posts': posts, 
                                                  'applied' : applied, 
                                                  'is_member' : is_member,
                                                  'current_user': request.user,
                                                  'active_users': active_users,
                                                  'pending': pending_requests_count(request.user)})
    
@login_required
def join_request_club(request, club_id):
    club = Club.objects.get(id=club_id)
    current_user = request.user
    club.pending_members.add(current_user)
    messages.add_message(request, messages.SUCCESS, "Join request sent.")
    return redirect('show_club', club_id = club_id)

        
@login_required
def cancel_request(request, club_id):
    club = Club.objects.get(id=club_id)
    current_user = request.user
    club.pending_members.remove(current_user)
    return redirect('show_club', club_id = club_id)

@login_required
def admin_accept_request(request, club_id, user_id):
    try:
        club = Club.objects.get(id=club_id)
        requesting_user = User.objects.get(id=user_id)
        if request.user == club.owner and requesting_user in club.pending_members.all():
            club.pending_members.remove(requesting_user)
            club.members.add(requesting_user)
    except ObjectDoesNotExist:
        raise Http404
    else:
        return redirect('show_club', club_id = club_id)
    
@login_required
def pending_requests(request, club_id):
    club= Club.objects.get(id=club_id)
    pending = club.pending_members.all()
    return render(request, 'pending_requests.html', {'pending':pending, 'club': club}) 

    
@login_required
def all_pending_requests(request):
    pending ={}
    counted = 0
    current_user = request.user
    clubs = Club.objects.filter(owner = current_user)
    for club in clubs:
        pending[club] = list(club.pending_members.all())
        # pending.append(club.pending_members.all())

    return render(request, 'pending_all_requests.html', {'pending':pending, 'count': pending_requests_count(current_user), 'counted': counted}) 

