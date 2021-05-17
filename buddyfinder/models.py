from cloudinary.models import CloudinaryField
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Max
from django.utils import timezone

import csv

# Create your models here.

path = 'buddyfinder/matches.csv'


# User account model
# Extends Django User Model (username, first_name, last_name, and email fields)
# Adds phone_number, bio, cleanliness_level, noise_level, morning_preference, lease, and budget fields
class User(AbstractUser):
    phone_number = models.CharField(max_length=12)
    bio = models.TextField(default="Please update your bio!")
    cleanliness_level = models.CharField(max_length=200, default="Neutral")
    noise_level = models.CharField(max_length=200, default="Neutral")
    morning_preference = models.CharField(max_length=200, default="Neutral")
    lease = models.CharField(max_length=200)
    budget = models.IntegerField(default=500)
    image = CloudinaryField('image', default="wyy3pna3gxgiafzyvn4g")
    spotify_song = models.CharField(max_length=100, default="", blank=True)
    spotify_artist = models.CharField(max_length=100, default="", blank=True)
    spotify_link = models.CharField(max_length=64, default="", blank=True)

    # Can also do album cover later.

    def score(self, User1):
        score = self.score_morning(User1) + self.noise_lvl(User1) + self.score_cleanliness(
            User1) + (3 * self.score_budget(User1)) + self.score_lease(User1)
        self.update_matches(User1, score)
        return score

    def score_all(self):
        for user in User.objects.all():
            if self != user:
                self.score(user)
        return

    def get_scores(self):
        match_list = list()
        exists = False
        with open(path, mode='r') as match_file_r:
            match_reader = csv.reader(match_file_r, delimiter=',')
            for row in match_reader:
                if self.username in row:
                    if self.username == row[0] and self.username != row[1] and row[3] == 'n' and row[4] != 'r':
                        other_user = User.objects.get(username=row[1])
                        match_list.append(
                            [other_user, round(float(row[2]) / 0.07, 2)])
                    if self.username == row[1] and self.username != row[0] and row[3] != 'r' and row[4] == 'n':
                        other_user = User.objects.get(username=row[0])
                        match_list.append(
                            [other_user, round(float(row[2]) / 0.07, 2)])
        ordered_matches = sorted(match_list, key=lambda l: l[1], reverse=True)
        for match in ordered_matches:
            match[1] = str(match[1])
        return ordered_matches

    def get_favorites(self):
        match_list = list()
        exists = False
        with open(path, mode='r') as match_file_r:
            match_reader = csv.reader(match_file_r, delimiter=',')
            for row in match_reader:
                if self.username in row:
                    if self.username == row[0] and self.username != row[1] and row[3] == 'a' and row[4] == 'a':
                        other_user = User.objects.get(username=row[1])
                        match_list.append(
                            [other_user, round(float(row[2]) / 0.07, 2)])
                    if self.username == row[1] and self.username != row[0] and row[3] == 'a' and row[4] == 'a':
                        other_user = User.objects.get(username=row[0])
                        match_list.append(
                            [other_user, round(float(row[2]) / 0.07, 2)])
        ordered_matches = sorted(match_list, key=lambda l: l[1], reverse=True)
        for match in ordered_matches:
            match[1] = str(match[1])
        return ordered_matches

    def get_pending(self):
        match_list = list()
        exists = False
        with open(path, mode='r') as match_file_r:
            match_reader = csv.reader(match_file_r, delimiter=',')
            for row in match_reader:
                if self.username in row:
                    if self.username == row[0] and self.username != row[1] and row[3] == 'a' and row[4] == 'n':
                        other_user = User.objects.get(username=row[1])
                        match_list.append(
                            [other_user, round(float(row[2]) / 0.07, 2)])
                    if self.username == row[1] and self.username != row[0] and row[3] == 'n' and row[4] == 'a':
                        other_user = User.objects.get(username=row[0])
                        match_list.append(
                            [other_user, round(float(row[2]) / 0.07, 2)])
        ordered_matches = sorted(match_list, key=lambda l: l[1], reverse=True)
        for match in ordered_matches:
            match[1] = str(match[1])
        return ordered_matches

    def update_matches(self, User2, score):
        rows = list()
        exists = False
        with open(path, mode='r') as match_file_r:
            match_reader = csv.reader(match_file_r, delimiter=',')
            for row in match_reader:
                if not (self.username in row and User2.username in row):
                    rows.append(row)
                else:
                    exists = True
                    rows.append([row[0], row[1], score, row[3], row[4]])
            if not exists:
                rows.append([self.username, User2.username, score, 'n', 'n'])
        with open(path, mode='w', newline='') as match_file_w:
            match_writer = csv.writer(match_file_w, delimiter=',')
            for row in rows:
                match_writer.writerow(row)
        return

    def manage(self, User2, action):
        rows = list()
        exists = False
        with open(path, mode='r') as match_file_r:
            match_reader = csv.reader(match_file_r, delimiter=',')
            for row in match_reader:
                if not (self.username in row and User2 in row):
                    rows.append(row)
                else:
                    exists = True
                    if self.username == row[0]:
                        rows.append([row[0], row[1], row[2], action, row[4]])
                    if self.username == row[1]:
                        rows.append([row[0], row[1], row[2], row[3], action])
            if not exists:
                rows.append([self.username, User2, '0.0', action, 'n'])
        with open(path, mode='w', newline='') as match_file_w:
            match_writer = csv.writer(match_file_w, delimiter=',')
            for row in rows:
                match_writer.writerow(row)
        return

    def score_morning(self, User1):
        if self.morning_preference == User1.morning_preference:
            return 1
        else:
            return 0

    def score_lease(self, User1):
        if self.lease == User1.lease:
            return 1
        else:
            return 0

    def score_cleanliness(self, User1):
        if self.cleanliness_level == User1.cleanliness_level:
            return 1
        else:
            return 0

    def noise_lvl(self, User1):
        if self.noise_level == User1.noise_level:
            return 1
        else:
            return 0

    def score_budget(self, User1):
        if self.budget > User1.budget:
            score = (self.budget - User1.budget) / self.budget
        else:
            score = (User1.budget - self.budget) / User1.budget
        return 1 - score


