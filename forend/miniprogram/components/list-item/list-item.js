
// components/list-item/list-item.js
Component({
    /**
     * 组件的属性列表
     */
    properties: {
        historyList: { // 距离顶部多少时 触发 upper
            type: Array,
            value: []
        },

    },

    data: {
        startX: 0, //开始坐标
        startY: 0,
        isTouchMove: [],
    },

    /**
     * 组件的方法列表
     */
    methods: {
        //手指触摸动作开始 记录起点X坐标
        touchstart: function (e) {
            let list = this.properties.historyList
            //开始触摸时 重置所有删除
            for (var i in list) {
                if (this.data.isTouchMove[i]) //只操作为true的
                    this.data.isTouchMove[i] = false
            }

            this.setData({
                isTouchMove: this.data.isTouchMove,
                startX: e.changedTouches[0].clientX,
                startY: e.changedTouches[0].clientY,
            })

        },

        //滑动事件处理
        touchmove: function (e) {
            let startX = this.data.startX //开始X坐标
            let startY = this.data.startY //开始Y坐标
            let touchMoveX = e.changedTouches[0].clientX //滑动变化坐标
            let touchMoveY = e.changedTouches[0].clientY //滑动变化坐标
            let index = e.currentTarget.dataset.index

            //获取滑动角度
            let angle = this.angle({
                X: startX,
                Y: startY
            }, {
                    X: touchMoveX,
                    Y: touchMoveY
                });

            //滑动超过30度角 return
            if (Math.abs(angle) > 30) return;
            if (touchMoveX > startX) //右滑
            {
                this.data.isTouchMove[index] = false
                this.setData({
                    isTouchMove: this.data.isTouchMove
                })
            } else //左滑
            {
                this.data.isTouchMove[index] = true
                this.setData({
                    isTouchMove: this.data.isTouchMove
                })
            }
        },

        /**
         * 计算滑动角度
         * @param {Object} start 起点坐标
         * @param {Object} end 终点坐标
         */
        angle: function (start, end) {
            var _X = end.X - start.X,
                _Y = end.Y - start.Y

            //返回角度 /Math.atan()返回数字的反正切值
            return 360 * Math.atan(_Y / _X) / (2 * Math.PI);

        },

        //删除事件
        del: function (e) {
            let index = e.currentTarget.dataset.index
            this.triggerEvent('delete', {
                list: this.properties.historyList,
                index
            })
        },

        showDetail(e){
            wx.navigateTo({
                url: '/pages/testDetail/testDetail',
            })
        }
    },

})