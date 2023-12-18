import Vue from 'vue'
import App from './App.vue'
import store from './store'
import VueDraggableResizable from 'vue-draggable-resizable'

import './plugins/element.js'
// 注册引入EventBus
const EventBus = new Vue;
Vue.prototype.$EventBus = EventBus;

Vue.component('vue-draggable-resizable', VueDraggableResizable)

Vue.config.productionTip = false;

new Vue({
  store,
  render: h => h(App)
}).$mount('#app')
