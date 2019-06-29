// 云函数入口文件
const cloud = require('wx-server-sdk')

cloud.init()
const db = cloud.database()
const _ = db.command

// 云函数入口函数
exports.main = async (event, context) => {
  // const wxContext = cloud.getWXContext()

  // return {
  //   event,
  //   openid: wxContext.OPENID,
  //   appid: wxContext.APPID,
  //   unionid: wxContext.UNIONID,
  // }
  try {
    return await db.collection('User_Login').doc('login_number').update({
      // data 传入需要局部更新的数据
      data: {
        login_number: 34
      }
    })
  } catch (e) {
    console.error(e)
  }
}