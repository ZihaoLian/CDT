// pages/home/home.js
const app = getApp();
Page({

    /**
     * 页面的初始数据
     */
    data: {
        autoplay: true,
        indicatorDots: true,
        circular_information: true,
        CustomBar: app.globalData.CustomBar,
        ContentHeight: app.globalData.ContentHeight
    },

    query_jiaocheng: function() {
        wx.navigateTo({
            url: '../manual/manual',
        })
    },

    toDescribe: function() {
        wx.switchTab({
            url: '../test/test',
        })
    },

    setting: function() {
        wx.navigateTo({
            url: '../setting/setting',
        })
    }
})