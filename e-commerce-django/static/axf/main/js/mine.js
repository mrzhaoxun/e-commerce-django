$(function () {

    $("#not_login").click(function () {

        window.open('/App/login/', target="_self");

    })

    $("#regis").click(function () {

        window.open('/App/register/', target="_self");
    })

     $("#not_pay").click(function () {

        window.open('/App/orderlistnotpay/', target="_self");

    })

     $("#not_receive").click(function () {

        window.open('/App/orderlistnotreceive/', target="_self");

    })

    $("#not_appraise").click(function () {

        window.open('/App/orderlistnotappraise/', target="_self");

    })
})