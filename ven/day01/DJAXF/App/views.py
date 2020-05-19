import logging
import re
import uuid
import os
from io import BytesIO
from random import randrange

from alipay import AliPay

from PIL import Image, ImageDraw, ImageFont
from PIL.ImageDraw import ImageDraw

#import alipay
# from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
# from alipay.aop.api.domain.AlipayTradeAppPayModel import AlipayTradeAppPayModel
# from alipay.aop.api.domain.SettleDetailInfo import SettleDetailInfo
# from alipay.aop.api.domain.SettleInfo import SettleInfo
# from alipay.aop.api.domain.SubMerchant import SubMerchant
# from alipay.aop.api.request.AlipayTradeAppPayRequest import AlipayTradeAppPayRequest
# from alipay.aop.api.request.AlipayTradePagePayRequest import AlipayTradePagePayRequest
from django.core.cache import cache
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from App.views_constant import *
from App.models import MainWheel, MainNav, MainMustBuy, MainShop, MainShow, FoodType, Goods, Users, Cart, Order, \
    OrderGoods, Address
from App.views_helper import hash_str, send_email_activate, send_email_change_password, get_total_price, \
    rand_color, rand_wd
from DJAXF.settings import MEDIA_KEY_PREFIX, ALI_APP_ID, APP_PRIVATE_KEY, ALI_PUBLIC_KEY, MERCHANT_ID, code_font

# from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
# from alipay.aop.api.domain.AlipayTradePagePayModel import AlipayTradePagePayModel

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def index(request):
    return redirect(reverse('App:home'))


def home(request):
    main_wheels = MainWheel.objects.all()

    main_navs = MainNav.objects.all()

    main_mustbuys = MainMustBuy.objects.all()

    main_shops = MainShop.objects.all()
    main_shop_1 = main_shops[0:1]
    main_shop_2 = main_shops[1:3]
    main_shop_3 = main_shops[3:7]
    main_shop_4 = main_shops[7:11]

    main_shows = MainShow.objects.all()

    date = {
        'title': '首页',
        'main_wheels': main_wheels,
        'main_navs': main_navs,
        'main_mustbuys': main_mustbuys,
        'main_shop_1': main_shop_1,
        'main_shop_2': main_shop_2,
        'main_shop_3': main_shop_3,
        'main_shop_4': main_shop_4,
        'main_shows': main_shows,
    }

    # ip = request.META.get('REMOTE_ADDR')
    # print(ip)

    return render(request, 'main/home.html', context=date)


def market(request):
    return redirect(reverse('App:market_with_params', kwargs={
        'typeid': 104749,
        'childcid': 0,
        'order_rule': 0,
    }))


def market_with_params(request, typeid, childcid, order_rule):
    foodtypes = FoodType.objects.all()
    goods_list = Goods.objects.filter(categoryid=typeid)

    # 不是全部类型
    if int(childcid) != 0:
        goods_list = goods_list.filter(childcid=childcid)

    # 排序
    if order_rule == ORDER_TOTAL:
        pass

    elif order_rule == ORDER_PRICE_UP:
        goods_list = goods_list.order_by('marketprice')

    elif order_rule == ORDER_PRICE_DOWN:
        goods_list = goods_list.order_by('-marketprice')

    elif order_rule == ORDER_SALE_UP:
        goods_list = goods_list.order_by('productnum')

    elif order_rule == ORDER_SALE_DOWN:
        goods_list = goods_list.order_by('-productnum')

    foodtype = foodtypes.get(typeid=typeid)
    foodtypechildnames = foodtype.childtypenames.split('#')
    foodtypechildnames_list = []
    for foodtypechildname in foodtypechildnames:
        foodtypechildnames_list.append(foodtypechildname.split(':'))

    # for i in foodtypechidlnames:
    #     n = eval(i)
    #
    #     print(type(n))
    #     print(n)

    data = {
        'title': '闪购',
        'foodtypes': foodtypes,
        'goods_list': goods_list,
        'typeid': typeid,
        'childcid': childcid,
        'order_rule': order_rule,
        'foodtypechildnames_list': foodtypechildnames_list,
        'sort_titles': sort_titles,

    }

    return render(request, 'main/market.html', context=data)


