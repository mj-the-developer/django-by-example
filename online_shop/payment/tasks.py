from io import BytesIO

from celery import shared_task
from django.contrib.staticfiles import finders
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import weasyprint

from orders.models import Order


@shared_task
def payment_completed(order_id: int):
    order = Order.objects.get(id=order_id)
    subject = f"Online Shop - Invoice no. {order_id}"
    message = "Please, find attached the invoice for your recent purchase."
    email = EmailMessage(subject, message, 'admin@onlineshop.com', [order.email])

    html = render_to_string('admin/orders/order/pdf.html', {'order': order})
    out = BytesIO()
    stylesheets = [weasyprint.CSS(finders.find('css/pdf.css'))]
    weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)
    email.attach(f"order_{order.id}.pdf", out.getvalue(), 'application/pdf')
    email.send()
