from django.shortcuts import render, redirect
from .forms import SignUpForm, CreateClubForm

def feed(request):
    return render(request, 'feed.html')

def home(request):
    return render(request, 'home.html')

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('feed')

    else:
        form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form})

def create_club(request):
    if request.method == 'POST':
        form = CreateClubForm(request.POST)
        if form.is_valid():
            #club = form.save(commit=False)
            club = form.save()
            club.admins.add(request.user)
            club.members.add(request.user)
            return redirect('feed') # should take you to the newly created club's page - not implemented yet

    form = CreateClubForm()
    return render(request, 'create_club.html', {'form': form})
