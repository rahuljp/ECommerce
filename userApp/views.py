from django.shortcuts import render,redirect
from userApp.forms import UserForm,UserProfileInfoForm,UpdateForm,UpdatedForm
from django.utils.http import is_safe_url
from django.db import transaction
from userApp.models import UserProfileInfo
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
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        # Check to see both forms are valid
        if user_form.is_valid() and profile_form.is_valid():

            # Save User Form to Database
            user = user_form.save()

            # Hash the password
            user.set_password(user.password)

            # Update with Hashed password
            user.save()

            # Now we deal with the extra info!
            print(user)
            username = request.POST.get('username')
            password = request.POST.get('password')
        #    print(username)
        #    print(password)
            # Can't commit yet because we still need to manipulate
            profile = profile_form.save(commit=False)

            # Set One to One relationship between
            # UserForm and UserProfileInfoForm
            profile.user = user

            # Check if they provided a profile picture
            if 'profile_pic' in request.FILES:
                print('found it')
                # If yes, then grab it from the POST form reply
                profile.profile_pic = request.FILES['profile_pic']

            # Now save model
            profile.save()

            # Registration Successful!
            registered = True
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
        return redirect('home')
    else:
        # Was not an HTTP post so we just render the forms as blank.
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    # This is the render and context dictionary to feed
    # back to the registration.html file page.
    return render(request,'userApp/registration.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})

@transaction.non_atomic_requests
def user_login(request):
    next_ = request.GET.get('next')
    next_post=request.POST.get('next')
    redirect_to = next_ or next_post or None
    if request.method == 'POST':

        # First get the username and password supplied
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Django's built-in authentication function:
        user = authenticate(username=username, password=password)

        # If we have a user
    #    print(user)
        #print("de")
        if user:
            #Check it the account is active
            if user.is_active:
                # Log the user in.
                login(request,user)
                # Send the user back to some page.
                # In this case their homepage.
                #print(next_)
                path=redirect_to[:len(redirect_to)-1]
                currentdir=path[path.rfind('/')+1:]
                print(path[path.rfind('/')+1:])
                if redirect_to is not None and currentdir != 'register':
                    #return redirect(redirect_to)
                    return HttpResponseRedirect(redirect_to)
                else:
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
        return render(request, 'userApp/login.html', {'redirect_url':next_})

def profile(request):
    #print(request.user.id)
    queryset = UserProfileInfo.objects.filter(user_id=request.user.id)
    #print(queryset)
    context = {
        'object_list': queryset,
    }
    return render(request, "userApp/profile.html", context)



def update(request):

    registered = False

    id=request.user.id
    instance=UserProfileInfo.objects.filter(user_id=id)

    if request.method == 'POST':

        # Get info from "both" forms
        # It appears as one form to the user on the .html page
        user_form = UpdatedForm(data=request.POST)
        profile_form = UpdateForm(data=request.POST)

        # Check to see both forms are valid
        if user_form.is_valid() and profile_form.is_valid():

            # Save User Form to Database


            instance.user.first_name=user_form.first_name
            instance.user.last_name=user_form.last_name
            instance.address=profile_form.address
            instance.save()
            # Update with Hashed password

            # Now we deal with the extra info!
            username = request.POST.get('username')
            password = request.POST.get('password')



            # Set One to One relationship between
            # UserForm and UserProfileInfoForm

            registered = True


    else:
        # Was not an HTTP post so we just render the forms as blank.
        user_form = UpdatedForm()
        profile_form = UpdateForm()

    # This is the render and context dictionary to feed
    # back to the registration.html file page.
    return render(request,'userApp/update.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered,
                           'object':instance,
                           })
