$(function () {

    $("#alipay").click(function () {

        var $order = $(this);

        var order_id = $order.attr("orderid");

        // window.open('/App/alipay/?orderid=' + order_id, target="_self");
        window.open('/App/alipaymodel/?orderid=' + order_id, target="_self");


    })

})