// window.onload=function () {
//     // 这里面是需要初始化的函数
//     // loadHomePage();
// };
//
//
// function returnHome() {
//     let name = '/';
//     queryPage(name)
// }
// function nextPage() {
//     let name = '';
//     queryPage('', name)
// }
// function previousPage() {
//     queryPage('previous','')
// }
// // 向后端要文件数据
// function loadHomePage() {
//     // alert('初始化执行函数');
//     let name = '/';
//     $.ajax({
//             url: "/bpcloud/init_home/",
//             dataType: 'json',
//             type: 'GET',
//             data: {'name':name},
//             success: function (data) {
//                 for( var key in data){
//                     // alert(data[key]);
//                     alert(data[key]['name'])
//                 }
//                    console.log('成功');
//             },
//             fail: function (data) {
//                 console.log('失败');
//             }
//     });
// }
//
// // 功能函数请勿用作响应函数
// function queryPage(info, name) {
//     $.ajax({
//             url: "/bpcloud/query_page/",
//             dataType: 'json',
//             type: 'GET',
//             data: {'info':info, 'name':name},
//             success: function (data) {
//                 for( var key in data){
//                     // alert(data[key]);
//                     alert(data[key]['name'])
//                 }
//                    console.log('成功');
//             },
//             fail: function (data) {
//                 console.log('失败');
//             }
//     });
// }
//
// // 垃圾箱
// function queryDustbin() {
//     $.ajax({
//             url: "/bpcloud/query_dustbin/",
//             dataType: 'json',
//             type: 'GET',
//             data: {},
//             success: function (data) {
//                 for( var key in data){
//                     // alert(data[key]);
//                     alert(data[key]['name'])
//                 }
//                    console.log('成功');
//             },
//             fail: function (data) {
//                 console.log('失败');
//             }
//     });
// }
//
// function download(){
//     let download_file = document.createElement('a');
//     download_file.href = "home.html";      // 下载地址
//     download_file.download = 'home_test';  // 下载名字
//     download_file.click();
// }
// // 进度条
// function onProgress(evt) {       //看这个函数之前先看upload函数。这个函数可以接收一个evt(event)对象(细节自行查询progress)，他有3个属性lengthComputable，loaded，total，第一个属性是个bool类型的，代表是否支持，第二个代表当前上传的大小，第三个为总的大小，由此便可以计算出实时上传的百分比
//     if(evt.lengthComputable) {
//         var ele = document.getElementById('2');
//         var percent = Math.round((evt.loaded) * 100 / evt.total);
//         ele.style.width = percent + '%';
//         document.getElementById('3').innerHTML = percent + '%';
//     }
// }
//
// function getMd5List() {
//
// }
// // 计算md5
// function getMd5(name) {
//     //声明必要的变量
//     let fileReader = new FileReader(), box = document.getElementById('box');
//     //文件分割方法（注意兼容性）
//     let blobSlice = File.prototype.mozSlice || File.prototype.webkitSlice || File.prototype.slice,
//     file = document.getElementById(name).files[0],
//     //文件每块分割2M，计算分割详情
//     chunkSize = 2097152,
//     chunks = Math.ceil(file.size / chunkSize),
//     currentChunk = 0,
//
//     //创建md5对象（基于SparkMD5）
//     spark = new SparkMD5();
//
//     //每块文件读取完毕之后的处理
//     fileReader.onload = function(e) {
//         console.log("读取文件", currentChunk + 1, "/", chunks);
//         //每块交由sparkMD5进行计算
//         spark.appendBinary(e.target.result);
//         currentChunk++;
//
//         //如果文件处理完成计算MD5，如果还有分片继续处理
//         if (currentChunk < chunks) {
//             loadNext();
//         } else {
//             console.log("finished loading");
//             box.innerText = 'MD5 hash:' + spark.end();
//             console.info("计算的Hash", spark.end());
//         }
//     };
//
//      //处理单片文件的上传
//      function loadNext() {
//          let start = currentChunk * chunkSize, end = start + chunkSize >= file.size ? file.size : start + chunkSize;
//          fileReader.readAsBinaryString(blobSlice.call(file, start, end));
//      }
//
//      loadNext();
// }
//
// // 上传
// function uploadFile() {
//     // 先检查是否有重名
//     // checkDuplicationName()
//     // 然后检查MD5
//     getMd5('upload-file');
//     // 然后开始上传
//     let xhr = new XMLHttpRequest();
//     let file = document.getElementById('upload-file').files[0];   //取得文件数据，而.file对象只是文件信息
//     let form = new FormData();   //FormData是HTML5为实现序列化表单而提供的类，更多细节可自行查询
//     form.append('upload-file',file);   //这里为序列化表单对象form添加一个元素，即file
//     xhr.upload.addEventListener('progress',onProgress,false);     //xhr对象含有一个upload对象，它有一个progress事件，在文件上传过程中会被不断触发，我们为这个事件对应一个处理函数，每当事件触发就会调用这个函数，于是便可利用这个函数来修改当前进度，更多细节可自行查询
//     xhr.open('POST','/bpcloud/upload_file/',true);  //请将url改成上传url
//     xhr.setRequestHeader('X-CSRFTOKEN','{{ request.COOKIES.csrftoken }}');   //此处为Django要求，可无视，或者换成相应后台所要求的CSRF防护，不是django用户请去掉
//     xhr.send(form);   //发送表单
// }
//
// function uploadDir() {
//     // 先检查是否有重名
//     checkDuplicationName();
//     // 然后检查MD5, 返回MD5 list
//     getMd5List('upload-dir');
//     // 发送Md5 list给后端，后端发送需要上传的，其他显示秒传
//     // 然后开始上传
//     let xhr = new XMLHttpRequest();
//     let files = document.getElementById('upload-dir').files;
//     let fd = new FormData();
//     let path_list = [];
//     for (let i = 0; i < files.length; i++) {
//         path_list.push(files[i].webkitRelativePath);
//         fd.append("upload-dir", files[i]);
//     }
//     fd.append('path', path_list);
//     //xhr对象含有一个upload对象，它有一个progress事件，
//     // 在文件上传过程中会被不断触发，我们为这个事件对应一个处理函数，
//     // 每当事件触发就会调用这个函数，于是便可利用这个函数来修改当前进度，更多细节可自行查询
//     xhr.upload.addEventListener('progress',onProgress,false);
//     xhr.open('POST','/bpcloud/upload_dir/',true);
//     //此处为Django要求，可无视，或者换成相应后台所要求的CSRF防护
//     xhr.setRequestHeader('X-CSRFTOKEN','{{ request.COOKIES.csrftoken }}');
//     xhr.send(fd);   //发送表单
// }
//
// function checkDuplicationName() {
//
// }
//
// function createNewFolder() {
//     let data = [];
//     let df_list = [];
//     data.push({'info': created_name});
//     data.push({'opera': 'create'});
//     data.push({'df_list': df_list});
//     opera(data);
// }
//
// function del() {
//     let info_list;
//     let data = [];
//     let df_list = [];
//     for(let info of info_list){
//         df_list.push({
//         'name':     info['name'],
//         'df_type':  info['df_type'],
//         });
//     }
//     data.push({'info': ''});
//     data.push({'opera': 'delete'});
//     data.push({'df_list': df_list});
//     opera(data);
// }
//
// function delCom() {
//     // 需要询问是否是彻底删除
//     let info_list;
//     let data = [];
//     let df_list = [];
//     for(let info of info_list){
//         df_list.push({
//         'name': info['name'],
//         'df_type': info['df_type'],
//         });
//     }
//     data.push({'info': ''});
//     data.push({'opera': 'delCom'});
//     data.push({'df_list': df_list});
//     opera(data);
// }
//
// function move() {
//     let info_list;
//     let data = [];
//     let df_list = [];
//     for(let info of info_list){
//         df_list.push({
//         'name': info['name'],
//         'df_type': info['df_type'],
//         });
//     }
//     data.push({'info': to_path});
//     data.push({'opera': 'moveTo'});
//     data.push({'df_list': df_list});
//     opera(data);
// }
//
// function copy() {
//     let info_list;
//     let data = [];
//     let df_list = [];
//     for(let info of info_list){
//         df_list.push({
//         'name': info['name'],
//         'df_type': info['df_type'],
//         });
//     }
//     data.push({'info': to_path});
//     data.push({'opera': 'copyTo'});
//     data.push({'df_list': df_list});
//     opera(data);
// }
//
// function rename() {
//     let data = [];
//     let df_list = [];
//     data.push({'info': to_path});
//     data.push({'opera': 'rename'});
//     data.push({'df_list': df_list});
//     opera(data);
// }
//
// function recover() {
//     let info_list;
//     let data = [];
//     let df_list = [];
//     for(let info of info_list){
//         df_list.push({
//         'name':     info['name'],
//         'df_type':  info['df_type'],
//         'delete_time':     info['del_time'],
//         });
//     }
//     data.push({'opera': 'recover'});
//     data.push({'df_list': df_list});
//     opera(data);
// }
//
// function opera(data) {
//     $.ajax({
//         url: "/bpcloud/dfile_opera/",
//         dataType: 'json',
//         type: 'GET',
//         data: data,
//         success: function (data) {
//             console.log('成功');
//         },
//         fail: function (data) {
//             console.log('失败');
//         }
//     });
// }