from django.core.exceptions import ObjectDoesNotExist
from .models import Club, User

class UserCommandslub:
    def __init__(self, owner_username: str):
        self.owner = owner_username
        self.members = [owner_username]
        self.admins = [owner_username]
        self.visibility = 'private'
        self.posts = []
        self.reminders = []

    def invite_user(self, username: str) -> None:
        if self.owner == username or username in self.admins:
            self.members.append(username)

    def remove_user(self, username: str) -> None:
        if self.owner == username or username in self.admins:
            if username in self.members:
                self.members.remove(username)
                self.admins.remove(username)
                try:
                    user = User.objects.get(username=username)
                    club = Club.objects.get(name=self.name)
                    club.members.remove(user)
                    club.admins.remove(user)
                except ObjectDoesNotExist:
                    pass

    def make_admin(self, username: str) -> None:
        if self.owner == username or self.owner in self.admins:
            if username in self.members and username not in self.admins:
                self.admins.append(username)
                try:
                    user = User.objects.get(username=username)
                    club = Club.objects.get(name=self.name)
                    club.admins.add(user)
                except ObjectDoesNotExist:
                    pass

    def remove_admin(self, username: str) -> None:
        if self.owner == username or self.owner in self.admins:
            if username in self.admins and len(self.admins) > 1:
                self.admins.remove(username)
                try:
                    user = User.objects.get(username=username)
                    club = Club.objects.get(name=self.name)
                    club.admins.remove(user)
                except ObjectDoesNotExist:
                    pass

    def set_visibility(self, visibility: str) -> None:
        if self.owner in self.admins:
            if visibility in ['public', 'private']:
                self.visibility = visibility
                try:
                    club = Club.objects.get(name=self.name)
                    club.visibility = visibility
                    club.save()
                except ObjectDoesNotExist:
                    pass

    def add_post(self, author: str, content: str) -> None:
        if self.owner == author or author in self.admins:
            self.posts += ({'author': author, 'content': content, 'likes': []},)
            try:
                club = Club.objects.get(name=self.name)
                club.post_set.create(author=author, content=content)
            except ObjectDoesNotExist:
                pass

    def like_post(self, index: int, username: str) -> None:
        if username in self.members and index < len(self.posts):
            post = self.posts[index]
            if username not in post['likes']:
                post['likes'].append(username)
                try:
                    club = Club.objects.get(name=self.name)
                    post = club.post_set.get(id=index+1)
                    user = User.objects.get(username=username)
                    post.likes.add(user)
                except ObjectDoesNotExist:
                    pass

    def unlike_post(self, index: int, username: str) -> None:
        if username in self.members and index < len(self.posts):
            post = self.posts[index]
            if username in post['likes']:
                post['likes'].remove(username)
                try:
                    club = Club.objects.get(name=self.name)
                    post = club.post_set.get(id=index+1)
                    user = User.objects.get(username=username)
                    post.likes.remove(user)
                except ObjectDoesNotExist:
                    pass

    def add_reminder(self, author: str, content: str) -> None:
        if author == self.owner:
            self.reminders += [{'author': author, 'content': content}]
            try:
                club = Club.objects.get(name=self.name)
                club.reminder_set.create(author=author, content=content)
            except ObjectDoesNotExist:
                pass
        else:
            print("Only the club owner can create meeting reminders.")
