from django.http import HttpRequest
from django.shortcuts import redirect
from django.utils import timezone
from django.views.decorators.http import require_POST

from coupons.forms import CouponApplyForm
from coupons.models import Coupon


@require_POST
def coupon_apply(request: HttpRequest):
    now = timezone.now()
    form = CouponApplyForm(request.POST)

    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code=code, active=True, valid_from__lte=now, valid_to__gte=now)
            request.session['coupon_id'] = coupon.id
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None

    return redirect('cart:cart_detail')
