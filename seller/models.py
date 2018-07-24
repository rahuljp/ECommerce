from django.db import models
# Create your models here.
from django.contrib.auth.models import User

# Create your models here.
#class SellerProfileInfo(models.Model):

    # Create relationship (don't inherit from User!)
    #user_seller = models.OneToOneField(User,on_delete=models.CASCADE)

    # Add any additional attributes you want
    #address = models.CharField(max_length=30, blank=True)
    # pip install pillow to use this!
    # Optional: pip install pillow --global-option=”build_ext” --global-option=”--disable-jpeg”
    #profile_pic = models.ImageField(upload_to='image',blank=True)
    #is_user= models.CharField(max_length=30, default=False)

    #def __str__(self):
        # Built-in attribute of django.contrib.auth.models.User !
    #    return self.user_seller.username


class Medium(models.Model):
    product_id=models.IntegerField()
    seller_id=models.IntegerField()
    quantity=models.IntegerField()
    model=models.CharField(max_length=30, blank=True)
    company = models.CharField(max_length=30, blank=True)
    title = models.CharField(max_length=120,default='Laptop')
