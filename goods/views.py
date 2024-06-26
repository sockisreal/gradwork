from django.core.paginator import Paginator
from django.shortcuts import get_list_or_404, render
from goods.models import Composition, Products
from goods.utils import q_search
from django.contrib.auth.decorators import login_required

@login_required
def catalog(request, category_slug=None):

    page = request.GET.get('page', 1)
    order_by = request.GET.get('order_by', None)
    query = request.GET.get('q', None)

    if category_slug == 'all':
        goods = Products.objects.all()
    elif query:
        goods = q_search(query)
    else:
        goods = Products.objects.filter(category__slug=category_slug)

    if order_by and order_by != 'default':
        goods = goods.order_by(order_by)
    
    paginator = Paginator(goods, 9)
    current_page = paginator.page(int(page))

    context = {
        'title': 'FlowerAI - Каталог',
        'goods': current_page,
        'slug_url': category_slug
    }
    return render(request, 'goods/catalog.html', context)



def product(request, product_slug):
    
    product = Products.objects.get(slug=product_slug)
    composition = Composition.objects.filter(product__slug=product_slug)
    context = {
        'title': 'FlowerAI - Товар',
        'product': product,
        'composition': composition
    }
    return render(request, 'goods/product.html', context=context)
