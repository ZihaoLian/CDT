// 云函数入口文件
const cloud = require('wx-server-sdk')

cloud.init()

// 云函数入口函数
exports.main = async (event, context) => {
    var fileName = 'data3.doc'
    var s1 = "(" + 2 + " " + 3 + " " + 3 + "/n";
    //var s = record_x.toString() + record_y.toString() + record_t.toString(); //将x,y,t写入文件中
    // fs.writeFileSync('C:/Data/' + fileName, s1, 'utf8');
    fs.writeFileSync(`${wx.env.USER_DATA_PATH}/` + fileName, s1, 'utf8');
    //fs.appendFileSync(`${wx.env.USER_DATA_PATH}/` + fileName, drawInfos, 'utf8');
    //var filepath = wx.env.USER_DATA_PATH + '/' + fileName
    // filepath = 'C:/Data/' + fileName;

    //上传到云文件中
    wx.cloud.init();
    wx.cloud.uploadFile({
      cloudPath: 'data3.doc',
      filePath: filepath,
      name: fileName,
    })
    console.log("ni")
}