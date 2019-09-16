let timeUtil = require('../utils/time.js')
const fs = wx.getFileSystemManager(); //获取文件管理系统
const app = getApp()
const subapi = `${app.globalData.host}/api/v1`

function upload(url, filePath, name, data){
    wx.uploadFile({
        url: url,             //后台端口
        filePath: filePath,   // 要发送的资源路径
        name: name,           // 后端通过这个名字来获取前端发过去的资源文件
        method: 'POST',
        formData: data,       // 额外的要发送给后端的表单数据
        success(res) {
            console.log(res)
            //do something
        }
    })
}

module.exports = {
    // 保存测试记录
    storeClock(hour, minute, fileName, drawArr1, drawArr2, image1, image2) {
        return new Promise(resolve => {
            wx.showLoading({
                title: '正在上传数据',
                mask: true
            })
            
            let hourFormat = timeUtil.timeFormat(hour)
            let minuteFormat = timeUtil.timeFormat(minute)
            let handTime = hourFormat + ':' + minuteFormat;
            let testTime = timeUtil.getTime()

            // let testData = {
            //     testTime: time,
            //     handTime: handTime,
            //     person: app.globalData.userInfo.openId,
            // }
            // app.post(`${subapi}/cdtTest/`, testData)

            this.saveFileAndImage(fileName, drawArr1, image1, 1, handTime, testTime)
            this.saveFileAndImage(fileName, drawArr2, image2, 2, handTime, testTime)
            resolve()  // 获得resolve数据才能返回
        })

    },

    async saveFileAndImage(fileName, drawArr, image, idx, handTime, testTime) {
        // 创建数据文件1
        let filePath = `${wx.env.USER_DATA_PATH}/${fileName}_${idx}.docx`
        fs.writeFileSync(filePath, '-1 -1 -1\n', 'utf8')
        for (var j in drawArr) {
            fs.appendFileSync(filePath, drawArr[j].x.toString() + ' ' + drawArr[j].y.toString() + ' ' + drawArr[j].t.toString() + '\n', 'utf8')
        }

        let data = {
            fileName: fileName,
            testTime: testTime,
            handTime: handTime,
            person: app.globalData.userInfo.openId,
        }

        await upload(`${subapi}/file/`, filePath, 'file', data)
        await upload(`${subapi}/image/`, image, 'image', data)
    }
}