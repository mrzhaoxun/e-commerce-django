from django.urls import path, re_path

from App import views

app_name = 'App'

urlpatterns = [
    path('index/', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('market/', views.market, name='market'),
    re_path(r'marketwithparams/(?P<typeid>\d+)/(?P<childcid>\d+)/(?P<order_rule>\d+)/', views.market_with_params,
            name='market_with_params'),
    path('cart/', views.cart, name='cart'),
    path('mine/', views.mine, name='mine'),

    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('checkuser/', views.check_user, name='check_user'),
    path('checkemail/', views.check_email, name='check_email'),
    path('activate/', views.activate, name='activate'),
    path('forgetpassword/', views.forget_password, name='forget_password'),
    path('resetpassword/', views.reset_password, name='reset_password'),

    path('addtocart/', views.add_to_cart, name='add_to_cart'),
    path('changecartstate/', views.change_cart_state, name='change_cart_state'),

    path('addshopping/', views.add_shopping, name='add_shopping'),
    path('subshopping/', views.sub_shopping, name='sub_shopping'),
    path('allselect/', views.all_select, name='all_select'),

    path('makeorder/', views.make_order, name='makeorder'),
    path('orderdetail/', views.order_detail, name='order_detail'),
    path('orderlistnotpay/', views.order_list_not_pay, name='order_list_not_pay'),
    path('orderlistnotreceive/', views.order_list_not_receive, name='order_list_not_receive'),
    path('orderlistnotappraise/', views.order_list_not_appraise, name='order_list_not_appraise'),

    path('payed/', views.payed, name='payed'),
    path('receive/', views.receive, name='receive'),
    path('appraise/<int:orderid>/', views.appraise, name='appraise'),

    path('getcode/', views.get_code, name='get_code'),
    path('alipaymodel/', views.ali_pay_model, name='ali_pay'),
    path('alipay/', views.ali_pay, name='ali_pay'),

    path('addaddress/', views.add_address, name='add_address'),
    path('deladdress/', views.del_address, name='del_address'),
    path('address/', views.address, name='address'),
    path('defaultaddress/', views.default_address, name='default_address'),

    path('coupon/', views.coupon, name='coupon'),

]