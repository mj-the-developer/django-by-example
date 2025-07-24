from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render

from cart.cart import Cart
from orders.models import Order, OrderItem
from orders.forms import OrderCreateForm
from orders.tasks import order_created


def order_create(request: HttpRequest):
    cart = Cart(request)
    
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order ,product=item['product'], price=item['price'], quantity=item['quantity'])
            cart.clear()
            order_created.delay(order.id)
            request.session['order_id'] = order.id
            return redirect('payment:process')
    else:
        form = OrderCreateForm()

    return render(request, 'orders/order/create.html', {'form': form, 'cart': cart})


@staff_member_required
def admin_order_detail(request: HttpRequest, order_id: int):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/orders/order/detail.html', {'order': order})
