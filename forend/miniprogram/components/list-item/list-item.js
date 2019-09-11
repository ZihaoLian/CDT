// components/list-item/list-item.js
Component({
    /**
     * 组件的属性列表
     */
    options: {
        multipleSlots: true // 在组件定义时的选项中启用多slot支持
    },

    properties: {
        list: { // 距离顶部多少时 触发 upper
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
            let list = this.properties.messList
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
            this.data.list.splice(index, 1) //splice(index, number, addItem)返回删除的数组
            console.log(this.data.list)
            // 所有要带到主页面的数据，都装在eventDetail里面
            var eventDetail = {
                list: this.data.list
            }
            // 触发事件的选项 bubbles是否冒泡，composed是否可穿越组件边界，capturePhase 是否有捕获阶段
            var eventOption = {
                composed: true
            }
            this.triggerEvent('componentCall', eventDetail, eventOption)
        },

        showModal(e) {
            let index = e.currentTarget.dataset.index
            let detail = e.currentTarget.dataset.detail
            let sendId = e.currentTarget.dataset.sendId
            let which = e.currentTarget.dataset.which
            let name = e.currentTarget.dataset.name
            this.triggerEvent('tap', {
                index: index,
                detail: detail,
                sender: sendId,
                which: which,
                name: name
            })
        }


    },

})
