from django.http import HttpResponse
from django.shortcuts import render,redirect
from userApp.models import UserProfileInfo
from django.db import transaction
# Create your views here.
@transaction.non_atomic_requests
def home_page(request):
    request.session['isSeller']=False
    if request.user.is_authenticated:
        currentUser=None
        currentUser=UserProfileInfo.objects.filter(user=request.user).first()
        if currentUser is not None:
            request.session['isSeller']=currentUser.is_seller
#    print(request.session['isSeller'])
    return render(request,'home/index.html',{'isSeller':request.session['isSeller']})
