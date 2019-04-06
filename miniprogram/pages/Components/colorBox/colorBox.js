// Components/colorBox.js
Component({
  /**
   * 组件的属性列表
   */
  options: {
    multipleSlots: true
  },

  properties: {
    selected: {
      type: Boolean,
      value: false
    },
    color:{
      type: String,
      value: "red"
    }
  },

  /**
   * 组件的初始数据
   */
  data: {

  },

  /**为什么dataset.color没有这东西 */
  attached(){
    this.setData({
      color: this.dataset.color
    })
  },
  /**
   * 组件的方法列表
   */
  methods: {
    /**在内部私有方法中建议以下划线开头
     * triggerEvent用于触发事件
     */

    //选中笔刷
    _select(e){
      this.triggerEvent("select");
    }
  }
})
