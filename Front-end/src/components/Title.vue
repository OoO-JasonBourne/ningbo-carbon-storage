<template>
    <div class="header">
        <!-- 标题   -->
        <div class="title">
            <img class="logo" @click="refreshPage" :src="src" alt="">
            <span>{{ titleText }}</span>
        </div>
        <!-- 按钮组 -->
        <div class="funcBtns">
            <span class="funcBtn btn1" ref="btn1" @click="changePage(1)">数据分布</span>
            <span class="funcBtn" ref="btn2" @click="changePage(2)">模型计算</span>
            <span class="funcBtn" ref="btn3" @click="managePanelShow">图层管理</span>
            <span class="funcBtn" ref="btn4" @click="tablePanelShow">统计图表</span>
        </div>
        <!-- 研究区 -->
        <div class="area">
            <span>研究区 </span>
            <el-select class="input" v-model="value" @change="hangleStudy()" size="mini">
                <el-option v-for="item in studyArea" :key="item.value" :label="item.label" :value="item.value">
                </el-option>
            </el-select>
        </div>
        <!-- 控件 -->
        <div ref="customControl" class="custom-control"></div>
    </div>
</template>

<script>
import { mapState, mapMutations } from 'vuex';


export default {
    data() {
        return {
            src: 'Img/logo.png',
            titleText: '宁波海岸带湿地碳储量估算系统',
            value: 0,
            studyArea: [
                {
                    value: 0,
                    label: '宁波'
                },
                {
                    value: 1,
                    label: '杭州湾'
                },
                {
                    value: 2,
                    label: '梅山湾'
                },
                {
                    value: 3,
                    label: '蟹钳湾'
                }
            ]
        }
    },
    computed: {
        ...mapState(["cesiumControl", "curStudy"]),
        cesiumBtns() {
            return this.cesiumControl.cesiumBtns;
        },
    },
    mounted() {
        this.$EventBus.$on('ReLocation', data => {
            this.hangleStudy()
        });
        // 监听 dialogVisible 的状态
        this.$EventBus.$on('onTableAndManage', val => {
            // 改变 <图层管理> 和 <统计图表> 的标题样式
            this.changeTableAndManage(val)
        })
    },
    watch: {
        // 监听 vuex 中的cesium图层切换组件,自定义加载
        cesiumBtns(newVal, oldVal) {
            this.$refs.customControl.appendChild(newVal);
        },
    },
    methods: {
        ...mapMutations(["changeStudyID", "changeStudyData"]),
        // 使用 window.location.reload() 方法刷新页面
        refreshPage() {
            window.location.reload();
        },
        // 切换研究区
        hangleStudy() {
            const id = this.value;
            this.changeStudyID(id) // 将下拉框val的值传给 vuex 
            const dataSources = viewer.dataSources._dataSources;    // 获取已添加的图层
            let curdata;
            if (id != 0) {
                if (id === 1) {
                    curdata = dataSources.filter(item => item.name === "HZW_ROI.json")
                    this.$EventBus.$emit('onStudyTextSwitch', '杭州湾')
                } else if (id === 2) {
                    curdata = dataSources.filter(item => item.name === "MSG_ROI.json")
                    this.$EventBus.$emit('onStudyTextSwitch', '梅山湾')
                } else if (id == 3) {
                    curdata = dataSources.filter(item => item.name === "XQG_ROI.json")
                    this.$EventBus.$emit('onStudyTextSwitch', '蟹钳湾')
                }
                // 飞行
                if (curdata[0].show == false) {
                    // 如果一开始为隐藏，就先设为 true 飞过去之后在改为 false
                    curdata[0].show = true;
                    viewer.flyTo(curdata[0], {
                        duration: 0.5,
                        offset: {
                            heading: 0,
                            pitch: -90,
                            range: 50000
                        }
                    }).then(() => {
                        // 飞行结束后将 show 设置回 false
                        curdata[0].show = false;
                    });
                } else {
                    // 如果为显示，直接飞行
                    viewer.flyTo(curdata[0], {
                        duration: 0.5, // 飞行持续时间
                        offset: {
                            heading: 0,
                            pitch: -90,
                            range: 50000
                        }
                    })
                }

            } else {
                this.$EventBus.$emit('onStudyTextSwitch', '研究区矢量')
                viewer.camera.flyTo({
                    destination: Cesium.Cartesian3.fromDegrees(121.56, 29.86, 200000),
                    duration: 0.5 // 飞行持续时间
                });
            }

        },
        // 激活管理面板
        managePanelShow() {
            this.$EventBus.$emit('onManagePanel', [true, 1])
        },
        // 激活Table面板
        tablePanelShow() {
            this.$EventBus.$emit('onTablePanel', true)
        },
        // 显示模型或者数据分布页面
        changePage(id) {
            this.$emit('onChangePage', id)
            if (id === 1) {
                this.$refs.btn1.style = 'color:rgb(243, 174, 84)';
                this.$refs.btn2.style = 'color:#FFF'
            } else if (id === 2) {
                this.$refs.btn1.style = 'color:#FFF';
                this.$refs.btn2.style = 'color:rgb(243, 174, 84)'
            }
        },
        // 改变 <图层管理> 和 <统计图表> 的标题样式
        changeTableAndManage(val) {
            // 使用对象语法来动态设置样式，以减少冗余代码
            let id = val[0], status = val[1];
            if (id === 3) {
                this.setStyle(this.$refs.btn3, status);
            } else if (id === 4) {
                this.setStyle(this.$refs.btn4, status);
            }
        },
        // 使用对象语法来动态设置样式
        setStyle(ref, status) {
            ref.style.color = status ? 'rgb(243, 174, 84)' : '#FFF';
        }
    },

}
</script>

<style lang="less" scoped>
.header {
    position: fixed;
    width: 100%;
    height: 50px;
    z-index: 10;
    background-color: #008b8b;
    color: #FFF;
    display: flex;
    justify-content: space-between;
    align-items: center;

    caret-color: transparent;
    /* 阻止光标闪烁 */
    user-select: none;
    /* 可选，阻止文本选择 */

    .title {
        position: relative;
        display: flex;
        font: 800 20px "SimHei", sans-serif;
        width: 350px;
        height: 100%;
        line-height: 50px;

        .logo {
            height: 100%;
            margin-right: 8px;
        }

        .logo:hover {
            cursor: pointer;
        }
    }

    .funcBtns {
        .funcBtn {
            margin: 0 10px;
        }

        .btn1 {
            color: rgb(243, 174, 84);
        }

        .funcBtn:hover {
            cursor: pointer;
            color: rgb(243, 174, 84);
        }
    }

    .area {
        font: 400 16px "SimHei", sans-serif;
    }

    .area:hover {
        cursor: pointer;
    }
}

// select 输出框的样式
::v-deep .el-select .el-input__inner {
    color: #FFF;
    background-color: #008b8b;
    width: 100px;
    font-size: 14px;
}

// select 下拉框的样式
::v-deep .el-select-dropdown__list {
    background-color: #006400;
}
</style>