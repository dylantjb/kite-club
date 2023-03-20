from django import forms
from django.core.validators import RegexValidator
from .models import User, Club, Post, Event

from django.forms.widgets import DateInput, TimeInput

class LogInForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget = forms.PasswordInput())

class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'bio', 'favourite_genre']
        widgets = {'bio': forms.Textarea()}

    new_password = forms.CharField(
        label = 'Password',
        widget = forms.PasswordInput(),
        validators = [RegexValidator(
            regex = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',
            message = 'Password must contain an uppercase character, a lowercase character and a number.'
        )]
    )

    password_confirmation = forms.CharField(label = 'Password confirmation', widget = forms.PasswordInput())

    def clean(self):
        super().clean()
        new_password = self.cleaned_data.get('new_password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if new_password != password_confirmation:
            self.add_error('password_confirmation', 'Confirmation does not match password.')

    def save(self):
        super().save(commit = False)
        user = User.objects.create_user(
            self.cleaned_data.get('username'),
            first_name = self.cleaned_data.get('first_name'),
            last_name = self.cleaned_data.get('last_name'),
            email = self.cleaned_data.get('email'),
            bio = self.cleaned_data.get('bio'),
            favourite_genre = self.cleaned_data.get('favourite_genre'),
            password = self.cleaned_data.get('new_password')
        )
        return user

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'bio', 'favourite_genre']
        widgets = {'bio': forms.Textarea()}

class CreateClubForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ['name','owner', 'theme', 'bio', 'rules']
        widgets = {
            'owner': forms.HiddenInput(attrs = {'is_hidden': True}),
            'bio': forms.Textarea()
        }
        def save(self):
            super().save(commit = False)

            club = Club.objects.create()
            return club

class PostForm(forms.ModelForm):
    """Form to ask user for post text.

    The post author must be by the post creator.
    """

    class Meta:
        """Form options."""

        model = Post
        fields = ['text']
        widgets = {
            'text': forms.Textarea()
        }
    def save(self):
        super().save(commit = False)

        post = Post.objects.create(

        )
        return post

class EventForm(forms.ModelForm):
    """Form to create or update an event"""
    # address = forms.CharField(label='Address', widget=forms.TextInput(attrs={'placeholder': 'Optional'}))
    # eventLink = forms.CharField(label='Event Link', widget=forms.TextInput(attrs={'placeholder': 'Optional'}))

    class Meta:
        """Form options."""

        model = Event
        fields = ['title', 'description', 'date', 'location', 'startTime', 'endTime', 'address', 'eventLink']
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
            'startTime': forms.TimeInput(attrs={'type': 'time'}),
            'endTime': forms.TimeInput(attrs={'type': 'time'})
        }
        
    def clean(self):
        cleaned_data = super().clean()

        address = cleaned_data.get("address")
        event_link = cleaned_data.get("eventLink")

        if address and event_link: # both were entered
            self.add_error('address', 'Your meeting should be online or in person, but cannot be both.')
            self.add_error('eventLink', 'Your meeting should be online or in person, but cannot be both.')
            # raise forms.ValidationError("Your meeting should be online or in person, but cannot be both")
        elif not address and not event_link: # neither were entered
            self.add_error('address', 'Your meeting should be online or in person, but cannot be both.')
            self.add_error('eventLink', 'Your meeting should be online or in person, but cannot be both.')
            # raise forms.ValidationError("Your meeting should be online or in person, but cannot be both")


    def save(self, club):
        """Create a new user."""

        super().save(commit=False)
        event = Event.objects.create(
            club = club,
            title=self.cleaned_data.get('title'),
            description=self.cleaned_data.get('description'),
            #Change admin to current user
            date = self.cleaned_data.get('date'),
            location = self.cleaned_data.get('location'),
            address = self.cleaned_data.get('address'),
            selectedBook = None,
            #selectedBook = self.cleaned_data.get('selectedBook'),
            startTime = self.cleaned_data.get('startTime'),
            endTime = self.cleaned_data.get('endTime'),
            eventLink = self.cleaned_data.get('eventLink'),
        )
        return event