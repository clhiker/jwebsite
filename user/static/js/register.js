(function ($) {
    "use strict";


    /*==================================================================
   [ Focus input ]*/
    $('.input-content').each(function () {
        $(this).on('blur', function () {
            if ($(this).val().trim() !== "") {
                $(this).addClass('has-val');
            } else {
                $(this).removeClass('has-val');
            }
        })
    });


    /*==================================================================
    [ Validate ]*/
    var input = $('.validate-input .input-content');

    $('.validate-register-form').on('submit', function () {
        var check = true;

        // // Validate  FBI验证 O(∩_∩)O
        // for (var i = 0; i < input.length; i++) {
        //     if (validate(input[i]) === false) {
        //         showValidate(input[i]);
        //         check = false;
        //     }
        // }
        
        const password = $('#password-input').val();
        const verifyPassword = $('#verify-password-input').val();
        if(password !== verifyPassword) {
            alert("两次密码输入不一致，请重新输入！");
            check = false;
        }
        // Register
        if (check === true) {
            const username = $('#username-input').val();
            const email = 'cl1911618290@mail.dlut.edu.cn';
            const verification_code = '9527';
            var post_data = {
                "username": username,
                "password": password,
                "email": $('#telephone-input').val(),
                "verification_code": $('#verify-code-input').val(),
            };
            $.ajax({
                url: "/user/register.html",
                dataType: 'json',
                type: 'POST',
                data: post_data,
                success: function (data) {
                    if (data['res'] === 're200'){
                        location.href = '/';
                    }
                    else {
                        alert(data['res']);
                        location.href = "/user/register.html";
                    }
                },
                fail: function (data) {
                    console.log(data);
                }
            });
        }

        return check;
    });


    $('.validate-register-form .input-content').each(function () {
        $(this).focus(function () {
            hideValidate(this);
        });
    });

    function validate(input) {
        if ($(input).attr('type') === 'text') {
            // 用户名：4-16位字母,数字,汉字,下划线
            if ($(input).val().match(/^[a-zA-Z0-9_\u4e00-\u9fa5]{4,16}$/) == null) {
                console.log($(input).val())
                alert("用户名不合法！\n用户名由汉字、字母、数字、下划线组成，长度为4-16位！");
                return false;
            }
        } else if ($(input).attr('type') === 'password') {
            // 密码：包括至少1个大写字母，1个小写字母，1个数字，1个特殊字符，最少6位
            if ($(input).val().match(/^.*(?=.{6,})(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*? ]).*$/) == null) {
                alert("密码格式不合法！\n密码包括至少1个大写字母，1个小写字母，1个数字，1个特殊字符，最少6位！");
                return false;
            }
        } else {
            if ($(input).val().trim() === '') {
                return false;
            }
        }
    }

    function showValidate(input) {
        var thisAlert = $(input).parent();

        $(thisAlert).addClass('alert-validate');
    }

    function hideValidate(input) {
        var thisAlert = $(input).parent();

        $(thisAlert).removeClass('alert-validate');
    }

    /*==================================================================
    [ Get Verify Code ]*/
    $('.get-verify-code-btn').click(function () {
        var countdown = 0;

        if (countdown === 0) {
            $(this).removeAttr("disabled");
            $(this).value = "点击获取";
            countdown = 60;
            var telephone = $('#telephone-input').val();
            alert('已将验证码发送至邮箱，请查收');
            var post_data = {'email': telephone};
            $.ajax({
                url: "/user/verify_email",
                dataType: 'json',
                type: 'GET',
                data: post_data,
                success: function (data) {
                    console.log(data)
                },
                fail: function (data) {
                    console.log(data);
                }
            });
            // $.get("/user/register.html", {
            //     phone: telephone
            // }, function (data) {
            //     /** @namespace data.messages */
            //     if (data.messages !== null && data.messages[0].code === '1000') {
            //         window.location.href = "storage";
            //     } else {
            //         alert(data.messages[0].message);
            //     }
            // });
        } else {
            $(this).setAttribute("disabled", true);
            $(this).value = "重新发送(" + countdown + ")";
            $(this).border = "1px solid black";
            countdown--;
            if (countdown > 1) {
                setTimeout(function () {
                    setTime(button)
                }, 1000);
            }
        }
    })

})(jQuery);
