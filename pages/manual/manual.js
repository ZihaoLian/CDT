// pages/manual/manual.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    manualImg: [{
      url: 'https://gss0.baidu.com/9vo3dSag_xI4khGko9WTAnF6hhy/zhidao/pic/item/dcc451da81cb39dbdfa123c0d0160924aa1830c6.jpg',
        txt: "教程1"
      },
      {
        url: 'https://gss0.baidu.com/9vo3dSag_xI4khGko9WTAnF6hhy/zhidao/pic/item/dcc451da81cb39dbdfa123c0d0160924aa1830c6.jpg',
        txt: "教程2"
      },
      {
        url: 'https://gss0.baidu.com/9vo3dSag_xI4khGko9WTAnF6hhy/zhidao/pic/item/dcc451da81cb39dbdfa123c0d0160924aa1830c6.jpg',
        txt: "教程3"
      }
    ],
    index:0,

  },
  bindChange: function(e) {
    var appInstance = this;
    var bindex = e.detail.current;
    console.log(bindex);
    var length = appInstance.data.manualImg.length;
    if (bindex == length - 1) {
      wx.showModal({
        title: '开始测试',
        content: '',
        success: function(res) {
          if (res.confirm) {
            console.log('用户点击确定')
            wx.redirectTo({
              url: '../logs/logs'
            });
          } else if (res.cancel) {
            console.log('用户点击取消')
            appInstance.setData({
              index: e.detail.current-1
            })
          }
        }
      });
    }
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

  }

})