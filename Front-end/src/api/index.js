import axios from 'axios';
import base from './base';

const api = {
    /*
     *  加载统计数据
     */
    loadingStatis() {
        return axios.get(base.baseUrl + base.loadingStatis)
    },
    /*
    *  数据选取
    */
    loadingImg() {
        return axios.get(base.baseUrl + base.loadingImg)
    },
    /*
    *  请求任务列表
    */
    loadingTaskList() {
        return axios.get(base.baseUrl + base.loadingTaskList)
    },
    /*
    *  插入任务
    */
    saveModelTask(params) {
        return axios.post(base.baseUrl + base.saveModelTask, params)
    },
    /*
    *  计算NDVI
    */
    calcNDVI(params) {
        return axios.post(base.baseUrl + base.calcNDVI, params)
    },
    /*
    *  计算像素数量
    */
    calcPixel(params) {
        return axios.post(base.baseUrl + base.calcPixel, params)
    },
}

export default api;