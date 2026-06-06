from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class ExtendedRegisterForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=150, 
        required=True, 
        label="Ім'я"
    )
    last_name = forms.CharField(
        max_length=150, 
        required=True, 
        label="Прізвище"
    )
    email = forms.EmailField(
        required=True, 
        label="Адреса електронної пошти"
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user