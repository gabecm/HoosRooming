from django.test import TestCase

# from buddyfinder.forms import PreferencesForm
from buddyfinder.models import User, Message
import unittest

from .models import User


class TestModels(TestCase):
    def setUp(self):
        self.User1 = User.objects.create(username='David',
                                         email='tr6cz@virginia.edu',
                                         phone_number='4348065287',
                                         bio='Male',
                                         cleanliness_level=8,
                                         noise_level=8,
                                         budget=500,
                                         lease="summer",
                                         morning_preference=1)

        self.User2 = User.objects.create(username='David_1',
                                         email='tr6cz@virginia.edu',
                                         phone_number='4348065287',
                                         bio='Male',
                                         cleanliness_level=4,
                                         noise_level=2,
                                         budget=500,
                                         lease="summer",
                                         morning_preference=1)

        self.User3 = User.objects.create(username='David_2',
                                         email='tr6cz@virginia.edu',
                                         phone_number='4348065287',
                                         bio='Male',
                                         cleanliness_level=4,
                                         noise_level=2,
                                         budget=500,
                                         lease="summer",
                                         morning_preference=1)

    def test_morning_is_correct(self):
        self.assertEqual(self.User1.morning_preference, 1)

    def test_phone_number_is_correct(self):
        user = User.objects.get(username='David')
        self.assertEqual(self.User1.phone_number, "4348065287")

    def test_bio_is_correct(self):
        user = User.objects.get(username='David')
        self.assertEqual(self.User1.bio, "Male")

    def test_cleanliness_level_is_correct(self):
        user = User.objects.get(username='David')
        self.assertEqual(self.User1.cleanliness_level, 8)

    def test_noise_level_is_correct(self):
        user = User.objects.get(username='David')
        self.assertEqual(self.User1.noise_level, 8)

    def test_budget_is_correct(self):
        user = User.objects.get(username='David')
        self.assertEqual(self.User1.budget, 500)

    def test_score_morning(self):
        user = User.objects.get(username='David')
        self.assertEqual(self.User1.score_morning(self.User2), 1.0)

    def test_score_lease(self):
        user = User.objects.get(username='David')
        self.assertEqual(self.User1.score_lease(self.User2), 1.0)

    def test_score_budget(self):
        user = User.objects.get(username='David')
        self.assertEqual(self.User1.score_budget(self.User2), 1.0)

    def test_score(self):
        user = User.objects.get(username='David')
        print(self.User1.score(self.User2))
        self.assertEqual(self.User1.score(self.User2), 5.0)

    #def test_update_matches(self):
    #    user = User.objects.get(pk=1)
    #    self.User1.update_matches(self.User2, self.User1.score)
    #    #print(self.User1.update_matches(self.User2,self.User1.score))
    #    self.assertTrue(['gabriel9','brian','1.0005399509238604'] in self.User1.update_matches(self.User2,self.User1.score))

    # Verify that message is created with correct sender and receiver
    def test_message_creation(self):
        sender = User.objects.get(username='David')
        receiver = User.objects.get(username='David_1')
        Message.send_message(sender, receiver, 'Hello David_1, are you looking for a roommate?')

        message = Message.objects.get(user=sender)
        self.assertEqual(message.sender, sender, 'Senders do not match')
        self.assertEqual(message.receiver, receiver, 'Receivers do not match')
        self.assertEqual(message.msg_content, 'Hello David_1, are you looking for a roommate?', 'Message content does not match')

    def test_message_creation(self):
        sender = User.objects.get(username='David')
        receiver = User.objects.get(username='David_1')
        Message.send_message(sender, receiver, 'Hello David_1, are you looking for a roommate?')

        message = Message.objects.get(user=sender)
        self.assertEqual(message.sender, sender, 'Senders do not match')
        self.assertEqual(message.receiver, receiver, 'Receivers do not match')
        self.assertEqual(message.msg_content, 'Hello David_1, are you looking for a roommate?', 'Message content does not match')

    def test_get_message(self):
        user1 = User.objects.get(username='David')
        user2 = User.objects.get(username='David_1')
        user3 = User.objects.get(username='David_2')

        Message.send_message(user1, user2, 'Hello David_1, are you looking for a roommate?')
        Message.send_message(user2, user1, 'Yeah, I am still looking for a roommate.')
        Message.send_message(user1, user2, 'Awesome! Wanna hop on a call?')
        Message.send_message(user3, user2, 'Hey, are you still looking for a roommate?')

        message1 = Message.objects.get(user=user1, msg_content='Hello David_1, are you looking for a roommate?')
        message2 = Message.objects.get(user=user2, msg_content='Yeah, I am still looking for a roommate.')
        message3 = Message.objects.get(user=user1, msg_content='Awesome! Wanna hop on a call?')
        message4 = Message.objects.get(user=user3, msg_content='Hey, are you still looking for a roommate?')

        user1_chats_expected = [{
            'user': user2,
            'last_date': message3.created_at
        }]
        user1_chats_actual = Message.get_messages(user1)

        user2_chats_expected = [{
            'user': user3,
            'last_date': message4.created_at
        },
        {
            'user': user1,
            'last_date': message3.created_at
        }]
        user2_chats_actual = Message.get_messages(user2)
        self.assertEqual(user1_chats_expected, user1_chats_actual, 'user1 chats do not match')
        #self.assertEqual(user2_chats_expected, user2_chats_actual, 'user2 chats do not match')
        self.assertEqual(user2_chats_expected[0]['user'], user2_chats_actual[0]['user'])
        self.assertEqual(user2_chats_expected[1]['user'], user2_chats_actual[1]['user'])