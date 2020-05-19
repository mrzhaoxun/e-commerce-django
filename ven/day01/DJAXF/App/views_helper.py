import hashlib
from random import randint


from django.core.mail import send_mail
from django.template import loader

from App.models import Cart
from DJAXF.settings import EMAIL_HOST_USER, SEVER_HOST, SEVER_PORT, code_font


def hash_str(source):
    return hashlib.new('sha512', source.encode('utf-8')).hexdigest()


def send_email_activate(username, email, u_token):

    subject = 'hello{}'.format(username)

    message = "!"

    data = {
        'username': username,
        'activate_url': 'http://{}:{}/App/activate/?u_token={}'.format(
            SEVER_HOST, SEVER_PORT, u_token)

    }

    html_message = loader.get_template('user/activate.html').render(data)

    from_email = EMAIL_HOST_USER

    recipient_list = [email,]

    send_mail(subject=subject, message=message, html_message=html_message, from_email=from_email,
              recipient_list=recipient_list, )


def send_email_change_password(username, email, p_token):

    print(p_token)

    subject = 'Dear {}'.format(email)

    message = 'reset_password'

    data = {
        'username': username,
        'email': email,
        'reset_password_url': 'http://{}:{}/App/resetpassword/?p_token={}'.format(
            SEVER_HOST, SEVER_PORT, p_token
        )
    }

    html_message = loader.get_template('user/reset_password_email.html').render(data)

    from_email = EMAIL_HOST_USER

    recipient_list = [email, ]

    send_mail(subject=subject, message=message, html_message=html_message, from_email=EMAIL_HOST_USER,
              recipient_list=recipient_list)


def get_total_price():

    carts = Cart.objects.filter(c_is_select=True)

    total = 0

    if carts.exists():
        for cart in carts:
            total += cart.c_goods.price*cart.c_goods_num

    return '{:.2f}'.format(total)


def rand_wd():
    text = ''
    for i in range(4):
        n = chr(randint(65, 90))
        text += n
    return text


def rand_color():
    return randint(64, 255), randint(64, 255), randint(64, 160)



