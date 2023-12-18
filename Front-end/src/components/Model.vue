<template>
    <div class="model">
        <div class="modelTitle">
            <i class="el-icon-s-unfold"></i><span>碳储量估算</span>
        </div>
        <hr />
        <div style="margin: 10px 0;" class="dataSelect">
            <div class="modelTitle2">数据选取</div>
            <div style="margin: 10px 0;"></div>

            <div class="imgItems">
                <div v-for="(item, index) in imgData" class="item">
                    {{ item.name }}
                    <el-button @click="loading(item.name)" plain type="primary" size="mini"
                        style="position: absolute ;right: 5px;">加载</el-button>
                    <el-button @click="selected(item.name)" plain type="primary" size="mini"
                        style="position: absolute ;right: 60px;">选取</el-button>
                </div>
            </div>
            <div style="margin: 20px 0;"></div>
            <div class="imgSelected">
                {{ curImg }}
            </div>
            <div class="btns" style="display: flex; justify-content: space-around; margin-right: 20px;">
                <el-button type="success" @click="start">计算</el-button>
                <el-button type="warning" @click="reseting">重置</el-button>
            </div>

        </div>
    </div>
</template>

<script>
import api from '../api/index'

import { mapMutations } from 'vuex'

export default {
    data() {
        return {
            imgData: [],
            curImg: '', //当前选取的影像
        }
    },
    mounted() {
        this.loadData()
    },
    methods: {
        ...mapMutations(["addLayers"]),
        // 加载影像数据
        loadData() {
            api.loadingImg().then((res) => {
                if (res.status === 200) {
                    this.imgData = res.data;
                } else {
                    console.log('数据加载失败')
                }
            }).catch((error) => {
                console.log(error)
            })
        },
        // 加载影像
        loading(name) {
            // 打开管理面板
            this.$EventBus.$emit('onManagePanel', [true, 1])
            // 判断要加载的图层是否已经存在
            const imageLayers = viewer.imageryLayers._layers;
            const ifExists = imageLayers.some(item => {
                return item.name == name
            })
            // 如果已存在直接返回,不存在则加载
            if (ifExists) {
                this.$message.warning('图层已存在')
                return
            }
            // 加载 WMS 服务(栅格影像图层)
            const provider = new Cesium.WebMapServiceImageryProvider({
                url: 'http://localhost:8080/geoserver/NingBo_Carbon/wms',
                layers: 'NingBo_Carbon:' + name,
                parameters: {
                    transparent: true,
                    format: "image/png",
                    version: '1.1.1',
                    exceptions: 'application/vnd.ogc.se_inimage'
                }
            });
            const imageryLayer = viewer.imageryLayers.addImageryProvider(provider);
            // 为图层添加name属性
            imageryLayer.name = name;
            // 将图层添加到vuex中
            this.addLayers(name)
        },
        // 选取
        selected(name) {
            this.curImg = name;
        },
        // 开始计算
        start() {
            if (this.curImg === '') {
                this.$message.error('请选择数据');
                return
            };
            this.$message.success('开始执行')
            // 打开管理面板
            this.$EventBus.$emit('onManagePanel', [true, 2])
            // 将任务插入数据表， 并返回任务 ID
            api.saveModelTask({
                name: 'Res_' + this.curImg
            }).then((res) => {
                if (res.status === 200) {
                    // 任务列表
                    this.$EventBus.$emit('onModelData', res.data[1])
                    // 发起后续计算NDVI请求
                    return api.calcNDVI({
                        id: res.data[0],
                        name: this.curImg
                    })
                } else {
                    console.log('插入数据失败');
                    // 如果插入数据失败，直接抛出错误，跳到 catch 处理
                    throw new Error('插入数据失败');
                }
            }).then((res) => {
                if (res.status === 200) {
                    this.$message.success('计算完成')
                    // 任务列表
                    this.$EventBus.$emit('onModelData', res.data)
                } else {
                    console.log('模型请求失败');
                    // 如果计算失败，直接抛出错误，跳到 catch 处理
                    throw new Error('模型请求失败');
                }
            })
                .catch((error) => {
                    console.log(error)
                })
        },
        reseting() {
            this.curImg = ''
        }
    }
}
</script>

<style>
.modelTitle2 {
    font-size: 18px;
    line-height: 40px;
}

.model {
    position: fixed;
    display: flex;
    flex-direction: column;
    top: 50px;
    width: 300px;
    height: 100vh;
    overflow-y: auto;
    background-color: rgb(209, 209, 216);
    z-index: 10;
    padding-left: 10px;

    .modelTitle {
        position: sticky;
        top: 0px;
        /* 固定在容器的顶部 */
        width: 100%;
        height: 40px;
        line-height: 40px;
        font-size: 20px;
        font-weight: 500;
        z-index: 20;
        background-color: rgb(209, 209, 216);
    }

    .dataSelect {
        .imgItems {
            overflow-y: auto;
            width: 100%;

            .item {
                position: relative;
                display: flex;
                align-items: center;
                height: 40px;
                border: 2px solid rgb(243, 243, 243);
                padding: 0 5px;
                margin: 5px 5px 5px 0;
                color: rgb(7, 74, 100);
            }
        }

        .imgSelected {
            padding: 0 5px;
            margin: 5px 5px 5px 0;
            height: 40px;
            background-color: #008b8b;
            line-height: 40px;
            text-align: center;
            color: #FFF;
        }
    }
}
</style>