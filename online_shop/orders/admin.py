import csv
import datetime
from typing import Any

from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.urls import reverse
from django.utils.safestring import mark_safe

from orders.models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


@admin.action(description='Export to CSV')
def export_to_csv(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet[Any]):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f"attachment; filename={modeladmin.opts.verbose_name}.csv"
    writer = csv.writer(response)

    fields = [field for field in modeladmin.opts.get_fields() if not field.many_to_many and not field.one_to_many]
    writer.writerow([field.verbose_name for field in fields])

    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)

    return response


def stripe_payment_url(obj: Order):
    url = obj.get_stripe_url()
    if obj.stripe_id:
        html = f'<a href="{url}" target="_blank">{obj.stripe_id}</a>'
        return mark_safe(html)
    return ''


def order_detail(obj: Order):
    url = reverse('orders:admin_order_detail', args=[obj.id])
    return mark_safe(f'<a href="{url}">View</a>')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'first_name',
        'last_name',
        'email',
        'postal_code',
        'city',
        'paid',
        stripe_payment_url,
        'created',
        order_detail,
    ]
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
    actions = [export_to_csv]
