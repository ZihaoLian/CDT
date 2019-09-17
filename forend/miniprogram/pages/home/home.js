// pages/home/home.js
const app = getApp();
const personapi = require("../../api/personapi.js")

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

    onLoad() {
        wx.cloud.callFunction({
            name: "login"
        }).then(res => {
            app.globalData.userInfo.openId = res.result.openid
            return personapi.login()
        }).then(res => app.globalData.userInfo = res,
            () => {
                wx.showModal({
                    title: '温馨提示',
                    content: '是否需要查看教程，以帮助您快速上手我们的小程序',
                    success(res){
                        if(res.confirm){
                            wx.redirectTo({
                                url: '/pages/manual/manual',
                            })
                        }
                    }
                })
                return personapi.newUser()
            }).then(res => app.globalData.userInfo = res)
    },


})