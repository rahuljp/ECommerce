from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse
from .models import Order
from cart.models import Cart
from seller.models import Medium
from userApp.models import UserProfileInfo
from django.db import transaction,IntegrityError

#https://docs.djangoproject.com/en/2.0/topics/db/transactions/
#https://stackoverflow.com/questions/31734306/django-transactions-atomic-requests?rq=1
# Create your views here.
@transaction.non_atomic_requests
def createOrder(request):
    if request.user.is_authenticated:
        cart_obj=Cart.objects.filter(user=request.user,active=True,total__gte=0.01).first()
        #print(cart_obj)
        if cart_obj is not None:
            order_obj=Order.objects.filter(cart=cart_obj).first()
            #print("hehehe")
            #print(order_obj)
            user_info=UserProfileInfo.objects.filter(user=request.user).first()
            print(user_info)
            if order_obj is None:
                Order.objects.create(cart=cart_obj)
                order_obj=Order.objects.filter(cart=cart_obj).first()
                order_obj.user=request.user
                order_obj.save()
            return render(request,"order/checkout.html",{'cart_obj':cart_obj,'order_obj':order_obj,'user_info':user_info,'isSeller':request.session['isSeller']})
        else:
            return HttpResponse("This cart is inactive, go back and click on Cart icon to active new Cart")
    else:
        return render(request, 'userApp/login.html', {'redirect_url':request.build_absolute_uri})

#must run under a transatcion

def setAddress(request):
    if request.method=="POST":
        try:
            address=request.POST.get('address')
            #print("papa")
            order_id=request.POST.get('order_id')
            print(order_id)
            cart_id=request.POST.get('cart_id')
            cart_obj=Cart.objects.get(id=cart_id)
            print(cart_obj.active)
            if cart_obj.active:
                order_obj=Order.objects.filter(order_id=order_id).first()

                for item in cart_obj.products.all():
                    print(item.price)
                    medium_obj=Medium.objects.filter(product_id=item.id,quantity__gte=1).first()

                    if medium_obj:
                        medium_obj.quantity=medium_obj.quantity-1
                        medium_obj.save()
                        print(medium_obj.quantity)
                    else:
                        return HttpResponse("At least one of your Item in cart is Out Of Stock and has been removed from it! ")
                order_obj.address=address
                order_obj.active=False
                print(request.POST.get('updateAddress'))
                order_obj.save()
                cart_obj.active=False
                cart_obj.save()
                if request.POST.get('updateAddress') is not None:
                    user_obj=UserProfileInfo.objects.filter(user=request.user).first()
                    user_obj.address=order_obj.address
                #    print(user_obj.user.username)
                    print("go")
                    user_obj.save()
                return render(request,'order/payment.html',{'isSeller':request.session['isSeller']})
            else:
                return HttpResponse("Order already has been Placed. You can't place same order multiple time.")
        except IntegrityError:
            handle_exception()
            return HttpResponse("Your all active order has been Placed!")
    return HttpResponse("Create order first to set address")

@transaction.non_atomic_requests
def orderHistory(request):
    if request.user.is_authenticated:
        order=Order.objects.filter(user=request.user,active=False)
        return render(request,'order/order_history.html',{'order':order})

    return redirect('home')
