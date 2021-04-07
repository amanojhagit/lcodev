from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt

import braintree

# Create your views here.


gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id="rtrzrqxrvkyjncxq",
        public_key="ww78sh2f7bcqry6b",
        private_key="e2a624326aa3a8c6d184e7cad0d6d782"
    )
)


def validate_user_session(id,token):
    UserModel=get_user_model()
    try:
        user= UserModel.objects.get(pk=id)
        if user.session_token==token:
            return True
        return False
    except UserModel.DoesNotExist:
        return False

@csrf_exempt
def generate_token(request,id,token):
    if not validate_user_session(id,token):
        return JsonResponse({'error':'Invalid Session Please login again'})
    return JsonResponse({'clientToken': gateway.client_token.generate(),'success':'True'})


@csrf_exempt
def process_payment():
    if not validate_user_session(id,token):
        return JsonResponse({'error':'Invalid Session Please login again'})

    nonce_from_the_client= request.POST["paymentMethodNounce"]
    amount_from_the_client= request.POST["amount"]

    result=gateway.transaction.sale({
        "amount":amount_from_the_client,
        "payment_method_nonce": nonce_from_the_client,
         "options": {
             "submit_for_settlement": True
        }
    })

    if result.is_success:
        return JsonResponse({"success":result.is_success,"transection":{'id':result.transection.id,'amount':result.transection.amount}})
    
    else:
        return JsonResponse({'error':True,'Success':False})