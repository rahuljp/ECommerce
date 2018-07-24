from django import forms
from django.contrib.auth.models import User
from userApp.models import UserProfileInfo
from categoryApp.models import Product

class SellerForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username','email','password')


class SellerProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('address','profile_pic')

class ProductForm(forms.ModelForm):
    class Meta():
        model=Product
        fields=('title','company','model','price','image')
