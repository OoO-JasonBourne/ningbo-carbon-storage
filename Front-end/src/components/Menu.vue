<template>
    <div class="menu">
        <div class="menuTitle">
            <i class="el-icon-s-unfold"></i><span>碳储量分布详情</span>
        </div>
        <hr />
        <div style="margin: 10px 0;" class="studyArea">
            <div class="menuTitle2">研究区</div>
            <div style="margin: 10px 0;"></div>
            <el-checkbox v-model="checked" size="medium" border @change="handleCheck">
                {{ area }}</el-checkbox>
            <el-button
                style="position: absolute;right: 0; margin-right: 20px; color: #0b7df0;background-color: rgb(203, 203, 209);"
                @click="locate" size="medium"><i class="el-icon-position"></i></el-button>
        </div>

        <!-- 一条虚线 -->
        <div style="border-top: 1px dashed #a0522d;width: 100%;height: 0; margin: 5px -5px;"></div>

        <div class="simple">
            <span class="menuTitle2">实地样本集</span>
            <div style="margin: 10px 0;"></div>
            <el-checkbox :indeterminate="isIndeterminate" border size="medium" v-model="checkAll"
                @change="handleCheckAllChange">
                全选</el-checkbox>
            <div style="margin: 15px 0;"></div>
            <el-checkbox-group v-model="checkedVeges" @change="handleCheckedVegesChange" class="vertical-checkbox-group">
                <el-checkbox border size="small" v-for="vege in veges" :label="vege" :key="vege" class="vertical-checkbox">
                    <span class="checkbox-label">{{ vege }}</span>
                </el-checkbox>
            </el-checkbox-group>
            <div class="legend">
                <div class="legend-circle" style="color: #ff8c00;">●</div>
                <div class="legend-circle" style="color: #48decc;">●</div>
                <div class="legend-circle" style="color: #FFF;">●</div>
            </div>
        </div>

        <!-- 一条虚线 -->
        <div style="border-top: 1px dashed #a0522d;width: 100%;height: 0; margin: 5px -5px;"></div>
        <!-- 影像检索 -->
        <ImageSelect />
    </div>
</template>

<script>
import ImageSelect from './ImageSelect.vue';
import { mapState } from 'vuex';


export default {
    data() {
        return {
            area: '研究区矢量',
            checked: true,
            checkAll: true,
            checkedVeges: ['互花米草', '芦苇', '其他盐沼植被'],
            veges: ['互花米草', '芦苇', '其他盐沼植被'],
            isIndeterminate: true,
        }
    },
    components: {
        ImageSelect,
    },
    computed: {
        ...mapState(["study"]),
    },
    mounted() {
        this.$EventBus.$on('onStudyTextSwitch', text => {
            this.area = text;
        })
    },
    watch: {
    },
    methods: {
        // 显隐研究区矢量
        handleCheck() {
            // 操作图层
            const dataSources = viewer.dataSources._dataSources.filter((item, index) => {
                // 判断是否为shp, shp不含type属性，点位有 type = 'point'
                return !item.hasOwnProperty('type')
            });
            dataSources.forEach(item => {
                item.show = this.checked;
            })
        },
        // 点击重新定位
        locate() {
            this.$EventBus.$emit('ReLocation', true)
        },
        // 全选
        handleCheckAllChange(val) {
            this.checkedVeges = val ? this.veges : [];
            this.isIndeterminate = false;
            this.handleShowVege()
        },
        // 单选
        handleCheckedVegesChange(value) {
            let checkedCount = value.length;
            this.checkAll = checkedCount === this.veges.length;
            this.isIndeterminate = checkedCount > 0 && checkedCount < this.veges.length;
            this.handleShowVege()
        },
        // 显隐盐沼植被
        handleShowVege() {
            const vegeMap = {
                '互花米草': 'HHMC_Wild_Samples.json',
                '芦苇': 'Luwei_Wild_Samples.json',
                '其他盐沼植被': 'OtherVege_Wild_Samples.json'
            }
            // 对应的盐沼植被种类
            const vegesShow = this.checkedVeges.map(key => vegeMap[key])

            viewer.dataSources._dataSources.forEach(item => {
                // 如果植被在vegesShow中， show = true， 否则 show = false
                if (item.hasOwnProperty('type')) {
                    if (vegesShow.includes(item.name)) {
                        item.show = true;
                    } else {
                        item.show = false;
                    }

                }
            })


        }
    }

}
</script>

<style lang="less" scoped>
.menuTitle2 {
    font-size: 18px;
    line-height: 40px;
}

.menu {
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

    .menuTitle {
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

    // 研究区
    .studyArea {}

    // 实地样本集
    .simple {
        position: relative;



        .legend {
            position: absolute;
            bottom: 10px;
            right: 100px;
            width: 40px;
            height: 105px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            align-items: center;

            .legend-circle {
                /* 调整圆的直径 */
                width: 20px;
                height: 20px;
                border-radius: 50%;
            }
        }
    }
}

.vertical-checkbox-group {
    display: flex;
    flex-direction: column;

}

// 实体样本集多选框排列
.vertical-checkbox {
    display: flex;
    align-items: center;
    width: 140px;
    margin: 5px 0;

}

// 实体样本集多选框排列
.el-checkbox.is-bordered+.el-checkbox.is-bordered {
    margin-left: 0;

}

// 实体样本集多选框字体样式
::v-deep.el-checkbox.is-bordered.el-checkbox--small .el-checkbox__label {
    color: #050505;
    font-size: 16px;
}

// 多选框文字样式(全选)
::v-deep.el-checkbox.is-bordered.el-checkbox--medium .el-checkbox__label {
    font-size: 16px;
}
</style>