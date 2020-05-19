$(function () {

    var $username = $("#username_input");

    $username.change(function () {
        var username = $username.val().trim();

        if (username.length) {

            //    将用户名发送给服务器进行预校验
            $.getJSON('/App/checkuser/', {'username': username}, function (data) {

                console.log(data);

                var $username_info = $("#username_info");

                if (data['status'] === 200) {
                    $username_info.html("用户名可用").css("color", 'green');
                } else if (data['status'] === 901) {
                    $username_info.html("用户已存在").css('color', 'red');
                }

            })

        }

    })


    var $email = $("#email_input");

    $email.change(function () {
        var email = $email.val().trim();

        if (email.length) {

            //    将用户名发送给服务器进行预校验
            $.getJSON('/App/checkemail/', {'email': email}, function (data) {

                console.log(data);

                var $email_info = $("#email_info");

                if (data['status'] === 200) {
                    $email_info.html("email可用").css("color", 'green');
                } else if (data['status'] === 901) {
                    $email_info.html("email存在").css('color', 'red');
                }

            })

        }

    })



})


function check() {
    var $username = $("#username_input");

    var username = $username.val().trim();

    if (!username) {
        return false
    }

    var info_color = $("#username_info").css('color');

    console.log(info_color);

    if (info_color === 'rgb(255, 0, 0)') {
        return false
    }


    var password_input = $("#password_input").val();

    var password_confirm_input = $("#password_confirm_input").val();

    if (password_input === "") {
        alert("密码不能为空");

        return false;

    }

    if (password_input !== password_confirm_input) {
        alert("两次密码不一致!");

        return false;
    }

    var $password_input = $("#password_input");

    var password = $password_input.val().trim();

    $password_input.val(md5(password));

    return true
}

