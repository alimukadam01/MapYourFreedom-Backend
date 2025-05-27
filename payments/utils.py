import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY



def create_checkout_session(payment_id, book):

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': book.price,
                        'product_data': {
                            'name': book.name,
                            'images': ["https://www.google.com/imgres?q=map%20your%20freedom&imgurl=https%3A%2F%2Fwww.mapyourfreedom.com%2Fimages%2Fmap-your-freedom-book-cover.png&imgrefurl=https%3A%2F%2Fwww.mapyourfreedom.com%2Fmap-your-freedom-the-book.php&docid=kfR7Fy4MJ5ridM&tbnid=beWHW8v4EcQxgM&vet=12ahUKEwjwvPS05MyMAxVghf0HHdCQIWgQM3oFCIMBEAA..i&w=786&h=692&hcb=2&ved=2ahUKEwjwvPS05MyMAxVghf0HHdCQIWgQM3oFCIMBEAA"]
                        },
                    },
                    'quantity': 1
                },
            ],
            mode='payment',
            success_url='https://book.mapyourfreedom.com/user-profile?result=success',
            cancel_url='https://book.mapyourfreedom.com/user-profile?result=fail',
            client_reference_id=payment_id
        )
        return checkout_session
    
    except Exception as error:
        print(error)
        return None


