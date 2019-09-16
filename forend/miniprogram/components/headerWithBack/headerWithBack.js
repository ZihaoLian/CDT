const app = getApp()
// components/headerWithBack/headerWithBack.js
Component({
    /**
     * 组件的属性列表
     */
    properties: {
        title: String
    },

    /**
     * 组件的初始数据
     */
    data: {
        CustomBar: app.globalData.CustomBar,
        StatusBar: app.globalData.StatusBar,
    },

})
