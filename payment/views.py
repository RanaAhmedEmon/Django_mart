from django.shortcuts import render, HttpResponseRedirect, redirect
from django.urls import reverse
from django.contrib import messages
from .models import Order
from sslcommerz_python.payment import SSLCSession
from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def payment(request):
    # Check if the user is logged in before proceeding to payment
    if not request.user.is_authenticated:
        messages.info(request, "Please log in to make the payment.")
        return redirect('payment:checkout')

    # Set up SSLCommerz sandbox credentials for testing
    store_id = 'djang66dcba287b754'
    store_pass = 'djang66dcba287b754@ssl'
    mypayment = SSLCSession(sslc_is_sandbox=True, sslc_store_id=store_id, sslc_store_pass=store_pass)

    # Define URLs for success, failure, and cancellation of payment
    status_url = request.build_absolute_uri(reverse('payment:complete'))
    mypayment.set_urls(success_url=status_url, fail_url=status_url, cancel_url=status_url, ipn_url=status_url)

    # Retrieve the last order of the current user and set the amount for payment
    order_qs = Order.objects.filter(user=request.user).last()
    order_total = order_qs.amount

    # Set product details for SSLCommerz integration
    mypayment.set_product_integration(total_amount=Decimal(order_total), currency='BDT', product_category='Mixed',
                                      product_name=order_qs.items_json, num_of_item=1,
                                      shipping_method='Courier', product_profile='general')

    # Set customer information for the payment session
    current_user = request.user
    mypayment.set_customer_info(name=current_user.username, email=current_user.email,
                                address1=order_qs.address1, postcode=order_qs.zip_code, city=order_qs.city,
                                country="Bangladesh", phone=order_qs.phone)

    # Set shipping information if different from billing
    mypayment.set_shipping_info(shipping_to=current_user.username, address=order_qs.address1,
                                city=order_qs.city, postcode=order_qs.zip_code, country="Bangladesh")

    # Initialize payment and redirect to the payment gateway
    response_data = mypayment.init_payment()
    return redirect(response_data['GatewayPageURL'])


@csrf_exempt
def complete(request):
    # This view handles the payment response from SSLCommerz
    if request.method == 'POST':
        payment_data = request.POST
        status = payment_data.get('status')

        # Check if the payment status is valid
        if status == 'VALID':
            val_id = payment_data.get('val_id')
            tran_id = payment_data.get('tran_id')
            messages.success(request, "Your Payment Completed Successfully!")
            return HttpResponseRedirect(reverse('payment:purchase', kwargs={'val_id': val_id, 'tran_id': tran_id}))
        elif status == 'FAILED':
            messages.warning(request, "Your Payment Failed. Please try again!")
        
    return render(request, 'payment/complete.html', {})


@csrf_exempt
def purchase(request, val_id, tran_id):
    # Confirm the order and mark it as purchased
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if not order_qs.exists():
        return redirect(reverse('ecommerceapp:index'))

    order = order_qs[0]
    order.ordered = True
    order.orderId = tran_id  # Assuming Order model has fields orderId and paymentId
    order.paymentId = val_id
    order.save()
    return redirect(reverse('payment:orders'))


@csrf_exempt
def order_view(request):
    # Display a list of completed orders for the logged-in user
    try:
        orders = Order.objects.filter(user=request.user, ordered=True)
        context = {'orders': orders}
    except:
        messages.warning(request, "You don't have an active order!")
        return redirect('/')

    return render(request, 'order.html', context)
