import stripe
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from core.models import Book
from .models import Payment
from .utils import create_checkout_session

# Create your views here.

@api_view(['POST'])
def checkout(request):

    book_id = request.data.get('book_id')
    if not book_id:
        return Response({
            "detail": "Bad Request"
        }, status=status.HTTP_400_BAD_REQUEST)
     
    book = Book.objects.get(id=book_id)
    if not book:
        return Response({
            'detail': 'Not Found'
        }, status=status.HTTP_404_NOT_FOUND)

    try:
        payment = Payment.objects.create(user_id = request.user.id)
        checkout_session = create_checkout_session(payment.id, book)

        return Response({
            "detail": checkout_session.url
        }, status=status.HTTP_200_OK)
    
    except Exception as error:
        print(error)
        return Response({
            "detail": "Internal Server Error"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['POST'])
@permission_classes([AllowAny])
def stripe_webhook(request):

    if request.method == "POST":

        payload = request.data
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

        event = stripe.Event.construct_from(
            payload, settings.STRIPE_SECRET_KEY
        )
        if event["type"] == "checkout.session.completed":
            checkout_obj = event["data"]["object"]


            payment = Payment.objects.get(id = checkout_obj['client_reference_id'])
            user = payment.user
            
            user.has_book_access = True

            payment.currency = checkout_obj.get('currency')
            payment.total_amount = checkout_obj['amount_total']
            payment.session_id = checkout_obj['id']
            payment.payment_intent_id = checkout_obj['payment_intent']
            payment.status = checkout_obj['status']
            payment.payment_status = checkout_obj['payment_status']
            payment.customer_email = checkout_obj['customer_details']['email']
            payment.session_created_at = checkout_obj['created']

            payment.save()
            user.save()
            
            return Response({
                "detail": "OK"
            }, status=status.HTTP_200_OK)

        else:
            print("Payment Failed")
            return Response({
                "detail": "Not Found"
            }, status=status.HTTP_404_NOT_FOUND)
