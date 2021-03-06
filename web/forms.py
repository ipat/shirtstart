from django import forms
# from django.core.excpetions import ValidationError

from web.models import *
class DateInput(forms.DateInput):
    input_type = 'date'

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password')

class UserProfileForm(forms.ModelForm):
	birthdate = forms.DateField(widget=DateInput())
	class Meta:
		model = UserProfile
		fields = ('gender', 'birthdate')