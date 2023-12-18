<template>
    <vue-draggable-resizable ref="draggable" class="managePanel" :w="300" :h="500" :x="x" :y="y" :z="20" :parent="true"
        v-show=show>
        <div class="manageBtns">
            <el-button ref="btn1" @click="handle(1)" :class="{ 'btn': true, 'active': activeId === 1 }"
                size="mini">图层管理器</el-button>
            <el-button ref="btn2" @click="handle(2)" :class="{ 'btn': true, 'active': activeId === 2 }"
                size="mini">任务管理器</el-button>
            <i class="el-icon-s-unfold" @click="show = false" style="margin-left: auto ;align-self: center;"></i>
        </div>

        <div v-if="activeId == 1" class="layerPanel">
            <div v-for="layer in wmsLayers" class="layer">
                <hr>
                <div class="row row1">
                    <el-checkbox v-model="checkedLayers[layer]" checked @change="changeSelect(layer, checkedLayers[layer])">
                        {{ layer }}
                    </el-checkbox>
                    <div class="icons">
                        <i class="el-icon-s-help" @click="pixelCalc(layer)" v-if="layer.slice(0, 4) !== 'LC08'"></i>
                        &thinsp;
                        <i class="el-icon-s-unfold" @click="removeLayer(layer)"></i>
                    </div>


                </div>
                <div class="row row2" v-if="layer.slice(0, 4) !== 'LC08'">
                    <span style="display: block;">{{ getLeftValue(layer) }}</span>
                    <img src="Img/style.png">
                    <span style="display: block;">{{ getRightValue(layer) }}</span>
                </div>
            </div>
        </div>
        <div v-else-if="activeId == 2" class="taskPanel">
            <el-table :data="modelData" style="width: 100%" stripe size="mini">
                <el-table-column prop="id" label="ID" width="40">
                </el-table-column>
                <el-table-column prop="name" label="NAME" min-width>
                </el-table-column>
                <el-table-column label="状态" width="80">
                    <template slot-scope="{ row }">
                        <el-tag :type="row.status === 1 ? '' : 'success'">
                            {{ row.status === 1 ? '已完成' : '正在执行' }}
                        </el-tag>
                    </template>
                </el-table-column>
                <el-table-column prop="timer" label="时间" min-width>
                </el-table-column>

                <el-table-column fixed="right" label="操作" width="50px">
                    <template slot-scope="{ row }">
                        <!-- <el-button @click="handleLoad(row.tiles_url, row.name)" type="text" size="medium"><i
                                class="el-icon-view"></i></el-button> -->
                        <el-button @click="handleDownload(row.name, row.res_url)" type="text" size="medium"><i
                                class="el-icon-download"></i></el-button>
                    </template>
                </el-table-column>
            </el-table>
        </div>
    </vue-draggable-resizable>
</template>

<script>
import api from '../api/index'
import { mapState, mapMutations } from 'vuex';

