function check() {

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