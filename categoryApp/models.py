import random
import os
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.core.validators import MinValueValidator

from django.urls import reverse
from .utils import unique_slug_generator


TITLE_CHOICES = (
    ('Laptop', 'Laptop'),
    ('Smartphone', 'Smartphone'),
    ('TVs', 'TVs'),
)



class Product(models.Model):
    title           = models.CharField(max_length=120,choices=TITLE_CHOICES,default='Laptop')
    company         = models.CharField(max_length=120,null=False,default='Samsung')
    model           = models.CharField(max_length=200,null=False,default='s-123')
    slug            = models.SlugField(blank=True, unique=True)
    description     = models.TextField(blank=False,default='avc')
    price           = models.DecimalField(decimal_places=2,
                        max_digits=20, default=39.99,validators=[MinValueValidator(0.01),])
    image           = models.ImageField(upload_to='image', null=True, blank=True)



    def get_absolute_url(self):
        #return "/category/{slug}/".format(slug=self.slug)
         return reverse("category:detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title


def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(product_pre_save_receiver, sender=Product)
