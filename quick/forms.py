from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelMultipleChoiceField
from quick.models import Interest, Profile

__author__ = 'Travis'



class EmailUserCreationForm(UserCreationForm):
    username = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'placeholder': '10 Character Max'}))
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'your@gmail.com'}))
    phone = forms.CharField(max_length=12, widget=forms.TextInput(attrs={'placeholder': '415-555-1111'}))

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "first_name", "last_name", "phone")

    def clean_username(self):
            # Since User.username is unique, this check is redundant,
            # but it sets a nicer error message than the ORM. See #13147.
            username = self.cleaned_data["username"]
            try:
                User.objects.get(username=username)
            except User.DoesNotExist:
                return username
            raise forms.ValidationError(
                self.error_messages['duplicate_username'],
                code='duplicate_username',)


class ProfileCreationForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['oauth_token', 'email', 'user']



