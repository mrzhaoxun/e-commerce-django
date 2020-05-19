ORDER_TOTAL = "0"
ORDER_PRICE_UP = "1"
ORDER_PRICE_DOWN = "2"
ORDER_SALE_UP = "3"
ORDER_SALE_DOWN = "4"

sort_titles = [['综合排序', '0'],
               ['价格升序', '1'],
               ['价格降序', '2'],
               ['销量升序', '3'],
               ['销量降序', '4']]

# http code
HTTP_USER_EXIST = 901
HTTP_OK = 200

#oder_status
#未付款
ORDER_STATUS_NOT_PAY = 0
#未发货
ORDER_STATUS_NOT_SEND = 1
#未签收
ORDER_STATUS_NOT_RECEIVE = 2
#未评价
ORDER_STATUS_NOT_APPRAISE = 3
#申请退换货
ORDER_SALE_APPLY_RETURN = -1
#申请售后通过
ORDER_SALE_APPLY_REFUSE = -2
#申请售后驳回
ORDER_SALE_APPLY_PASS = -3