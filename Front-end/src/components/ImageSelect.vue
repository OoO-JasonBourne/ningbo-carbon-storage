<template>
    <div class="tiff">
        <span class="menuTitle2">影像检索</span>
        <div class="dropdownBtns">
            <el-select v-model="cur.area" clearable @clear="clearItem(1)">
                <el-option v-for="item in area" :key="item.value" :label="item.label" :value="item.value">
                </el-option>
            </el-select>

            <el-select v-model="cur.sensor" clearable @clear="clearItem(2)">
                <el-option v-for="item in sensor" :key="item.value" :label="item.label" :value="item.value">
                </el-option>
            </el-select>

            <el-select v-model="cur.form" clearable @clear="clearItem(3)">
                <el-option v-for="item in form" :key="item.value" :label="item.label" :value="item.value">
                </el-option>
            </el-select>

            <el-button @click="clearAll" size="mini" style="background-color: rgba(0, 0, 0, 0);color: red;">
                <i class="el-icon-circle-close" style="font-size: 18px;"></i>
            </el-button>
        </div>

        <div class="imgItems">
            <div v-for="(name, index) in curImgs" class="item">
                {{ name }}
                <el-button @click="loading(index)" plain type="primary" size="mini"
                    style="position: absolute ;right: 5px;">加载</el-button>
            </div>
        </div>
    </div>
</template>

<script>
import { mapMutations } from 'vuex';

export default {
    data() {
        return {
            count: 0,
            cur: {
                area: '研究区',
                sensor: '传感器',
                form: '类型'
            },
            area: [
                { value: 'NingBo', label: '宁波' },
                { value: 'HZW', label: '杭州湾' },
                { value: 'MSW', label: '梅山湾' },
                { value: 'XQW', label: '蟹钳湾' }
            ],
            sensor: [
                { value: 'UAV', label: '无人机' },
                { value: 'S2', label: 'S2' },
            ],
            form: [
                { value: 'AGB', label: '植被地上生物量AGB' },
                { value: 'VC', label: '植被碳储量VC' },
                { value: 'TC', label: '总碳储量TC' },
            ],
            imgsName: [
                'S2_HZW_AGB_10m_2022',
                'S2_MSW_AGB_10m_2022',
                'S2_XQW_AGB_10m_2022',
                'S2_NingBo_AGB_10m_2022',
                'S2_NingBo_TC',
                'S2_NingBo_VC',
                'UAV_HZW_AGB_1m_2022',
                'UAV_MSW_AGB_1m_2022',
                'UAV_XQW_AGB_1m_2022',
            ]
        }
    },
    computed: {
        curImgs() {
            let area = this.cur.area == '研究区' ? '' : this.cur.area;
            let sensor = this.cur.sensor == '传感器' ? '' : this.cur.sensor;
            let form = this.cur.form == '类型' ? '' : this.cur.form;
            const filtedImgs = this.imgsName.filter(item => {
                return item.includes(area) && item.includes(sensor) && item.includes(form)
            })
            return filtedImgs
        }
    },
    methods: {
        ...mapMutations(['addLayers']),
        // 清空选项
        clearItem(id) {
            console.log(id)
            switch (id) {
                case 1:
                    this.cur.area = '研究区';
                case 2:
                    this.cur.sensor = '传感器';
                case 3:
                    this.cur.form = '类型';
            }
        },
        clearAll() {
            this.cur.area = '研究区';
            this.cur.sensor = '传感器';
            this.cur.form = '类型';
        },
        // 加载影像
        loading(index) {
            // 打开管理面板
            this.$EventBus.$emit('onManagePanel', [true, 1])
            // 判断要加载的图层是否已经存在
            const imageLayers = viewer.imageryLayers._layers;
            const ifExists = imageLayers.some(item => {
                return item.name == this.curImgs[index]
            })
            // 如果已存在直接返回,不存在则加载
            if (ifExists) {
                this.$message.warning('图层已存在')
                return
            }
            // 加载 WMS 服务(栅格影像图层)
            const provider = new Cesium.WebMapServiceImageryProvider({
                
                url: 'http://39.101.79.18:8080/geoserver/NingBo_Carbon/wms',
                layers: 'NingBo_Carbon:' + this.curImgs[index],
                parameters: {
                    transparent: true,
                    format: "image/png",
                    version: '1.1.1',
                    exceptions: 'application/vnd.ogc.se_inimage'
                }
            });
            const imageryLayer = viewer.imageryLayers.addImageryProvider(provider);
            // 为图层添加name属性
            imageryLayer.name = this.curImgs[index];
            // 将图层添加到vuex中
            this.addLayers(this.curImgs[index])
        }
    }
}
</script>

<style lang="less" scoped>
// 影像集
.tiff {
    position: relative;
    display: flex;
    flex: 1;
    flex-direction: column;
    min-height: 350px;
    /* 垂直方向布局 */
    // height: 100vh; /* 设置合适的高度，例如100vh代表整个视口高度 */

    .menuTitle2 {
        font-size: 18px;
        line-height: 40px;
    }

    .dropdownBtns {
        display: flex;
    }

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
}

::v-deep .el-select {
    .el-input {
        background-color: rgba(20, 19, 19, 0);

        .el-input__inner {
            background-color: rgba(241, 230, 230, 0);
            color: #000;
            padding: 10px;
            border-color: 'red';
        }

        .el-select__caret {
            color: #000;
        }
    }
}
</style>