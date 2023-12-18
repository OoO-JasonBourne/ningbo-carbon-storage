<template>
    <div class="home">
        <Menu v-if="pageId == 1"></Menu>
        <Model v-else-if="pageId == 2"></Model>
        <Title v-on:onChangePage='changeId'></Title>
        <CesiumMap />
        <Table />
    </div>
</template>

<script>
import CesiumMap from './Cesium.vue'
import Title from '../components/Title.vue'
import Menu from '../components/Menu.vue'
import Model from '../components/Model.vue'

// 使用 import 语法引入需要懒加载的组件
const Table = () => import('../components/Table.vue');

export default {
    data() {
        return {
            pageId: 1,  // id为1表示数据分布页面， 为2 表示 模型计算页面
        }
    },
    mounted() {
    },
    components: {
        CesiumMap,
        Title,
        Menu,
        Model,
        Table
    },
    methods: {
        changeId(id) {
            this.pageId = id;
        }
    }

}
</script>

<style lang="less" scoped>
.home {
    width: 100%;
    height: 100%
}
</style>