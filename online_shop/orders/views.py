from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.staticfiles import finders
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
import weasyprint

from cart.cart import Cart
from orders.models import Order, OrderItem
from orders.forms import OrderCreateForm
from orders.tasks import order_created


def order_create(request: HttpRequest):
    cart = Cart(request)
    
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order: Order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            
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


@staff_member_required
def admin_order_pdf(request: HttpRequest, order_id: int):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('admin/orders/order/pdf.html', {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f"filename=order_{order.id}.pdf"
    weasyprint.HTML(string=html).write_pdf(response, stylesheets=[weasyprint.CSS(finders.find('css/pdf.css'))])
    return response
