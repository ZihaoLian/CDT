let timeUtil = require('../utils/time.js')

const db = wx.cloud.database()
const clockNumColl = db.collection("testResult")
const fs = wx.getFileSystemManager(); //获取文件管理系统
const app = getApp()
const subapi = `${app.globalData.host}/api/v1`

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
            let time = timeUtil.getTime()

            let testData = {
                testTime: time,
                handTime: handTime,
                person: app.globalData.userInfo.openId,
            }
            app.post(`${subapi}/cdtTest/`, testData)

            this.saveFileAndImage(fileName, drawArr1, image1, 1, handTime, time)
            this.saveFileAndImage(fileName, drawArr2, image2, 2, handTime, time)

            // clockNumColl.add({
            //     data: {
            //         hour,
            //         minute,
            //         fileName,
            //         time: new Date()
            //     }
            // }).then(() => {
            //     resolve()
            // })
        })

    },

    async saveFileAndImage(fileName, drawArr, image, idx, handTime, time) {
        // 创建数据文件1
        fs.writeFileSync(`${wx.env.USER_DATA_PATH}/${fileName}_${idx}.doc`, '-1 -1 -1\n', 'utf8')
        for (var j in drawArr) {
            fs.appendFileSync(`${wx.env.USER_DATA_PATH}/${fileName}_${idx}.doc`, drawArr[j].x.toString() + ' ' + drawArr[j].y.toString() + ' ' + drawArr[j].t.toString() + '\n', 'utf8')
        }

        // let fileData = {
        //     name: fileName,
        //     file: `${wx.env.USER_DATA_PATH}/${fileName}_${idx}.doc`,
        //     testTime: time,
        //     person: app.globalData.userInfo.openId,
        // }
        
        // await app.post(`${subapi}/file/`, fileData)

        //console.log(image)
        let imageData = {
            name: fileName,
            image: image,
            testTime: time,
            person: app.globalData.userInfo.openId,
        }
        await wx.uploadFile({
            url: `${subapi}/image/`, //仅为示例，非真实的接口地址
            filePath: image,
            name: 'file',
            method: 'POST',
            formData: imageData,
            success(res) {
                const data = res.data
                console.log(res)
                //do something
            }
        })
        // await app.post(`${subapi}/image/`, imageData)
       
        // try{
        //     // 定义表格名
        //     let dataCVS = fileName + idx + '.xlsx'
        //     let allData = drawArr;
        //     // 将数据存到excel中
        //     const buffer = xlsx.build([{
        //         name: 'cdtData',
        //         data: allData
        //     }])
        //     console.log('将数据存到excel中')
        //     // 将excle文件保存到云存储里
        //     fs.writeFile('test1.xlsx', allData, err => {
        //         if(err){
        //             console.log("导出表格失败")
        //             throw new Error(err)
        //         }
        //     });
        //     return await cloud.uploadFile({
        //         cloudPath: dataCVS,
        //         fileContent: buffer  // excel二进制文件
        //     })
        // }
        // catch(e){
        //     console.error(e)
        // }

        
        
        // 上传数据文件
        // await wx.cloud.uploadFile({
        //     // cloudPath: `CDTData/${fileName}_${idx}.doc`,
        //     // filePath: `${wx.env.USER_DATA_PATH}/${fileName}_${idx}.doc`
        // })
        // // 上传图片文件
        // await wx.cloud.uploadFile({
        //     cloudPath: `CDTImage/${fileName}_${idx}.png`,
        //     filePath: image
        // })
    }
}