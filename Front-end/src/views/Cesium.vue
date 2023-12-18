<template>
    <div class="cesium">
        <div id="CesiumMap"></div>
        <ManagePanel />
        <Chart />
    </div>
</template>

<script>
import ManagePanel from '../components/ManagePanel.vue'
import Chart from '@/components/Chart.vue';
import { mapMutations } from 'vuex';

export default {
    name: 'CesiumMap',
    data() {
        return {
            NingBoPosi: {
                longitude: 121.56,
                latitude: 29.86
            },
            GeoData: {
                area: [
                    './Static/Study/HZW_ROI.json',
                    './Static/Study/MSG_ROI.json',
                    './Static/Study/XQG_ROI.json',
                ],
                simples: [
                    './Static/Simple/HHMC_Wild_Samples.json',
                    './Static/Simple/Luwei_Wild_Samples.json',
                    './Static/Simple/OtherVege_Wild_Samples.json',
                ]
            }
        }
    },
    components: {
        ManagePanel,
        Chart
    },
    mounted() {
        this.initMap()
        // console.log(viewer)
    },
    methods: {
        ...mapMutations(["changeStudyData"]),
        // 初始化 Cesium地图
        initMap() {
            Cesium.Ion.defaultAccessToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI0OTExOTY1NS00ZWNkLTRlYTEtYjNhZC0yMjYzYzhhYzg4NjEiLCJpZCI6MTA3MzgzLCJpYXQiOjE2NjI2MDcwNDh9.Gu0kC4cPTh8aSKOw5AKrrgFb3opi-5puKS6nC7_6Mag';
            const viewer = new Cesium.Viewer('CesiumMap', {
                animation: false,
                homeButton: false,
                infoBox: false,
                sceneModePicker: false,
                timeline: false,
                navigationHelpButton: false,
                fullscreenButton: false,
                selectionIndicator: false,
                geocoder: false
            });
            window.viewer = viewer;
            viewer._cesiumWidget._creditContainer.style.display = "none";
            // 飞行
            viewer.camera.flyTo({
                destination: Cesium.Cartesian3.fromDegrees(this.NingBoPosi.longitude, this.NingBoPosi.latitude, 200000),
                // duration: 1 // 飞行持续时间
            });
            // 捕获按钮组件
            this.findCesiumControl();
            // 初始化图层
            this.initLayers();
        },
        // 初始化地图控件
        findCesiumControl() {
            // 假设 Cesium 控件有一个类名为 "cesium-control"
            const cesiumBtnElement = document.querySelector('.cesium-viewer-toolbar');
            // 如果找到了 Cesium 控件的 DOM 元素
            if (cesiumBtnElement) {
                // 将找到的元素添加到 vuex 中
                this.$store.commit('cesiumBtnHandle', cesiumBtnElement)
            }
        },
        // 添加自定义图层
        initLayers() {
            // 三个研究区 shp 图层
            this.GeoData.area.forEach(item => {
                viewer.dataSources.add(
                    Cesium.GeoJsonDataSource.load(item, {
                        stroke: Cesium.Color.GOLDENROD,
                        fill: Cesium.Color.fromAlpha(Cesium.Color.GOLDENROD, 0.05),
                    })
                )
            })

            // 三种作物, 转换为 entities 添加到地图上
            this.GeoData.simples.forEach((item, index) => {
                // 根据 id 设置颜色
                let color;
                if (index === 0) {
                    color = Cesium.Color.DARKORANGE
                } else if (index === 1) {
                    color = Cesium.Color.DARKTURQUOISE
                } else if (index === 2) {
                    color = Cesium.Color.FLORALWHITE
                }
                // 加载图层
                Cesium.GeoJsonDataSource.load(item).then(data => {
                    data.type = 'point';
                    // 获取加载的数据
                    var entities = data.entities;
                    // 将数据添加到场景中
                    viewer.dataSources.add(data);
                    entities.values.forEach(function (entity) {
                        // 去掉默认的图标
                        entity.billboard = undefined;
                        entity.type = 'point';
                        // 在这里对每个 entity 进行定制
                        entity.point = new Cesium.PointGraphics({
                            color: color,
                            pixelSize: 10
                        });
                    });
                })

            })
        }
    }
}
</script>

<style lang="less" scoped>
.cesium {
    position: absolute;
    top: 50px;
    left: 300px;
    width: calc(100% - 300px);
    height: calc(100% - 50px);
    z-index: 1;

    #CesiumMap {
        width: 100%;
        height: 100%;
    }
}
</style>