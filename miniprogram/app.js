//app.js
//const worker = wx.createWorker('workers/request/index.js')
App({
    onLaunch: function() {
        wx.getSystemInfo({
            success: e => {
                this.globalData.StatusBar = e.statusBarHeight;
                this.globalData.CustomBar = e.statusBarHeight + 46;
                // 用于转换成rpx
                this.globalData.scale = e.screenWidth / 750
                this.globalData.ContentHeight = e.screenHeight - this.globalData.CustomBar - 60;
            }
        })


        wx.cloud.init({
            traceUser: true,
        })


        // 展示本地存储能力
        var logs = wx.getStorageSync('logs') || []
        logs.unshift(Date.now())
        wx.setStorageSync('logs', logs)


        // 获取用户信息
        wx.getSetting({
            success: res => {
                if (res.authSetting['scope.userInfo']) {
                    // 已经授权，可以直接调用 getUserInfo 获取头像昵称，不会弹框
                    wx.getUserInfo({
                        success: res => {
                            // 可以将 res 发送给后台解码出 unionId
                            this.globalData.userInfo = res.userInfo

                            // 由于 getUserInfo 是网络请求，可能会在 Page.onLoad 之后才返回
                            // 所以此处加入 callback 以防止这种情况
                            if (this.userInfoReadyCallback) {
                                this.userInfoReadyCallback(res)
                            }
                        }
                    })
                }
            }
        })

        wx.cloud.callFunction({
            name: "login"
        }).then(res => {
            this.globalData.openId = res.result.openid
        })
    },
    globalData: {
        userInfo: null,
    }
})