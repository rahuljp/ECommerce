from django.shortcuts import render
from seller.forms import SellerForm,SellerProfileInfoForm,ProductForm
from categoryApp.models import Product
from seller.models import Medium
from userApp.models import UserProfileInfo
from django.db import transaction
# Extra Imports for the Login and Logout Capabilities
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
@transaction.non_atomic_requests
def special(request):
    # Remember to also set login url in settings.py!
    # LOGIN_URL = '/basic_app/user_login/'
    return HttpResponse("You are logged in. Nice!")

@login_required
@transaction.non_atomic_requests
def user_logout(request):
    # Log out the user.
    logout(request)
    # Return to homepage.
    return HttpResponseRedirect(reverse('home'))

@transaction.non_atomic_requests
def register(request):

    registered = False

    if request.method == 'POST':

        # Get info from "both" forms
        # It appears as one form to the user on the .html page
        user_form = SellerForm(data=request.POST)
        profile_form = SellerProfileInfoForm(data=request.POST)

        # Check to see both forms are valid
        # Check to see both forms are valid
        if user_form.is_valid() and profile_form.is_valid():

            # Save User Form to Database
            user = user_form.save()

            # Hash the password
            user.set_password(user.password)
            print(user.username)
            # Update with Hashed password
            user.save()

            # Now we deal with the extra info!

            # Can't commit yet because we still need to manipulate
            profile = profile_form.save(commit=False)

            # Set One to One relationship between
            # SellerForm and SellerProfileInfoForm
            profile.user = user

            # Check if they provided a profile picture
            if 'profile_pic' in request.FILES:
                print('found it')
                # If yes, then grab it from the POST form reply
                profile.profile_pic = request.FILES['profile_pic']
                print(profile.profile_pic)

            # Now save model
            profile.save()
            id_1=user.id
            instance=UserProfileInfo.objects.get(user_id=id_1)
            instance.is_seller=True
            instance.save()
            # Registration Successful!
            registered = True
            username = request.POST.get('username')
            password = request.POST.get('password')
            current_user = authenticate(username=username, password=password)
            if current_user:
                #Check it the account is active
                if current_user.is_active:
                    # Log the user in.
                    login(request,current_user)
                    # Send the user back to some page.
                    # In this case their homepage.
                    return HttpResponseRedirect(reverse('home'))
                else:
                    # If account is not active:
                    return HttpResponse("Your account is not active.")

        else:
            # One of the forms was invalid if this else gets called.
            print(user_form.errors,profile_form.errors)

    else:
        user_form = SellerForm()
        profile_form = SellerProfileInfoForm()

    # This is the render and context dictionary to feed
    # back to the registration.html file page.
    return render(request,'seller/registration.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})

@transaction.non_atomic_requests
def user_login(request):

    if request.method == 'POST':
        # First get the username and password supplied
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Django's built-in authentication function:
        user = authenticate(username=username, password=password)

        # If we have a user
        if user:
            #Check it the account is active
            id=user.id
                #print(id)
            try:
                instance=UserProfileInfo.objects.get(user_id=id,is_seller=True)
                    #print(instance.user_seller.id)
            except UserProfileInfo.DoesNotExist:
                    #print(id)
                return HttpResponse("You are not seller get lost")
            if user.is_active:
                # Log the user in.
                login(request,user)
                # Send the user back to some page.
                # In this case their homepage.
                return HttpResponseRedirect(reverse('home'))
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details supplied.")

    else:
        #Nothing has been provided for username or password.
        return render(request, 'seller/login.html', {})


# Create your views here.
def add_product(request):

    #registered = False
    id=request.user.id
    #print(id)
    try:
        instance=UserProfileInfo.objects.get(user_id=id,is_seller=True)
        #print(instance.user_seller.id)
    except UserProfileInfo.DoesNotExist:
        #print(id)
        return HttpResponse("You are not seller")
    if request.method == 'POST':

        # Get info from "both" forms
        # It appears as one form to the user on the .html page
        #user_form = SellerForm(data=request.POST)
        product_form =ProductForm(data=request.POST)

        # Check to see both forms are valid
        if product_form.is_valid():

            # Save User Form to Database

            # Hash the password
                    # Update with Hashed password

            # Can't commit yet because we still need to manipulate
            temp = product_form.save(commit=False)
            title_1=temp.title
            #print(title_1)
            model_1=temp.model
            company_1=temp.company
            price_1=temp.price
            if 'image' in request.FILES:
                print('found it')
                # If yes, then grab it from the POST form reply
                temp.image = request.FILES['image']
            image_1=temp.image

            try:
                instance = Product.objects.get(title=title_1,model=model_1,company=company_1)
                pid=instance.id   #product id
                sid=request.user.id

                try:
                    instance_inter=Medium.objects.get(product_id=pid,seller_id=sid)
                    instance_inter.quantity=(instance_inter.quantity)+1
                    instance_inter.save()
                except Medium.DoesNotExist:
                    obj=Medium(product_id=pid,seller_id=sid,quantity=1,model=model_1,company=company_1)
                    obj.save()

            except Product.DoesNotExist:
                obj1=Product(title=title_1,model=model_1,company=company_1,price=price_1)
                if 'image' in request.FILES:
                    print('found it')
                    # If yes, then grab it from the POST form reply
                    obj1.image = request.FILES['image']
                obj1.save()
                instance_new = Product.objects.get(title=title_1,model=model_1,company=company_1)
                pid_1=instance_new.id   #product id
                sid_1=request.user.id
                obj_new=Medium(product_id=pid_1,seller_id=sid_1,quantity=1,model=model_1,company=company_1)
                obj_new.save()

            # Check if they provided a profile picture

            # Now save model
        #    temp.save()

            # Registration Successful!




    else:
        # Was not an HTTP post so we just render the forms as blank.
        product_form = ProductForm()

    # This is the render and context dictionary to feed
    # back to the registration.html file page.
    return render(request,'seller/add_product.html',
                          {
                           'product_form':product_form,
                           'isSeller':request.session['isSeller'],
                           })
