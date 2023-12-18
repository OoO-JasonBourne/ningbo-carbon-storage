const base = {
    baseUrl: 'http://39.101.79.18:5086',
    loadingImg: '/api/data/modelImg', // 加载影像数据
    loadingStatis: '/api/data/statistical',  // 加载图表数据
    loadingTaskList: '/api/data/taskList',  // 加载任务列表
    saveModelTask: '/api/model/taskInsert', // 插入模型任务
    calcNDVI: '/api/model/NDVI',    // 计算NDVI
    calcPixel: '/api/model/calcPixel',  // 计算像素数量
}

export default base;