// pages/test/test.js
const app = getApp();
var startX = 0;
var startY = 0;
var begin = false; //设置是否开始绘画
var curDrawArr = []; //用来存储每个笔画的轨迹
var drawInfos = []; //用来存储每个笔画数组的数组
var timer; //计时器
var time_num = 0;
var t_num = 0;
var record_x = 0;
var record_y = 0;
var record_t = 0;

wx.cloud.init()

Page({

    /**
     * 页面的初始数据
     */
    data: {
        CustomBar: app.globalData.CustomBar,
        StatusBar: app.globalData.StatusBar,
        filePath: wx.env.USER_DATA_PATH+'/data.doc'
    },

    /**
     * 生命周期函数--监听页面加载
     */
    onLoad: function(options) {
    },

    /**
     * 生命周期函数--监听页面初次渲染完成
     */
    onReady: function() {
        this.context = wx.createCanvasContext('firstcanvas'); //获取画布
        this.fs = wx.getFileSystemManager(); //获取文件管理系统

    },

    /**
     * 生命周期函数--监听页面显示
     */
    onShow: function() {

    },

    /**
     * 生命周期函数--监听页面隐藏
     */
    onHide: function() {

    },

    /**
     * 生命周期函数--监听页面卸载
     */
    onUnload: function() {

    },

    /**
     * 页面相关事件处理函数--监听用户下拉动作
     */
    onPullDownRefresh: function() {

    },

    /**
     * 页面上拉触底事件的处理函数
     */
    onReachBottom: function() {

    },

    /**
     * 用户点击右上角分享
     */
    onShareAppMessage: function() {

    },

    //存储数据
    store() {
        this.fs.writeFileSync(this.data.filePath, '', 'utf8')
        for (var i in drawInfos) {
            var stroke = drawInfos[i]
            for (var j in stroke) {
                this.fs.appendFileSync(this.data.filePath, stroke[j].x.toString()+','+stroke[j].y.toString()+'\n', 'utf8')
            }
        }
        // wx.openDocument({
        //     filePath: this.data.filePath,
        //     fileType: 'doc'
        // })
        wx.cloud.uploadFile({
          cloudPath: 'data.doc',
          filePath: this.data.filePath,
        })
    },

    // 开始绘制线条
    lineBegin: function(x, y) {
        begin = true;
        this.context.beginPath();
        startX = x;
        startY = y;
        //this.context.moveTo(startX, startY)
        this.lineAddPoint(x, y);
    },
    // 绘制线条中间添加点
    lineAddPoint: function(x, y) {
        this.context.moveTo(startX, startY)
        record_XY(x, y); //开始每过12ms记录一次位置
        // storedata(x, y, t_num); //存储进文件里
        // console.log(startX, startY);
        this.context.lineTo(x, y);
        this.context.stroke();
        startX = x;
        startY = y;
    },

    // 绘制线条结束
    lineEnd: function() {
        this.context.closePath();
        begin = false;
        clearTimeout(timer); //清除定时器
    },

    // 绘制开始 手指开始按到屏幕上
    touchStart: function(e) {
        this.lineBegin(e.touches[0].x, e.touches[0].y)
        curDrawArr.push({
            x: e.touches[0].x,
            y: e.touches[0].y
        });
    },

    // 绘制中 手指在屏幕上移动
    touchMove: function(e) {
        if (begin) {
            this.lineAddPoint(e.touches[0].x, e.touches[0].y);
            this.context.draw(true);
            curDrawArr.push({
                x: e.touches[0].x,
                y: e.touches[0].y
            });
        }
    },

    // 绘制结束 手指抬起
    touchEnd: function() {
        curDrawArr.push({ //用来标记笔画的结束
            x: -1,
            y: -1
        })
        drawInfos.push(curDrawArr); //将笔画存入到数组中
        curDrawArr = []; //将笔画清空，以备继续使用
        this.lineEnd();
    },

    //开始画钟
    start_draw: function() {
        console.log(t_num.toString())
    },

    //实现不将数据存入云存储钟
    removedata: function() {
        var object = {
            'filepath': wx.env.USER_DATA_PATH + '/' + fileName
        }
        this.fs.removeSavedFile(object)
    },

    next_step: function() {
        this.store()
    },

    cancel_draw: function() {

    }
})

//用来定时获取记录数据
function record_XY(x, y) {s
    t_num = time_num * 12;
    timer = setTimeout(function() {
        // console.log(x, y, t_num); 
        time_num = time_num + 1;
        record_XY(x, y);
    }, 12)
}
