App({
    globalData: {
        userInfo: {},
        host: "http://127.0.0.1:8000"
    },
    onLaunch: function() {
        wx.getSystemInfo({
            success: e => {
                this.globalData.StatusBar = e.statusBarHeight;
                this.globalData.CustomBar = e.statusBarHeight + 46;
                // 用于转换成rpx
                this.globalData.scale = e.screenWidth * 2 / 750
                this.globalData.ContentHeight = e.screenHeight - this.globalData.CustomBar - 60;
                //console.log(e.screenHeight)
            }
        })


        wx.cloud.init({
            traceUser: true,
        })


        wx.cloud.callFunction({
            name: "login"
        }).then(res => {
            this.globalData.userInfo.openId = res.result.openid
        })
    },

    get(url, data) {
        return new Promise((resolve, reject) => {
            //网络请求
            wx.request({
                url,
                data,
                success: function(res) { //服务器返回数据
                    if (res.statusCode == 200) {
                        resolve(res.data);
                    } else { //返回错误提示信息
                        if (res.data.detail) {
                            reject(res.data.detail)
                        } else
                            reject(res.data.errMsg);
                    }
                },
                fail: function(e) {
                    reject('网络出错');
                }
            })
        });
    },

    post(url, data) {
        return new Promise((resolve, reject) => {
            //网络请求
            wx.request({
                url,
                data,
                method: 'POST',
                header: {
                    'content-type': 'application/json'
                },
                success: function(res) { //服务器返回数据
                    if (res.statusCode == 201 || res.statusCode == 200) {
                        resolve(res.data);
                    } else { //返回错误提示信息
                        console.log(res.data)
                        reject()
                    }
                },
                fail: function(e) {
                    reject('网络出错');
                }
            })
        });
    },

    put(url, data) {
        return new Promise((resolve, reject) => {
            //网络请求
            wx.request({
                url,
                data,
                method: 'PUT',
                success: function(res) { //服务器返回数据
                    if (res.statusCode == 200) {
                        resolve(res.data)
                    }
                },
                fail: function(e) {
                    reject('网络出错');
                }
            })
        });
    },

})