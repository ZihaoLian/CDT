// pages/descirbe/describe.js
const app = getApp();
Page({

    /**
     * 页面的初始数据
     */
    data: {
        list: [
            {
                testTime: '2019.09.09 12:00:00',
                url:"/image/1.png"
            },
            {
                testTime: '2019.09.09 12:00:00',
                url: "/image/2.png"
            }
        ]
    },

    // 删除
    onDelete: function(e) {
        this.data.list.splice(e.detail.index,1)
        this.setData({
            list:this.data.list
        })
    },
  
})