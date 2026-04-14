$("#registerForm").on("submit", function(e){
    e.preventDefault();

    const username = $("#username").val();
    const password = $("#password").val();
    const confirmPassword = $("#confirmPassword").val();
    const phone = $("#phone").val();
    const address = $("#address").val();
    
    console.log(password,  confirmPassword);

    if(password != confirmPassword){
        alert("Mật khẩu không không trùng khớp");
        return;
    }

    $.ajax({
        url: "/register",
        method: "POST",
        contentType: "application/json",
        data: JSON.stringify({
            username: username,
            password: password,
            phone: phone,
            address: address
        }),
        success: function(res){
            if(res.token){
                localStorage.setItem("token", res.token)
                alert("Đăng ký thành công")
                window.location.href = "/"
            }else{
                alert("Sai tài khoản")
            }
        },
        error: function(err){
            alert(err.responseJSON.error);
        }
    });
});