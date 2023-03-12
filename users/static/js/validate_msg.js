
function err_messages(set_border, message, message_target) {
    set_border.style.borderColor = "red";
    document.getElementById(message_target).innerHTML = message;
}

$("#email").click(function () {
    document.getElementById('email').style.removeProperty('border');
    document.getElementById("mailmessage").innerHTML = '';
});
$("#username").click(function () {
    document.getElementById('username').style.removeProperty('border');
    document.getElementById("uname_message").innerHTML = '';
});
$("#first_name").click(function () {
    document.getElementById('first_name').style.removeProperty('border');
    document.getElementById("name_message").innerHTML = '';
});
$("#last_name").click(function () {
    document.getElementById('last_name').style.removeProperty('border');
    document.getElementById("last_name_message").innerHTML = '';
});
$("#pwd").click(function () {
    document.getElementById('pwd').style.removeProperty('border');
    document.getElementById("pwd_message").innerHTML = '';
});

function clearpwd() {
    document.getElementById('nwpwd').style.removeProperty('border');
    document.getElementById("nwpwd_message").innerHTML = '';
}
function clearotp() {
    document.getElementById('otp').style.removeProperty('border');
    document.getElementById("otp_message").innerHTML = '';
}