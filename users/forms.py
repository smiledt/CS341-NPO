from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from users.models import UserAccountInfo


class UserForm(forms.ModelForm):
    """ This is the default user form """
    password = forms.CharField(
        widget=forms.PasswordInput(), label='Password:')
    password2 = forms.CharField(
        widget=forms.PasswordInput(), label='Confirm Password:')
    email = forms.EmailField(max_length=254, help_text="Valid email address.")

    # Validation
    def clean(self):
        all_clean_data = super().clean()
        password = all_clean_data['password']
        password2 = all_clean_data['password2']

        if password != password2:
            raise forms.ValidationError(
                "Please ensure that the passwords match.")

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password', 'password2')


class UserAccountForm(forms.ModelForm):
    """ This is the adtional information about the user type (donor or volunteer) """
    class Meta:
        model = UserAccountInfo
        fields = ('job',)

class DeleteAccountForm(forms.Form):
    username = forms.CharField(required=True)
