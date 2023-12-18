import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    // Cesium 控件
    cesiumControl: {
      cesiumBtns: null
    },
    study: {
      curStudyID: 0, // 当前选中研究区
      curStudyData: null,
    },
    wmsLayers: [],

  },
  getters: {
  },
  mutations: {
    cesiumBtnHandle(state, data) {
      state.cesiumControl.cesiumBtns = data;
    },
    // 切换研究区
    changeStudyID(state, val) {
      state.study.curStudyID = val;
    },
    changeStudyData(state, val) {
      state.study.curStudyData = val;
    },
    addLayers(state, layer){
      // 添加图层
      state.wmsLayers.push(layer);
    },
  },
  actions: {
  },
  modules: {
  }
})
