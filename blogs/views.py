
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.views.generic.edit import UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy

from django.conf import settings

from django.core.exceptions import ObjectDoesNotExist

from .forms import CreateClubForm, LogInForm, SignUpForm, UserForm, PostForm, EventForm, BookForm, CommentForm
from .models import Club, User, Post, Book, Event, Comments

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

class UpdateClubView(LoginRequiredMixin, UpdateView):
    model = Club
    form = CreateClubForm
    template_name = "club_settings.html"

    def get(self, request, club_id, *args, **kwargs):
        club = get_object_or_404(Club, id=club_id)
        form = CreateClubForm(instance=club)
        return self.render_to_response(
            {"request": request, "club": club, "form": form}, *args, **kwargs
        )

    def get_success_url(self):
        messages.add_message(
            self.request, messages.SUCCESS, "Your club has been updated successfully!"
        )
        return redirect("club_list") # club may be deleted


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
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
        if Book.objects.all():
            count = Book.objects.count()
            for i in range(0,2):
                random_books.append(Book.objects.all()[randint(0, count - 1)])
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
    user_posts = [post for post in Post.objects.all() if request.user == post.author]
    return render(request, 'profile.html', {'user': user, 'posts': user_posts, 'pending': pending_requests_count(request.user)})

@login_required
def user_profile(request):
    try:
        user = User.objects.get(id=request.user.id)
    except ObjectDoesNotExist:
        raise Http404
    user_posts = [post for post in Post.objects.all() if request.user == post.author]
    return render(request, 'profile.html', {'user': user, 'posts': user_posts, 'pending': pending_requests_count(request.user)})

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
            club = form.save(owner=request.user)
            messages.add_message(request, messages.SUCCESS, "Club created successfully.")
            return redirect('show_club', club_id = club.id) # should take you to the newly created club's page - not implemented yet
        else:
            messages.add_message(request, messages.ERROR, "This club name is already taken, please choose another name.")
    else:
        form = CreateClubForm(initial = {'owner': request.user})
    return render(request, 'create_club.html', {'form': form, 'pending': pending_requests_count(request.user)})

@login_required
def create_event(request, club_id):
    club = Club.objects.get(id=club_id)
    if request.user == club.owner:
        if request.method == 'POST':
            form = EventForm(request.POST)
            if form.is_valid():
                event = form.save(club)
                messages.add_message(request, messages.SUCCESS, "Event created successfully.")
                return redirect('show_club', club_id = event.club.id)
        else:
            form = EventForm()
        return render(request, 'create_event.html', {
            'form': form,
            'club': club,
            'pending': pending_requests_count(request.user)
        })
    else:
        return redirect('show_club', club_id)


@login_required
def attend_event(request, event_id):
    # club = Club.objects.get(id=club_id)
    event = Event.objects.get(id=event_id)
    club = event.club
    # club = Club.objects.get(id=event.club.id)
    if request.user in club.members.all() or request.user in club.admins.all():
        if request.user not in event.attendees.all():
            event.attendees.add(request.user)
        else:
            event.attendees.remove(request.user)
    return redirect('show_club', club_id = club.id)

@login_required
def add_comment(request, post_id):
    post = Post.objects.get(id=post_id)
    current_user = request.user
    post_user = post.author
    club = post.in_club
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data.get('text')
            comment = Comments.objects.create(post=post, club=club, author=current_user, commented_user = post_user, text=text)
        return redirect('show_club', club_id = club.id)
    else:
        form = CommentForm()
    return redirect('show_club', club_id = club.id)
    


@login_required
def club_list(request):
    clubs = Club.objects.all()
    return render(request, 'club_list.html', {'clubs': clubs, 'pending': pending_requests_count(request.user)})

