// pages/descirbe/describe.js
const app = getApp();
Page({

    /**
     * 页面的初始数据
     */
    data: {
        CustomBar: app.globalData.CustomBar / 568 * app.globalData.sclar * 750,
        StatusBar: app.globalData.StatusBar / 568 * app.globalData.sclar * 750,
        list: [
            {
                time: '2019.09.09 12:00:00',
                unionId: "第一条"
            },
            {
                time: '2019.09.09 12:00:00',
                unionId: "第二条"
            }
        ]
    },

    /**
     * 生命周期函数--监听页面加载
     */
    onLoad: function (options) {

    },

    /**
     * 生命周期函数--监听页面初次渲染完成
     */
    onReady: function () {
        this.Modal = this.selectComponent("#modal");
    },

    /**
     * 生命周期函数--监听页面显示
     */
    onShow: function () {

    },

    /**
     * 生命周期函数--监听页面隐藏
     */
    onHide: function () {

    },

    /**
     * 生命周期函数--监听页面卸载
     */
    onUnload: function () {

    },

    /**
     * 页面相关事件处理函数--监听用户下拉动作
     */
    onPullDownRefresh: function () {

    },

    /**
     * 页面上拉触底事件的处理函数
     */
    onReachBottom: function () {

    },

    /**
     * 用户点击右上角分享
     */
    onShareAppMessage: function () {

    },

    showDialog: function() {
        this.Modal.showModal();  // show dialog
    },

    onDelete: function(e) {
        console.log(this.data.list)
        console.log("HGHG")
        //console.log(e.detail.list)
    }
  
})