// pages/descirbe/describe.js
const app = getApp();
const CDTapi = require("../../api/CDTapi.js")
Page({

    /**
     * 页面的初始数据
     */
    data: {
        list: []
    },

    onLoad() {
        CDTapi.getHistory().then(res => {
            res.detail_list.forEach(v=>{
                v.testTime = v.testTime.replace("T"," ")
                v.testTime = v.testTime.replace("Z", "")
            })
            this.setData({
                list: res.detail_list
            })
        }, () => {})
    },

    // 删除
    onDelete: function(e) {
        this.data.list.splice(e.detail.index, 1)
        this.setData({
            list: this.data.list
        })
    },

})