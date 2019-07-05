
function xhrUploadFile(file_object, hash_code, filename) {
    let fileUploadTime = new Date();   // 上传时间 当前操作时间

    let xhr = new XMLHttpRequest();
    let form = new FormData();
    form.append('upload-file',file_object);
    alert(filename);
    form.append('fileName', filename);
    form.append('fileSize', file_object.size);
    form.append('fileType', file_object.type);
    form.append('fileHash', hash_code);
    form.append('fileUploadTime', fileUploadTime.toISOString());


    // 这里绑定了进度条，前端也可以动态创建进度页面
    xhr.upload.addEventListener('progress',onProgress,false);

    xhr.open('POST','/bpcloud/upload_file/',true);
    xhr.setRequestHeader('X-CSRFTOKEN','{{ request.COOKIES.csrftoken }}');
    xhr.send(form);   //发送表单
    // xhr.onreadystatechange = function () {
    //     if(xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
    //         console.log(xhr.responseText)
    //     }
    // }
}

// function xhrUploadDir(dir_label_name) {
//     let xhr = new XMLHttpRequest();
//     let files = document.getElementById(dir_label_name).files;
//     let fd = new FormData();
//     let path_list = [];
//     for (let i = 0; i < files.length; i++) {
//         path_list.push(files[i].webkitRelativePath);
//         fd.append(dir_label_name, files[i]);
//     }
//     fd.append('path', path_list);
//
//     // 这里绑定了进度条，前端也可以动态创建进度页面
//     xhr.upload.addEventListener('progress',onProgress,false);
//
//     xhr.open('POST','/bpcloud/upload_dir/',true);
//     xhr.setRequestHeader('X-CSRFTOKEN','{{ request.COOKIES.csrftoken }}');
//     xhr.send(fd);
// }

// 统一操作
function unifyOp(info_list, operation, op_info) {
    let data = {};
    data['info'] = op_info;
    data['opera'] = operation;
    data['info_list'] = JSON.stringify(info_list);
    $.ajax({
            url: "/bpcloud/dfile_opera/",
            dataType: 'json',
            type: 'GET',
            data: data,
            success: function (res) {
                alert('success');
                if(res['res'] === 'res200'){
                    flushPage();
                }
                else {
                    // 返回失败信息
                    alert(res['res']);
                }
            },
            fail: function (res) {
                console.log('失败');
                fail()
            }
    });
}


function multipleTran(url, data, success, fail) {
    $.ajax({
            url: url,
            dataType: 'json',
            type: 'GET',
            data: data,
            success: function (res) {
                if(res['res'] === 'res200'){
                    console.log(res['res']);
                    success(data);      // 成功执行成功函数
                }
                else {
                    // 失败打印出错信息
                    alert(res['res']);
                }
            },
            fail: function (res) {
                console.log('失败');
                fail()
            }
    });
}

function pageChange(url, data, success, fail) {
    $.ajax({
            url: url,
            dataType: 'json',
            type: 'GET',
            data: data,
            success: function (res) {
                if(res['res'] === 'error'){
                    alert('error!');
                }
                else {
                    success(res['res']);
                }
            },
            fail: function (res) {
                console.log('失败');
                fail();
            }
    });
}