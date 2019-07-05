window.onload=function () {
    // 这里面是需要初始化的函数
    // loadHomePage();
};
// 第一类操作，页面移动
// 第一次加载入页面
function loadHomePage() {
    // alert('初始化执行函数');
    pageChange(
        '/bpcloud/init_home/',
        {'name': '/'},
        function (page_info) {
            console.log(page_info);
            // 数据遍历举例
            for(let key in page_info){
                alert(page_info[key]['name']);            // 
                alert(page_info[key]['df_type']);         // 文件或文件夹
                alert(page_info[key]['change_time']);
                alert(page_info[key]['size']);
                alert(page_info[key]['type']);            // 文件类型
            }
        }
    );
}
function returnHome() {
    let name = '/';
    queryPage('', name);
}
function nextPage() {
    let name = 'B';
    queryPage('', name);
}
function previousPage() {
    queryPage('previous','');
}
function flushPage() {
    queryPage( 'flush', '');
}

function queryPage(info, name) {
    pageChange(
        '/bpcloud/query_page/',
        {'name': name, 'info': info},
        function (page_info) {
            for(let key in page_info){
                alert(page_info[key]['name']);            // 可根据后缀简单判断文件类型
                alert(page_info[key]['df_type']);         // 其中type为D或F,
                alert(page_info[key]['change_time']);
                alert(page_info[key]['size']);
                alert(page_info[key]['type']);            // 文件类型, 后缀
            }
        }
    );
}
// 垃圾箱
function queryDustbin() {
    pageChange(
        "/bpcloud/query_dustbin/",
        {},
        function (page_info) {
            // 数据遍历举例
            for(let key in dusbin_info){
                dusbin_info[key]['name'];         // 可根据后缀简单判断文件类型
                dusbin_info[key]['type'];         // 其中type为D或F,
                dusbin_info[key]['delete_time'];
            }
        }
    );

}

// 第二类操作上传下载
function download(){
    let url = '/storage/dd8f1df7d4645edd896fae86607ad9b7.1.jpg';
    // let url = '/static/js/home.js';
    let download_file = document.createElement('a');
    download_file.href = url;      // 下载地址
    download_file.download = '1.jpg';       // 下载名字
    download_file.click();
    // // 首先检查如果选定中含有文件夹，显示无法下载
    // let name_list = [('1.jpg')];
    // // 获取真实路径
    // $.ajax({
    //         url: '/bpcloud/download/',
    //         dataType: 'json',
    //         type: 'POST',
    //         data: {'name_list': JSON.stringify(name_list)},
    //         success: function (res) {
    //         if (res['res'] === 'error'){
    //             alert('下载失败');
    //         }
    //         else {
    //             // 如果返回正确地址则下载
    //             let real_path_list = res['res'];
    //             let count = 0;
    //             for(let name in name_list){
    //                 let download_file = document.createElement('a');
    //                 download_file.href = real_path_list[count++];      // 下载地址
    //                 download_file.download = name;       // 下载名字
    //                 download_file.click();
    //             }
    //         }
    //     }
    // });
}



// 上传
function uploadFile() {
    // 先检查是否有重名
    // checkDuplicationName(name);
    // 然后检查MD5
    // 这里是上传标签的id，可修改
    let files = document.getElementById('upload-file').files;
    // 获取文件信息
    for (let i = 0; i < files.length; i++) {
        let fileName = files[i].name;      // 文件名
        let fileSize = files[i].size;      // 文件大小 单位：B
        let fileType = files[i].type;      // 文件类型 比如：application/pdf image/jpeg text/plain
        let fileUploadTime = new Date();   // 上传时间 当前操作时间
        // 读取文件内容
        getMd5(files[i], fileName);
    }
}

function uploadDir() {
    // 先检查是否有重名
    // checkDuplicationName(dir_name);
    // 这里是上传标签的id，可修改
    // getMd5('upload-dir');
    // 发送Md5 list给后端，后端发送需要上传的，其他显示秒传
    // 然后开始上传
    // xhrUploadDir('upload-dir');
    let files = document.getElementById('upload-dir').files;
    // 获取文件信息
    for (let i = 0; i < files.length; i++) {
        let fileName = files[i].webkitRelativePath;      // 文件名
        let fileSize = files[i].size;      // 文件大小 单位：B
        let fileType = files[i].type;      // 文件类型 比如：application/pdf image/jpeg text/plain
        let fileUploadTime = new Date();   // 上传时间 当前操作时间
        // 读取文件内容
        getMd5(files[i], fileName);
    }
}

// 第三类操作
// 新建文件夹
function createNewFolder() {
    // 获取新建的文件夹名
    let dir_name = 'new folder';
    // 检查是否重名
    // checkDuplicationName(dir_name);
    // 如果没有重名就进行操作
    unifyOp([], 'create', dir_name);
}

