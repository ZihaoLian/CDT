const app = getApp()
const personapi = require("../../../api/personapi.js")

// miniprogram/pages/person/edit/edit.js
Page({

    /**
     * 页面的初始数据
     */
    data: {
        ageList: [...(new Array(100)).keys()],
    },

    onLoad() {
        this.setData({
            profile: app.globalData.userInfo
        })
    },

    changeProfile(e) {
        this.data.profile[e.target.dataset.which] = e.detail.value
        this.setData({
            profile: this.data.profile
        })
    },

    bindGetUserInfo() {
        app.globalData.userInfo = this.data.profile
        personapi.updateUser(this.data.profile).then(res => console.log(res))
        wx.navigateBack()
    }
})