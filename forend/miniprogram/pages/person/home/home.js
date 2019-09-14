const app = getApp();
const personapi = require("../../../api/personapi.js")

Page({

    /**
     * 页面的初始数据
     */
    data: {},

    navHistory() {
        wx.navigateTo({
            url: '/pages/history/history',
        })
    },

    getInfo(e) {
        wx.navigateTo({
            url: '../edit/edit',
        })
    },

})