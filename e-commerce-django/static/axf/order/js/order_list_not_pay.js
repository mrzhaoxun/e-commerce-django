$(function () {

    $(".order").click(function () {

        var $order = $(this);

        var order_id = $order.attr("orderid");

        window.open('/App/orderdetail/?orderid=' + order_id, target="_self");

    })

    $(".btn").click(function () {

        var $order = $(this);

        var order_id = $order.attr("orderid");

        window.open('/App/orderdetail/?orderid=' + order_id, target="_self");

    })

    $("#back_button").click(function () {

                window.open('/App/mine/',target='_self');


        })

})