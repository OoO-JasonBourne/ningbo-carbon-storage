<template>
    <el-dialog title="统计数据" :visible.sync="dialogVisible" width="60%" class="table">
        <el-tabs v-model="activeName" @tab-click="handleClick">
            <el-tab-pane label="面积统计(m2)" name="first">
                <el-table :data="tableData" style="width: 100%" stripe>
                    <el-table-column prop="studyArea" label="区域">
                    </el-table-column>
                    <el-table-column prop="area_HHMC" label="互花米草">
                    </el-table-column>
                    <el-table-column prop="area_LW" label="芦苇">
                    </el-table-column>
                    <el-table-column prop="area_Other" label="其它植被">
                    </el-table-column>
                    <el-table-column prop="area_ALL" label="总面积">
                    </el-table-column>
                </el-table>
            </el-tab-pane>
            <el-tab-pane label="生物量(Kg)" name="second">
                <el-table :data="tableData" style="width: 100%">
                    <el-table-column prop="studyArea" label="区域">
                    </el-table-column>
                    <el-table-column prop="biomass_HHMC" label="互花米草">
                    </el-table-column>
                    <el-table-column prop="biomass_LW" label="芦苇">
                    </el-table-column>
                    <el-table-column prop="biomass_Other" label="其它植被">
                    </el-table-column>
                    <el-table-column prop="biomass_All" label="总生物量">
                    </el-table-column>
                </el-table>
            </el-tab-pane>
            <el-tab-pane label="碳储量(Kg)" name="third">
                <el-table :data="tableData" style="width: 100%">
                    <el-table-column prop="studyArea" label="区域">
                    </el-table-column>
                    <el-table-column prop="stock_HHMC" label="互花米草">
                    </el-table-column>
                    <el-table-column prop="stock_LW" label="芦苇">
                    </el-table-column>
                    <el-table-column prop="stock_Other" label="其它植被">
                    </el-table-column>
                    <el-table-column prop="stock_Soil" label="土壤碳储量">
                    </el-table-column>
                    <el-table-column prop="stock_Vege" label="植被碳储量">
                    </el-table-column>
                    <el-table-column prop="stock_All" label="总碳储量">
                    </el-table-column>
                </el-table>
            </el-tab-pane>
            <el-tab-pane label="其它" name="fourth">
                <el-table :data="tableData" style="width: 100%">
                    <el-table-column prop="studyArea" label="区域">
                    </el-table-column>
                    <el-table-column prop="AGB" label="AGB密度(g/m2)">
                    </el-table-column>
                    <el-table-column prop="density" label="碳密度(g/m2)">
                    </el-table-column>
                    <el-table-column prop="Value" label="碳汇价值(￥)">
                    </el-table-column>
                </el-table>
            </el-tab-pane>
        </el-tabs>
    </el-dialog>
</template>

<script>
import api from '../api/index'

export default {
    data() {
        return {
            dialogVisible: false,
            activeName: 'first',
            tableData: []
        }
    },
    mounted() {
        // 请求统计数据
        this.loadingStatis();
        // 激活面板
        this.$EventBus.$on('onTablePanel', val => {
            this.dialogVisible = val;
        })
    },
    watch: {
        // 监听 dialogVisible 的状态
        dialogVisible(newVal, oldVal){
            this.$EventBus.$emit('onTableAndManage', [4, newVal])
        }
    },
    methods: {
        handleClick(tab, event) {
            // console.log(tab, event);
        },
        // 请求统计数据
        loadingStatis() {
            api.loadingStatis().then((res) => {
                if (res.status === 200) {
                    this.tableData = res.data;
                } else {
                    console.log('数据加载失败')
                }
            }).catch(error => {
                console.log(error)
            })
        }
    }
}

</script>

<style>
.el-dialog {
    height: 50%;
    position: relative;
    overflow-y: auto;
    background-color: aliceblue;

}

.el-dialog__header {
    background-color: #008b8b;
}

.el-dialog__title {
    color: #FFF;
}

.el-dialog__headerbtn .el-dialog__close {
    color: #FFF;
}
</style>