@login_required
def club(request, club_id):
    try:
        club = Club.objects.get(id=club_id)
        posts = Post.objects.filter(in_club=club).prefetch_related('comments')
        events = Event.objects.filter(club=club)
        comments = Comments.objects.filter(club=club)
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
                    return render(request, 'club_page.html', {'club': club, 'form': form, 'posts': posts})
            else:
                return redirect('log_in')
        form = PostForm()
        comment_form = CommentForm()
        applied = False
        is_member = False
        active_users = active_count(club)
        if request.user in club.members.all():
            is_member = True
        if request.user in club.pending_members.all():
            applied = True
        return render(request, 'club_page.html', {'club': club,
                                                  'events': events,
                                                  'form': form,
                                                  'comment_form': comment_form,
                                                  'posts': posts,
                                                  'applied': applied,
                                                  'is_member': is_member,
                                                  'current_user': request.user,
                                                  'current_book': club.book,
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
    except ObjectDoesNotExist as exc:
        raise Http404 from exc

    if request.user in (club.owner, club.admins.all()) and requesting_user in club.pending_members.all():
        club.pending_members.remove(requesting_user)
        club.members.add(requesting_user)
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def admin_decline_request(request, club_id, user_id):
    try:
        club = Club.objects.get(id=club_id)
        requesting_user = User.objects.get(id=user_id)
    except ObjectDoesNotExist as exc:
        raise Http404 from exc

    if request.user in (club.owner, club.admins.all()):
        club.pending_members.remove(requesting_user)
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def pending_requests(request, club_id):
    club = Club.objects.get(id=club_id)
    pending = club.pending_members.all()
    return render(request, 'pending_requests.html', {'pending':pending, 'club': club})

@login_required
def all_pending_requests(request):
    pending = {}
    for club in Club.objects.all():
        if request.user in (club.owner, club.admins.all()):
            pending.update({club: club.pending_members})
    return render(request, 'pending_all_requests.html', {'pending': pending})

@login_required
def featured_book(request, club_id):
    club = Club.objects.get(id=club_id)
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():

            featured_book = form.save(request.user)
            club.book = featured_book

            club.save()
            messages.add_message(request, messages.SUCCESS, "Added featured book.")
            return redirect('show_club', club_id=club_id)
    else:
        form = BookForm()
        return render(request, 'create_featured_book.html', {
            'form': form,
            'club': club,
            'pending': pending_requests_count(request.user)
        })


@login_required
def promote_admin(request, club_id, user_id):
    club = get_object_or_404(Club, id=club_id)
    user = get_object_or_404(club.admins, id=user_id)
    if request.user != club.owner:
        return redirect("home")
    if request.method == "POST":
        club.admins.add(request.user)
        club.admins.remove(user)
        print(club.owner)
        club.owner = user
        club.save()
        messages.success(request, f'{user.first_name} {user.last_name} has been promoted to owner.')
    return redirect("club_settings", club.id)

@login_required
def demote_admin(request, club_id, user_id):
    club = get_object_or_404(Club, id=club_id)
    user = get_object_or_404(club.admins, id=user_id)
    if request.user != club.owner:
        return redirect("home")
    if request.method == "POST":
        club.admins.remove(user)
        club.members.add(user)
        club.save()
        messages.success(request, f'{user.first_name} {user.last_name} has been demoted to member.')
    return redirect("club_settings", club.id)

@login_required
def promote_user(request, club_id, user_id):
    club = get_object_or_404(Club, id=club_id)
    user = get_object_or_404(club.members, id=user_id)
    if request.user not in (club.admins.all(), club.owner):
        return redirect("home")
    if request.method == "POST":
        club.admins.add(user)
        club.members.remove(user)
        club.save()
        messages.success(request, f'{user.first_name} {user.last_name} has been promoted to admin.')
    return redirect("club_settings", club.id)

@login_required
def kick_user(request, club_id, user_id):
    club = get_object_or_404(Club, id=club_id)
    user = get_object_or_404(club.members, id=user_id)
    if request.user not in (club.admins.all(), club.owner):
        return redirect("home")
    if request.method == "POST":
        club.members.remove(user)
        club.save()
        messages.success(request, f'{user.first_name} {user.last_name} has been kicked from the club.')
    return redirect("club_settings", club.id)


@login_required
def delete_club(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    if request.user != club.owner:
        return redirect("home")
    if request.method == "POST":
        club.delete()
    return redirect("club_list")

@login_required
def delete_user(request):
    if request.method == "POST":
        password = request.POST.get('deleteAccountPassword')
        user = authenticate(username=request.user.username, password=password)
        if user:
            request.user.delete()
            messages.success(request, 'Your account has been deleted.')
            return log_out(request)
        messages.error(request, "Invalid password.")
        return redirect("account_details")
    return redirect("home")


@login_required
def leave_club(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    if request.user in club.members.all():
        club.members.remove(request.user)
    elif request.user in club.admins.all():
        club.admins.remove(request.user)
    return redirect("club_page", club_id)



# def searchbar(request, search_string):
#     club_name = search_string[6:]

#     try:
#         print(club_name)
#         club = Club.objects.filter(name = club_name).first()
#         print(club)
#         club_id = club.id
#         print(club_id)
#         return redirect('club_dashboard', club.id)
#     except:
#         messages.error(request, "Sorry we cant find this club. ")

#     return redirect('user_dashboard', club.id)


