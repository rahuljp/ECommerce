from django.http import Http404
from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404
from django.db import transaction

from cart.models import Cart
from .models import Product



class ProductListView(ListView):
    template_name = "categoryApp/list.html"

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all()


def product_list_view(request):
    queryset = Product.objects.all()
    context = {
        'object_list': queryset,
        'isSeller':request.session['isSeller']
    }
    return render(request, "categoryApp/list.html", context)



class ProductDetailSlugView(DetailView):
    queryset = Product.objects.all()
    template_name = "categoryApp/detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailSlugView, self).get_context_data(*args, **kwargs)#super().get_context_data(*args,**kwargs)
        cart_obj,new_obj=Cart.objects.newCart_or_getCart(self.request)
        context['cart']=cart_obj
        context['isSeller']=self.request.session['isSeller']
        print('pp')
        print(context['cart'])
        print('pp')
        return context


    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        #instance = get_object_or_404(Product, slug=slug, active=True)
        try:
            instance = Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            raise Http404("Not found..")
        except Product.MultipleObjectsReturned:
            qs = Product.objects.filter(slug=slug)
            instance = qs.first()
    #    except:
    #        raise Http404("Uhhmmm ")
        return instance



class ProductDetailView(DetailView):
    #queryset = Product.objects.all()
    template_name = "categoryApp/detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs) #super().get_context_data(*args,**kwargs)
        context['isSeller']=self.request.session['isSeller']
        print(context)
        # context['abc'] = 123
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        pk = self.kwargs.get('pk')
        instance = Product.objects.get_by_id(pk)
        if instance is None:
            raise Http404("Product doesn't exist")
        return instance

    # def get_queryset(self, *args, **kwargs):
    #     request = self.request
    #     pk = self.kwargs.get('pk')
    #     return Product.objects.filter(pk=pk)


def product_detail_view(request, pk=None, *args, **kwargs):
    # instance = Product.objects.get(pk=pk, featured=True) #id
    # instance = get_object_or_404(Product, pk=pk, featured=True)
    # try:
    #     instance = Product.objects.get(id=pk)
    # except Product.DoesNotExist:
    #     print('no product here')
    #     raise Http404("Product doesn't exist")
    # except:
    #     print("huh?")

    instance = Product.objects.get_by_id(pk)
    if instance is None:
        raise Http404("Product doesn't exist")
    #print(instance)
    # qs  = Product.objects.filter(id=pk)

    # #print(qs)
    # if qs.exists() and qs.count() == 1: # len(qs)
    #     instance = qs.first()
    # else:
    #     raise Http404("Product doesn't exist")

    context = {
        'object': instance,
        'isSeller':request.session['isSeller']
    }
    return render(request, "categoryApp/detail.html", context)
