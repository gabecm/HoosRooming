from django import forms
from .models import User
from .models import Message


class PreferencesForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('phone_number', 'bio', 'cleanliness_level', 'noise_level',
                  'morning_preference', 'lease', 'budget', 'image')


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('sender', 'receiver', 'msg_content', 'created_at')
