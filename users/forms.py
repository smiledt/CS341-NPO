from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, help_text="Valid email address.")
    phoneNumber = forms.CharField(
        max_length=12, required=False, help_text="Optional")
    job = forms.CharField(max_length=10, required=True,
                          help_text="Volunteer or Donor")

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',
                  'phoneNumber', 'job', 'password1', 'password2')

class DeleteAccountForm(forms.Form):
    username = forms.CharField()

# class SummaryForm(forms.Form):
#     username = forms.CharField()