export default {
    data() {
        return {
            modelData: [],
            checkedLayers: {},  // 保存每个图层的选中状态
            show: false,
            activeId: 1,
            x: 0,
            y: 100,
            lengedValues: {
                'S2_HZW_AGB_10m_2022': { left: -66, right: 5003 },
                'S2_MSW_AGB_10m_2022': { left: -98, right: 4765 },
                'S2_NingBo_AGB_10m_2022': { left: -101, right: 4770 },
                'S2_NingBo_TC': { left: 9268, right: 21031 },
                'S2_NingBo_VC': { left: 0, right: 2921 },
                'S2_XQW_AGB_10m_2022': { left: -494, right: 4899 },
                'UAV_HZW_AGB_1m_2022': { left: 0, right: 6514 },
                'UAV_MSW_AGB_1m_2022': { left: 0, right: 6261 },
                'UAV_XQW_AGB_1m_2022': { left: 574, right: 6219 }
            }
        }
    },
    computed: { 
        ...mapState(['wmsLayers']),
    },
    watch: {
        // 监听 管理面板 的状态
        show(newVal, oldVal) {
            this.$EventBus.$emit('onTableAndManage', [3, newVal])
        }
    },
    mounted() {
        // 显示管理面板
        this.$EventBus.$on('onManagePanel', val => {
            this.show = val[0];
            this.activeId = val[1]
        });

        this.$nextTick(() => {
            // 自定义 管理面板右侧位置
            this.x = this.$el.parentElement.clientWidth - 270;
        });
        // 加载模型任务列表
        this.loadingTask();
        // 接受Model数据
        this.$EventBus.$on('onModelData', data => {
            const dataArray = eval(data)
            this.modelData = dataArray;
        })


    },
    methods: {
        ...mapMutations(["addLayers"]),
        handle(id) {
            this.activeId = id;
        },
        // 改变勾选框状态触发事件，显隐图层
        changeSelect(layerName, layerStatus) {
            const imageLayers = viewer.imageryLayers._layers;
            const selectLayer = imageLayers.filter(item => {
                return item.name == layerName;
            });
            selectLayer[0].show = layerStatus;
        },
        // 加载任务列表
        loadingTask() {
            api.loadingTaskList().then((res) => {
                if (res.status === 200) {
                    this.modelData = res.data
                } else {
                    console.log('请求模型任务列表失败')
                }
            }).catch((error) => {
                console.log(error)
            })
        },
        // 移除图层
        removeLayer(layerName) {
            // 移除图层
            const imageLayers = viewer.imageryLayers._layers;
            const selectLayer = imageLayers.filter(item => {
                return item.name == layerName;
            });
            viewer.imageryLayers.remove(selectLayer[0])
            // 从 vuex 中移除
            let index = this.wmsLayers.indexOf(layerName);
            if (index !== -1) {
                this.wmsLayers.splice(index, 1)
            }
        },
        // 设置图例值
        getLeftValue(layer) {
            return this.lengedValues[layer] ? this.lengedValues[layer].left : '';
        },
        getRightValue(layer) {
            return this.lengedValues[layer] ? this.lengedValues[layer].right : '';
        },
        // 判断是否不为L8数据
        isLayerValid(layer) {
            return layer.slice(0, 3) !== 'LC08';
        },
        // // 点击加载影像
        handleLoad(url, name) {
            console.log(name)
            name = 'Res_' + name;
            const imageLayers = viewer.imageryLayers._layers;
            const ifExists = imageLayers.some(item => {
                return item.name == name
            })
            // 如果已存在直接返回,不存在则加载
            if (ifExists) {
                this.$message.warning('图层已存在')
                return
            }
            const ImageUrl = 'http://localhost/carbon/' + url;
            
            console.log(ImageUrl)
            // 加载影像
            const imageryLayer = new Cesium.TileMapServiceImageryProvider({
                url: ImageUrl,
                // name: name
            });
            viewer.imageryLayers.addImageryProvider(imageryLayer);
            // 将图层添加到vuex中
            this.addLayers(name)
        },
        // 下载
        handleDownload(name, url) {
            // 影像文件 URL
            const imageUrl = 'http://localhost/carbon/' + url;

            // 创建一个虚拟的<a>标签，并设置其属性
            const link = document.createElement('a');
            link.href = imageUrl;
            link.download = name + 'tif'; // 设置下载文件的名称

            // 模拟点击<a>标签，触发下载
            document.body.appendChild(link);
            link.click();

            // 清理
            document.body.removeChild(link);
        },
        // 请求服务，计算图层 像素点
        pixelCalc(layer){
            // 激活 Chart 页面
            this.$EventBus.$emit('onChartPanel', [layer, ''])
            // 向后端请求数据
            api.calcPixel({
                name: layer
            }).then((res) => {
                if(res.status === 200){
                    this.$EventBus.$emit('onChartPanel', [layer, res.data])
                } else {
                    console.log('Pixel计算失败')
                }
            }).catch((error) => {
                console.log(error)
            })
        }
    }
}

</script>

<style lang="less" scoped>
::v-deep .el-checkbox__label {
    font-size: 16px;
}

::v-deep.el-table tr {
    font-size: 12px;
}

.managePanel {
    position: absolute;
    top: 0;
    background-color: rgb(209, 216, 221);
    border-radius: 10px;
    max-height: 70%;


    .manageBtns {
        margin: 15px;
        display: flex;
        justify-content: space-around;
        align-items: center;

        .btn {
            margin: 0;
        }

        .btn1.active {
            color: #FFF;
            /* 设置选中状态下的字体颜色 */
            background-color: #008b8b;
            /* 设置选中状态下的背景色 */
        }

        .btn.active {
            color: #FFF;
            background-color: #008b8b;
        }
    }

    .layerPanel {
        position: relative;
        overflow-y: auto;
        height: calc(100% - 60px);

        .layer {
            width: 100%;
            height: 50px;
            // border: 1px solid #008b8b;
            margin-bottom: 10px;

            .row {
                position: relative;
                display: flex;
                align-items: center;
                font-size: 14px;
                color: #008b8b;
                margin-left: 10px;

                .icons {
                    position: absolute;
                    right: 10px;
                    font-size: 18px;
                }

                .icons:hover {
                    cursor: pointer;
                }

                img {
                    position: absolute;
                    width: 50%;
                    left: 0;
                    transform: translate(50%, 0);

                }
            }

            .row1 {
                height: 50%;
            }

            .row2 {
                justify-content: space-between;

                width: 60%;
                height: 30%;
                background-color: #fff;
                margin: 0 auto;
            }

        }

    }

    .taskPanel {
        position: relative;
        overflow-y: auto;
        height: calc(100% - 60px);
    }
}
</style>
