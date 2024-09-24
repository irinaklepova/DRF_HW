import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_KEYS


def create_stripe_product(obj):
    """Функция создания Stripe продукта"""

    product_name = f'{obj.course_pay}' if obj.course_pay else f'{obj.lesson_pay}'
    stripe_product = stripe.Product.create(
        name=f'{product_name}',
    )
    return stripe_product['id']


def create_stripe_price(product, product_id):
    """ Создает цену в Stripe"""

    stripe_price = stripe.Price.create(
        currency='rub',
        unit_amount=product * 100,
        product=product_id
    )
    return stripe_price['id']


def create_stripe_session(price):
    """ Функция создает сессию на оплату в Stripe"""

    session = stripe.checkout.Session.create(
        success_url='http://127.0.0.1:8000/',
        line_items=[{'price': price, 'quantity': 1}],
        mode='payment',

    )
    return session.get('id'), session.get('url')
