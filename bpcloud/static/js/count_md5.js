// var running = false;
// getFileMd5=function(file,template){
//     if (running) {
//         return;
//     }
//
//     if (!file) {
//         return;
//     }
//
//     var blobSlice = File.prototype.slice || File.prototype.mozSlice || File.prototype.webkitSlice,
//         chunkSize = 2097152,                           // read in chunks of 2MB
//         chunks = Math.ceil(file.size / chunkSize),
//         currentChunk = 0,
//         spark = new SparkMD5.ArrayBuffer(),
//         fileReader = new FileReader();
//
//     fileReader.onload = function (e) {
//         console.log('read chunk nr', currentChunk + 1, 'of', chunks);
//         spark.append(e.target.result);                   // Append array buffer
//         currentChunk++;
//
//         if (currentChunk < chunks) {
//             loadNext();
//         } else {
//             running = false;
//             var md5=spark.end();
//             template.find("#inputMd5sum").value = md5;
//             console.info('getFileMd5 finished loading computed hash',md5);  // Compute hash
//         }
//     };
//
//     fileReader.onerror = function () {
//         running = false;
//         console.warn('oops, getFileMd5 something went wrong.');
//     };
//
//     function loadNext() {
//         var start = currentChunk * chunkSize,
//             end = start + chunkSize >= file.size ? file.size : start + chunkSize;
//
//         fileReader.readAsArrayBuffer(blobSlice.call(file, start, end));
//     }
//
//     running = true;
//     loadNext();
// };

// 计算md5
function getMd5(file_object, filename) {
    //声明必要的变量
    let fileReader = new FileReader();
    //文件分割方法（注意兼容性）
    let blobSlice = File.prototype.mozSlice || File.prototype.webkitSlice || File.prototype.slice,
    file = file_object,
    //文件每块分割2M，计算分割详情
    chunkSize = 2097152,
    chunks = Math.ceil(file_object.size / chunkSize),
    currentChunk = 0,

    //创建md5对象（基于SparkMD5）
    spark = new SparkMD5();

    //每块文件读取完毕之后的处理
    fileReader.onload = function(e) {
        console.log("读取文件", currentChunk + 1, "/", chunks);
        //每块交由sparkMD5进行计算
        spark.appendBinary(e.target.result);
        currentChunk++;

        //如果文件处理完成计算MD5，如果还有分片继续处理
        if (currentChunk < chunks) {
            loadNext();
        } else {

            let file_hash = spark.end();
            $.ajax({
                url: '/bpcloud/hash_check/',
                dataType: 'json',
                type: 'POST',
                data: {'hash_code': file_hash},
                success: function (res) {
                    if(res['res'] === 'exist'){
                        // alert(res['res'])
                        // 秒传,刷新页面
                        // flushPage();
                    }
                    else {
                        // 上传
                        // alert(res['res']);
                        xhrUploadFile(file_object, file_hash, filename);
                    }
                },
                fail: function (res) {
                    console.log('失败');
                }
        });
        }
    };

     //处理单片文件的上传
     function loadNext() {
         let start = currentChunk * chunkSize, end = start + chunkSize >= file.size ? file.size : start + chunkSize;
         fileReader.readAsBinaryString(blobSlice.call(file, start, end));
     }

     loadNext();
}