def cart(request):
    carts = Cart.objects.filter(c_user=request.user)

    not_all_select = carts.filter(c_is_select=False).exists()

    user = request.user

    data = {
        'title': '购物车',
        'carts': carts,
        'not_all_select': not_all_select,
        'total_price': get_total_price(),
        'user': request.user,

    }
    try:
        default_address_obj = Address.objects.get(pk=user.u_defaultaddress)
    except:
        default_address_obj = Address.objects.first()
    data['default_address_obj'] = default_address_obj

    return render(request, 'main/cart.html', context=data)


def mine(request):
    user_id = request.session.get('user_id')

    data = {
        'title': '我的',
        'is_login': False,
    }

    if user_id:
        user = Users.objects.get(pk=user_id)
        data['username'] = user.u_username
        print(user.u_icon.url)
        data['icon'] = MEDIA_KEY_PREFIX + user.u_icon.url
        data['is_login'] = True
        data['order_not_pay'] = Order.objects.filter(o_user=user).filter(o_status=ORDER_STATUS_NOT_PAY).count()
        data['order_not_receive'] = Order.objects.filter(o_user=user).filter(o_status__in=[
            ORDER_STATUS_NOT_SEND, ORDER_STATUS_NOT_RECEIVE]).count()
        data['order_not_appraise'] = Order.objects.filter(o_user=user).filter(
            o_status=ORDER_STATUS_NOT_APPRAISE).count()

    return render(request, 'main/mine.html', context=data)


def register(request):
    if request.method == 'GET':

        data = {
            'title': '注册',
        }

        error_message = request.session.get('error_message')

        if error_message:
            del request.session['error_message']
            data['error_message'] = error_message

        return render(request, 'user/register.html', context=data)

    elif request.method == 'POST':

        if str(request.POST['verify_code']).lower() != request.session.get('verify_code'):
            request.session['error_message'] = '验证码不正确'

            return redirect(reverse('App:register'))

        user = Users()

        user.u_username = request.POST['username']

        user.u_email = request.POST['email']

        password = request.POST['password']
        user.u_password = hash_str(password)

        user.u_icon = request.FILES['icon']

        user.save()

        u_token = uuid.uuid4().hex

        cache.set(u_token, user.id, timeout=60 * 60 * 3)

        send_email_activate(username=user.u_username, email=user.u_email, u_token=u_token)

        return redirect(reverse('App:login'))


def login(request):
    if request.method == 'GET':

        error_message = request.session.get('error_message')

        data = {
            'title': '登陆',
        }

        if error_message:
            del request.session['error_message']

            data['error_message'] = error_message

        return render(request, 'user/login.html', context=data)

    elif request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']
        password = hash_str(password)

        try:
            match_user = Users.objects.get(Q(u_username=username) | Q(u_email=username))

            if match_user.u_password == password:

                if not match_user.is_active:
                    request.session['error_message'] = '用户未激活，请前往邮箱激活'
                    return redirect(reverse('App:login'))

                request.session['user_id'] = match_user.id

                return redirect(reverse('App:mine'))

            else:
                request.session['error_message'] = '密码错误或账户不存在'
                return redirect(reverse('App:login'))

        except Exception as e:
            request.session['error_message'] = '密码错误或账户不存在'
            return redirect(reverse('App:login'))


def logout(request):
    request.session.flush()

    return redirect(reverse('App:mine'))


def check_user(request):
    username = request.GET.get('username')

    users = Users.objects.filter(u_username=username)

    data = {
        'status': HTTP_OK,
        'msg': 'user can use',
    }

    if users.exists():
        data['status'] = HTTP_USER_EXIST
        data['msg'] = 'user already exist'
    else:
        pass

    return JsonResponse(data=data)

def check_email(request):
    email = request.GET.get('email')

    users = Users.objects.filter(u_email=email)

    data = {
        'status': HTTP_OK,
        'msg': 'email can use',
    }

    if users.exists():
        data['status'] = HTTP_USER_EXIST
        data['msg'] = 'email already exist'
    else:
        pass

    return JsonResponse(data=data)


def activate(request):
    u_token = request.GET.get('u_token')

    user_id = cache.get(u_token)

    if user_id:
        cache.delete(u_token)

        user = Users.objects.get(pk=user_id)

        user.is_active = True

        user.save()

        return redirect(reverse('App:login'))

    return render(request, 'user/activate_fail.html')


