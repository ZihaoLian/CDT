// pages/test/test.js
var app = getApp();
app.globalData.isLogin = true;
var startX = 0;
var startY = 0;
var begin = false; //设置是否开始绘画
var curDrawArr = []; //用来存储每个笔画的轨迹
var timer; //计时器
var time_num = 0;
var t_num = 0;
var is_next_step = false;
var is_empty = false;

wx.cloud.init()

Page({
  /**
   * 页面的初始数据
   */
  data: {
    CustomBar: app.globalData.CustomBar / 568 * app.globalData.sclar * 750,
    StatusBar: app.globalData.StatusBar / 568 * app.globalData.sclar * 750,
    canvasHeight: 341 / 568 * app.globalData.sclar * 750,
    filepath: wx.env.USER_DATA_PATH + '/',
    hour: 0,
    minute: 0,
    step_tip: '请复现你刚才画的时钟',
    filename: '',
    is_begin_draw: false,
    is_finish: false,
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
    
  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {
    this.context = wx.createCanvasContext('firstcanvas'); //获取画布
    this.fs = wx.getFileSystemManager(); //获取文件管理系统
    if (app.globalData.userLoginNumber > 1) {
      this.clear(); //注意这个变量才是时间变化的关键
    }
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

  // 开始绘制线条
  lineBegin: function (x, y) {
    if(this.data.is_begin_draw){
      begin = true;
      this.context.beginPath();
      startX = x;
      startY = y;
      //this.context.moveTo(startX, startY)
      this.lineAddPoint(x, y);
      is_next_step = true
    }
  },

  // 绘制线条中间添加点
  lineAddPoint: function (x, y) {
    this.context.moveTo(startX, startY)
    this.context.lineTo(x, y);
    this.context.stroke();
    startX = x;
    startY = y;
  },

  // 绘制线条结束
  lineEnd: function () {
    this.context.closePath();
    begin = false;
  },

  // 绘制开始 手指开始按到屏幕上
  touchStart: function (e) {
    if(!this.data.is_begin_draw){
      this.tishiStart();
    }
    else{
      this.lineBegin(e.touches[0].x, e.touches[0].y)
    }
    
  },

  // 绘制中 手指在屏幕上移动
  touchMove: function (e) {
    if (begin) {
      this.lineAddPoint(e.touches[0].x, e.touches[0].y);
      this.context.draw(true);
    }
  },

  // 绘制结束 手指抬起
  touchEnd: function () {
    curDrawArr.push({ //用来标记笔画的结束
      x: -1,
      y: -1,
      t: -1
    })
    this.lineEnd();
  },

  //开始画钟
  start_draw: function () {
    this.context.setFillStyle('#ffffff');
    this.context.fillRect(app.globalData.screen_width * (7 / 750), app.globalData.screen_heigh * (125 / 568), app.globalData.screen_width * 0.98, 341 / 568 * app.globalData.screen_height);
    this.context.draw();
    this.getOpen(); //获取命名需要
    this.setData({
      filepath: this.data.filepath + this.data.filename.toString() + '_' + app.globalData.userLoginNumber.toString() + '_2.doc',
      is_begin_draw: true, 
    })
    record_XY(); //开始记录数据
  },

  //结束画钟
  finish_step: function () {
    if(is_next_step && !is_empty){
      wx.showToast({
        title: '请稍等片刻上传数据',
      })
      this.store();
      clearTimeout(timer); //关掉定时器
      ++app.globalData.userLoginNumber; //用来递增用户第几次进行测试
      wx.showModal({
        title: '提示',
        content: '你已经完成画测试了，是否再测试一次',
        cancelColor: "#000000",
        confirmColor: "#000000",
        success(res){
          if(res.confirm){
            wx.navigateBack({
              
            })
          }
          else if(res.cancel){
            wx.switchTab({
              url: '../home/home',
            })
          }
        }
      })
      this.setData({
        is_finish: true
      })
    }
    else{
      this.void_withoutDraw();
    }
  },

  //获取用户的openid来自动命名文件
  getOpen: function(){
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
    this.fs.writeFileSync(this.data.filepath.toString() + this.data.filename.toString() + '_' + app.globalData.userLoginNumber.toString() +'_2.doc', '-1 -1 -1\n', 'utf8');
    for (var j in curDrawArr) {
      this.fs.appendFileSync(this.data.filepath.toString() + this.data.filename.toString() + '_' + app.globalData.userLoginNumber.toString() + '_2.doc', curDrawArr[j].x.toString() + ' ' + curDrawArr[j].y.toString() + ' ' + curDrawArr[j].t.toString() + '\n', 'utf8')
    }
    //判断是否上传数据
    if (!is_empty) {
      this.save_draw_data(this.data.filename.toString())
      this.save_first_draw(this.data.filename.toString())
    }
  }, 

  save_draw_data: function(filename){
    wx.cloud.uploadFile({
      cloudPath: 'CDTData/' + filename + '_' + app.globalData.userLoginNumber +'_2.doc',
      filePath: this.data.filepath.toString() + filename + '_' + app.globalData.userLoginNumber +'_2.doc',
      success: res => {
        console.log("数据上传成功")
      }
    })
  },

  //保存最后绘制的图片
  save_first_draw: function (file_name) {
    var number = app.globalData.userLoginNumber; //这里记得要记录下app.globalData.userLoginNumber, 否则后面进行回调时app.globalData.userLoginNumber就会出错
    wx.canvasToTempFilePath({
      x: app.globalData.screen_width * (7/750),
      y: app.globalData.screen_heigh * (125 / 568),
      width: app.globalData.screen_width * 0.98,
      height: 341 / 568 * app.globalData.screen_height,
      destWidth: 256,
      destHeight: 256,
      canvasId: 'firstcanvas',
      success(res) {
        //将截取的图片上传到云存储上
        wx.cloud.uploadFile({
          cloudPath: 'CDTImage/' + file_name + '_' + number.toString() +'_2.png' ,
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

  //再次测试
  // back(){
  //   if(is_next_step && this.data.is_finish){
  //     this.clear(); //刷新页面，进行下一次测试
  //     wx.navigateBack({

  //     })
  //   }
  //   else if(is_next_step && !this.data.is_finish){
  //     wx.showModal({
  //       title: '提示',
  //       content: '请先点击结束按钮再进行下一次测试',
  //       showCancel: false,
  //       confirmColor: "#000000"
  //     })
  //   }
  //   else{
  //     this.void_withoutDraw();
  //   }
  // },

  void_withoutDraw: function () {
    wx.showModal({
      title: '提示',
      content: '你还没开始画钟呢，请画完再继续下一步',
      showCancel: false,
      confirmColor: '#000000'
    })
  },

  cancel_step: function () {
    if(is_next_step){
      wx.showModal({
        title: '确定要取消吗?',
        content: '取消后将重新进行测试!!!',
        showCancel: false,
        confirmColor: '#000000',
        success(res) {
          if (res.confirm) {
          } else if (res.cancel) {
          }
        }
      })
      is_empty = true
      this.clear(); // 清空数组内容
      clearTimeout(timer);
      //删除第一次上传的文件 
      this.deletecloudeFile('wx.env.USER_DATA_PATH' + '/CDTData/' + this.data.filename.toString() + '_' + app.globalData.userLoginNumber.toString() + '_1.doc');
      this.deletecloudeFile('wx.env.USER_DATA_PATH' + '/CDTImage/' + this.data.filename.toString() + '_' + app.globalData.userLoginNumber.toString() + '_1.png');

      //判断用户在画完后取消
    //   var o2 ={
    //     path: 'wx.env.USER_DATA_PATH' + '/CDTData/' + this.data.filename.toString() + '_' + app.globalData.userLoginNumber.toString() + '_2.doc'
    //   }
    //   this.fs.access(o2)
    }
    else{
      this.void_withoutDraw();
    }
  },

  //删除云存储上的文件
  deletecloudeFile:function(filename){
    wx.cloud.deleteFile({
      fileList: [filename],
      success: res => {
        // handle success
        console.log(res.fileList)
      },
      fail: err => {
        // handle error
      }
    })
  },

  //清楚画布上的内容
  clear: function () {
    time_num = 0; //注意这个变量才是时间变化的关键
    startX = 0;
    startY = 0;
    curDrawArr = []; //清空绘画笔迹
    this.context.setFillStyle('#ffffff');
    this.context.fillRect(app.globalData.screen_width * (6 / 750), app.globalData.screen_heigh * (125 / 568), app.globalData.screen_width * 0.98, 341 / 568 * app.globalData.screen_height);
    this.context.draw();
  },

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
})

//用来定时获取记录数据
function record_XY() {
  t_num = time_num * 12;
  timer = setTimeout(function () {
    if((startX != 0 ||  startY !=0)&&begin){
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