// 放入回收站
function discard() {
    let info_list = [
        {'name': 'd.mp3', 'df_type': 'F'},
        {'name': 'B', 'df_type': 'D'},
    ];
    unifyOp(info_list, 'delete', '');
}

// 彻底删除
function delCom() {
    // 需要询问是否是彻底删除
    // isDeleteCompletely()?
    alert('真的要彻底删除吗');
    // 如果彻底删除进行操作
    let info_list = [
        {'name': 'd.mp3', 'df_type': 'F'},
        {'name': 'B', 'df_type': 'D'},
    ];
    unifyOp(info_list, 'delCom', '');
}

// 移动到
function move() {
    let info_list = [
        {'name': 'd.mp3', 'df_type': 'F'},
        {'name': 'B', 'df_type': 'D'},
    ];
    let to_path = '/A/';

    // 首先进行操作可行性检查
    multipleTran(
        '/bpcloud/move_check/',
        {'info_list': JSON.stringify(info_list),
                'to_path': to_path},
        function (info_list) {
            // 可行进行移动操作
            unifyOp(info_list, 'moveTo', to_path);
        }
    );

}

// 复制到
function copy() {
    let info_list = [
        {'name': 'd.mp3', 'df_type': 'F'},
        {'name': 'B', 'df_type': 'D'},
    ];
    let to_path = '/';
    // 首先进行操作可行性检查
    multipleTran(
        '/bpcloud/move_check/',
        {'info_list': JSON.stringify(info_list),
                'to_path': to_path},
        function (info_list) {
            unifyOp(info_list, 'copyTo', to_path);
        }
    );
}

// 重命名
function rename() {
    // 获取新建的文件夹名
    let new_name = 'new_a.txt';
    let info_list = [
        {'name': 'a.txt', 'df_type': 'F'},
    ];
    // 检查是否重名
    // checkDuplicationName(name, df_type);
    // 如果重名打印信息
    unifyOp(info_list, 'rename', new_name);
}


function recovery() {
    // 在恢复之前首先要检查冲突
    let info_list = [
        {'name': 'd.mp3', 'df_type': 'F', 'delete_time': '2019-07-02 11:28:41'},
        {'name': 'B', 'df_type': 'D', 'delete_time': '2019-07-02 11:28:41'},
    ];
    // 首先进行操作可行性检查
    multipleTran(
        '/bpcloud/recovery_check/',
        {'info_list': JSON.stringify(info_list)},
                function (info_list) {
            unifyOp(info_list, 'recovery', '');
        }
    );
}


// //前端： 检查是否有重复命名
// function checkDuplicationName(dir_name) {
//     // 检查新建的dir_name是否已经存在
//     return true;
// }









// 进度条，可自行设计
// 前端大体如此
// <div id='1' style="height:20px;width:100px;border:2px solid gray;float:left;margin-right:10px;">
//     <div id='2' style="height:100%;width:0px;background:gray;"></div>
// </div>
// <b style="margin-right:20px" id='3'>0%</b><br>
// 这个函数可以接收一个evt(event)对象(细节自行查询progress)，
// 他有3个属性lengthComputable，loaded，total，第一个属性是个bool类型的，代表是否支持，
// 第二个代表当前上传的大小，第三个为总的大小，由此便可以计算出实时上传的百分比
function onProgress(evt) {
    if(evt.lengthComputable) {
        var ele = document.getElementById('2');
        var percent = Math.round((evt.loaded) * 100 / evt.total);
        ele.style.width = percent + '%';
        document.getElementById('3').innerHTML = percent + '%';
    }
}







// function uploadFile() {
//
//     // 先检查是否有重名
//     // checkDuplicationName(name);
//     // 然后检查MD5
//     // 这里是上传标签的id，可修改
//     let hashCode = getMd5('upload-file');
//
//     const files = document.getElementById('upload-file').files;
//     // 获取文件信息
//     for (let i = 0; i < files.length; i++) {
//         let fileName = files[i].name;      // 文件名
//         let fileSize = files[i].size;      // 文件大小 单位：B
//         let fileType = files[i].type;      // 文件类型 比如：application/pdf image/jpeg text/plain
//         let fileUploadTime = new Date();   // 上传时间 当前操作时间
//         // 读取文件内容
//         var reader = new FileReader();
//         reader.readAsBinaryString(files[i]);  // 二进制读取
//         reader.onload = function() {  // onload成功读取文件后调用
//             var data = this.result;        // 文件内容
//             $.ajax({
//                 url:'/bpcloud/upload/',
//                 method: 'post',
//                 data: {
//                     "fileName": fileName,
//                     "fileSize": fileSize,
//                     "fileType": fileType,
//                     "fileUploadTime": fileUploadTime,
//                     "hashCode": hashCode,
//                     "data": data,
//                 },
//             })
//         };
//     }
//
//     // for (let i = 0; i < fileJSONArray.length; i++) {
//     //     console.log(fileJSONArray[i].fileName, fileJSONArray[i].fileSize, fileJSONArray[i].fileType);
//     // }
// }