def forget_password(request):
    if request.method == 'GET':

        data = {
            'title': '忘记密码',
        }

        error_message = request.session.get('error_message')

        if error_message:
            del request.session['error_message']
            data['error_message'] = error_message

        return render(request, 'user/forget_password.html', context=data)

    if request.method == 'POST':

        if str(request.POST['verify_code']).lower() != request.session.get('verify_code'):
            request.session['error_message'] = '验证码不正确'

            return redirect(reverse('App:forget_password'))

        email = request.POST['email']

        try:
            forget_user = Users.objects.get(u_email=email)

            if forget_user:
                print('get email')

                p_token = uuid.uuid4().hex

                username = forget_user.u_username

                cache.set(p_token, email, 60 * 60)

                send_email_change_password(username, email, p_token)

                request.session['error_message'] = '邮件已发送，请通过邮件链接修改密码！'

                return redirect(reverse('App:login'))

        except Exception as e:
            request.session['error_message'] = '邮箱不存在，请重新输入'

            return redirect(reverse('App:forget_password'))


def reset_password(request):

    if request.method == "GET":

        p_token = request.GET.get('p_token')

        email = cache.get(p_token)

        if email:
            data = {
                'title': '重设密码',
            }
            cache.set('reset_user_email', email, 60*5)

            return render(request, 'user/reset_password.html', data)

        request.session['error_message'] = '链接过期，请重新申请！'
        return redirect(reverse('App:forget_password'))

    elif request.method == "POST":

        try:

            email = cache.get('reset_user_email')

            reset_user = Users.objects.get(u_email=email)

            reset_user.u_password = hash_str(request.POST.get('new_password'))

            print(reset_user.u_password)

            reset_user.save()

            request.session['error_message'] = '密码重设成功！'

            return redirect(reverse('App:login'))

        except:

            request.session['error_message'] = '链接过期，请重新申请！'

            return redirect(reverse('App:forget_password'))


def add_to_cart(request):
    goodsid = request.GET.get('goodsid')

    carts = Cart.objects.filter(Q(c_user=request.user) & Q(c_goods_id=goodsid))

    if carts.exists():
        cart_obj = carts.first()
        cart_obj.c_goods_num = cart_obj.c_goods_num + 1
        cart_obj.save()

    else:
        cart_obj = Cart(c_goods_id=goodsid, c_user=request.user)
        cart_obj.save()

    data = {
        'status': 200,
        'msg': 'add success',
        'c_goods_num': cart_obj.c_goods_num,
    }

    return JsonResponse(data)


def change_cart_state(request):
    cart_id = request.GET.get('cartid')

    try:
        cart_obj = Cart.objects.get(pk=cart_id)
        cart_obj.c_is_select = not cart_obj.c_is_select
        cart_obj.save()

    except:
        print('wrong_change_cart_state')

    not_all_select = Cart.objects.filter(c_user=request.user).filter(c_is_select=False).exists()

    data = {
        'status': 200,
        'msg': '更改购物车选中成功',
        'c_is_select': cart_obj.c_is_select,
        'not_all_select': not_all_select,
        'total_price': get_total_price(),
    }

    return JsonResponse(data)


def add_shopping(request):
    cart_id = request.GET.get('cartid')

    cart_obj = Cart.objects.get(pk=cart_id)

    data = {
        'status': 200,
        'msg': '增加数量成功',
    }

    cart_obj.c_goods_num = cart_obj.c_goods_num + 1
    cart_obj.save()
    data['c_goods_num'] = cart_obj.c_goods_num

    data['total_price'] = get_total_price()

    return JsonResponse(data)


def sub_shopping(request):
    cart_id = request.GET.get('cartid')

    cart_obj = Cart.objects.get(pk=cart_id)

    data = {
        'status': 200,
        'msg': '减少数量成功',
    }

    if cart_obj.c_goods_num > 1:
        cart_obj.c_goods_num = cart_obj.c_goods_num - 1
        cart_obj.save()
        data['c_goods_num'] = cart_obj.c_goods_num

    else:
        cart_obj.delete()
        data['c_goods_num'] = 0

    data['total_price'] = get_total_price()

    return JsonResponse(data)


def all_select(request):
    cart_list = request.GET.get('cart_list')

    data = {
        'status': 200,
        'msg': '全选执行',
    }

    if cart_list:
        cart_list = cart_list.split('#')
        print(type(cart_list))
        carts = Cart.objects.filter(pk__in=cart_list)

        for cart_obj in carts:
            cart_obj.c_is_select = not cart_obj.c_is_select
            cart_obj.save()

    data['total_price'] = get_total_price()

    return JsonResponse(data)


