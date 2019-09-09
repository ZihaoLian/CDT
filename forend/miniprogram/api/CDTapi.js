const db = wx.cloud.database()
const clockNumColl = db.collection("testResult")
const fs = wx.getFileSystemManager(); //获取文件管理系统

class CDTapi {
    // 保存测试记录
    storeClock(hour, minute, fileName, drawArr1, drawArr2, image1, image2) {
        return new Promise(resolve=>{
            wx.showLoading({
                title: '正在上传数据',
                mask:true
            })
            this.saveFileAndImage(fileName, drawArr1, image1, 1)
            this.saveFileAndImage(fileName, drawArr2, image2, 2)

            clockNumColl.add({
                data: {
                    hour,
                    minute,
                    fileName,
                    time: new Date()
                }
            }).then(() => {
                resolve()
            })
        })
        
    }

    async saveFileAndImage(fileName, drawArr, image, idx) {
        // 创建数据文件1
        fs.writeFileSync(`${wx.env.USER_DATA_PATH}/${fileName}_${idx}.doc`, '-1 -1 -1\n', 'utf8')
        for (var j in drawArr) {
            fs.appendFileSync(`${wx.env.USER_DATA_PATH}/${fileName}_${idx}.doc`, drawArr[j].x.toString() + ' ' + drawArr[j].y.toString() + ' ' + drawArr[j].t.toString() + '\n', 'utf8')
        }

        // 上传数据文件
        await wx.cloud.uploadFile({
            cloudPath: `CDTData/${fileName}_${idx}.doc`,
            filePath: `${wx.env.USER_DATA_PATH}/${fileName}_${idx}.doc`
        })

        // 上传图片文件
        await wx.cloud.uploadFile({
            cloudPath: `CDTImage/${fileName}_${idx}.png`,
            filePath: image
        })
    }
}

module.exports = new CDTapi()