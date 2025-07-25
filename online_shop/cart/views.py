from typing import override
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from shop.recommender import Recommender
from shop.models import Product
from cart.cart import Cart
from cart.forms import CartAddProductForm
from coupons.forms import CouponApplyForm


@require_POST
def cart_add(request: HttpRequest, product_id: int):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)

    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product, quantity=cd['quantity'], override_quantity=cd['override'])

    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request: HttpRequest, product_id: int):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request: HttpRequest):
    cart = Cart(request)
    coupon_apply_form = CouponApplyForm()

    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'override': True})

    r = Recommender()
    cart_products = [item['product'] for item in cart]

    if cart_products:
        recommended_products = r.suggest_products_for(cart_products, max_results=4)
    else:
        recommended_products = []

    return render(request, 'cart/detail.html', {
        'cart': cart,
        'coupon_apply_form': coupon_apply_form,
        'recommended_products': recommended_products
    })