def make_order(request):
    carts = Cart.objects.filter(c_user=request.user).filter(c_is_select=True)

    order = Order(o_user=request.user, o_price=get_total_price())

    order.save()

    for cart in carts:
        ordergoods = OrderGoods(o_order=order, o_goods=cart.c_goods, o_goods_num=cart.c_goods_num)
        ordergoods.save()
        cart.delete()

    data = {
        'status': 200,
        'msg': '下单',
        'order_id': order.id,
    }

    return JsonResponse(data)


def order_detail(request):
    order_id = request.GET.get('orderid')

    order = Order.objects.get(pk=order_id)

    data = {
        'title': '订单页面',
        'order_id': order_id,
        'order': order,
    }

    return render(request, 'order/order_detail.html', context=data)


def order_list_not_pay(request):
    orders_not_pay = Order.objects.filter(o_user=request.user).filter(o_status=ORDER_STATUS_NOT_PAY)

    data = {
        'title': '未付款订单',
        'orders_not_pay': orders_not_pay,
    }

    return render(request, 'order/order_list_not_pay.html', context=data)


def order_list_not_receive(request):
    orders_not_receive = Order.objects.filter(o_user=request.user).filter(o_status__in=[
        ORDER_STATUS_NOT_SEND, ORDER_STATUS_NOT_RECEIVE])

    data = {
        'title': '未付款订单',
        'orders_not_receive': orders_not_receive,
    }

    return render(request, 'order/order_list_not_receive.html', context=data)


def order_list_not_appraise(request):
    order_not_appraise = Order.objects.filter(o_status=ORDER_STATUS_NOT_APPRAISE)

    data = {
        'title': '未评价订单',
        'order_not_appraise': order_not_appraise,
    }

    return render(request, 'order/order_list_not_appraise.html', context=data)


def payed(request):
    order_id = request.GET.get('orderid')

    order = Order.objects.get(pk=order_id)

    order.o_status = ORDER_STATUS_NOT_SEND

    order.save()

    data = {
        'status': 200,
        'msg': '支付成功！',

    }

    return JsonResponse(data)


def receive(request):
    order_id = request.GET.get('orderid')

    order = Order.objects.get(pk=order_id)

    order.o_status = ORDER_STATUS_NOT_APPRAISE

    order.save()

    data = {
        'status': 200,
        'msg': '已收货',
    }

    return JsonResponse(data)


def appraise(request, orderid):
    data = {
        'title': '评价页面',
        'order_id': orderid,
    }

    return render(request, 'order/order_appraise.html', context=data)


def address(request):
    if request.method == "GET":

        address_list = Address.objects.filter(a_user=request.user)
        help_message = request.session.get('help_message')

        data = {
            'title': '地址管理',
            'address_list': address_list,
        }

        if help_message:
            del request.session['help_message']
            data['help_message'] = help_message
        return render(request, 'user/address.html', data)


def add_address(request):
    if request.method == "GET":
        return render(request, 'order/order_add_address.html')

    elif request.method == "POST":
        address = Address()
        address.a_nickname = request.POST['nickname']
        address.a_phone = request.POST['phone']
        address.a_detail = request.POST['detail']
        address.a_user = request.user
        address.save()

        return redirect(reverse('App:address'))


def del_address(request):
    address_id = request.GET.get('addressid')
    address = Address.objects.get(pk=address_id)
    address.delete()
    return redirect(reverse('App:address'))


def default_address(request):

    user = request.user
    user.u_defaultaddress = request.GET.get('addressid')
    user.save()
    request.session['help_message'] = '设置默认地址成功！'

    return redirect(reverse('App:address'))


def get_code(request):
    mode = 'RGB'
    size = (200, 100)

    image = Image.new(mode=mode, size=size, color=rand_color())
    image_draw = ImageDraw(image, mode=mode)
    font = ImageFont.truetype(code_font, 80)
    text = rand_wd().lower()
    request.session['verify_code'] = text

    for i in range(4):
        image_draw.text((45 * i + randrange(20), randrange(30)), text[i], fill=rand_color(), font=font)

    for i in range(6000):
        image_draw.point((randrange(201), randrange(101)), rand_color())

    for i in range(randrange(3)):
        xy = ((randrange(201), randrange(101)), (randrange(201), randrange(101)))
        image_draw.line(xy, fill=rand_color(), width=2)

    fp = BytesIO()
    image.save(fp, 'png')
    return HttpResponse(fp.getvalue(), content_type='image/png')


