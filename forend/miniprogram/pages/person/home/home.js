// pages/personCenter/personCenter.js
const app = getApp();
Page({

    /**
     * 页面的初始数据
     */
    data: {
        CustomBar: app.globalData.CustomBar / 568 * app.globalData.sclar * 750,
        StatusBar: app.globalData.StatusBar / 568 * app.globalData.sclar * 750,
    },

    getInfo(e) {
        if (e.detail.errMsg == "getUserInfo:fail auth deny") {
            wx.showToast({
                title: '暂未登录，无法编辑资料',
                icon: "none"
            })
        } else {
            if (!app.globalData.userInfo) {
                app.globalData.userInfo = e.detail.userInfo
            }
            wx.navigateTo({
                url: '../edit/edit',
            })
        }
    }
})