const app = getApp()

Component({
    /**
     * 组件的属性列表
     */
    properties: {
        title: String
    },

    data: {
        CustomBar: app.globalData.CustomBar,
        StatusBar: app.globalData.StatusBar,
    },

})