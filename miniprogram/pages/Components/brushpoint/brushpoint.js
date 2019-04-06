// Components/brushpoint/brushpoint.js
Component({
  options: {
    multipleSlots: true // 在组件定义时的选项中启用多slot支持
  },
  /**
   * 组件的属性列表
   */
  properties: {
    color: {
      type: String,
      value: "red"
    },

    radius: {
      type: Number,
      value: 20
    },

    width: {
      type: String,
      value: "60rpx"
    },

    height: {
      type: String,
      value: "60rpx"
    },
  
    selected: {
      type: Boolean,
      value: false
    },
  },

  /**
   * 组件的初始数据
   */
  data: {
    hiddenEffect: true,
  },

  attached(){
    this.setData({
      innerRadius: this.properties.radius * 1.7 + 10,
      outterRadius: this.properties.radius * 1.7 + 20,
    });
  },
  /**
   * 组件的方法列表
   */
  methods: {

    //选中笔刷
    _select(e){
      this.setData({
        hiddenEffect: false
      });

      /**这是什么用法 */
      setTimeout(() => {
        this.setData({
            hiddenEffect: true
        });
      }, 500);
      this.triggerEvent("select");
    }
  }
})
