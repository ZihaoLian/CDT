const app = getApp()

// miniprogram/pages/person/edit/edit.js
Page({

    /**
     * 页面的初始数据
     */
    data: {
        CustomBar: app.globalData.CustomBar / 568 * app.globalData.sclar * 750,
        StatusBar: app.globalData.StatusBar / 568 * app.globalData.sclar * 750,
        ageList: [...(new Array(100)).keys()],
    },

    onLoad(){
        this.setData({
            profile:app.globalData.userInfo
        })
    },

    changeProfile(e) {
        this.data.profile[e.target.dataset.which] = e.detail.value
        this.setData({
            profile: this.data.profile
        })
    },

    bindGetUserInfo(){
        app.globalData.userInfo = this.data.profile
        wx.navigateBack()
    }
})