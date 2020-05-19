$(function () {

    $("#receive").click(function () {

        console.log("已收货");

        var orderid = $(this).attr("orderid");

        $.getJSON("/App/receive/", {"orderid": orderid}, function (data) {
            console.log(data);

            if(data['status'] === 200){
                window.open('/App/mine/', target='_self');
            }

        })
    })

    $("#back_button").click(function () {

                window.open('/App/mine/',target='_self');

        })

})