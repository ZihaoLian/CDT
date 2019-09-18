// pages/test/test.js
const app = getApp();
const CDTapi = require("../../api/CDTapi.js")

var startX = 0;
var startY = 0;
var begin = false; //设置是否开始绘画

Page({
    /**
     * 页面的初始数据
     */
    data: {
        CustomBar: app.globalData.CustomBar / 568 * app.globalData.sclar * 750,
        StatusBar: app.globalData.StatusBar / 568 * app.globalData.sclar * 750,
        // canvasHeight: (341 / 568) * app.globalData.sclar * 750 * 2,
        canvasHeight: (820 / 1334) * app.globalData.sclar * 1334 * 2,
        hour: 0,
        minute: 0,
        step_tip: '请点击开始按钮进行测试',
        showModal: false,
        is_begin_draw: false,
        showModalStatus: false,

        tempArr: [],
        drawArr1: [],
        drawArr2: [],
        image1: "",
        image2: "",
        secondStep: false
    },


    onLoad: function() {
        this.context = wx.createCanvasContext('canvas')
    },

    onShow() {
        this.data.drawArr1 = []
        this.data.drawArr2 = []
        this.data.image1 = ""
        this.data.image2 = ""
        this.data.interval && clearInterval(this.data.interval); //关掉定时器

        this.setData({
            is_begin_draw: false, //防止下次进来后就直接进行画钟
            step_tip: "请点击开始按钮进行测试",
            secondStep: false
        })

        this.clear()
    },


    // 开始绘制线条
    lineBegin: function(x, y) {
        if (this.data.is_begin_draw) {
            begin = true;
            this.context.beginPath();
            startX = x;
            startY = y;
            console.log(startX, startY)
            this.lineAddPoint(x, y);
        }
    },

    // 绘制线条中间添加点
    lineAddPoint: function(x, y) {
        this.context.moveTo(startX, startY)
        this.context.lineTo(x, y);
        this.context.stroke();
        startX = x;
        startY = y;
    },

    // 绘制线条结束
    lineEnd: function() {
        this.context.closePath();
        begin = false;
    },

    // 绘制开始 手指开始按到屏幕上
    touchStart: function(e) {
        if (!this.data.is_begin_draw) { //必须先按开始按钮才能开始测试
            this.tishiStart();
        } else {
            this.lineBegin(e.touches[0].x, e.touches[0].y)
        }
    },

    // 绘制中 手指在屏幕上移动
    touchMove: function(e) {
        if (begin) {
            this.lineAddPoint(e.touches[0].x, e.touches[0].y);
            this.context.draw(true);
        }
    },

    // 绘制结束 手指抬起
    touchEnd: function() {
        if (begin) {
            this.data.tempArr.push({ //用来标记笔画的结束
                x: -1,
                y: -1,
                t: -1
            })
            this.lineEnd();
        }
    },


    // 生成随机的文件名
    genFileName() {
        return (Math.random() * 10000000).toString(16).substr(0, 4) + Date.now().toString();
    },

    //开始画钟
    start_draw: function() {
        this.clear()

        // 允许开始画钟
        this.setData({
            is_begin_draw: true,
        })

        if (this.data.secondStep == false) {
            this.createNonceStr(); //随机生成时钟点数、设置上传路径
        }

        this.record_XY(); //开始记录数据
    },

    //下一步进行复现画钟
    next_step: function() {
        if (this.data.tempArr.length != 0) { //防止没开始就点击下一步了
            wx.showToast({
                title: '步骤一已完成'
            })
            this.saveDraw('image1')
            this.data.drawArr1 = this.data.tempArr

            this.clear()
            clearInterval(this.data.interval); //关掉定时器

            this.setData({
                is_begin_draw: false, //防止下次进来后就直接进行画钟
                step_tip: "步骤二：请复现你刚才画的时钟",
                secondStep: true
            })
        } else {
            this.void_withoutDraw();
        }
    },

    finsh() {
        let that = this
        if (this.data.tempArr.length != 0) {
            this.saveDraw('image2')
            this.data.drawArr2 = this.data.tempArr
            this.data.tempArr = []

            this.clear()
            clearInterval(this.data.interval); //关掉定时器
        } else {
            this.void_withoutDraw();
        }
    },

    void_withoutDraw: function() {
        wx.showModal({
            title: '提示',
            content: '你还没开始画钟呢，请画完再继续下一步',
            showCancel: false,
            confirmColor: '#000000'
        })
    },

    cancel_step: function() {
        this.clear(); // 清空数组内容 
    },

    //随机生成时钟点数
    createNonceStr: function() {
        this.setData({
            hour: Math.floor(Math.random() * 120 % 12),
            minute: parseInt(Math.random() * 120 % 12)
        })
        while (Math.abs(this.data.hour - this.data.minute) < 3 || Math.abs(this.data.hour - this.data.minute) > 4) { //不让时针和分针靠的太近
            this.setData({
                hour: Math.floor(Math.random() * 120 % 12),
                minute: parseInt(Math.random() * 120 % 12)
            })
        }
        this.setData({
            hour: this.data.hour + 1,
            minute: this.data.minute * 5,
        })
        this.setData({
            step_tip: "步骤一：请画出一个" + this.data.hour + "点" + this.data.minute + "分的时钟",
            fileName: this.genFileName()
        })
    },

    //存储数据
    store() {
        let that = this
        CDTapi.storeClock(this.data.hour, this.data.minute, this.data.fileName, this.data.drawArr1, this.data.drawArr2, this.data.image1, this.data.image2).then(res => {
            wx.hideLoading()
            console.log(JSON.parse(res.data))
            if (!JSON.parse(res.data).result) {
                wx.showModal({
                    title: '测试结果',
                    content: '恭喜您，身体状况良好，请继续保持',
                    showCancel: false,
                    confirmText: "我知道了",
                    success(res) {
                        if (res.confirm) {
                            wx.showModal({
                                title: '提示',
                                content: '你已经完成画钟测试了，是否再测试一次',
                                cancelColor: "#000000",
                                confirmColor: "#000000",
                                success(res) {
                                    if (res.confirm) {
                                        that.setData({
                                            is_begin_draw: false, //防止下次进来后就直接进行画钟
                                            step_tip: "请点击开始按钮进行测试",
                                            secondStep: false
                                        })
                                        that.clear()
                                    } else if (res.cancel) {
                                        wx.switchTab({
                                            url: '../home/home',
                                        })
                                    }
                                }
                            })
                        }
                    }
                })
            }
        })
    },


    //保存最后绘制的图片
    saveDraw(which) {
        let that = this
        wx.canvasToTempFilePath({
            x: app.globalData.screen_width * (7 / 750),
            y: app.globalData.screen_heigh * (125 / 568),
            width: app.globalData.screen_width * 0.98,
            height: 341 / 568 * app.globalData.screen_height,
            destWidth: 256,
            destHeight: 256,
            canvasId: 'canvas',
            success(res) {
                that.data[which] = res.tempFilePath
                if (which == "image2") {
                    that.store()

                }
            }
        })
    },

    //清除画布上的内容
    clear: function() {
        startX = 0;
        startY = 0;
        this.data.tempArr = []; //清空绘画笔迹
        this.context.setFillStyle('#ffffff');
        this.context.fillRect(app.globalData.screen_width * (5 / 750), app.globalData.screen_heigh * (125 / 568), app.globalData.screen_width * 0.98, 341 / 568 * app.globalData.screen_height);
        this.context.draw();
    },

    //控制用户必须点击开始按钮才能进行测试
    tishiStart: function() {
        wx.showModal({
            title: '提示',
            content: '请先点击开始按钮再开始',
            showCancel: false,
            confirmColor: '#000000'
        })
    },


    //用来定时获取记录数据
    record_XY() {
        var t_num = 0
        this.data.interval = setInterval(() => {
            if ((startX != 0 || startY != 0) && begin) {
                this.data.tempArr.push({ //每隔12ms记录一次
                    x: startX,
                    y: startY,
                    t: t_num
                });
            }
            t_num += 12
        }, 12)
    }
})