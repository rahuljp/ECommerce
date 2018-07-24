from django.shortcuts import render
from django.db.models import Q
from django.db import transaction
# Create your views here.
from django.views.generic import ListView
from categoryApp.models import Product
from seller.models import Medium

@transaction.non_atomic_requests
class SearchProductView(ListView):
    template_name = "search/result.html"
    def get_context_data(self, *args, **kwargs):
        context = super(SearchProductView, self).get_context_data(*args, **kwargs)
        query = self.request.GET.get('q')
        context['query'] = query
        context['isSeller']=self.request.session['isSeller']
        return context

    def get_queryset(self, *args, **kwargs):
        query = self.request.GET.get('q', None) # method_dict['q']
        print(query+'s')
        print('some changes')
        if query is not None:
            query='%'+query+'%'
            result = Product.objects.raw('''SELECT product.id,product.title AS title,product.company
            AS company,product.model AS model,product.slug AS slug,product.description AS description,
            product.price AS price,product.image AS image
            FROM categoryApp_product AS product INNER JOIN seller_medium AS seller
            ON product.id=seller.product_id
            WHERE (LOWER(product.title) LIKE %s OR LOWER(product.company) LIKE %s
            OR LOWER(product.model) LIKE %s) AND seller.quantity >0 GROUP BY product.id
             ''',[query.lower(),query.lower(),query.lower()])

            return result
            #return Product.objects.filter(Q(title__icontains=query)|Q(company__icontains=query)|Q(model__icontains=query))

        '''
        __icontains = field contains this
        __iexact = fields is exactly this
        '''
