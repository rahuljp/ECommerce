from django.conf.urls import url
from seller import views

# SET THE NAMESPACE!
app_name = 'seller'

# Be careful setting the name to just /login use userlogin instead!
urlpatterns=[
    url(r'^register/$',views.register,name='register'),
    url(r'^seller_login/$',views.user_login,name='seller_login'),
    url(r'^add_pro/$',views.add_product,name='add_pro'),
]
