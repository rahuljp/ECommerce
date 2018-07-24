from django import forms
from django.contrib.auth.models import User
from userApp.models import UserProfileInfo

class UserForm(forms.ModelForm):
#    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username','email','password','first_name','last_name')

class UpdateForm(forms.ModelForm):
    #password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = UserProfileInfo
        fields = ('address',)

class UpdatedForm(forms.ModelForm):
    #password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('first_name','last_name')

class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('address','profile_pic')
