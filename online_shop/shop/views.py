from django.http import HttpRequest
from django.shortcuts import get_object_or_404, render

from cart.forms import CartAddProductForm
from shop.recommender import Recommender
from shop.models import Category, Product


def product_list(request: HttpRequest, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    if category_slug:
        language = request.LANGUAGE_CODE
        category = get_object_or_404(Category, translations__language_code=language, translations__slug=category_slug)
        products = products.filter(category=category)

    return render(request, 'shop/product/list.html', {'category': category, 'categories': categories, 'products': products})


def product_detail(request: HttpRequest, id: int, slug: str):
    language = request.LANGUAGE_CODE
    product = get_object_or_404(Product, translations__language_code=language, id=id, translations__slug=slug, available=True)
    cart_product_form = CartAddProductForm()

    r = Recommender()
    recommended_products = r.suggest_products_for([product], 4)

    return render(request, 'shop/product/detail.html', {
        'product': product,
        'cart_product_form': cart_product_form,
        'recommended_products': recommended_products,
    })