def coupon(request):
    return render(request, 'user/coupon.html')
"""
def ali_pay(request):

    #日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s',
        filemode='a', )
    logger = logging.getLogger('')
    
    #创建支付宝客户端实例，设置
    alipay_client_config = AlipayClientConfig(sandbox_debug=True)
    alipay_client_config.app_id = ALI_APP_ID

    with open(os.path.join(BASE_DIR, 'alipay_key/应用私钥2048.txt'), 'r')as f:
        alipay_client_config.app_private_key = f.read()

    with open(os.path.join(BASE_DIR, 'alipay_key/支付宝公钥.txt'), 'r') as f:
        alipay_client_config.alipay_public_key = f.read()
    # alipay_client_config.sign_type = 'RSA2'

    client = DefaultAlipayClient(alipay_client_config=alipay_client_config)

    # 得到客户端对象。注意，一个alipay_client_config对象对应一个DefaultAlipayClient，定义DefaultAlipayClient对象后，
    # alipay_client_config不得修改，如果想使用不同的配置，请定义不同的DefaultAlipayClient。
    # logger参数用于打印日志，不传则不打印，建议传递。


    # order_id = request.GET.get('orderid')
    # order = get_object_or_404(Order, pk=order_id)
    # total_price = order.o_price
    # goods_amount = order.ordergoods_set.count()

    #创建 网页 请求对象
    # 对照接口文档，构造请求对象
    model = AlipayTradePagePayModel()
    model.out_trade_no = "pay201805020000226"
    model.total_amount = 50
    model.subject = "测试"
    model.body = "支付宝测试"
    model.product_code = "FAST_INSTANT_TRADE_PAY"
    settle_detail_info = SettleDetailInfo()
    settle_detail_info.amount = 50
    settle_detail_info.trans_in_type = "userId"
    settle_detail_info.trans_in = "2088302300165604"
    settle_detail_infos = list()
    settle_detail_infos.append(settle_detail_info)
    settle_info = SettleInfo()
    settle_info.settle_detail_infos = settle_detail_infos
    model.settle_info = settle_info
    sub_merchant = SubMerchant()
    sub_merchant.merchant_id = "2088301300153242"
    model.sub_merchant = sub_merchant
    request = AlipayTradePagePayRequest(biz_model=model)
    # 得到构造的请求，如果http_method是GET，则是一个带完成请求参数的url，如果http_method是POST，则是一段HTML表单片段
    response = client.page_execute(request, http_method="GET")
    print("alipay.trade.page.pay response:" + response)

    return redirect(response)
"""


def ali_pay_model(request):

    order_id = request.GET.get('orderid')

    order = Order.objects.get(pk=order_id)

    order.o_status = ORDER_STATUS_NOT_SEND

    order.save()

    data = {'title': '模拟支付完成',
            'orderid': order_id,
            }

    return render(request, 'order/alipay_model.html', data)


def ali_pay(request):
    # 构建支付的科幻  AlipayClient
    alipay_client = AliPay(
        appid=ALI_APP_ID,
        app_notify_url=None,  # 默认回调url
        app_private_key_string=APP_PRIVATE_KEY,
        alipay_public_key_string=ALI_PUBLIC_KEY,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=True  # 默认False
    )
    # 使用Alipay进行支付请求的发起
    order_id = request.GET.get('orderid')
    order = get_object_or_404(Order, pk=order_id)
    total_price = order.o_price
    goods_amount = order.ordergoods_set.count()

    subject = "车车的可爱Ukulele"

    # 电脑网站支付，需要跳转到https://openapi.alipay.com/gateway.do? + order_string
    order_string = alipay_client.api_alipay_trade_page_pay(
        out_trade_no=order_id,
        total_amount=total_price,
        subject=subject,
        return_url="http://www.1000phone.com",
        notify_url="http://www.1000phone.com"  # 可选, 不填则使用默认notify url
    )

    # 客户端操作

    return redirect("https://openapi.alipaydev.com/gateway.do?" + order_string)
