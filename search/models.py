from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
def get_absolute_url(self):
    #return "/category/{slug}/".format(slug=self.slug)
     return reverse("category:detail", kwargs={"slug": self.slug})