# ************************************************************************
#   Title: Instagram clone in Django
#   Author: Bryon Lara
#   Date: April 18, 2021
#   URL: https://github.com/byronlara5/django_instagram_clone_youtube
#   Tutorial URL: https://www.youtube.com/watch?v=YYSx4xD7wfE
# ************************************************************************
class Message(models.Model):
    user = models.ForeignKey(User, related_name="user",
                             on_delete=models.CASCADE, null=True)
    sender = models.ForeignKey(
        User, related_name="sender", on_delete=models.CASCADE, null=True)
    receiver = models.ForeignKey(
        User, related_name="receiver", on_delete=models.CASCADE, null=True)
    msg_content = models.TextField(max_length=500, null=True)
    created_at = models.DateTimeField(
        auto_now=False, auto_now_add=False, null=True)

    # Site Instagram clone later
    def send_message(from_user, to_user, content):
        senders_message = Message(
            user=from_user,
            sender=from_user,
            receiver=to_user,
            msg_content=content,
            created_at=timezone.now()
        )
        receivers_message = Message(
            user=to_user,
            sender=from_user,
            receiver=from_user,
            msg_content=content,
            created_at=timezone.now()
        )
        senders_message.save()
        receivers_message.save()
        return senders_message

    def get_messages(user):
        user_messages = Message.objects.filter(user=user).values('receiver').annotate(
            last_date=Max('created_at')).order_by('-last_date')
        chats = []
        for message in user_messages:
            chats.append({
                'user': User.objects.get(pk=message['receiver']),
                'last_date': message['last_date']
            })

        return chats
