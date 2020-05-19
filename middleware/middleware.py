from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from App.models import Users

REQUIRE_LOGIN_JSON = [
    '/App/addtocart/',
    '/App/changecartstate/',
    '/App/makeorder/',
]

REQUIRE_LOGIN = {
    '/App/cart/',
    '/App/orderdetail/',
    '/App/orderlistnotpay/',
    '/App/orderlistnotreceive/',
    '/App/orderlistnotappraise/',
    '/App/addaddress/',
    '/App/address/',
    '/App/defaultaddress/',
}


class LoginMiddleware(MiddlewareMixin):

    def process_request(self, request):

        if request.path in REQUIRE_LOGIN_JSON:

            user_id = request.session.get('user_id')

            if user_id:
                try:
                    user = Users.objects.get(pk=user_id)

                    request.user = user
                except:
                    # return redirect(reverse('App:login'))
                    data = {
                        'status': 302,
                        'msg': '用户实效请重新登陆',
                    }
                    return JsonResponse(data)

            else:
                # return redirect(reverse('App:login'))
                data = {
                    'status': 302,
                    'msg': '用户未登录',
                }

                print('#中间件运行')
                return JsonResponse(data)

        if request.path in REQUIRE_LOGIN:
            user_id = request.session.get('user_id')

            if user_id:
                try:
                    user = Users.objects.get(pk=user_id)

                    request.user = user
                except:
                    return redirect(reverse('App:login'))

            else:
                return redirect(reverse('App:login'))
