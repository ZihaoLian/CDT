// pages/test/test.js
const app = getApp();
var startX = 0;
var startY = 0;
var begin = false; //设置是否开始绘画
var curDrawArr = []; //用来存储每个笔画的轨迹
var timer; //计时器
var time_num = 0;
var t_num = 0;

wx.cloud.init()

Page({
    /**
     * 页面的初始数据
     */
    data: {
      CustomBar: app.globalData.CustomBar/568 * app.globalData.sclar * 750,
      StatusBar: app.globalData.StatusBar/568 * app.globalData.sclar * 750,
      canvasHeight: 341/ 568 * app.globalData.sclar * 750,
      filepath: wx.env.USER_DATA_PATH + '/',       
      hour: 0, 
      minute: 0,
      step_tip: '请点击开始按钮进行测试',
      filename: '' ,
      showModal: false,
      is_begin_draw: false,
      showModalStatus: false,
      is_empty : false,
      is_next_step: false
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
      this.context = wx.createCanvasContext('firstcanvas'); //获取画布
      this.fs = wx.getFileSystemManager(); //获取文件管理系统
      this.db = wx.cloud.database(); //获取数据库系统
      this.getOpen(); //获得用户的openid来自动命名文件
      if(app.globalData.userLoginNumber > 1){
        this.clear(); //在这里必须将画布画成白色，否则后面将画布转化为图片背景就会变成透明的
      }
    },

    /**
     * 生命周期函数--监听页面隐藏
     */
    onHide: function() {
      //this.store()
      //clearTimeout(timer); //关掉定时器
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

    // 开始绘制线条
    lineBegin: function(x, y) {
      if(this.data.is_begin_draw){
        begin = true;
        this.context.beginPath();
        startX = x;
        startY = y;
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
      if(!this.data.is_begin_draw){ //必须先按开始按钮才能开始测试
        this.tishiStart();
      }
      else{
        this.setData({
          is_next_step: true //放在这里防止用户不画钟就点击下一步
        })
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
      curDrawArr.push({ //用来标记笔画的结束
          x: -1,
          y: -1,
          t: -1
      })
      this.lineEnd();
    },

  //开始画钟
  start_draw: function() {
    this.context.setFillStyle('#ffffff');
    this.context.fillRect(app.globalData.screen_width * (7 / 750), app.globalData.screen_heigh * (125 / 568), app.globalData.screen_width * 0.98, 341 / 568 * app.globalData.screen_height);
    this.context.draw();

    //设置上传路径 和 允许开始画钟
    this.setData({
      filepath: this.data.filepath + this.data.filename.toString() + '_' + app.globalData.userLoginNumber.toString() + '_1.doc',
      is_begin_draw: true,
      is_empty: false
    })

    this.createNonceStr(); //随机生成时钟点数
    record_XY(); //开始记录数据
  },

  //下一步进行复现画钟
  next_step: function() {
    if(this.data.is_next_step && !this.data.is_empty){ //防止没开始就点击下一步了
      wx.showToast({
        title: '请稍等片刻上传数据',
        icon: 'loading'
      })
      this.store();
      clearTimeout(timer); //关掉定时器
      this.setData({
        is_begin_draw: false, //防止下次进来后就直接进行画钟
        is_next_step: false,
        is_empty: true
      })
      //this.clear(); // 清楚数据，以备下次继续使用
      wx.showToast({
        title: '步骤一已完成',
        duration: 1000,
        success: function () {
          wx.navigateTo({
            url: '../test2/test2',
          })
        }
      })
    }
    else{
      this.void_withoutDraw();
    }
  },

  void_withoutDraw:function(){
    wx.showModal({
      title: '提示',
      content: '你还没开始画钟呢，请画完再继续下一步',
      showCancel: false,
      confirmColor: '#000000'
    })
  },

  cancel_step: function(){
    if(this.data.is_next_step){
      wx.showModal({
        title: '确定要取消吗?',
        content: '取消后将重新进行测试!!!',
        showCancel: false,
        confirmColor: '#000000',
        success(res) {
          if (res.confirm) {
          }
        }
      })
      this.clear(); // 清空数组内容 
      this.setData({
        is_empty : true, //防止点击“取消”后点击“下一步”
        is_begin_draw: false,
        is_next_step: false
      })
      
    }
    else{
      this.void_withoutDraw();
    }
  },

  //随机生成时钟点数
  createNonceStr: function () {
    this.setData({
      hour: Math.floor(Math.random() * 120 % 12),
      minute: parseInt(Math.random() * 120 % 12)
    })
    while (Math.abs(this.data.hour - this.data.minute) < 3 || Math.abs(this.data.hour - this.data.minute)>5){ //不让时针和分针靠的太近
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
      step_tip: "请画出一个" + this.data.hour + "点" + this.data.minute + "分的时钟"
    })
  },

  //获取用户的openid来自动命名文件
  getOpen: function () {
    wx.cloud.callFunction({
      name: 'getUserOpenId',
      complete: res => {
        this.setData({
          filename: res['result']['openid']
        })
      }
    })
  },

  //存储数据
  store() {
    this.record_clock(); //记录时钟点数
    this.fs.writeFileSync(this.data.filepath.toString() + this.data.filename.toString() + '_' + app.globalData.userLoginNumber.toString() + '_1.doc', '-1 -1 -1\n', 'utf8')

    for (var j in curDrawArr) {
      this.fs.appendFileSync(this.data.filepath.toString() + this.data.filename.toString() + '_' + app.globalData.userLoginNumber.toString() + '_1.doc', curDrawArr[j].x.toString() + ' ' + curDrawArr[j].y.toString() + ' ' + curDrawArr[j].t.toString() + '\n', 'utf8')
    }

    //判断是否上传数据
    if (!this.data.is_empty) {
      this.save_data_draw(this.data.filename.toString()) //保存数据
      this.save_first_draw(this.data.filename.toString()) //保存图片
    }
    else{
      this.delete_clock();
    }
  },

  //保存数据
  save_data_draw:function(filename){
    wx.cloud.uploadFile({
      cloudPath: 'CDTData/' + filename + '_' + app.globalData.userLoginNumber.toString()+ '_1.doc',
      filePath: this.data.filepath.toString() + filename + '_' + app.globalData.userLoginNumber.toString() + '_1.doc',
      success: res => {
        console.log("数据上传成功")
      }
    })
  },


  //保存最后绘制的图片
  save_first_draw: function (filename) {
    wx.canvasToTempFilePath({
      x: app.globalData.screen_width * (7 / 750),
      y: app.globalData.screen_heigh*(125/568),
      width: app.globalData.screen_width * 0.98,
      height: 341/ 568 * app.globalData.screen_height,
      destWidth: 256,
      destHeight: 256,
      canvasId: 'firstcanvas',
      success(res) {
        //将截取的图片上传到云存储上
        wx.cloud.uploadFile({
          cloudPath: 'CDTImage/' + filename + '_'+ app.globalData.userLoginNumber.toString()+ '_1.png',
          filePath: res.tempFilePath, // 文件路径
          success: res => {
            console.log("图片上传成功")
          },
          fail: err => {
            // handle error
            console.log("图片上传失败");
          }
        })
      }
    })
  },


  //清楚画布上的内容
  clear:function(){
    time_num = 0; //注意这个变量才是时间变化的关键
    startX = 0;
    startY = 0;
    curDrawArr = []; //清空绘画笔迹
    this.context.setFillStyle('#ffffff');
    this.context.fillRect(app.globalData.screen_width * (5 / 750), app.globalData.screen_heigh * (125 / 568), app.globalData.screen_width * 0.98, 341 / 568 * app.globalData.screen_height);
    this.context.draw();
  },

  //控制用户必须点击开始按钮才能进行测试
  tishiStart: function () {
    wx.showModal({
      title: '提示',
      content: '请先点击开始按钮再开始',
      showCancel: false, 
      confirmColor: '#000000',
      success(res) {
        if (res.confirm) {
          console.log("用户点击确认")
        }
      }
    })
  },

  //记录用户画的时钟的点数
  record_clock:function(){
    this.db.collection('User_clock').add({
      data: {
        hour: this.data.hour,
        minute: this.data.minute,
        open_id: this.data.filename.toString() + '_' + app.globalData.userLoginNumber.toString()
      },
      success: res => {
        // 在返回结果中会包含新创建的记录的 _id
        console.log('[数据库] [新增记录] 成功，记录 _id: ', res._id)
      },
      fail: err => {
        console.error('[数据库] [新增记录] 失败：', err)
      }
    })
  },

  //删除用户画的点数
  delete_clock: function(){
    if (this.data.counterId) {
      this.db.collection('User_clock').doc(this.data.counterId).remove({
        success: res => {
          wx.showToast({
            title: '删除成功',
          })
          this.setData({
            counterId: '',
            hour: null,
            minute: null,
            open_id: null
          })
        },
        fail: err => {
          wx.showToast({
            icon: 'none',
            title: '删除失败',
          })
          console.error('[数据库] [删除记录] 失败：', err)
        }
      })
    } else {
      wx.showToast({
        title: '无记录可删，请见创建一个记录',
      })
    }
  }
})

//用来定时获取记录数据
function record_XY() {
  t_num = time_num * 12;
  timer = setTimeout(function() {
    if ((startX != 0 || startY != 0) && begin){
      curDrawArr.push({ //每隔12ms记录一次
        x: startX,
        y: startY,
        t: t_num
      });
    }
    time_num = time_num + 1;
    record_XY();
  }, 12)
}

