$("#tagler").click(function () {
    $(this).toggleClass() == "";
    var pwd = document.getElementById("pwd");
    if (pwd.type == "password") {
        document.getElementById("pwd").type = "text";
        $(this).toggleClass("tim-icons icon-zoom-split");
    } else {
        document.getElementById("pwd").type = "password";
        $(this).toggleClass("tim-icons icon-lock-circle");
    }
});

function play(){
    nwpwd = document.getElementById("nwpwd").type
    if (nwpwd == "password") {
        document.getElementById("nwpwd").type = "text";
        document.getElementById("spn").className = "tim-icons icon-zoom-split";
    } else {
        document.getElementById("nwpwd").type = "password";
        document.getElementById("spn").className = "tim-icons icon-lock-circle";
    }
    }

