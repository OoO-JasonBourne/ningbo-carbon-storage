<template>
  <div id="app">
    <Home />
  </div>
</template>

<script>
import Home from './views/Home.vue'

export default {
  name: 'App',
  components: {
    Home
  },
}
</script>

<style lang="less">
html,
body,
#app {
  width: 100%;
  height: 100%;
  // box-sizing: border-box;
  padding: 0px;
  margin: 0px;
  font-family: "SimHei", sans-serif;
      /* 阻止光标闪烁 */
  caret-color: transparent;
    /* 阻止文本选择 */
  user-select: none;

}

* {
  padding: 0px;
  margin: 0px;
}
</style>
