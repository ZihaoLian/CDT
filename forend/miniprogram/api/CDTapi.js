let timeUtil = require('../utils/time.js')
const fs = wx.getFileSystemManager(); //获取文件管理系统
const app = getApp()
const subapi = `${app.globalData.host}/api/v1`

function upload(url, filePath, name, data) {
    return new Promise(resolve => {
        wx.uploadFile({
            url: url, //后台端口
            filePath: filePath, // 要发送的资源路径
            name: name, // 后端通过这个名字来获取前端发过去的资源文件
            method: 'POST',
            formData: data, // 额外的要发送给后端的表单数据
            success(res) {
                resolve(res)
            }
        })
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
            this.saveFileAndImage(fileName, drawArr2, image2, 2, handTime, testTime).then(res => {
                resolve(res) // 获得resolve数据才能返回
            })
        })

    },

    async saveFileAndImage(fileName, drawArr, image, idx, handTime, testTime) {
        let y = []
        for (let i in drawArr) {
            y.push(drawArr[i].y)
        }
        let max = Math.max.apply(null, y)

        for (let k in drawArr) {
            if (drawArr[k].y != -1) {
                drawArr[k].y = Math.abs(drawArr[k].y - max)
            }
        }

        // 创建数据文件1
        let filePath = `${wx.env.USER_DATA_PATH}/${fileName}_${idx}.csv`
        fs.writeFileSync(filePath, drawArr[0].x.toString() + ', ' + drawArr[0].y.toString() + ', ' + drawArr[0].t.toString() + '\n', 'utf8')
        for (var j = 1; j < drawArr.length; j++) {
            fs.appendFileSync(filePath, drawArr[j].x.toString() + ', ' + drawArr[j].y.toString() + ', ' + drawArr[j].t.toString() + '\n', 'utf8')
        }

        let data = {
            fileName: fileName,
            testTime: testTime,
            handTime: handTime,
            idx: idx,
            person: app.globalData.userInfo.openId,
            // person: 'opNJ75XxQ82mIEXpVUo3dSTMomv4'
        }

        await upload(`${subapi}/image/`, image, 'image', data)
        res = await upload(`${subapi}/file/`, filePath, 'file', data)
        return res
    },

    // 获取最近测试结果
    getHistory() {
        return app.get(`${subapi}/cdtTest/${app.globalData.userInfo.openId}`)
    }
}