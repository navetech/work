from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def index(request):
#    return HttpResponse("Hello, world. You're at the polls index.")

    context = {}
    return render(request, 'sample/checkout.html', context)



def checkout(request):
#    return HttpResponse("Hello, world. You're at the polls index.")

    context = {}
    return render(request, 'sample/checkout.html', context)


def success(request):
#    return HttpResponse("Hello, world. You're at the polls index.")

    context = {}
    return render(request, 'sample/success.html', context)


def cancel(request):
#    return HttpResponse("Hello, world. You're at the polls index.")

    context = {}
    return render(request, 'sample/cancel.html', context)


from django.http import JsonResponse

import os

import stripe
# This is a sample test API key. Sign in to see examples pre-filled with your key.
stripe.api_key = 'sk_test_4eC39HqLyjWDarjtT1zdp7dc'


YOUR_DOMAIN = 'http://localhost:4242'

def create_checkout_session(request):
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': 2000,
                        'product_data': {
                            'name': 'Stubborn Attachments',
                            'images': ['https://i.imgur.com/EHyR2nP.png'],
                        },
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '/success',
            cancel_url=YOUR_DOMAIN + '/cancel',
        )
        return JsonResponse({'id': checkout_session.id})
    except Exception as e:
        return JsonResponse(error=str(e)), 403


