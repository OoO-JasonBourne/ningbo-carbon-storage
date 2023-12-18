<template>
    <vue-draggable-resizable ref="draggable" class="chartsPanel" :w="260" :h="300" :x="x" :y="y" :z="20" :parent="true"
        v-show=show>
        <div class="chartTitle">
            <span>{{ title }}</span>
            <button type="text" @click="show = false" class="btn"><i class="el-icon-close" size="medium"></i></button>
        </div>
        <div id="Echart"></div>
    </vue-draggable-resizable>
</template>

<script>
import echarts from '../plugins/echarts'
export default {
    data() {
        return {
            show: false,
            x: 20,
            y: 10,
            pixelData: [],
            title: '',
        }
    },
    mounted() {
        // this.$nextTick(() => {
        //     this.chartInit();
        // });
        this.$EventBus.$on('onChartPanel', val => {
            if (val[1]) {
                this.pixelData = val[1]
                this.chartInit()
                return
            };
            this.show = true;
            this.title = val[0];
            // this.animationInit();
        })
    },
    methods: {
        // 加载等待动画
        animationInit() {
            var chartDom = document.getElementById('Echart');
            var myChart = echarts.init(chartDom);
            var option;
            option = {
                graphic: {
                    elements: [
                        {
                            type: 'group',
                            left: 'center',
                            top: 'center',
                            children: new Array(7).fill(0).map((val, i) => ({
                                type: 'rect',
                                x: i * 20,
                                shape: {
                                    x: 0,
                                    y: -40,
                                    width: 10,
                                    height: 80
                                },
                                style: {
                                    fill: '#5470c6'
                                },
                                keyframeAnimation: {
                                    duration: 1000,
                                    delay: i * 200,
                                    loop: true,
                                    keyframes: [
                                        {
                                            percent: 0.5,
                                            scaleY: 0.3,
                                            easing: 'cubicIn'
                                        },
                                        {
                                            percent: 1,
                                            scaleY: 1,
                                            easing: 'cubicOut'
                                        }
                                    ]
                                }
                            }))
                        }
                    ]
                }
            };

            option && myChart.setOption(option);
        },
        // 初始化 饼状图
        chartInit() {
            var chartDom = document.getElementById('Echart');
            var myChart = echarts.init(chartDom);
            var option;

            option = {
                tooltip: {
                    trigger: 'item',
                    position: [0, 260],
                    backgroundColor: 'rgba(50, 50, 50, 0.5)',
                    textStyle: {
                        color: '#FFF',
                        fontFamily: 'sans-serif',
                    }
                },
                series: [
                    {
                        type: 'pie',
                        radius: ['30%', '70%'],
                        avoidLabelOverlap: true,
                        label: {
                            show: false,
                            position: 'center'
                        },
                        emphasis: {
                            label: {
                                show: true,
                                fontSize: 16,
                                fontWeight: 'bold'
                            }
                        },
                        labelLine: {
                            show: true
                        },
                        data: this.pixelData,

                        // 设置颜色数组，可以根据需要自定义颜色
                        color: ['#abdda4', '#ffffbf', '#fdae61', '#d7191c'],
                    }
                ]
            };
            option && myChart.setOption(option);
        },
    }

}

</script>


<style>
.chartsPanel {
    position: absolute;
    top: 0;

    /* border: 1px solid yellow; */
    .chartTitle {
        height: 40px;
        font: 400 16px/40px "SimHei", sans-serif;
        ;
        color: #0f0f0f;
        background-color: #b8c2cf;
        text-align: center;
        border-radius: 15px 15px 0 0;

        .btn {
            position: absolute;
            right: 10px;
            top: 5px;
            border: none;
            width: 30px;
            height: 30px;
        }

        .btn:hover {
            cursor: pointer;
            color: red;
            font-size: 18px;
        }

    }

    #Echart {
        position: relative;
        width: 100%;
        height: calc(100% - 40px);
        background-color: rgba(85, 147, 228, 0.3);
    }
}
</style>