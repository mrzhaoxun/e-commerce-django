$(function () {

    $("#alipay").click(function () {

        var $order = $(this);

        var order_id = $order.attr("orderid");

        // window.open('/App/alipay/?orderid=' + order_id, target="_self");
        window.open('/App/alipay/?orderid=' + order_id, target="_self");


    })

    $("#back_button").click(function () {

                window.open('/App/mine/',target='_self');

        })

})