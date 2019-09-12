const app = getApp();
const personapi = require("../../../api/personapi.js")

Page({

    /**
     * 页面的初始数据
     */
    data: {},

    getInfo(e) {
        if (e.detail.errMsg == "getUserInfo:fail auth deny") {
            wx.showToast({
                title: '暂未登录，无法编辑资料',
                icon: "none"
            })
        } else {
            personapi.login().then(res => {
                app.globalData.userInfo = res
            }).catch(() => {
                for (let item in e.detail.userInfo) {
                    app.globalData.userInfo[item] = e.detail.userInfo[item]
                }
                personapi.newUser()
            })
            wx.navigateTo({
                url: '../edit/edit',
            })
        }
    }
})