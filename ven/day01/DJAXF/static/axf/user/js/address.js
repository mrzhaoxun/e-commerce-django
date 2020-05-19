$(function () {


    $("#add_address").click(function () {

        window.open('/App/addaddress/', target = '_self');

    })

    $(".default_address").click(function () {

        var $address = $(this);

        var address_id = $address.attr("addressid");

        window.open('/App/defaultaddress/?addressid=' + address_id, target="_self");


    })

    $(".del_address").click(function () {

        var $address = $(this);

        var address_id = $address.attr("addressid");

        window.open('/App/deladdress/?addressid=' + address_id, target="_self");


    })


})